from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import engine, get_db

# Cria as tabelas no banco de dados SQLite
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WS Work Motors API",
    description="API para listagem e cadastro de veículos com integração de Inteligência Artificial",
    version="1.0.0"
)

# Configuração de CORS 
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

# Endpoints da api

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
    # Valida se o modelo_id fornecido realmente existe
    modelo = db.query(models.Modelo).filter(models.Modelo.id == carro.modelo_id).first()
    if not modelo:
        raise HTTPException(status_code=404, detail="Modelo não encontrado. Verifique o modelo_id.")
        
    novo_carro = crud.create_carro(db=db, carro=carro)
    
    # Preenche os dados relacionais para devolver no JSON de resposta imediata
    novo_carro.nome_modelo = modelo.nome
    novo_carro.nome_marca = modelo.marca.nome_marca if modelo.marca else None
    
    return novo_carro