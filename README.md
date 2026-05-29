# 🚗 WS Work Motors - Full Stack Challenge

Bem-vindo ao repositório do **WS Work Motors**, uma aplicação Full Stack moderna desenvolvida como resolução do desafio técnico para a WS Work.

Este projeto consolida os requisitos de **Front-end** e **Back-end** em um único monorepo, utilizando arquitetura orientada a microsserviços através de contêineres Docker, persistência relacional e integração nativa com Inteligência Artificial.

---

## 🛠️ Stack Tecnológica

### Front-end

* React (Vite)
* TypeScript (tipagem estrita e DTOs)
* Tailwind CSS (UI/UX responsiva)
* Axios (consumo de API)

### Back-end

* Python 3.10
* FastAPI (alta performance e rotas assíncronas)
* SQLAlchemy (ORM)
* Pydantic v2 (validação de schemas)
* PostgreSQL (banco de dados relacional via Docker)
* Integração OpenAI (GPT-3.5 Turbo)

---

## 💡 Diferenciais e Decisões Arquiteturais

### 1. Padrão BFF — Backend For Frontend

Em vez de sobrecarregar o cliente React com múltiplas requisições, como carros, marcas e modelos, além do cruzamento de dados locais, o Back-end atua como um **BFF**.

Ele realiza o processo de *Data Flattening* e entrega os objetos já resolvidos para o Front-end, economizando processamento no navegador e simplificando a camada de apresentação.

---

### 2. ETL e Idempotência — Seed Inteligente

O requisito de consumir as APIs oficiais da WS Work, `cars.json` e `cars_by_brand.json`, foi resolvido a nível de banco de dados.

O contêiner Python executa um script `seed.py` na inicialização, responsável por:

* Extrair dados das duas rotas oficiais;
* Resolver conflitos e duplicidades;
* Criar a árvore relacional;
* Popular o banco PostgreSQL automaticamente.

O script é **idempotente**, protegendo os dados em reinícios do servidor e evitando duplicações.

---

### 3. Persistência Dinâmica — Upsert

O formulário de cadastro permite texto livre para **Marca** e **Modelo**.

O Back-end intercepta a requisição, verifica se as entidades já existem e, caso não existam, cria as marcas e modelos *on the fly* antes de salvar o veículo.

Com isso, a aplicação mantém a integridade referencial mesmo aceitando entradas dinâmicas do usuário.

---

### 4. Resiliência na IA

A funcionalidade de IA possui um bloco de *Fallback*.

Caso a API da OpenAI apresente timeout, indisponibilidade ou falha de créditos, a aplicação intercepta o erro e gera uma descrição local padronizada.

Dessa forma, o usuário e o Front-end nunca recebem um erro `500` não tratado.

---

## 🚀 Como Executar o Projeto com Docker

O ecossistema está **100% conteinerizado**.

Não é necessário instalar Node.js, Python ou PostgreSQL na máquina local.

### Pré-requisitos

Antes de iniciar, certifique-se de possuir instalado:

* Docker
* Docker Compose

---

### 1. Clone o repositório

```bash
git clone https://github.com/EricBCezimbra/ws-work-fullstack-test.git
cd ws-work-fullstack-test
```

---

### 2. Suba a infraestrutura completa

```bash
docker-compose up --build
```

> **Observação:**
> Na primeira execução, o Docker aguardará o PostgreSQL inicializar através do Healthcheck.
> Em seguida, o script de Seed será executado automaticamente, baixando os dados das APIs da WS Work.

---

### 3. Acesse a aplicação

| Serviço            | URL                        |
| :----------------- | :------------------------- |
| Front-end          | http://localhost:5173      |
| Back-end — Swagger | http://localhost:8000/docs |

---

## 📚 Documentação de Componentes Reutilizáveis

Atendendo ao requisito de documentação do Front-end, o componente principal de exibição, `<VehicleCard />`, foi desenhado para ser totalmente **Dumb/Presentational**.

Isso facilita sua reutilização em outros contextos, como:

* Carrinho de compras;
* Página de favoritos;
* Listagens promocionais;
* Destaques da semana;
* Vitrines de veículos.

---

## `<VehicleCard />`

### Props

| Prop    | Tipo    | Descrição                                                                                                                   |
| :------ | :------ | :-------------------------------------------------------------------------------------------------------------------------- |
| `carro` | `Carro` | Objeto integral do veículo contendo especificações técnicas e campos achatados pelo BFF, como `nome_marca` e `nome_modelo`. |

---

### Comportamento

#### Line-Clamp

Utiliza limitação nativa de 3 linhas para a descrição do veículo, garantindo que textos grandes gerados pela IA não quebrem o grid de exibição.

#### Intl

A formatação de moeda é delegada ao `Intl.NumberFormat` nativo do navegador, permitindo suporte à localização sem a necessidade de bibliotecas externas pesadas.

---

### Exemplo de uso em outras telas

```tsx
import { VehicleCard } from './components/VehicleCard';

function PromocoesSemana({ veiculoDestaque }) {
  return (
    <div className="w-full max-w-sm">
      <VehicleCard carro={veiculoDestaque} />
    </div>
  );
}
```

---

## 👨‍💻 Autor

Desenvolvido por **Eric Bitencourt Cezimbra** — 2026
