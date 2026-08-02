import os
from datetime import datetime
import pandas as pd
from sqlalchemy import text
from database import criar_banco_se_nao_existir, engine

# 📁 Caminhos
PASTA_PROCESSED = os.path.join("data", "processed")
PASTA_LOGS = "logs"
CAMINHO_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")

os.makedirs(PASTA_LOGS, exist_ok=True)

ARQUIVOS_TABELAS = {
    "competicoes.xlsx": ("competicoes", "id_competicao"),
    "temporadas.xlsx": ("temporadas", "id_temporada"),
    "times.xlsx": ("times", "id_time"),
    "tecnicos.xlsx": ("tecnicos", "id_tecnico"),
    "arbitros.xlsx": ("arbitros", "id_arbitro"),
    "jogadores.xlsx": ("jogadores", "id_jogador"),
    "tabela_partidas_tratada.xlsx": ("tabela_partidas_tratada", "id_partida"),
    "artilheiros.xlsx": ("artilheiros", "id_jogador"),
}

def executar_script_sql():
    """Etapa DDL: Executa o DDL bruto com tipos, PKs e FKs explícitas."""
    print("🛠️ [Banco] Aplicando DDL com tipos e chaves explícitas (schema.sql)...")
    try:
        with open(CAMINHO_SCHEMA, "r", encoding="utf-8") as file:
            sql_script = file.read()
        
        with engine.begin() as conn:  # .begin() garante commit/rollback isolado
            conn.execute(text(sql_script))
        print("✅ Estrutura de tabelas e relacionamentos verificada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao executar DDL (schema.sql): {e}")

def carregar_dados_incrementais():
    """Etapa DML: Identifica novos registros via PK e insere sem duplicatas."""
    print("\n🔄 [Banco] Iniciando carga incremental...")
    data_hoje = datetime.now().strftime("%Y-%m-%d")

    for arquivo, (tabela, col_id) in ARQUIVOS_TABELAS.items():
        caminho_completo = os.path.join(PASTA_PROCESSED, arquivo)

        if not os.path.exists(caminho_completo):
            print(f"⚠️ Arquivo não encontrado: {caminho_completo}")
            continue

        try:
            df_novo = pd.read_excel(caminho_completo)

            if df_novo.empty or col_id not in df_novo.columns:
                print(f"ℹ️ Tabela '{tabela}': Arquivo vazio ou coluna '{col_id}' ausente.")
                continue

            # Tratamento especial de datas para evitar conflito com o PostgreSQL
            for col in df_novo.columns:
                if "data" in col or "date" in col:
                    df_novo[col] = pd.to_datetime(df_novo[col], errors="coerce")

            # Garante tipo numérico/consistente para comparação de IDs
            df_novo[col_id] = df_novo[col_id].astype(int)

            # Busca IDs já existentes abrindo uma conexão limpa por tabela
            with engine.connect() as conn:
                query = text(f'SELECT "{col_id}" FROM {tabela};')
                df_existente = pd.read_sql(query, con=conn)

            if not df_existente.empty:
                ids_existentes = set(df_existente[col_id].astype(int))
                df_inserir = df_novo[~df_novo[col_id].isin(ids_existentes)]
            else:
                df_inserir = df_novo

            # Carga apenas do delta (dados novos)
            if not df_inserir.empty:
                # Inserção isolada dentro de transação individual
                with engine.begin() as conn_insert:
                    df_inserir.to_sql(
                        name=tabela, con=conn_insert, if_exists="append", index=False
                    )

                nome_log = f"insert_{tabela}_{data_hoje}.csv"
                caminho_log = os.path.join(PASTA_LOGS, nome_log)
                df_inserir.to_csv(caminho_log, index=False)

                print(
                    f"✅ Tabela '{tabela}': {len(df_inserir)} novos registros inseridos! Log: {caminho_log}"
                )
            else:
                print(f"ℹ️ Tabela '{tabela}': 0 registros novos. Nenhuma duplicata gerada.")

        except Exception as e:
            print(f"❌ Erro ao processar tabela '{tabela}': {e}")

def executar_carga_completa_banco():
    """Função orquestradora oficial para ser chamada na main.py"""
    criar_banco_se_nao_existir()
    executar_script_sql()
    carregar_dados_incrementais()

if __name__ == "__main__":
    executar_carga_completa_banco()