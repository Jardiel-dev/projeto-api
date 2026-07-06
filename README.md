# Projeto API - Football Data

## Objetivo

Projeto para estudo de Git, GitHub e consumo de APIs utilizando Python.

## Tecnologias

- Python
- Requests
- Pandas
- Git
- GitHub

## Estrutura

```
projeto-api/
│
├── data/
│   ├── raw/
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

## Como executar

1. Criar o ambiente virtual.
2. Instalar as dependências:

```bash
pip install -r requirements.txt
```

3. Criar um arquivo `.env`:

```env
API_KEY=SEU_TOKEN
```

4. Executar:

```bash
python src/extract.py
```

## Resultado

O programa consulta a API Football Data e salva um arquivo CSV em:

```
data/raw/competicoes.csv
```