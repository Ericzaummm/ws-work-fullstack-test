from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Marca(Base):
    __tablename__ = "marcas"

    id = Column(Integer, primary_key=True, index=True)
    nome_marca = Column(String, unique=True, index=True)

    modelos = relationship("Modelo", back_populates="marca")


class Modelo(Base):
    __tablename__ = "modelos"

    id = Column(Integer, primary_key=True, index=True)
    marca_id = Column(Integer, ForeignKey("marcas.id"))
    nome = Column(String, index=True)
    valor_fipe = Column(Float)

    marca = relationship("Marca", back_populates="modelos")
    carros = relationship("Carro", back_populates="modelo")


class Carro(Base):
    __tablename__ = "carros"

    id = Column(Integer, primary_key=True, index=True)
    modelo_id = Column(Integer, ForeignKey("modelos.id"))
    timestamp_cadastro = Column(DateTime, default=datetime.utcnow)
    
    ano = Column(Integer)
    combustivel = Column(String)
    num_portas = Column(Integer)
    cor = Column(String)
    quilometragem = Column(Integer)
    valor_anuncio = Column(Float)
    descricao = Column(String)

    modelo = relationship("Modelo", back_populates="carros")