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


def extrair_dados(url, chave, arquivo):
    print("Conectando à API...")

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Conexão realizada com sucesso!")

        dados = response.json()

        tabela = pd.DataFrame(dados[chave])

        print(tabela.head())

        tabela.to_csv(f"data/raw/{arquivo}.csv", index=False)

        print(f"\nArquivo salvo em data/raw/{arquivo}.csv")

        return tabela

    print(f"Erro: {response.status_code}")
    print(response.text)
    return None


extrair_dados(
    url,
    "scorers",
    "artilheiros"
)