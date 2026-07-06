


import requests
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

url = "https://api.football-data.org/v4/competitions"

headers = {
    "X-Auth-Token": API_KEY
}

print("Conectando à API...")

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Conexão realizada com sucesso!")

    dados = response.json()

    competicoes = dados["competitions"]

    tabela = pd.DataFrame(competicoes)

    print(tabela.head())

    tabela.to_csv("data/raw/competicoes.csv", index=False)

    print("\nArquivo salvo em data/raw/competicoes.csv")

else:
    print(f"Erro: {response.status_code}")
    print(response.text)