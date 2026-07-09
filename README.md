# Projeto API - Football Data

## Objetivo

Projeto para estudo de Git, GitHub e consumo de APIs utilizando Python.

O objetivo é extrair dados do Campeonato Brasileiro Série A utilizando a Football Data API e construir a primeira camada do pipeline de dados (Bronze).

---

## Tecnologias

- Python
- Requests
- Pandas
- python-dotenv
- Git
- GitHub

---

## Estrutura

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

## Dados extraídos

Competição utilizada:

- Campeonato Brasileiro Série A (ID 2013)

Arquivos gerados na camada Bronze:

- competicoes.csv
- temporadas.csv
- times.csv
- partidas.csv
- artilheiros.csv

---

## Como executar

1. Criar o ambiente virtual

2. Instalar as dependências

```bash
pip install -r requirements.txt
```

3. Criar o arquivo `.env`

```env
API_KEY=SEU_TOKEN
```

4. Executar

```bash
python src/extract.py
```

---

## Próximos passos

- Tratamento dos dados (Camada Silver)
- Modelagem do banco de dados
- Carga no banco
- Dashboard