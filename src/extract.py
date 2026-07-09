import requests
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

url = "https://api.football-data.org/v4/competitions/2013/scorers"

headers = {
    "X-Auth-Token": API_KEY
}


def conectar_api(url):
    print("Conectando à API...")

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Conexão realizada com sucesso!")
        return response.json()

    print(f"Erro: {response.status_code}")
    print(response.text)
    return None


dados = conectar_api(url)

if dados:

    artilheiros = dados["scorers"]

    tabela = pd.DataFrame(artilheiros)

    print(tabela.head())

    tabela.to_csv("data/raw/artilheiros.csv", index=False)

    print("\nArquivo salvo em data/raw/artilheiros.csv")