import requests
from database import SessionLocal, engine
import models

# Limpa o banco para não duplicar dados ao rodar novamente
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

def popular_banco():
    db = SessionLocal()
    print("Iniciando o download dos dados das DUAS rotas da WS Work...")

    carros_geral = []
    carros_por_marca = []

    # Puxando da primeira rota
    try:
        res1 = requests.get("https://wswork.com.br/cars.json")
        res1.raise_for_status()
        carros_geral = res1.json().get("cars", [])
    except Exception as e:
        print(f"Aviso: Erro em cars.json - {e}")

    # Puxando da segunda rota
    try:
        res2 = requests.get("https://wswork.com.br/cars_by_brand.json")
        res2.raise_for_status()
        carros_por_marca = res2.json().get("cars", [])
    except Exception as e:
        print(f"Aviso: Erro em cars_by_brand.json - {e}")

    # Unificando as listas (usando um dicionário para o ID do carro não duplicar)
    todos_carros = {}
    
    for c in carros_geral:
        todos_carros[c["id"]] = c
        
    for c in carros_por_marca:
        # Sobrescreve o carro se ele aparecer na segunda lista, porque aqui ele tem o campo "brand"
        todos_carros[c["id"]] = c 

    # Dicionário para "traduzir" os IDs de marca que vêm da API para nomes reais
    mapa_nomes_marcas = {
        1: "Toyota",
        2: "Volkswagen",
        3: "Chevrolet",
        4: "Honda",
        5: "Ford"
    }

    # Marca de segurança para carros que não vierem com o campo "brand"
    marca_default = models.Marca(nome_marca="Multimarcas")
    db.add(marca_default)
    db.commit()
    db.refresh(marca_default)
    
    marcas_criadas = {"default": marca_default.id}
    modelos_criados = {}

    print(f"Total de {len(todos_carros)} veículos únicos encontrados. Processando...")

    # Salvando no Banco Relacional
    for carro in todos_carros.values():
        brand_id = carro.get("brand")
        
        # Cria a Marca se ela ainda não existir no banco
        if brand_id and brand_id not in marcas_criadas:
            nome_marca = mapa_nomes_marcas.get(brand_id, f"Marca {brand_id}")
            nova_marca = models.Marca(nome_marca=nome_marca)
            db.add(nova_marca)
            db.commit()
            db.refresh(nova_marca)
            marcas_criadas[brand_id] = nova_marca.id

        marca_final_id = marcas_criadas.get(brand_id, marcas_criadas["default"])

        # Cria o Modelo se ainda não existir
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

        # Trata o valor (converte 50.000 para 50000.0)
        valor_real = carro.get("valor", 0.0)
        if valor_real < 1000:
            valor_real *= 1000

        # Insere o Carro Final
        novo_carro = models.Carro(
            id=carro.get("id"),
            modelo_id=modelo_id,
            ano=carro.get("ano", 2000),
            combustivel=carro.get("combustivel", "N/A"),
            num_portas=carro.get("num_portas", 4),
            cor=carro.get("cor", "N/A"),
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