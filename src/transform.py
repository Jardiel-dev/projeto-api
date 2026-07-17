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

# Converte colunas com dicionários/listas
colunas_complexas = ['area', 'competition', 'season', 'homeTeam', 'awayTeam', 'referees', 'score']
for col in colunas_complexas:
    df[col] = df[col].apply(parse_json)

# --- AJUSTE 4: Filtrar apenas partidas FINALIZADAS ---
df = df[df['status'] == 'FINISHED'].copy()

# --- AJUSTE 2 & FIX: Converter data_partida para datetime e remover fuso horário (compatível com Excel) ---
df['data_partida'] = pd.to_datetime(df['utcDate'], errors='coerce').dt.tz_localize(None)

# IDs Principais
df['id_area'] = df['area'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
df['id_competicao'] = df['competition'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
df['id_temporada'] = df['season'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
df['id_partida'] = df['id']

# Times
df['id_casa'] = df['homeTeam'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
df['id_fora'] = df['awayTeam'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)

# --- AJUSTE 1 & 3: Buscar árbitro dinamicamente por type == 'REFEREE' ---
def get_arbitro_id(referees_list):
    if isinstance(referees_list, list):
        for ref in referees_list:
            if isinstance(ref, dict) and ref.get('type') == 'REFEREE':
                return ref.get('id')
    return None

df['id_arbitro'] = df['referees'].apply(get_arbitro_id)

# Detalhes da Partida
df['rodada'] = df['matchday']

# --- TRADUÇÕES PARA PORTUGUÊS ---

# 1. Status (Como filtramos FINISHED, todos serão FINALIZADO)
mapeamento_status = {
    'FINISHED': 'FINALIZADO'
}
df['status'] = df['status'].map(mapeamento_status).fillna('FINALIZADO')

# 2. Tradução do Resultado
mapeamento_resultado = {
    'HOME_TEAM': 'MANDANTE',
    'AWAY_TEAM': 'VISITANTE',
    'DRAW': 'EMPATE'
}

df['resultado'] = df['score'].apply(lambda x: x.get('winner') if isinstance(x, dict) else None)
df['resultado'] = df['resultado'].map(mapeamento_resultado).fillna(df['resultado'])

# Placares
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

# Seleciona exatamente as colunas na ordem da planilha
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

print("✅ Todos os ajustes do Marcos foram salvos com sucesso!")
print(f"📄 Total de partidas finalizadas processadas: {len(df_final)}")