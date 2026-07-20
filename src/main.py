import sys
import os

# Alinha os caminhos para evitar erros de importação de módulos locais
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Importa as rotinas de execução de cada script do pipeline
from extract import executar_extracao
from transform import executar_transformacao
import generate_dimensions

def main():
    print("=======================================================")
    print("🚀 INICIANDO PIPELINE UNIFICADO DE DADOS DE FUTEBOL ⚽")
    print("=======================================================")
    
    # Passo 1: Ingestão de Dados Brutos (API -> CSVs na Camada Bronze)
    executar_extracao()
    
    # Passo 2: Construção da Tabela Fato (Fato Partidas na Camada Silver)
    executar_transformacao()
    
    # Passo 3: Geração de todas as Dimensões Normalizadas (Camada Silver)
    print("\n====== [CAMADA SILVER] INICIANDO GERAÇÃO DAS DIMENSÕES ======")
    generate_dimensions.generate_temporadas()
    generate_dimensions.generate_competicoes()
    generate_dimensions.generate_times_tecnicos_jogadores()
    generate_dimensions.generate_artilheiros()
    generate_dimensions.generate_arbitros()
    
    print("\n=======================================================")
    print("🎉 [SUCESSO] Todo o ecossistema de dados está atualizado!  ")
    print("=======================================================")

if __name__ == '__main__':
    main()