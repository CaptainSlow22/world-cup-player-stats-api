from pathlib import Path
import sqlite3
import pandas as pd

DB_FILENAME = 'players_stats.db'

def init_db():
    if not Path(DB_FILENAME).is_file():
        Path(DB_FILENAME).touch()

def load_csv_to_db():
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS Stats (nationality text, position text, national_team_jersey_number int, player_DOB text, club text, player_name text, appearances int, goals_scored int, assists_provided int )''')
    stats_data = pd.read_csv('FIFA WC 2022 Players Stats.csv')
    stats_data.drop(['FIFA Ranking ', 'National Team Kit Sponsor', 'Dribbles per 90', 'Interceptions per 90', 'Tackles per 90', 'Total Duels Won per 90', 'Save Percentage', 'Clean Sheets', 'Brand Sponsor/Brand Used'], axis=1, inplace=True)
    stats_data.columns = ['nationality', 'position', 'national_team_jersey_number', 'player_DOB', 'club', 'player_name', 'appearances', 'goals_scored', 'assists_provided' ]
    stats_data.to_sql('Stats', conn, if_exists='append', index=False)

def table_exists(cursor):
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Stats' ''')
    if not cursor.fetchone()[0]:
        return False
    return True

def get_by_nationality(nationality):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    if not table_exists(cursor):
        load_csv_to_db()
    cursor.execute('''SELECT * FROM Stats WHERE nationality = ?''', (nationality,))
    return cursor.fetchall()

def get_by_player_name(player_name):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    if not table_exists(cursor):
        load_csv_to_db()
    cursor.execute('''SELECT * FROM Stats WHERE player_name = ?''', (player_name,))
    return cursor.fetchone()

def get_by_club(club):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    if not table_exists(cursor):
        load_csv_to_db()
    cursor.execute('''SELECT * FROM Stats WHERE club = ?''', (club,))
    return cursor.fetchall()

def add_player_to_db(nationality, position, national_team_jersey_number, player_DOB, club, player_name, appearances, goals_scored, assists_provided):  
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    if not table_exists(cursor):
        load_csv_to_db()
    cursor.execute('''
        INSERT INTO Stats ('nationality', 'position', 'national_team_jersey_number', 'player_DOB',  
                          'club', 'player_name', 'appearances', 
                          'goals_scored', 'assists_provided')
                           VALUES (?,?,?,?,?,?,?,?,?)''', 
                           (nationality, position, national_team_jersey_number, player_DOB, club, player_name, appearances, goals_scored, assists_provided))
    conn.commit()


def update_player(player_name, nationality=None, position=None, national_team_jersey_number=None, player_DOB=None,  
                club=None, appearances=None, 
                goals_scored=None, assists_provided=None):
     conn = sqlite3.connect(DB_FILENAME)
     cursor = conn.cursor()
     if not table_exists(cursor):
        load_csv_to_db()
     params = [nationality, position, national_team_jersey_number, player_DOB, club, appearances,
              goals_scored, assists_provided]
     params_names = ['nationality', 'position', 'national_team_jersey_number', 'player_DOB', 'club',
                    'appearances', 'goals_scored', 'assists_provided']
     for param, param_name in zip(params, params_names):
        if param:
            query = '''
                    UPDATE Stats SET ''' + param_name + '''    
                    = ? WHERE player_name = ?''' 
            cursor.execute(query, (param, player_name))
     conn.commit()

def delete_player(player_name):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    if not table_exists(cursor):
        load_csv_to_db()
    cursor.execute('''DELETE FROM Stats WHERE player_name = ?''',  
                       (player_name,))
    conn.commit()

