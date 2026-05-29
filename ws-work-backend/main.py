import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

import models, schemas, crud
from database import engine, get_db

# Carrega as variáveis de ambiente (ex: OPENAI_API_KEY) do ficheiro .env
load_dotenv()

# Inicializa o cliente da OpenAI de forma segura, sem expor chaves no código-fonte
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Criação das tabelas na base de dados caso ainda não existam
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WS Work Motors API",
    description="API RESTful para gestão de catálogo de veículos com integração de Inteligência Artificial.",
    version="1.0.0"
)

# Configuração do CORS (Cross-Origin Resource Sharing)
# Fundamental numa arquitetura Monorepo/Desacoplada para permitir que o Front-end (React)
# faça requisições ao Back-end (FastAPI) sem ser bloqueado pelas políticas de segurança do navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
def read_root():
    """Endpoint de verificação de estado (Health Check) da API."""
    return {"mensagem": "API da WS Work Motors a correr com sucesso!"}

@app.get("/marcas", response_model=List[schemas.MarcaResponse], tags=["Marcas"])
def read_marcas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retorna a lista de todas as marcas registadas."""
    return crud.get_marcas(db, skip=skip, limit=limit)

@app.get("/modelos", response_model=List[schemas.ModeloResponse], tags=["Modelos"])
def read_modelos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retorna a lista de todos os modelos registados."""
    return crud.get_modelos(db, skip=skip, limit=limit)

@app.get("/carros", response_model=List[schemas.CarroResponse], tags=["Carros"])
def read_carros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna o catálogo completo de carros.
    Delega ao crud.py a responsabilidade de realizar o 'Data Flattening' (BFF), devolvendo 
    os dados relacionais já resolvidos para o Front-end consumir diretamente.
    """
    return crud.get_carros(db, skip=skip, limit=limit)

@app.post("/carros", response_model=schemas.CarroResponse, tags=["Carros"])
def create_carro(carro: schemas.CarroCreate, db: Session = Depends(get_db)):
    """
    Regista um novo veículo.
    A lógica de negócio complexa (criação dinâmica de Marcas e Modelos inexistentes) 
    foi isolada na camada CRUD, mantendo este controlador limpo e focado 
    apenas em orquestrar o tráfego HTTP.
    """
    # Delega a tarefa para a função criada no crud.py
    return crud.create_carro(db=db, carro=carro)

@app.post("/gerar-descricao", tags=["Inteligência Artificial"])
async def gerar_descricao_ia(dados: schemas.IADescricaoRequest):
    """
    Integração com a API da OpenAI (ChatGPT).
    Recebe os dados parciais do veículo do formulário React e utiliza engenharia de prompts 
    para gerar uma descrição de vendas persuasiva.
    
    Resiliência: Possui um mecanismo de 'Fallback' elegante para garantir que a interface 
    do utilizador não quebre caso a API da OpenAI falhe, gere timeout ou falte saldo.
    """
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
        # Fallback de segurança gerado localmente pelo Python
        texto_fallback = f"Oportunidade imperdível! {dados.marca} {dados.modelo} {dados.ano} na belíssima cor {dados.cor}. Apenas {dados.quilometragem}km rodados. Excelente estado de conservação por apenas R$ {dados.valor}. Entre em contacto agora e agende um test drive!"
        return {"descricao": texto_fallback}