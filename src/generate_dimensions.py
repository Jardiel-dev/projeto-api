import os
import ast
import pandas as pd

# Caminhos das pastas
RAW_DIR = os.path.join('data', 'raw')
PROCESSED_DIR = os.path.join('data', 'processed')
os.makedirs(PROCESSED_DIR, exist_ok=True)

def safe_eval(val):
    """Auxiliar para converter strings que parecem dicionários/listas em objetos Python."""
    if pd.isna(val) or val is None:
        return None
    if isinstance(val, (dict, list)):
        return val
    try:
        return ast.literal_eval(str(val))
    except (ValueError, SyntaxError):
        return None

def format_date_br(val):
    """Converte strings de data (ex: 2020-05-15...) para o formato brasileiro DD/MM/AAAA."""
    if pd.isna(val) or val is None:
        return None
    try:
        return pd.to_datetime(val).strftime('%d/%m/%Y')
    except Exception:
        return val

def translate_position(pos):
    """Mapeia as posições dos jogadores de inglês para português."""
    mapping = {
        'Goalkeeper': 'Goleiro',
        'Defence': 'Defensor',
        'Midfield': 'Meio-campista',
        'Offence': 'Atacante'
    }
    return mapping.get(pos, pos)


def generate_temporadas():
    print("⏳ Processando: temporadas.xlsx...")
    df_temp = pd.read_csv(os.path.join(RAW_DIR, 'temporadas.csv'))
    
    # Tratando o vencedor para pegar apenas o ID
    df_temp['winner_obj'] = df_temp['winner'].apply(safe_eval)
    df_temp['id_vencedor'] = df_temp['winner_obj'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
    
    # Buscando o id_competicao a partir do arquivo competicoes.csv
    try:
        df_comp = pd.read_csv(os.path.join(RAW_DIR, 'competicoes.csv'))
        id_competicao = df_comp['id'].iloc[0] if not df_comp.empty else None
    except Exception:
        id_competicao = None
        
    df_temp['id_competicao'] = id_competicao
    
    # Formatando as datas
    df_temp['data_inicio'] = df_temp['startDate'].apply(format_date_br)
    df_temp['data_fim'] = df_temp['endDate'].apply(format_date_br)
    
    # Renomeando
    df_temp = df_temp.rename(columns={
        'id': 'id_temporada',
        'currentMatchday': 'rodada_atual'
    })
    
    # IDs posicionados na frente
    colunas_ordenadas = ['id_temporada', 'id_competicao', 'id_vencedor', 'data_inicio', 'data_fim', 'rodada_atual']
    df_final = df_temp[colunas_ordenadas]
    
    df_final.to_excel(os.path.join(PROCESSED_DIR, 'temporadas.xlsx'), index=False)
    print("✅ temporadas.xlsx gerado com sucesso!")


def generate_competicoes():
    print("⏳ Processando: competicoes.xlsx...")
    df = pd.read_csv(os.path.join(RAW_DIR, 'competicoes.csv'))
    
    df['area_obj'] = df['area'].apply(safe_eval)
    df['id_area'] = df['area_obj'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
    
    df = df.rename(columns={
        'id': 'id_competicao',
        'name': 'nome_competicao',
        'code': 'codigo',
        'type': 'tipo',
        'emblem': 'escudo_url'
    })
    
    # IDs posicionados na frente
    colunas_ordenadas = ['id_competicao', 'id_area', 'nome_competicao', 'codigo', 'tipo', 'escudo_url']
    df_final = df[colunas_ordenadas]
    
    df_final.to_excel(os.path.join(PROCESSED_DIR, 'competicoes.xlsx'), index=False)
    print("✅ competicoes.xlsx gerado com sucesso!")


def generate_times_tecnicos_jogadores():
    print("⏳ Processando: times.xlsx, tecnicos.xlsx e jogadores.xlsx...")
    df = pd.read_csv(os.path.join(RAW_DIR, 'times.csv'))
    
    # 1. Tabela Times
    df['area_obj'] = df['area'].apply(safe_eval)
    df['pais'] = df['area_obj'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
    
    df_times_renamed = df.rename(columns={
        'id': 'id_time',
        'name': 'nome_time',
        'shortName': 'nome_curto',
        'tla': 'sigla',
        'crest': 'escudo_url',
        'founded': 'ano_fundacao',
        'venue': 'estadio'
    })
    
    colunas_times = ['id_time', 'nome_time', 'nome_curto', 'sigla', 'pais', 'ano_fundacao', 'estadio', 'escudo_url']
    df_times = df_times_renamed[colunas_times]
    df_times.to_excel(os.path.join(PROCESSED_DIR, 'times.xlsx'), index=False)
    print("✅ times.xlsx gerado com sucesso!")
    
    # 2. Tabela Técnicos
    tecnicos_list = []
    for _, row in df.iterrows():
        coach = safe_eval(row['coach'])
        if isinstance(coach, dict) and coach.get('id'):
            tecnicos_list.append({
                'id_tecnico': coach.get('id'),
                'id_time': row['id'],
                'nome_tecnico': coach.get('name'),
                'data_nascimento': format_date_br(coach.get('dateOfBirth')),
                'nacionalidade': coach.get('nationality')
            })
            
    df_tecnicos = pd.DataFrame(tecnicos_list)
    df_tecnicos.to_excel(os.path.join(PROCESSED_DIR, 'tecnicos.xlsx'), index=False)
    print("✅ tecnicos.xlsx gerado com sucesso!")
    
    # 3. Tabela Jogadores
    jogadores_list = []
    for _, row in df.iterrows():
        squad = safe_eval(row['squad'])
        if isinstance(squad, list):
            for player in squad:
                if isinstance(player, dict) and player.get('id'):
                    jogadores_list.append({
                        'id_jogador': player.get('id'),
                        'id_time': row['id'],
                        'nome_jogador': player.get('name'),
                        'posicao': translate_position(player.get('position')),
                        'data_nascimento': format_date_br(player.get('dateOfBirth')),
                        'nacionalidade': player.get('nationality')
                    })
                    
    df_jogadores = pd.DataFrame(jogadores_list)
    df_jogadores.to_excel(os.path.join(PROCESSED_DIR, 'jogadores.xlsx'), index=False)
    print("✅ jogadores.xlsx gerado com sucesso!")


def generate_artilheiros():
    print("⏳ Processando: artilheiros.xlsx...")
    df = pd.read_csv(os.path.join(RAW_DIR, 'artilheiros.csv'))
    
    artilheiros_list = []
    for _, row in df.iterrows():
        player = safe_eval(row['player'])
        team = safe_eval(row['team'])
        
        artilheiros_list.append({
            'id_jogador': player.get('id') if isinstance(player, dict) else None,
            'id_time': team.get('id') if isinstance(team, dict) else None,
            'partidas_jogadas': row['playedMatches'],
            'gols': row['goals'],
            'assistencias': row['assists'],
            'penaltis': row['penalties']
        })
        
    df_artilheiros = pd.DataFrame(artilheiros_list)
    df_artilheiros.to_excel(os.path.join(PROCESSED_DIR, 'artilheiros.xlsx'), index=False)
    print("✅ artilheiros.xlsx gerado com sucesso!")


def generate_arbitros():
    print("⏳ Processando: arbitros.xlsx...")
    df = pd.read_csv(os.path.join(RAW_DIR, 'partidas.csv'))
    
    arbitros_list = []
    for _, row in df.iterrows():
        referees = safe_eval(row['referees'])
        if isinstance(referees, list):
            for ref in referees:
                if isinstance(ref, dict) and ref.get('id'):
                    tipo = ref.get('type')
                    if tipo == 'REFEREE':
                        tipo = 'Árbitro'
                        
                    arbitros_list.append({
                        'id_arbitro': ref.get('id'),
                        'nome_arbitro': ref.get('name'),
                        'tipo_arbitro': tipo,
                        'nacionalidade': ref.get('nationality')
                    })
                    
    df_arbitros = pd.DataFrame(arbitros_list)
    
    if not df_arbitros.empty:
        df_arbitros = df_arbitros.drop_duplicates(subset=['id_arbitro'])
    
    df_arbitros.to_excel(os.path.join(PROCESSED_DIR, 'arbitros.xlsx'), index=False)
    print("✅ arbitros.xlsx gerado com sucesso!")


if __name__ == '__main__':
    print("🚀 Geração das dimensões em execução independente...\n")
    generate_temporadas()
    generate_competicoes()
    generate_times_tecnicos_jogadores()
    generate_artilheiros()
    generate_arbitros()