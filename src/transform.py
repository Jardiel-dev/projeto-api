import pandas as pd
import ast
import os

# --- FUNÇÕES AUXILIARES DE LIMPEZA ---
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

# --- DICIONÁRIO COMPLETO DE TRADUÇÃO DE POSIÇÕES ---
MAPA_POSICOES = {
    'Goalkeeper': 'Goleiro',
    'Defence': 'Defensor',
    'Defender': 'Defensor',
    'Left-Back': 'Lateral Esquerdo',
    'Right-Back': 'Lateral Direito',
    'Centre-Back': 'Zagueiro',
    'Midfield': 'Meio-campista',
    'Midfielder': 'Meio-campista',
    'Defensive Midfield': 'Volante',
    'Central Midfield': 'Meio-campista Central',
    'Attacking Midfield': 'Meio-campista Ofensivo',
    'Left Midfield': 'Meia Esquerda',
    'Right Midfield': 'Meia Direita',
    'Offence': 'Atacante',
    'Forward': 'Atacante',
    'Centre-Forward': 'Centroavante',
    'Left Winger': 'Ponta Esquerdo',
    'Right Winger': 'Ponta Direito',
    'Winger': 'Ponta'
}

def executar_transformacao_completa():
    print("\n====== [CAMADA SILVER] INICIANDO TRANSFORMAÇÃO E PROCESSAMENTO ======")
    os.makedirs('data/processed', exist_ok=True)
    
    # ==========================================
    # 1. PROCESSAMENTO DA TABELA FATO (PARTIDAS)
    # ==========================================
    print("⏳ Processando Tabela Fato: partidas.xlsx...")
    df_partidas = pd.read_csv('data/raw/partidas.csv')
    
    colunas_complexas = ['area', 'competition', 'season', 'homeTeam', 'awayTeam', 'referees', 'score']
    for col in colunas_complexas:
        df_partidas[col] = df_partidas[col].apply(parse_json)
        
    df_partidas = df_partidas[df_partidas['status'] == 'FINISHED'].copy()
    
    # CONVERSÃO PARA DATETIME REAL (Sem fuso horário para compatibilidade do Excel)
    df_partidas['data_partida'] = pd.to_datetime(df_partidas['utcDate'], errors='coerce').dt.tz_localize(None)
    
    df_partidas['id_partida'] = df_partidas['id']
    df_partidas['id_competicao'] = df_partidas['competition'].apply(lambda x: x.get('id'))
    df_partidas['id_temporada'] = df_partidas['season'].apply(lambda x: x.get('id'))
    df_partidas['id_area'] = df_partidas['area'].apply(lambda x: x.get('id'))
    df_partidas['id_casa'] = df_partidas['homeTeam'].apply(lambda x: x.get('id'))
    df_partidas['id_fora'] = df_partidas['awayTeam'].apply(lambda x: x.get('id'))
    df_partidas['id_arbitro'] = df_partidas['referees'].apply(get_arbitro_id)
    df_partidas['rodada'] = df_partidas['matchday']
    df_partidas['status'] = 'FINALIZADO'
    
    mapeamento_resultado = {'HOME_TEAM': 'MANDANTE', 'AWAY_TEAM': 'VISITANTE', 'DRAW': 'EMPATE'}
    df_partidas['resultado'] = df_partidas['score'].apply(lambda x: x.get('winner')).map(mapeamento_resultado)
    
    df_partidas['placar_casa_intervalo'] = df_partidas['score'].apply(lambda x: x.get('halfTime', {}).get('home'))
    df_partidas['placar_casa_final'] = df_partidas['score'].apply(lambda x: x.get('fullTime', {}).get('home'))
    df_partidas['placar_fora_intervalo'] = df_partidas['score'].apply(lambda x: x.get('halfTime', {}).get('away'))
    df_partidas['placar_fora_final'] = df_partidas['score'].apply(lambda x: x.get('fullTime', {}).get('away'))
    
    colunas_fato = [
        'id_partida', 'id_competicao', 'id_temporada', 'id_area', 'id_casa', 'id_fora', 
        'id_arbitro', 'data_partida', 'status', 'rodada', 'resultado', 
        'placar_casa_intervalo', 'placar_casa_final', 'placar_fora_intervalo', 'placar_fora_final'
    ]
    df_partidas[colunas_fato].to_excel('data/processed/tabela_partidas_tratada.xlsx', index=False)
    print(f"✅ Tabela Fato salva! ({len(df_partidas)} partidas)")

    # ==========================================
    # 2. DIMENSÃO TEMPORADAS
    # ==========================================
    print("⏳ Processando Dimensão: temporadas.xlsx...")
    df_temp = pd.DataFrame([df_partidas['season'].iloc[0]]) if not df_partidas.empty else pd.DataFrame()
    if not df_temp.empty:
        df_dim_temp = pd.DataFrame({
            'id_temporada': df_temp['id'],
            'id_competicao': df_partidas['id_competicao'].iloc[0],
            'ano_inicio': pd.to_datetime(df_temp['startDate']).dt.year,
            'ano_fim': pd.to_datetime(df_temp['endDate']).dt.year,
            'data_inicio_completa': pd.to_datetime(df_temp['startDate']), # Datetime real
            'data_fim_completa': pd.to_datetime(df_temp['endDate'])       # Datetime real
        })
        df_dim_temp.to_excel('data/processed/temporadas.xlsx', index=False)
        print("✅ Dimensão temporadas gerada!")

    # ==========================================
    # 3. DIMENSÃO COMPETIÇÕES
    # ==========================================
    print("⏳ Processando Dimensão: competicoes.xlsx...")
    df_comp = pd.DataFrame([df_partidas['competition'].iloc[0]]) if not df_partidas.empty else pd.DataFrame()
    if not df_comp.empty:
        df_dim_comp = pd.DataFrame({
            'id_competicao': df_comp['id'],
            'id_area': df_partidas['id_area'].iloc[0],
            'nome_competicao': df_comp['name'],
            'codigo_competicao': df_comp['code'],
            'tipo': df_comp['type']
        })
        df_dim_comp.to_excel('data/processed/competicoes.xlsx', index=False)
        print("✅ Dimensão competicoes gerada!")

    # ==========================================
    # 4. DIMENSÕES: TIMES, TÉCNICOS E JOGADORES
    # ==========================================
    print("⏳ Processando Dimensões: times, tecnicos e jogadores...")
    df_raw_times = pd.read_csv('data/raw/times.csv')
    
    lista_times, lista_tecnicos, lista_jogadores = [], [], []
    
    for _, row in df_raw_times.iterrows():
        id_time = row['id']
        lista_times.append({
            'id_time': id_time,
            'nome_time': row['name'],
            'sigla': row['tla'],
            'fundacao': row['founded'],
            'estadio': row['venue']
        })
        
        # Técnico
        coach = parse_json(row['coach'])
        if coach and coach.get('id'):
            lista_tecnicos.append({
                'id_tecnico': coach.get('id'),
                'id_time': id_time,
                'nome_tecnico': coach.get('name'),
                'nacionalidade': coach.get('nationality'),
                'data_nascimento': pd.to_datetime(coach.get('dateOfBirth'), errors='coerce') # Datetime real
            })
            
        # Jogadores
        squad = parse_json(row['squad'])
        if isinstance(squad, list):
            for jogador in squad:
                if isinstance(jogador, dict) and jogador.get('id'):
                    # Mapeia e traduz dinamicamente a posição
                    posicao_original = jogador.get('position', '')
                    posicao_traduzida = MAPA_POSICOES.get(posicao_original, posicao_original if posicao_original else 'Não Informado')
                    
                    lista_jogadores.append({
                        'id_jogador': jogador.get('id'),
                        'id_time': id_time,
                        'nome_jogador': jogador.get('name'),
                        'posicao': posicao_traduzida,
                        'nacionalidade': jogador.get('nationality'),
                        'data_nascimento': pd.to_datetime(jogador.get('dateOfBirth'), errors='coerce') # Datetime real
                    })

    pd.DataFrame(lista_times).to_excel('data/processed/times.xlsx', index=False)
    pd.DataFrame(lista_tecnicos).drop_duplicates(subset=['id_tecnico']).to_excel('data/processed/tecnicos.xlsx', index=False)
    pd.DataFrame(lista_jogadores).drop_duplicates(subset=['id_jogador']).to_excel('data/processed/jogadores.xlsx', index=False)
    print("✅ Dimensões de times, tecnicos e jogadores geradas!")

    # ==========================================
    # 5. DIMENSÃO ARTILHEIROS
    # ==========================================
    print("⏳ Processando Dimensão: artilheiros.xlsx...")
    df_raw_artilheiros = pd.read_csv('data/raw/artilheiros.csv')
    lista_artilheiros = []
    
    for _, row in df_raw_artilheiros.iterrows():
        player_info = parse_json(row['player'])
        team_info = parse_json(row['team'])
        
        if player_info.get('id'):
            lista_artilheiros.append({
                'id_jogador': player_info.get('id'),
                'id_time': team_info.get('id'),
                'gols': row.get('goals', 0),
                'assistencias': row.get('assists', 0),
                'penaltis': row.get('penalties', 0)
            })
    pd.DataFrame(lista_artilheiros).to_excel('data/processed/artilheiros.xlsx', index=False)
    print("✅ Dimensão artilheiros gerada!")

    # ==========================================
    # 6. DIMENSÃO ÁRBITROS
    # ==========================================
    print("⏳ Processando Dimensão: arbitros.xlsx...")
    lista_arbitros = []
    for _, row in df_partidas.iterrows():
        referees = row['referees']
        if isinstance(referees, list):
            for ref in referees:
                if isinstance(ref, dict) and ref.get('type') == 'REFEREE':
                    lista_arbitros.append({
                        'id_arbitro': ref.get('id'),
                        'nome_arbitro': ref.get('name'),
                        'nacionalidade': ref.get('nationality'),
                        'tipo': 'Árbitro'
                    })
    if lista_arbitros:
        pd.DataFrame(lista_arbitros).drop_duplicates(subset=['id_arbitro']).to_excel('data/processed/arbitros.xlsx', index=False)
    print("✅ Dimensão arbitros gerada!")