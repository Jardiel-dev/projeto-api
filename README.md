Markdown# 
⚽ Projeto API - Football Data Pipeline & Analytics

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
* **Gestão de Variáveis & Segurança:** python-dotenv
* **Controle de Versão:** Git & GitHub

---

## 📂 Estrutura do Projeto

```text
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
│   ├── diagrama.pdf                 # Diagrama de Entidade-Relacionamento (DER)
│   └── relatorio_tecnico.pdf        # Relatório de Execução do Projeto
│
├── src/                             # Módulos Python
│   ├── carregar_dados.py            # Script ETL de carga no PostgreSQL (Silver -> Gold)
│   ├── dashboard.py                 # Módulo para visualizações
│   ├── database.py                  # Conexão segura e verificação/criação do PostgreSQL em 2 passos
│   ├── extract.py                   # Script de ingestão da API (Bronze)
│   ├── generate_dimensions.py       # Script de parsing e modelagem das Dimensões (Silver)
│   ├── main.py                      # Script principal de orquestração
│   └── transform.py                 # Script de limpeza e transformação de Partidas (Silver)
│
├── .env.example                     # Modelo seguro de variáveis de ambiente (Sem senhas)
├── .gitignore                       # Rastreamento ignorado para .env e .venv
├── README.md
└── requirements.txt
🌐 Fonte dos DadosOs dados são consumidos via Football Data API.Competição Principal: Campeonato Brasileiro Série A (Código: 2013)🏗️ Arquitetura e Modelagem de DadosO projeto segue a arquitetura em camadas (Medallion Architecture):Plaintext[ API REST ] ──> (src/extract.py) ──> [ data/raw/ (.csv) ] ──> (src/transform.py / generate_dimensions.py) ──> [ data/processed/ (.xlsx) ] ──> (src/carregar_dados.py) ──> [ PostgreSQL: futebol_db ]
                                      (Camada Bronze)                                                         (Camada Silver)                                                  (Camada Gold)
📐 Diagrama de Modelagem Relacional (DER)A modelagem do banco de dados foi estruturada em esquema relacional mantendo a tabela fato de partidas e suas respectivas tabelas de dimensão (Times, Jogadores, Artilheiros, Árbitros, Técnicos, Competições e Temporadas).📄 Visualizar Diagrama de Entidade-Relacionamento (PDF)1. Camada Bronze (data/raw/)Armazena as respostas brutas da API em formato CSV mantendo a estrutura original das respostas JSON.2. Camada Silver (data/processed/)Realiza a limpeza, tratamento de fusos horários, descompactação (unnest) de objetos complexos (listas e dicionários) e normalização relacional:Tabela ProcessadaFonte / OrigemPrincipais Tratamentos & Conteúdotabela_partidas_tratada.xlsxpartidas.csvAjuste de timezone, placares, status, rodadas e IDs das equipes.temporadas.xlsxtemporadas.csvExtração do id_vencedor e limpeza de datas de vigência.competicoes.xlsxcompeticoes.csvMapeamento do país e código oficial da competição.times.xlsxtimes.csvExtração do país, ano de fundação, estádio e links dos escudos.tecnicos.xlsxtimes.csv (coach)Unnest do objeto coach vinculado ao seu respectivo id_time.jogadores.xlsxtimes.csv (squad)Unnest completo da lista de atletas de cada clube.artilheiros.xlsxartilheiros.csvDescompactação dos objetos player e team com métricas de gols/assistências.arbitros.xlsxpartidas.csv (referees)Unnest e deduplicação dos árbitros e assistentes que atuaram nas partidas.3. Camada Gold (PostgreSQL - futebol_db)As tabelas tratadas da Camada Silver são ingeridas e persistidas no banco PostgreSQL (futebol_db) através do SQLAlchemy.A conexão foi arquitetada em 2 passos seguros:Passo 1 (Servidor Geral): Conecta ao banco postgres padrão para verificar se o banco futebol_db já existe no PostgreSQL e cria-o dinamicamente caso necessário.Passo 2 (Engine do Projeto): Conecta-se especificamente ao banco futebol_db para executar a carga automatizada das tabelas tratadas.🚀 Como Executar o Projeto1. Clonar o Repositório e Criar Ambiente VirtualBashgit clone [https://github.com/Jardiel-dev/projeto-api.git](https://github.com/Jardiel-dev/projeto-api.git)
cd projeto-api

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate
2. Instalar DependênciasBashpip install -r requirements.txt
3. Configurar Chaves e Conexão de Forma Segura (.env)Crie um arquivo .env na raiz do projeto baseado no modelo .env.example fornecido (o arquivo .env está protegido pelo .gitignore e não sobe para o Git):Snippet de códigoAPI_KEY=sua_chave_api_aqui
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha_aqui
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=futebol_db
4. Executar os Pipelines de DadosA. Extração de Dados Brutos (Camada Bronze):Bashpython src/extract.py
B. Processamento e Geração das Tabelas Relacionais (Camada Silver):Bashpython src/transform.py
python src/generate_dimensions.py
C. Teste da Conexão em 2 Passos & Carga no Banco PostgreSQL (Camada Gold):Bashpython src/database.py
python src/carregar_dados.py
📈 Status do Projeto & Próximos Passos[x] Ingestão e tratamento dos dados brutos em Camada Silver (Pandas / OpenPyXL);[x] Modelagem Relacional e disponibilização do Diagrama DER na pasta docs/;[x] Proteção das credenciais com python-dotenv e exclusão de senhas do versionamento;[x] Configuração da infraestrutura PostgreSQL com conexão automatizada em 2 passos;[x] Carga e povoamento automatizado das tabelas no banco de dados (futebol_db);[x] Geração de Relatório Técnico de Execução em PDF;[ ] Construção de endpoints com API REST (FastAPI/Flask) para disponibilização dos dados;[ ] Construção de Dashboard interativo (Power BI / Streamlit via src/dashboard.py).