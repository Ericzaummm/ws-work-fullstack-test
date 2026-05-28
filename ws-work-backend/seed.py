import requests
from database import SessionLocal, engine
import models

# cria as tabelas se elas não existirem.
models.Base.metadata.create_all(bind=engine)

def popular_banco():
    db = SessionLocal()
    
    # VERIFICAÇÃO
    # Se já existir pelo menos um carro no banco, significa que o seed já rodou antes.
    if db.query(models.Carro).first():
        print("Banco de dados já está populado. Pulando a importação da API.")
        db.close()
        return

    print("Iniciando o download dos dados das DUAS rotas da WS Work...")

    carros_geral = []
    carros_por_marca = []

    try:
        res1 = requests.get("https://wswork.com.br/cars.json")
        res1.raise_for_status()
        carros_geral = res1.json().get("cars", [])
    except Exception as e:
        print(f"Aviso: Erro em cars.json - {e}")

    try:
        res2 = requests.get("https://wswork.com.br/cars_by_brand.json")
        res2.raise_for_status()
        carros_por_marca = res2.json().get("cars", [])
    except Exception as e:
        print(f"Aviso: Erro em cars_by_brand.json - {e}")

    todos_carros = {}
    for c in carros_geral:
        todos_carros[c["id"]] = c
    for c in carros_por_marca:
        todos_carros[c["id"]] = c 

    mapa_nomes_marcas = {
        1: "Toyota",
        2: "Volkswagen",
        3: "Chevrolet",
        4: "Honda",
        5: "Ford"
    }

    marca_default = models.Marca(nome_marca="Multimarcas")
    db.add(marca_default)
    db.commit()
    db.refresh(marca_default)
    
    marcas_criadas = {"default": marca_default.id}
    
    # Dicionário de mapeamento: ID da API -> ID real gerado pelo nosso Postgres
    modelos_criados = {}

    print(f"Total de {len(todos_carros)} veículos únicos encontrados. Processando...")

    for carro in todos_carros.values():
        brand_id = carro.get("brand")
        
        if brand_id and brand_id not in marcas_criadas:
            nome_marca = mapa_nomes_marcas.get(brand_id, f"Marca {brand_id}")
            nova_marca = models.Marca(nome_marca=nome_marca)
            db.add(nova_marca)
            db.commit()
            db.refresh(nova_marca)
            marcas_criadas[brand_id] = nova_marca.id

        marca_final_id = marcas_criadas.get(brand_id, marcas_criadas["default"])

        modelo_id_api = carro.get("modelo_id")
        nome_modelo = carro.get("nome_modelo", "Desconhecido")

        if modelo_id_api not in modelos_criados:
            novo_modelo = models.Modelo(
                # Deixa o Postgres criar o ID sozinho
                nome=nome_modelo,
                valor_fipe=0.0,
                marca_id=marca_final_id
            )
            db.add(novo_modelo)
            db.commit()
            db.refresh(novo_modelo)
            # Guarda o ID verdadeiro que o banco gerou
            modelos_criados[modelo_id_api] = novo_modelo.id
            
        # Pega a chave estrangeira real do modelo
        modelo_final_id = modelos_criados[modelo_id_api]

        valor_real = carro.get("valor", 0.0)
        if valor_real < 1000:
            valor_real *= 1000

        # Insere o Carro Final
        novo_carro = models.Carro(
            modelo_id=modelo_final_id,
            ano=carro.get("ano", 2000),
            combustivel=carro.get("combustivel", "Flex"),
            num_portas=carro.get("num_portas", 4),
            cor=carro.get("cor", "Padrão"),
            quilometragem=0,
            valor_anuncio=valor_real,
            descricao="Veículo importado das APIs oficiais da WS Work."
        )
        db.add(novo_carro)

    db.commit()
    db.close()
    print("Banco de dados atualizado combinando as duas rotas com sucesso!")

if __name__ == "__main__":
    popular_banco()