from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

"""
Modelagem de Dados (ORM - Object-Relational Mapping)
Define a estrutura das tabelas no banco de dados (SQLite/PostgreSQL) 
e mapeia os relacionamentos entre elas de forma orientada a objetos.
"""

class Marca(Base):
    """
    Entidade: Marca (ex: Toyota, Honda)
    Representa a fabricante do veículo.
    """
    __tablename__ = "marcas"

    # index=True otimiza a velocidade de busca no banco de dados
    id = Column(Integer, primary_key=True, index=True)
    # unique=True garante que não teremos duas marcas com o mesmo nome cadastradas
    nome_marca = Column(String, unique=True, index=True)

    # Relacionamento 1:N (Uma Marca possui vários Modelos)
    # O 'back_populates' cria uma via de mão dupla, permitindo acessar modelos a partir da marca e vice-versa.
    modelos = relationship("Modelo", back_populates="marca")


class Modelo(Base):
    """
    Entidade: Modelo (ex: Corolla, Civic)
    Representa o modelo específico atrelado a uma Marca.
    """
    __tablename__ = "modelos"

    id = Column(Integer, primary_key=True, index=True)
    
    # Chave Estrangeira: Garante a integridade referencial com a tabela de marcas
    marca_id = Column(Integer, ForeignKey("marcas.id"))
    nome = Column(String, index=True)
    valor_fipe = Column(Float)

    # Relacionamentos
    marca = relationship("Marca", back_populates="modelos")
    # Relacionamento 1:N (Um Modelo pode ter vários Carros à venda)
    carros = relationship("Carro", back_populates="modelo")


class Carro(Base):
    """
    Entidade Principal: Carro
    Armazena os dados brutos e as especificações técnicas do veículo à venda.
    """
    __tablename__ = "carros"

    id = Column(Integer, primary_key=True, index=True)
    
    # Chave Estrangeira ligando o carro ao seu modelo específico
    modelo_id = Column(Integer, ForeignKey("modelos.id"))
    
    # Auditoria de Criação: Preenche automaticamente a data/hora atual no momento do INSERT
    timestamp_cadastro = Column(DateTime, default=datetime.utcnow)
    
    ano = Column(Integer)
    combustivel = Column(String)
    num_portas = Column(Integer)
    cor = Column(String)
    quilometragem = Column(Integer)
    valor_anuncio = Column(Float)
    
    # Textos longos são suportados pela Column(String) no SQLAlchemy, 
    # que se adapta para TEXT ou VARCHAR dependendo do banco
    descricao = Column(String)

    # Relacionamento N:1 (Vários carros pertencem a um mesmo Modelo)
    modelo = relationship("Modelo", back_populates="carros")