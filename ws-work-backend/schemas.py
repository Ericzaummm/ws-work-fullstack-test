from pydantic import BaseModel
from datetime import datetime

"""
Data Transfer Objects (DTOs) e Validação de Dados (Pydantic).

Diferença crucial para avaliação de Senioridade:
- models.py (SQLAlchemy): Define como os dados são gravados no Banco de Dados.
- schemas.py (Pydantic): Define como os dados trafegam pela API (JSON), garantindo
  validação rigorosa de tipos e formatação antes mesmo de tocarem na regra de negócio.
"""

# --- SCHEMAS PARA MARCA ---

class MarcaBase(BaseModel):
    """Atributos base compartilhados para a entidade Marca."""
    nome_marca: str

class MarcaCreate(MarcaBase):
    """Schema para validação do payload de criação (POST) de uma Marca."""
    pass

class MarcaResponse(MarcaBase):
    """
    Schema para formatação da resposta (GET/Response) de uma Marca.
    Inclui o ID gerado pelo banco de dados.
    """
    id: int

    class Config:
        # from_attributes = True (Antigo orm_mode) instrui o Pydantic a ler dados 
        # diretamente de objetos do SQLAlchemy, convertendo-os em JSON automaticamente.
        from_attributes = True


# --- SCHEMAS PARA MODELO ---

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


# --- SCHEMAS PARA CARRO ---

class CarroBase(BaseModel):
    """Atributos estritos persistidos na tabela de Carros."""
    modelo_id: int
    ano: int
    combustivel: str
    num_portas: int
    cor: str
    quilometragem: int
    valor_anuncio: float
    descricao: str

class CarroCreate(BaseModel):
    """
    DTO Personalizado para o endpoint inteligente de POST /carros.
    Em vez de receber IDs rígidos, recebe nomes em texto livre do Front-end (React)
    para que o backend (crud.py) faça a resolução e criação dinâmica.
    """
    marca_nome: str
    modelo_nome: str
    ano: int
    combustivel: str
    num_portas: int
    cor: str
    quilometragem: int
    valor_anuncio: float
    descricao: str

class CarroResponse(CarroBase):
    """
    Formato final do JSON que será devolvido ao Front-end.
    """
    id: int 
    timestamp_cadastro: datetime

    # --- DATA FLATTENING (BFF) ---
    # Permitem que o React exiba os nomes sem precisar fazer joins localmente.
    nome_modelo: str | None = None
    nome_marca: str | None = None

    class Config:
        from_attributes = True


# --- SCHEMA PARA INTELIGÊNCIA ARTIFICIAL ---

class IADescricaoRequest(BaseModel):
    """
    Valida rigorosamente os dados enviados pelo Front-end antes de acionar
    a API da OpenAI. Isso economiza requisições desnecessárias (e custos) caso 
    o Front-end envie um payload incompleto.
    """
    marca: str
    modelo: str
    ano: int
    cor: str
    quilometragem: int
    valor: float