from sqlalchemy.orm import Session
import models, schemas

def get_marcas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Marca).offset(skip).limit(limit).all

def get_modelos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Modelo).offset(skip).limit(limit).all()

def get_carros(db: Session, skip: int = 0, limit: int = 100):
    # Vai buscar os carros no banco
    carros = db.query(models.Carro).offset(skip).limit(limit).all()

    # Injeta os nomes da marca e modelo
    for carro in carros:
        if carro.modelo:
            carro.nome_modelo = carro.modelo.nome
            if carro.modelo.marca:
                carro.nome_marca = carro.modelo.marca.nome_marca
    return carros

def create_carro(db: Session, carro: schemas.CarroCreate):
    db_carro = models.Carro(**carro.model_dump()) # Usando model_dump (é Padrão do Pydantic v2)
    db.add(db_carro)
    db.commit()
    db.refresh(db_carro)
    return db_carro