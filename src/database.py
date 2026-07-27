import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

USUARIO = os.getenv("POSTGRES_USER", "postgres")
SENHA = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORTA = os.getenv("POSTGRES_PORT", "5432")
BANCO = os.getenv("POSTGRES_DB", "futebol_db")

# Utiliza o driver pg8000 que lida nativamente com encodings no Windows
URL_SERVIDO_GERAL = (
    f"postgresql+pg8000://{USUARIO}:{SENHA}@{HOST}:{PORTA}/postgres"
)
DATABASE_URL = f"postgresql+pg8000://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"


def criar_banco_se_nao_existir():
    """PASSO 1: Conecta no servidor PostgreSQL geral e garante que o banco 'futebol_db' existe."""
    try:
        engine_geral = create_engine(
            URL_SERVIDO_GERAL, isolation_level="AUTOCOMMIT"
        )
        with engine_geral.connect() as conn:
            resultado = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname='{BANCO}';")
            )
            if not resultado.scalar():
                conn.execute(text(f"CREATE DATABASE {BANCO};"))
                print(f"✨ Banco de dados '{BANCO}' criado com sucesso!")
            else:
                print(f"ℹ️ Banco de dados '{BANCO}' já existe.")
    except Exception as e:
        print(f"⚠️ Erro ao verificar/criar banco de dados: {e}")


# PASSO 2: Cria a Engine oficial do projeto
engine = create_engine(DATABASE_URL)


def testar_conexao():
    """Testa a conexão oficial com o banco 'futebol_db'."""
    try:
        with engine.connect() as conexao:
            print(
                f"⚡ Conexão com o banco '{BANCO}' no PostgreSQL realizada com sucesso!"
            )
    except Exception as e:
        print(f"❌ Erro ao conectar no banco de dados: {e}")


if __name__ == "__main__":
    criar_banco_se_nao_existir()
    testar_conexao()