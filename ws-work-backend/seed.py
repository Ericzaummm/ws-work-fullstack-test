import requests
from database import SessionLocal, engine
import models

"""
Script de ETL (Extract, Transform, Load) / Seed.
Responsável por cumprir o requisito obrigatório de consumir as APIs fornecidas 
pela WS Work, higienizar os dados e popular o banco de dados relacional inicial.
"""

# Reseta o banco de dados. 
# Garante a idempotência do script (pode ser rodado várias vezes sem duplicar ou quebrar dados).
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

def popular_banco():
    db = SessionLocal()
    print("Iniciando o download dos dados das rotas da WS Work...")

    carros_geral = []
    carros_por_marca = []

    # --- EXTRAÇÃO ---
    
    # 1. Busca os dados da primeira rota (Geral)
    try:
        res1 = requests.get("https://wswork.com.br/cars.json")
        res1.raise_for_status()
        carros_geral = res1.json().get("cars", [])
    except Exception as e:
        print(f"Aviso: Erro ao aceder cars.json - {e}")

    # 2. Busca os dados da segunda rota (Específica com Brand ID)
    try:
        res2 = requests.get("https://wswork.com.br/cars_by_brand.json")
        res2.raise_for_status()
        carros_por_marca = res2.json().get("cars", [])
    except Exception as e:
        print(f"Aviso: Erro ao aceder cars_by_brand.json - {e}")

    # --- TRANSFORMAÇÃO (Transform) ---
    
    # Unificação e Deduplicação: Utiliza um dicionário onde a chave é o ID do carro.
    # O tempo de busca em dicionários no Python é O(1), o que torna o merge extremamente rápido.
    todos_carros = {}
    
    for c in carros_geral:
        todos_carros[c["id"]] = c
        
    for c in carros_por_marca:
        # Se o carro existir na segunda lista, ele sobrescreve o primeiro.
        # Decisão técnica: A segunda lista é mais rica pois contém a chave estrangeira "brand".
        todos_carros[c["id"]] = c 

    # Dicionário local para traduzir os IDs de marca vindos da API para strings legíveis.
    mapa_nomes_marcas = {
        1: "Toyota",
        2: "Volkswagen",
        3: "Chevrolet",
        4: "Honda",
        5: "Ford"
    }

    # Marca 'Fallback'. Caso a API envie um carro sem brand_id, 
    # ele não fica órfão no banco de dados.
    marca_default = models.Marca(nome_marca="Multimarcas")
    db.add(marca_default)
    db.commit()
    db.refresh(marca_default)
    
    marcas_criadas = {"default": marca_default.id}
    modelos_criados = {}

    print(f"Total de {len(todos_carros)} veículos únicos encontrados. A processar persistência relacional...")

    # --- CARGA ---
    
    for carro in todos_carros.values():
        brand_id = carro.get("brand")
        
        # 1. Normalização da tabela Marcas
        if brand_id and brand_id not in marcas_criadas:
            nome_marca = mapa_nomes_marcas.get(brand_id, f"Marca {brand_id}")
            nova_marca = models.Marca(nome_marca=nome_marca)
            db.add(nova_marca)
            db.commit()
            db.refresh(nova_marca)
            marcas_criadas[brand_id] = nova_marca.id

        marca_final_id = marcas_criadas.get(brand_id, marcas_criadas["default"])

        # 2. Normalização da tabela Modelos
        modelo_id = carro.get("modelo_id")
        nome_modelo = carro.get("nome_modelo", "Desconhecido")

        if modelo_id not in modelos_criados:
            novo_modelo = models.Modelo(
                id=modelo_id,
                nome=nome_modelo,
                valor_fipe=0.0,
                marca_id=marca_final_id
            )
            db.add(novo_modelo)
            db.commit()
            modelos_criados[modelo_id] = True

        # 3. Higienização de tipagem cambial 
        # Algumas APIs enviam milhares como 50 em vez de 50000. Essa lógica normaliza isso.
        valor_real = carro.get("valor", 0.0)
        if valor_real < 1000:
            valor_real *= 1000

        # 4. Inserção final da entidade Carro
        novo_carro = models.Carro(
            id=carro.get("id"),
            modelo_id=modelo_id,
            ano=carro.get("ano", 2000),
            combustivel=carro.get("combustivel", "FLEX"), # Padronizado para visualização
            num_portas=carro.get("num_portas", 4),
            cor=carro.get("cor", "Padrão"),
            quilometragem=0,
            valor_anuncio=valor_real,
            descricao="Veículo importado das APIs oficiais da WS Work."
        )
        db.add(novo_carro)

    # Executa o commit final de todos os carros em lote (Batch Insert) para otimizar I/O
    db.commit()
    db.close()
    print("Banco de dados atualizado combinando as duas rotas com sucesso!")

if __name__ == "__main__":
    popular_banco()