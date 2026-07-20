import pandas as pd
import ast
import os

def parse_json(val):
    if pd.isna(val):
        return {}
    if isinstance(val, str):
        try:
            return ast.literal_eval(val)
        except:
            return {}
    return val

def get_arbitro_id(referees_list):
    if isinstance(referees_list, list):
        for ref in referees_list:
            if isinstance(ref, dict) and ref.get('type') == 'REFEREE':
                return ref.get('id')
    return None

def executar_transformacao():
    print("\n====== [CAMADA SILVER] INICIANDO TRANSFORMAÇÃO FATO PARTIDAS ======")
    caminho_raw = 'data/raw/partidas.csv'
    
    if not os.path.exists(caminho_raw):
        print(f"❌ Erro: O arquivo {caminho_raw} não existe. Execute a extração primeiro.")
        return

    df = pd.read_csv(caminho_raw)

    colunas_complexas = ['area', 'competition', 'season', 'homeTeam', 'awayTeam', 'referees', 'score']
    for col in colunas_complexas:
        df[col] = df[col].apply(parse_json)

    # Filtrar apenas partidas FINALIZADAS
    df = df[df['status'] == 'FINISHED'].copy()

    # Converter data_partida para datetime sem fuso horário
    df['data_partida'] = pd.to_datetime(df['utcDate'], errors='coerce').dt.tz_localize(None)

    # Mapeamento de IDs
    df['id_partida'] = df['id']
    df['id_area'] = df['area'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
    df['id_competicao'] = df['competition'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
    df['id_temporada'] = df['season'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
    df['id_casa'] = df['homeTeam'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
    df['id_fora'] = df['awayTeam'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
    df['id_arbitro'] = df['referees'].apply(get_arbitro_id)

    df['rodada'] = df['matchday']
    df['status'] = df['status'].map({'FINISHED': 'FINALIZADO'}).fillna('FINALIZADO')

    # Tradução do Resultado
    mapeamento_resultado = {'HOME_TEAM': 'MANDANTE', 'AWAY_TEAM': 'VISITANTE', 'DRAW': 'EMPATE'}
    df['resultado'] = df['score'].apply(lambda x: x.get('winner') if isinstance(x, dict) else None)
    df['resultado'] = df['resultado'].map(mapeamento_resultado).fillna(df['resultado'])

    # Placares
    df['placar_casa_intervalo'] = df['score'].apply(lambda x: x.get('halfTime', {}).get('home') if isinstance(x, dict) and isinstance(x.get('halfTime'), dict) else None)
    df['placar_casa_final'] = df['score'].apply(lambda x: x.get('fullTime', {}).get('home') if isinstance(x, dict) and isinstance(x.get('fullTime'), dict) else None)
    df['placar_fora_intervalo'] = df['score'].apply(lambda x: x.get('halfTime', {}).get('away') if isinstance(x, dict) and isinstance(x.get('halfTime'), dict) else None)
    df['placar_fora_final'] = df['score'].apply(lambda x: x.get('fullTime', {}).get('away') if isinstance(x, dict) and isinstance(x.get('fullTime'), dict) else None)

    # Organização das colunas seguindo o padrão de IDs na frente exigido pelo Marcos
    colunas_finais = [
        'id_partida', 'id_competicao', 'id_temporada', 'id_area', 
        'id_casa', 'id_fora', 'id_arbitro', 'data_partida', 'status', 
        'rodada', 'resultado', 'placar_casa_intervalo', 'placar_casa_final',
        'placar_fora_intervalo', 'placar_fora_final'
    ]

    df_final = df[colunas_finais]

    os.makedirs('data/processed', exist_ok=True)
    caminho_excel = 'data/processed/tabela_partidas_tratada.xlsx'
    df_final.to_excel(caminho_excel, index=False)

    print("✅ Tabela Fato (partidas) normalizada e salva com sucesso!")
    print(f"📄 Total de partidas processadas: {len(df_final)}")

if __name__ == '__main__':
    executar_transformacao()