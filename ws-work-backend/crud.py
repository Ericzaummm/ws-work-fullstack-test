from sqlalchemy.orm import Session
import models, schemas

def get_marcas(db: Session, skip: int = 0, limit: int = 100):
    """
    Retorna uma lista paginada de Marcas do banco de dados.
    """
    return db.query(models.Marca).offset(skip).limit(limit).all()

def get_modelos(db: Session, skip: int = 0, limit: int = 100):
    """
    Retorna uma lista paginada de Modelos do banco de dados.
    """
    return db.query(models.Modelo).offset(skip).limit(limit).all()

def get_carros(db: Session, skip: int = 0, limit: int = 100):
    """
    Busca o catálogo de carros e aplica o padrão BFF.
    
    Em vez de forçar o Front-end a buscar os IDs e depois cruzar os dados, 
    essa função injeta ativamente o nome da Marca e do Modelo 
    diretamente no objeto do Carro, reduzindo o processamento no lado do cliente.
    """
    carros = db.query(models.Carro).offset(skip).limit(limit).all()

    for carro in carros:
        # Resolve os relacionamentos via SQLAlchemy ORM
        if carro.modelo:
            carro.nome_modelo = carro.modelo.nome
            if carro.modelo.marca:
                carro.nome_marca = carro.modelo.marca.nome_marca
                
    return carros

def create_carro(db: Session, carro: schemas.CarroCreate):
    """
    Responsável pela inserção de um novo veículo com persistência dinâmica.
    
    Se o Front-end enviar uma Marca ou Modelo que ainda não existe no banco 
    de dados, esta função cria esses registros de forma relacional antes de 
    salvar o carro, garantindo a integridade referencial.
    """
    # 1. Verifica se a Marca existe (ignorando maiúsculas/minúsculas). Se não, cria.
    marca = db.query(models.Marca).filter(models.Marca.nome_marca.ilike(carro.marca_nome)).first()
    if not marca:
        marca = models.Marca(nome_marca=carro.marca_nome)
        db.add(marca)
        db.commit()
        db.refresh(marca)

    # 2. Verifica se o Modelo existe. Se não, cria vinculado à marca acima.
    modelo = db.query(models.Modelo).filter(models.Modelo.nome.ilike(carro.modelo_nome)).first()
    if not modelo:
        modelo = models.Modelo(nome=carro.modelo_nome, marca_id=marca.id, valor_fipe=0.0)
        db.add(modelo)
        db.commit()
        db.refresh(modelo)
        
    # 3. Mapeia os dados recebidos para o formato do Banco de Dados
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
    
    # Executa a transação no banco (Insert)
    db.add(db_carro)
    db.commit()
    db.refresh(db_carro)
    
    # Injeta os nomes na resposta imediata para que o card no React renderize sem erros
    db_carro.nome_modelo = modelo.nome
    db_carro.nome_marca = marca.nome_marca
    
    return db_carro