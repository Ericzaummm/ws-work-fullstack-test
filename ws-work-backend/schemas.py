from pydantic import BaseModel
from datetime import datetime

# Schemas para a marca

class MarcaBase(BaseModel):
    nome_marca: str

class MarcaCreate(MarcaBase):
    pass

class MarcaResponse(MarcaBase):
    id: int

    class Config:
        from_attributes = True

# Schemas para modelo

class ModeloBase(BaseModel):
    marca_id: int
    nome: str
    valor_fipe: float

class ModeloCreate(ModeloBase):
    pass

class ModeloResponse(ModeloBase):
    id: int

    class Config:
        from_attributes = True

# Schemas para o carro

class CarroBase(BaseModel):
    modelo_id: int
    ano: int
    combustivel: str
    num_portas: int
    cor: str
    quilometragem: int
    valor_anuncio: float
    descricao: str

class CarroCreate(CarroBase):
    pass

class CarroResponse(CarroBase):
    id: int 
    timestamp_cadastro: datetime

    nome_modelo: str | None = None
    nome_marca: str | None = None

    class Config:
        from_attributes = True