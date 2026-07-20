import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
headers = {"X-Auth-Token": API_KEY}

def extrair_dados(url, chave, arquivo):
    print(f"Conectando à API: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        dados = response.json()
        tabela = pd.DataFrame(dados[chave])
        # Garante a criação da pasta caso não exista
        os.makedirs("data/raw", exist_ok=True)
        tabela.to_csv(f"data/raw/{arquivo}.csv", index=False)
        print(f"✅ Arquivo salvo em data/raw/{arquivo}.csv")
        return tabela
    print(f"❌ Erro: {response.status_code} - {response.text}")
    return None

def executar_extracao():
    print("\n====== [CAMADA BRONZE] INICIANDO EXTRAÇÃO DE DADOS ======")
    competicao = 2013  # Campeonato Brasileiro

    # 1 - Principais artilheiros
    url_artilheiros = f"https://api.football-data.org/v4/competitions/{competicao}/scorers"
    extrair_dados(url_artilheiros, "scorers", "artilheiros")

    # 2 - Partidas
    url_partidas = f"https://api.football-data.org/v4/competitions/{competicao}/matches"
    extrair_dados(url_partidas, "matches", "partidas")

    # 3 - Times
    url_times = f"https://api.football-data.org/v4/competitions/{competicao}/teams"
    extrair_dados(url_times, "teams", "times")

if __name__ == '__main__':
    executar_extracao()