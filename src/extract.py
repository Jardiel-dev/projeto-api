import requests
import pandas as pd

# Coloque seu token aqui
API_KEY = "4b7bb6858259406e96d72ed682d423cf"

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