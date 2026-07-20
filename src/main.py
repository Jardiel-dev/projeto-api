import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from extract import executar_extracao
from transform import executar_transformacao_completa

def main():
    print("=======================================================")
    print("🚀 INICIANDO PIPELINE UNIFICADO DE DADOS DE FUTEBOL ⚽")
    print("=======================================================")
    
    # Passo 1: Ingestão de Dados Brutos (API -> CSVs na Camada Bronze)
    executar_extracao()
    
    # Passo 2: Transformação da Fato e Geração de Dimensões Normalizadas (Camada Silver)
    executar_transformacao_completa()
    
    print("\n=======================================================")
    print("🎉 [SUCESSO] Todo o ecossistema de dados está atualizado!  ")
    print("=======================================================")

if __name__ == '__main__':
    main()