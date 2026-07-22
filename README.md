# ⚽ Projeto API - Football Data Pipeline & Analytics

## 📌 Objetivo

Projeto desenvolvido para estudo prático de **Engenharia e Análise de Dados** utilizando Python, Git, GitHub, consumo de APIs REST e Banco de Dados Relacional.

O objetivo principal é construir um pipeline completo de dados do **Campeonato Brasileiro Série A** utilizando a **Football Data API**, evoluindo a arquitetura do projeto desde a ingestão bruta (**Camada Bronze**), passando pelo tratamento e estruturação relacional (**Camada Silver**), até a persistência em banco de dados **PostgreSQL** para consumo analítico (**Camada Gold**).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Consumo de Dados:** Requests
* **Processamento e ETL:** Pandas, OpenPyXL, AST (`literal_eval`)
* **Banco de Dados Relacional:** PostgreSQL / pgAdmin 4
* **ORM e Conectores:** SQLAlchemy, Psycopg2
* **Gestão de Variáveis:** python-dotenv
* **Controle de Versão:** Git & GitHub

---

## 📂 Estrutura do Projeto

projeto-api/
│
├── data/
│   ├── raw/                         # Camada Bronze (Dados Brutos em CSV)
│   │   ├── artilheiros.csv
│   │   ├── competicoes.csv
│   │   ├── partidas.csv
│   │   ├── temporadas.csv
│   │   └── times.csv
│   │
│   └── processed/                   # Camada Silver (Tabelas Tratadas em Excel)
│       ├── arbitros.xlsx
│       ├── artilheiros.xlsx
│       ├── competicoes.xlsx
│       ├── jogadores.xlsx
│       ├── tabela_partidas_tratada.xlsx
│       ├── tecnicos.xlsx
│       ├── temporadas.xlsx
│       └── times.xlsx
│
├── docs/                            # Documentações, esquemas do banco e relatórios
│
├── src/                             # Módulos Python
│   ├── carregar_dados.py            # Script ETL de carga no PostgreSQL (Silver -> Gold)
│   ├── dashboard.py                 # Módulo para visualizações
│   ├── database.py                  # Módulo de conexão e engine do PostgreSQL (SQLAlchemy)
│   ├── extract.py                   # Script de ingestão da API (Bronze)
│   ├── generate_dimensions.py       # Script de parsing e modelagem das Dimensões (Silver)
│   ├── main.py                      # Script principal de orquestração
│   └── transform.py                 # Script de limpeza e transformação de Partidas (Silver)
│
├── .env                             # Credenciais e API Keys (Ignorado no Git)
├── .gitignore
├── README.md
└── requirements.txt

---

## 🌐 Fonte dos Dados

Os dados são consumidos via **Football Data API**.

* **Competição Principal:** Campeonato Brasileiro Série A (Código: `2013`)

---

## 🏗️ Arquitetura e Modelagem de Dados

O projeto segue a arquitetura em camadas (**Medallion Architecture**):

[ API REST ] ──> (src/extract.py) ──> [ data/raw/ (.csv) ] ──> (src/transform.py / generate_dimensions.py) ──> [ data/processed/ (.xlsx) ] ──> (src/carregar_dados.py) ──> [ PostgreSQL: futebol_db ]
                                      (Camada Bronze)                                                           (Camada Silver)                                                  (Camada Gold)

### 1. Camada Bronze (`data/raw/`)
Armazena as respostas brutas da API em formato CSV mantendo a estrutura original das respostas JSON.

### 2. Camada Silver (`data/processed/`)
Realiza a limpeza, tratamento de fusos horários, descompactação (*unnest*) de objetos complexos (listas e dicionários) e normalização relacional:

| Tabela Processada | Fonte / Origem | Principais Tratamentos & Conteúdo |
| --- | --- | --- |
| **`tabela_partidas_tratada.xlsx`** | `partidas.csv` | Ajuste de timezone, placares, status, rodadas e IDs das equipes. |
| **`temporadas.xlsx`** | `temporadas.csv` | Extração do `id_vencedor` e limpeza de datas de vigência. |
| **`competicoes.xlsx`** | `competicoes.csv` | Mapeamento do país e código oficial da competição. |
| **`times.xlsx`** | `times.csv` | Extração do país, ano de fundação, estádio e links dos escudos. |
| **`tecnicos.xlsx`** | `times.csv` (`coach`) | *Unnest* do objeto `coach` vinculado ao seu respectivo `id_time`. |
| **`jogadores.xlsx`** | `times.csv` (`squad`) | *Unnest* completo da lista de atletas de cada clube. |
| **`artilheiros.xlsx`** | `artilheiros.csv` | Descompactação dos objetos `player` e `team` com métricas de gols/assistências. |
| **`arbitros.xlsx`** | `partidas.csv` (`referees`) | *Unnest* e deduplicação dos árbitros e assistentes que atuaram nas partidas. |

### 3. Camada Gold (`PostgreSQL - futebol_db`)
As tabelas tratadas da Camada Silver são ingeridas e persistidas no banco **PostgreSQL** (`futebol_db`) através do SQLAlchemy, disponibilizando dados modelados em Star Schema para consulta via SQL ou conexões de Business Intelligence / API.

---

## 🚀 Como Executar o Projeto

### 1. Clonar o Repositório e Criar Ambiente Virtual

git clone https://github.com/Jardiel-dev/projeto-api.git
cd projeto-api

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

### 2. Instalar Dependências

pip install -r requirements.txt

### 3. Configurar Chaves e Conexão (.env)

Crie um arquivo `.env` na raiz do projeto com as credenciais da API e do seu Banco PostgreSQL:

API_KEY=sua_chave_api_aqui
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha_aqui
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=futebol_db

### 4. Executar os Pipelines de Dados

**A. Extração de Dados Brutos (Camada Bronze):**

python src/extract.py

**B. Processamento e Geração das Tabelas Relacionais (Camada Silver):**

python src/transform.py
python src/generate_dimensions.py

**C. Carga no Banco PostgreSQL (Camada Gold):**

python src/carregar_dados.py

---

## 📈 Status do Projeto & Próximos Passos

* [x] Ingestão e tratamento dos dados brutos em Camada Silver (Pandas / OpenPyXL);
* [x] Modelagem Relacional em Star Schema (Tabela Fato `partidas` + 7 Tabelas de Dimensão);
* [x] Configuração da infraestrutura PostgreSQL e conexão automatizada via Python (SQLAlchemy);
* [x] Carga e povoamento automatizado das tabelas no banco de dados (`futebol_db`);
* [x] Geração de Relatório Técnico de Execução em PDF;
* [ ] Construção de endpoints com API REST (FastAPI/Flask) para disponibilização dos dados;
* [ ] Construção de Dashboard interativo (Power BI / Streamlit via `src/dashboard.py`).