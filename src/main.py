import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from extract import executar_extracao
from transform import executar_transformacao_completa
from carregar_dados import executar_carga_completa_banco

def main():
    print("=======================================================")
    print("🚀 INICIANDO PIPELINE UNIFICADO DE DADOS DE FUTEBOL ⚽")
    print("=======================================================")
    
    # Passo 1: Ingestão (API -> Bronze)
    executar_extracao()
    
    # Passo 2: Transformação (Silver)
    executar_transformacao_completa()
    
    # Passo 3: Carga e DDL no Banco (Gold/PostgreSQL)
    executar_carga_completa_banco()
    
    print("\n=======================================================")
    print("🎉 [SUCESSO] Todo o ecossistema de dados está atualizado!")
    print("=======================================================")

if __name__ == '__main__':
    main()