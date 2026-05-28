from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de ligação à base de dados. 
# Atualmente configurada para SQLite local, o que facilita o teste imediato 
# sem necessidade de infraestrutura extra.
SQLALCHEMY_DATABASE_URL = "sqlite:///./wswork.db"

# Cria o "motor" da base de dados.
# O argumento 'check_same_thread: False' é necessário apenas para o SQLite no FastAPI,
# pois o FastAPI pode aceder à base de dados a partir de múltiplas threads em requisições concorrentes.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Criação da fábrica de sessões.
# autocommit=False e autoflush=False garantem que nós temos controlo total sobre 
# quando as transações são gravadas (db.commit()) no código (no ficheiro crud.py).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que será herdada por todos os modelos de base de dados.
# É a partir dela que o SQLAlchemy sabe quais classes representam tabelas reais.
Base = declarative_base()

def get_db():
    """
    Função geradora para Injeção de Dependência no FastAPI.
    Garante que cada requisição HTTP receba a sua própria sessão de base de dados isolada.
    """
    db = SessionLocal()
    try:
        # 'yield' entrega a sessão temporariamente para a rota que a solicitou
        yield db
    finally:
        # O bloco 'finally' assegura categoricamente que a ligação será fechada
        # após a requisição terminar, evitando vazamento de memória
        # ou bloqueio da base de dados.
        db.close()