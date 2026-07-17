
```markdown
# ⚽ Projeto API - Football Data Pipeline

## 📌 Objetivo

Projeto desenvolvido para estudo prático de **Engenharia e Análise de Dados** utilizando Python, Git, GitHub e consumo de APIs REST.

O objetivo principal é construir um pipeline completo de dados do **Campeonato Brasileiro Série A** utilizando a **Football Data API**, evoluindo a arquitetura do projeto desde a ingestão bruta (**Camada Bronze**) até o tratamento, parse de objetos complexos e estruturação relacional em Excel (**Camada Silver**).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Consumo de Dados:** Requests
* **Processamento e ETL:** Pandas, OpenPyXL, AST (`literal_eval`)
* **Gestão de Variáveis:** python-dotenv
* **Controle de Versão:** Git & GitHub

---

## 📂 Estrutura do Projeto

```text
projeto-api/
│
├── data/
│   ├── raw/                       # Camada Bronze (Dados Brutos)
│   │   ├── artilheiros.csv
│   │   ├── competicoes.csv
│   │   ├── partidas.csv
│   │   ├── temporadas.csv
│   │   └── times.csv
│   │
│   └── processed/                 # Camada Silver (Tabelas Relacionais Tratadas)
│       ├── arbitros.xlsx
│       ├── artilheiros.xlsx
│       ├── competicoes.xlsx
│       ├── jogadores.xlsx
│       ├── tabela_partidas_tratada.xlsx
│       ├── tecnicos.xlsx
│       ├── temporadas.xlsx
│       └── times.xlsx
│
├── docs/                          # Documentações e esquemas do projeto
│
├── src/                           # Módulos Python
│   ├── dashboard.py               # Módulo para visualizações
│   ├── database.py                # Módulo para persistência em Banco de Dados
│   ├── extract.py                 # Script de ingestão da API (Bronze)
│   ├── generate_dimensions.py     # Script de parsing e modelagem das Dimensões (Silver)
│   ├── main.py                    # Script principal de orquestração
│   └── transform.py               # Script de limpeza e transformação de Partidas (Silver)
│
├── .env                           # Credenciais e API Keys (Ignorado no Git)
├── .gitignore
├── README.md
└── requirements.txt

```

---

## 🌐 Fonte dos Dados

Os dados são consumidos via **Football Data API**.

* **Competição Principal:** Campeonato Brasileiro Série A (Código: `2013`)

---

## 🏗️ Arquitetura e Modelagem de Dados

O projeto segue a arquitetura em camadas (**Medallion Architecture**):

```text
[ API REST ] ──> (src/extract.py) ──> [ data/raw/ (.csv) ] ──> (src/transform.py / generate_dimensions.py) ──> [ data/processed/ (.xlsx) ]
                                      (Camada Bronze)                                                         (Camada Silver)

```

### 1. Camada Bronze (`data/raw/`)

Armazena as respostas brutas da API em formato CSV mantendo o formato original das estruturas JSON/dicionários.

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

---

## 🚀 Como Executar o Projeto

### 1. Clonar o Repositório e Criar Ambiente Virtual

```bash
git clone [https://github.com/Jardiel-dev/projeto-api.git](https://github.com/Jardiel-dev/projeto-api.git)
cd projeto-api

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt

```

### 3. Configurar Chave da API

Crie um arquivo `.env` na raiz do projeto com a sua chave da API:

```env
API_KEY=sua_chave_aqui

```

### 4. Executar os Pipelines de Dados

**A. Extração de Dados Brutos (Camada Bronze):**

```bash
python src/extract.py

```

**B. Processamento e Geração das Tabelas Relacionais (Camada Silver):**

```bash
python src/transform.py
python src/generate_dimensions.py

```

Após a execução, todas as planilhas tratadas estarão disponíveis na pasta `data/processed/`.

---

## 📈 Próximos Passos

* [ ] Carga das tabelas processadas em Banco de Dados Relacional (PostgreSQL / SQLite via `src/database.py`);
* [ ] Modelagem Dimensional em Star Schema (Fatos e Dimensões);
* [ ] Construção de Dashboard interativo (Power BI / Streamlit via `src/dashboard.py`).

```

```