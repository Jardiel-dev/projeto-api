from sqlalchemy import create_engine

# 🔑 Configurações do Banco de Dados
USUARIO = "postgres"
SENHA = "749131"  
HOST = "localhost"
PORTA = "5432"
BANCO = "futebol_db"

# 🛠️ String de Conexão
DATABASE_URL = f"postgresql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"

# 🚀 Engine do SQLAlchemy
engine = create_engine(DATABASE_URL)


def testar_conexao():
    try:
        with engine.connect() as conexao:
            print("⚡ Conexão com o PostgreSQL realizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao conectar no banco de dados: {e}")


if __name__ == "__main__":
    testar_conexao()