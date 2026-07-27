from datetime import datetime
import os
import pandas as pd
from sqlalchemy import inspect
from database import criar_banco_se_nao_existir, engine

# 📁 Caminhos de pastas
PASTA_PROCESSED = os.path.join("data", "processed")
PASTA_LOGS = "logs"

# Garantir que a pasta de logs existe
os.makedirs(PASTA_LOGS, exist_ok=True)

# 🗺️ Mapeamento: "nome_do_arquivo.xlsx": "nome_da_tabela"
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


def criar_tabelas_iniciais():
    """Etapa 2.1: Garante que as tabelas existem no banco na primeira execução."""
    print("🛠️ [Etapa 2.1] Verificando/Criando estrutura inicial do banco...\n")
    inspector = inspect(engine)

    for arquivo, tabela in ARQUIVOS_TABELAS.items():
        caminho_completo = os.path.join(PASTA_PROCESSED, arquivo)
        if os.path.exists(caminho_completo):
            if not inspector.has_table(tabela):
                # Se a tabela não existir no PostgreSQL, cria a estrutura vazia
                df_amostra = pd.read_excel(caminho_completo, nrows=0)
                df_amostra.to_sql(
                    name=tabela, con=engine, if_exists="append", index=False
                )
                print(f"✨ Tabela '{tabela}' criada com sucesso!")
            else:
                print(f"ℹ️ Tabela '{tabela}' já existe no banco.")


def carregar_dados_incrementais():
    """Etapa 2.2: Identifica apenas dados novos, insere no PostgreSQL e gera logs CSV."""
    print(
        "\n🔄 [Etapa 2.2] Iniciando carga incremental e geração de logs...\n"
    )
    data_hoje = datetime.now().strftime("%Y-%m-%d")

    for arquivo, tabela in ARQUIVOS_TABELAS.items():
        caminho_completo = os.path.join(PASTA_PROCESSED, arquivo)

        if not os.path.exists(caminho_completo):
            print(f"⚠️ Arquivo não encontrado: {caminho_completo}")
            continue

        try:
            # 1. Lê os dados novos do Excel
            df_novo = pd.read_excel(caminho_completo)

            if df_novo.empty:
                print(f"ℹ️ Arquivo '{arquivo}' está vazio.")
                continue

            # Pega dinamicamente o nome da primeira coluna (ID principal)
            col_id = df_novo.columns[0]

            # 2. Busca os IDs já existentes no banco
            query = f'SELECT "{col_id}" FROM {tabela}'
            df_existente = pd.read_sql(query, con=engine)
            ids_existentes = set(df_existente[col_id])

            # 3. Filtra apenas os registros verdadeiramente novos
            df_inserir = df_novo[~df_novo[col_id].isin(ids_existentes)]

            if not df_inserir.empty:
                # 4. Insere apenas os novos dados no banco
                df_inserir.to_sql(
                    name=tabela, con=engine, if_exists="append", index=False
                )

                # 5. Salva o arquivo CSV de log na pasta 'logs'
                nome_log = f"insert_{tabela}_{data_hoje}.csv"
                caminho_log = os.path.join(PASTA_LOGS, nome_log)
                df_inserir.to_csv(caminho_log, index=False)

                print(
                    f"✅ Tabela '{tabela}': {len(df_inserir)} novos registros inseridos! Log salvo em: {caminho_log}"
                )
            else:
                print(
                    f"ℹ️ Tabela '{tabela}': Nenhum registro novo para inserir."
                )

        except Exception as e:
            print(f"❌ Erro ao processar tabela '{tabela}': {e}")

    print("\n🎉 Processo de carga incremental finalizado!")


if __name__ == "__main__":
    criar_banco_se_nao_existir()
    criar_tabelas_iniciais()
    carregar_dados_incrementais()