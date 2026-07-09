# Projeto API - Football Data

## Objetivo

Projeto desenvolvido para estudo de Engenharia de Dados utilizando Python, Git, GitHub e consumo de APIs.

O objetivo é extrair dados do Campeonato Brasileiro Série A utilizando a Football Data API e construir a primeira camada de um pipeline de dados (Camada Bronze), armazenando os dados brutos em arquivos CSV.

Durante o desenvolvimento foram aplicados conceitos como:

* consumo de APIs;
* manipulação de dados em formato JSON;
* transformação de dados utilizando Pandas;
* organização de projeto;
* versionamento com Git e GitHub.

---

# Tecnologias utilizadas

* Python
* Requests
* Pandas
* python-dotenv
* Git
* GitHub

---

# Estrutura do projeto

```
projeto-api/
│
├── data/
│   ├── raw/
│   │   ├── competicoes.csv
│   │   ├── temporadas.csv
│   │   ├── times.csv
│   │   ├── partidas.csv
│   │   └── artilheiros.csv
│   │
│   └── processed/
│
├── docs/
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── database.py
│   ├── dashboard.py
│   └── main.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Fonte dos dados

Os dados foram extraídos utilizando a:

**Football Data API**

Competição utilizada:

* Campeonato Brasileiro Série A
* Código da competição: `2013`

---

# Dados extraídos

As informações foram organizadas na camada Bronze, mantendo os dados brutos recebidos da API.

Tabelas geradas:

| Arquivo         | Descrição                               |
| --------------- | --------------------------------------- |
| competicoes.csv | Informações das competições disponíveis |
| temporadas.csv  | Temporadas relacionadas ao campeonato   |
| times.csv       | Times participantes da competição       |
| partidas.csv    | Partidas realizadas no campeonato       |
| artilheiros.csv | Principais artilheiros da competição    |

---

# Processo de extração

A extração foi desenvolvida utilizando uma função genérica responsável por buscar diferentes informações da API.

A função realiza:

* conexão com a API;
* validação da resposta;
* conversão do retorno JSON;
* criação de DataFrame utilizando Pandas;
* armazenamento dos dados em arquivos CSV.

A função recebe diferentes parâmetros:

* URL do endpoint;
* chave do JSON retornado pela API;
* nome do arquivo de saída.

Isso permite reutilizar o mesmo código para diferentes tabelas, evitando duplicação.

Exemplo:

```python
extrair_dados(
    url,
    "scorers",
    "artilheiros"
)
```

---

# Como executar o projeto

## 1. Criar ambiente virtual

```bash
python -m venv .venv
```

## 2. Ativar ambiente virtual

Windows:

```bash
.venv\Scripts\activate
```

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## 4. Configurar variável de ambiente

Criar um arquivo `.env` na raiz do projeto:

```env
API_KEY=SEU_TOKEN
```

## 5. Executar a extração

```bash
python src/extract.py
```

Após a execução, os arquivos serão gerados em:

```
data/raw/
```

---

# Controle de versão

O projeto utiliza Git para acompanhar a evolução do desenvolvimento.

As alterações são registradas através de commits, mantendo o histórico das etapas realizadas.

---

# Próximas etapas

* Tratamento e limpeza dos dados (Camada Silver);
* Padronização dos dados;
* Modelagem do banco de dados;
* Carga dos dados em banco;
* Construção de análises;
* Desenvolvimento de dashboard.
