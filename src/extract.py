import requests
import pandas as pd

from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")

url = "https://api.football-data.org/v4/competitions/2013/scorers"
headers = {
    "X-Auth-Token": API_KEY
}

print("Conectando à API...")

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Conexão realizada com sucesso!")

    dados = response.json()

    artilheiros = dados["scorers"]

    tabela = pd.DataFrame(artilheiros)

    print(tabela.head())

    tabela.to_csv("data/raw/artilheiros.csv", index=False)

    print("\nArquivo salvo em data/raw/artilheiros.csv")

    tabela.to_csv("data/raw/partidas.csv", index=False)

    print("\nArquivo salvo em data/raw/partidas.csv")

else:
    print(f"Erro: {response.status_code}")
    print(response.text)