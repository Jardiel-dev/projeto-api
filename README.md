
```markdown
# ⚽ Projeto API - Football Data Pipeline

## 📌 Objetivo

Projeto desenvolvido para estudo prático de **Engenharia e Análise de Dados** utilizando Python, Git, GitHub e consumo de APIs REST.

O objetivo principal é construir um pipeline completo de dados (ETL) do **Campeonato Brasileiro Série A** utilizando a **Football Data API**, evoluindo a arquitetura do projeto desde a ingestão bruta (**Camada Bronze**) até o tratamento unificado, parse de objetos complexos, tradução exaustiva e estruturação relacional em tabelas fortemente tipadas (**Camada Silver**).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Consumo de Dados:** Requests (API REST)
* **Processamento e ETL:** Pandas, OpenPyXL, AST (`literal_eval`)
* **Gestão de Variáveis:** python-dotenv
* **Controle de Versão:** Git & GitHub

---

## 📂 Estrutura do Projeto

```text
projeto-api/
│
├── data/
│   ├── raw/                       # Camada Bronze (Dados Brutos em CSV)
│   │   ├── artilheiros.csv
│   │   ├── competicoes.csv
│   │   ├── partidas.csv
│   │   ├── temporadas.csv
│   │   └── times.csv
│   │
│   └── processed/                 # Camada Silver (Tabelas Relacionais Tratadas em Excel)
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
│   ├── transform.py               # Módulo Unificado de Limpeza, Fato e Dimensões (Silver)
│   └── main.py                    # Orquestrador principal e centralizado do pipeline
│
├── .env                           # Credenciais e API Keys (Ignorado no Git)
├── .gitignore
├── README.md
└── requirements.txt

```

---

## 🌐 Fonte dos Dados

Os dados são consumidos via **Football Data API**.

* **Competição Principal:** Campeonato Brasileiro Série A (Código Oficial: `2013`)

---

## 🏗️ Arquitetura e Modelagem de Dados

O projeto adota os conceitos fundamentais da **Arquitetura Medallion**, dividindo o fluxo de maturação dos dados em duas fases principais:

```text
[ API REST ] ──> (src/extract.py) ──> [ data/raw/ (.csv) ] ──> (src/transform.py) ──> [ data/processed/ (.xlsx) ]
                                      (Camada Bronze)                                 (Camada Silver Unificada)

```

### 1. Camada Bronze (`data/raw/`)

Armazena os payloads brutos obtidos diretamente dos endpoints da API estruturados em arquivos CSV, mantendo a integridade original das propriedades JSON (dicionários e listas textuais) para auditorias de dados.

### 2. Camada Silver (`data/processed/`)

Fase onde ocorre a higienização de dados corporativos. Um processo completo unificado descompacta os objetos complexos (*unnest*) e aplica regras de modelagem relacional:

| Tabela Processada | Fonte / Origem | Principais Tratamentos & Conteúdo |
| --- | --- | --- |
| **tabela_partidas_tratada.xlsx** | partidas.csv | **Tabela Fato:** Contém chaves e métricas. Filtra apenas partidas concluídas (`FINISHED` -> `FINALIZADO`), realiza o parse e a ordenação de IDs estruturais. |
| **temporadas.xlsx** | temporadas.csv | **Dimensão:** Armazena vigências, chaves das competições e extração correta de anos temporais de início e fim. |
| **competicoes.xlsx** | competicoes.csv | **Dimensão:** Armazena metadados de identificação dos campeonatos processados e áreas geográficas. |
| **times.xlsx** | times.csv | **Dimensão:** Cadastro consolidado dos clubes com siglas, anos de fundação e estádios. |
| **tecnicos.xlsx** | times.csv (coach) | **Dimensão:** Isolamento de técnicos associados às suas equipes atuais via chaves estrangeiras. |
| **jogadores.xlsx** | times.csv (squad) | **Dimensão:** Unnest completo do elenco dos clubes com tratamento exaustivo de posições. |
| **artilheiros.xlsx** | artilheiros.csv | **Dimensão de Métricas:** Estatísticas de gols, assistências e pênaltis vinculadas aos IDs de jogadores e clubes, sem dados redundantes de texto. |
| **arbitros.xlsx** | partidas.csv (referees) | **Dimensão:** Isolamento, filtragem estrita pelo tipo principal (`REFEREE`) e eliminação de duplicatas de árbitros atuantes. |

---

## 📐 Engenharia de Atributos e Regras de Negócio (Silver)

Para preparar a base de dados para análises robustas em ferramentas de Business Intelligence (Power BI e Excel), implementamos melhorias profundas de Engenharia de Dados recomendadas por feedbacks de qualidade técnica:

* **Fim das Redundâncias Textuais:** Todas as tabelas de dimensão periféricas (como *Artilheiros, Jogadores e Técnicos*) foram normalizadas. Removemos colunas textuais duplicadas (ex: `nome_time` dentro de jogadores), tornando a integridade referencial estritamente dependente de chaves estrangeiras (`id_time`, `id_jogador`), reduzindo significativamente a pegada de armazenamento.
* **Organização Estrutural (IDs na Frente):** Para garantir escaneabilidade e seguir as convenções de design de bancos de dados, todas as chaves primárias e estrangeiras (`id_...`) foram posicionadas de forma padronizada como as **primeiras colunas** de todas as planilhas geradas.
* **Tipagem Temporal Nativa (`datetime`):** Para evitar problemas em que campos de data eram lidos como textos puros bloqueando agrupamentos temporais, todas as colunas cronológicas (datas de nascimento, início e término de temporadas, horários de jogos) passam pela conversão para o tipo primitivo `datetime` do Pandas. Isso garante que ferramentas de Analytics consigam agrupar os dados nativamente por Ano, Trimestre e Mês.
* **Tradução Localizada Completa:** Mapeamento exaustivo das posições dos atletas e termos operacionais de inglês para o português. Posições como *Goalkeeper* tornam-se *Goleiro*, *Centre-Back* vira *Zagueiro*, *Right Winger* vira *Ponta Direito*, etc., cobrindo todas as categorias sem valores nulos ou termos mistos no modelo. O tipo de arbitragem `REFEREE` também foi traduzido uniformemente para `Árbitro`.

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

Crie um arquivo chamado `.env` na raiz do seu projeto e insira o seu token de autorização da Football Data API:

```env
API_KEY=sua_chave_aqui

```

### 4. Executar o Orquestrador Centralizado

Para executar todo o pipeline de forma linear e sequencial, basta rodar o script controlador principal. Ele invocará a extração e a transformação completa da camada Silver de ponta a ponta:

```bash
python src/main.py

```

Após a conclusão da execução exibida nos logs do terminal, todos os arquivos relacionais altamente otimizados e prontos para consumo estarão salvos no diretório `data/processed/`.

---

## 📈 Próximos Passos

* [ ] Carga das tabelas processadas em Banco de Dados Relacional (PostgreSQL / SQLite via `src/database.py`);
* [ ] Modelagem Dimensional em Star Schema (Fatos e Dimensões);
* [ ] Construção de Dashboard interativo (Power BI / Streamlit via `src/dashboard.py`).

```

```
