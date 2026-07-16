import pandas as pd
import ast

# 1. Carrega os dados brutos da camada Bronze
df = pd.read_csv('data/raw/partidas.csv')

# Função auxiliar para converter string em dicionário/lista com segurança
def parse_json(val):
    if pd.isna(val):
        return {}
    if isinstance(val, str):
        try:
            return ast.literal_eval(val)
        except:
            return {}
    return val

# Converte colunas com dicionários
colunas_complexas = ['area', 'competition', 'season', 'homeTeam', 'awayTeam', 'referees', 'score']
for col in colunas_complexas:
    df[col] = df[col].apply(parse_json)

# --- TRATAMENTO COMPLETO (Todas as 16 colunas da planilha) ---

# IDs Principais
df['id_area'] = df['area'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
df['id_competicao'] = df['competition'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
df['id_temporada'] = df['season'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
df['id_partida'] = df['id']

# Times e Árbitro
df['id_casa'] = df['homeTeam'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
df['id_fora'] = df['awayTeam'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)

def get_arbitro_id(referees_list):
    if isinstance(referees_list, list) and len(referees_list) > 0:
        return referees_list[0].get('id')
    return None

df['id_arbitro'] = df['referees'].apply(get_arbitro_id)

# Detalhes da Partida
df['data_partida'] = df['utcDate']
df['status'] = df['status']
df['rodada'] = df['matchday']

# Placa e Resultados (Vêm de 'score')
df['resultado'] = df['score'].apply(lambda x: x.get('winner') if isinstance(x, dict) else None)

df['placar_casa_intervalo'] = df['score'].apply(
    lambda x: x.get('halfTime', {}).get('home') if isinstance(x, dict) and isinstance(x.get('halfTime'), dict) else None
)
df['placar_casa_final'] = df['score'].apply(
    lambda x: x.get('fullTime', {}).get('home') if isinstance(x, dict) and isinstance(x.get('fullTime'), dict) else None
)

df['placar_fora_intervalo'] = df['score'].apply(
    lambda x: x.get('halfTime', {}).get('away') if isinstance(x, dict) and isinstance(x.get('halfTime'), dict) else None
)
df['placar_fora_final'] = df['score'].apply(
    lambda x: x.get('fullTime', {}).get('away') if isinstance(x, dict) and isinstance(x.get('fullTime'), dict) else None
)

# Seleciona exatamente as colunas na ordem da planilha do Marcos
colunas_finais = [
    'id_area', 'id_competicao', 'id_temporada', 'id_partida',
    'id_casa', 'id_fora', 'id_arbitro', 'data_partida', 'status', 
    'rodada', 'resultado', 'placar_casa_intervalo', 'placar_casa_final',
    'placar_fora_intervalo', 'placar_fora_final'
]

df_final = df[colunas_finais]

# --- SALVAR O EXCEL TRATADO ---
caminho_excel = 'data/processed/tabela_partidas_tratada.xlsx'
df_final.to_excel(caminho_excel, index=False)

print("✅ Processamento concluído com sucesso!")
print(f"📄 Arquivo Excel gerado em: {caminho_excel}")