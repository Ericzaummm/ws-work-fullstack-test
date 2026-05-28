import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Lê a URL do banco a partir das variáveis de ambiente (injetadas pelo Docker).
# Se não encontrar (rodando localmente sem Docker), usa o SQLite como Fallback.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wswork.db")

# O argumento 'check_same_thread' é uma particularidade exclusiva do SQLite.
# Se a URL começar com 'sqlite', configuramos para ele. Se for Postgres, criamos o motor padrão.
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()