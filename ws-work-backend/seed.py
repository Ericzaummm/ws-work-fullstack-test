import requests
from database import SessionLocal, engine
import models

# Garantia de que as tabelas existem no SQLite
models.Base.metadata.create_all(bind=engine)

def popular_banco():
    db = SessionLocal()

    # Verifica se já existe a marca para não duplicar os dados
    if db.query(models.Marca).first():
        print("Essas marcas já possuem registro!")
        db.close()
        return
    print("Iniciando o Seed do banco de Dados...")

    # Integração com a API da ws-work
    # Aqui é onde o script vai fazer o download do json
    # response = requests.get("https://wswork.com.br/cars.json")
    # dados_ws = response.json()
    # (Como ainda não ssei o nome exato das chaves do JSON até testar, 
    # vou injetar dados estruturados para não quebrar a API)

    # Inserção das Marcas
    marcas_iniciais = ["Toyota", "Honda", "Volkswagen"]
    db_marcas = []

    for nome in marcas_iniciais:
        marca = models.Marca(nome_marca=nome)
        db.add(marca)
        db_marcas.append(marca)
    db.commit()

    # Inserção de Modelos
    modelos_iniciais = [
        {"nome": "Corolla XEI", "marca_idx": 0, "fipe": 110000.0},
        {"nome": "Civic Touring", "marca_idx": 1, "fipe": 125000.0},
        {"nome": "Nivus Highline", "marca_idx": 2, "fipe": 115000.0}
    ]

    db_modelos = []
    for m in modelos_iniciais:
        modelo = models.Modelo(
            nome=m["nome"], 
            valor_fipe=m["fipe"], 
            marca_id=db_marcas[m["marca_idx"]].id
        )
        db.add(modelo)
        db_modelos.append(modelo)
    db.commit()

    # Inserção de Carros
    carros_iniciais = [
        {"modelo_id": db_modelos[0].id, "ano": 2022, "combustivel": "Flex", "num_portas": 4, "cor": "Branco", "quilometragem": 35000, "valor_anuncio": 125000, "descricao": "Veículo impecável, único dono, todas as revisões feitas na concessionária. Ótima oportunidade de negócio!"},
        {"modelo_id": db_modelos[1].id, "ano": 2021, "combustivel": "Gasolina", "num_portas": 4, "cor": "Preto", "quilometragem": 48000, "valor_anuncio": 135000, "descricao": "Excelente estado de conservação. Motor turbo, teto solar e bancos em couro. Laudo cautelar 100% aprovado."},
        {"modelo_id": db_modelos[2].id, "ano": 2023, "combustivel": "Flex", "num_portas": 4, "cor": "Cinza", "quilometragem": 15000, "valor_anuncio": 130000, "descricao": "Carro de garagem, cheiro de novo. Pacote completo com painel digital e piloto automático adaptativo (ACC)."}
    ]
    
    for c in carros_iniciais:
        carro = models.Carro(**c)
        db.add(carro)
        
    db.commit()
    db.close()
    
    print("Banco de dados populado com sucesso! Os carros já estão disponíveis na API.")

if __name__ == "__main__":
    popular_banco()