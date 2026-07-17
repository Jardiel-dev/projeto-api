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


def generate_temporadas():
    print("⏳ Processando: temporadas.xlsx...")
    df = pd.read_csv(os.path.join(RAW_DIR, 'temporadas.csv'))
    
    # Tratando o vencedor (winner)
    df['winner_obj'] = df['winner'].apply(safe_eval)
    df['id_vencedor'] = df['winner_obj'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
    df['nome_vencedor'] = df['winner_obj'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
    
    # Seleção e renomeação
    df_final = df.rename(columns={
        'id': 'id_temporada',
        'startDate': 'data_inicio',
        'endDate': 'data_fim',
        'currentMatchday': 'rodada_atual'
    })[['id_temporada', 'data_inicio', 'data_fim', 'rodada_atual', 'id_vencedor', 'nome_vencedor']]
    
    df_final.to_excel(os.path.join(PROCESSED_DIR, 'temporadas.xlsx'), index=False)
    print("✅ temporadas.xlsx gerado com sucesso!")


def generate_competicoes():
    print("⏳ Processando: competicoes.xlsx...")
    df = pd.read_csv(os.path.join(RAW_DIR, 'competicoes.csv'))
    
    df['area_obj'] = df['area'].apply(safe_eval)
    df['nome_pais'] = df['area_obj'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
    
    df_final = df.rename(columns={
        'id': 'id_competicao',
        'name': 'nome_competicao',
        'code': 'codigo',
        'type': 'tipo',
        'emblem': 'escudo_url'
    })[['id_competicao', 'nome_competicao', 'codigo', 'tipo', 'nome_pais', 'escudo_url']]
    
    df_final.to_excel(os.path.join(PROCESSED_DIR, 'competicoes.xlsx'), index=False)
    print("✅ competicoes.xlsx gerado com sucesso!")


def generate_times_tecnicos_jogadores():
    print("⏳ Processando: times.xlsx, tecnicos.xlsx e jogadores.xlsx...")
    df = pd.read_csv(os.path.join(RAW_DIR, 'times.csv'))
    
    # 1. Tabela Times
    df['area_obj'] = df['area'].apply(safe_eval)
    df['pais'] = df['area_obj'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
    
    df_times = df.rename(columns={
        'id': 'id_time',
        'name': 'nome_time',
        'shortName': 'nome_curto',
        'tla': 'sigla',
        'crest': 'escudo_url',
        'founded': 'ano_fundacao',
        'venue': 'estadio'
    })[['id_time', 'nome_time', 'nome_curto', 'sigla', 'pais', 'ano_fundacao', 'estadio', 'escudo_url']]
    
    df_times.to_excel(os.path.join(PROCESSED_DIR, 'times.xlsx'), index=False)
    print("✅ times.xlsx gerado com sucesso!")
    
    # 2. Tabela Técnicos (Coluna coach)
    tecnicos_list = []
    for _, row in df.iterrows():
        coach = safe_eval(row['coach'])
        if isinstance(coach, dict) and coach.get('id'):
            tecnicos_list.append({
                'id_tecnico': coach.get('id'),
                'nome_tecnico': coach.get('name'),
                'data_nascimento': coach.get('dateOfBirth'),
                'nacionalidade': coach.get('nationality'),
                'id_time': row['id'],
                'nome_time': row['name']
            })
            
    df_tecnicos = pd.DataFrame(tecnicos_list)
    df_tecnicos.to_excel(os.path.join(PROCESSED_DIR, 'tecnicos.xlsx'), index=False)
    print("✅ tecnicos.xlsx gerado com sucesso!")
    
    # 3. Tabela Jogadores (Coluna squad)
    jogadores_list = []
    for _, row in df.iterrows():
        squad = safe_eval(row['squad'])
        if isinstance(squad, list):
            for player in squad:
                if isinstance(player, dict) and player.get('id'):
                    jogadores_list.append({
                        'id_jogador': player.get('id'),
                        'nome_jogador': player.get('name'),
                        'posicao': player.get('position'),
                        'data_nascimento': player.get('dateOfBirth'),
                        'nacionalidade': player.get('nationality'),
                        'id_time': row['id'],
                        'nome_time': row['name']
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
            'nome_jogador': player.get('name') if isinstance(player, dict) else None,
            'posicao': player.get('position') if isinstance(player, dict) else None,
            'nacionalidade': player.get('nationality') if isinstance(player, dict) else None,
            'id_time': team.get('id') if isinstance(team, dict) else None,
            'nome_time': team.get('name') if isinstance(team, dict) else None,
            'partidas_jogadas': row['playedMatches'],
            'gols': row['goals'],
            'assistencias': row['assists'],
            'penaltis': row['penalties']
        })
        
    df_artilheiros = pd.DataFrame(artilheiros_list)
    df_artilheiros.to_excel(os.path.join(PROCESSED_DIR, 'artilheiros.xlsx'), index=False)
    print("✅ artilheiros.xlsx gerado com sucesso!")


if __name__ == '__main__':
    print("🚀 Iniciando geração das tabelas relacionais em Excel...\n")
    generate_temporadas()
    generate_competicoes()
    generate_times_tecnicos_jogadores()
    generate_artilheiros()
    print("\n🎉 Todas as 6 tabelas foram geradas com sucesso na pasta 'data/processed/'!")