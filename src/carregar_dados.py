import os
import pandas as pd
from database import engine

# 📁 Caminho da pasta com os arquivos tratados
PASTA_PROCESSED = os.path.join("data", "processed")

# 🗺️ Mapeamento: "nome_do_arquivo.xlsx": "nome_da_tabela_no_postgres"
ARQUIVOS_TABELAS = {
    "competicoes.xlsx": "competicoes",
    "temporadas.xlsx": "temporadas",
    "times.xlsx": "times",
    "tecnicos.xlsx": "tecnicos",
    "arbitros.xlsx": "arbitros",
    "jogadores.xlsx": "jogadores",
    "artilheiros.xlsx": "artilheiros",
    "tabela_partidas_tratada.xlsx": "partidas",
}


def carregar_tudo():
    print("🚀 Iniciando a carga dos arquivos no PostgreSQL...\n")

    for arquivo, tabela in ARQUIVOS_TABELAS.items():
        caminho_completo = os.path.join(PASTA_PROCESSED, arquivo)

        if os.path.exists(caminho_completo):
            try:
                # 1. Leitura do arquivo Excel
                df = pd.read_excel(caminho_completo)

                # 2. Envio das informações para a tabela no PostgreSQL
                df.to_sql(
                    name=tabela,
                    con=engine,
                    if_exists="replace",  # Substitui a tabela caso já exista
                    index=False,
                )
                print(f"✅ Tabela '{tabela}' carregada com sucesso! ({len(df)} registros)")
            except Exception as e:
                print(f"❌ Erro ao carregar '{arquivo}': {e}")
        else:
            print(f"⚠️ Arquivo não encontrado: {caminho_completo}")

    print("\n🎉 Carga finalizada com sucesso!")


if __name__ == "__main__":
    carregar_tudo()