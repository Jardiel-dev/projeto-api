import requests
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

headers = {
    "X-Auth-Token": API_KEY
}


def extrair_dados(url, chave, arquivo):
    print(f"\nConectando à API: {url}")

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Conexão realizada com sucesso!")

        dados = response.json()

        tabela = pd.DataFrame(dados[chave])

        print(tabela.head())

        tabela.to_csv(f"data/raw/{arquivo}.csv", index=False)

        print(f"Arquivo salvo em data/raw/{arquivo}.csv")

        return tabela

    print(f"Erro: {response.status_code}")
    print(response.text)

    return None


# Campeonato Brasileiro
competicao = 2013


# 1 - Principais artilheiros
url_artilheiros = f"https://api.football-data.org/v4/competitions/{competicao}/scorers"

extrair_dados(
    url_artilheiros,
    "scorers",
    "artilheiros"
)


# 2 - Partidas
url_partidas = f"https://api.football-data.org/v4/competitions/{competicao}/matches"

extrair_dados(
    url_partidas,
    "matches",
    "partidas"
)


# 3 - Times
url_times = f"https://api.football-data.org/v4/competitions/{competicao}/teams"

extrair_dados(
    url_times,
    "teams",
    "times"
)