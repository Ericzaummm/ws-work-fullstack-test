import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

import models, schemas, crud
from database import engine, get_db

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WS Work Motors API",
    description="API para listagem e cadastro de veículos com integração de Inteligência Artificial",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"mensagem": "API da WS Work Motors rodando com sucesso!"}

@app.get("/marcas", response_model=List[schemas.MarcaResponse], tags=["Marcas"])
def read_marcas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_marcas(db, skip=skip, limit=limit)

@app.get("/modelos", response_model=List[schemas.ModeloResponse], tags=["Modelos"])
def read_modelos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_modelos(db, skip=skip, limit=limit)

@app.get("/carros", response_model=List[schemas.CarroResponse], tags=["Carros"])
def read_carros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_carros(db, skip=skip, limit=limit)

@app.post("/carros", response_model=schemas.CarroResponse, tags=["Carros"])
def create_carro(carro: schemas.CarroCreate, db: Session = Depends(get_db)):
    marca = db.query(models.Marca).filter(models.Marca.nome_marca.ilike(carro.marca_nome)).first()
    if not marca:
        marca = models.Marca(nome_marca=carro.marca_nome)
        db.add(marca)
        db.commit()
        db.refresh(marca)

    modelo = db.query(models.Modelo).filter(models.Modelo.nome.ilike(carro.modelo_nome)).first()
    if not modelo:
        modelo = models.Modelo(nome=carro.modelo_nome, marca_id=marca.id, valor_fipe=0.0)
        db.add(modelo)
        db.commit()
        db.refresh(modelo)
        
    db_carro = models.Carro(
        modelo_id=modelo.id,
        ano=carro.ano,
        combustivel=carro.combustivel,
        num_portas=carro.num_portas,
        cor=carro.cor,
        quilometragem=carro.quilometragem,
        valor_anuncio=carro.valor_anuncio,
        descricao=carro.descricao
    )
    db.add(db_carro)
    db.commit()
    db.refresh(db_carro)
    
    db_carro.nome_modelo = modelo.nome
    db_carro.nome_marca = marca.nome_marca
    
    return db_carro

@app.post("/gerar-descricao", tags=["Inteligência Artificial"])
async def gerar_descricao_ia(dados: schemas.IADescricaoRequest):
    prompt = f"""
    Aja como um vendedor de carros de luxo experiente e persuasivo.
    Escreva uma descrição atraente e direta de no máximo 3 linhas para um anúncio de venda.
    Destaque os pontos fortes.
    
    Dados do carro:
    - Marca: {dados.marca}
    - Modelo: {dados.modelo}
    - Ano: {dados.ano}
    - Cor: {dados.cor}
    - Quilometragem: {dados.quilometragem} km
    - Valor: R$ {dados.valor}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é o melhor vendedor de carros do Brasil."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        descricao_gerada = response.choices[0].message.content.strip()
        return {"descricao": descricao_gerada}
        
    except Exception as e:
        print(f"Erro na OpenAI: {e}")
        texto_fallback = f"Oportunidade imperdível! {dados.marca} {dados.modelo} {dados.ano} na belíssima cor {dados.cor}. Apenas {dados.quilometragem}km rodados. Excelente estado de conservação por apenas R$ {dados.valor}. Entre em contato agora e agende um test drive!"
        return {"descricao": texto_fallback}