import sqlite3
from pathlib import Path
from config import config

SCHEMA_FILE = Path(__file__).parent / 'schema.sql'

def run_migrations():
    # Conectar ao banco de dados
    connection = sqlite3.connect(config.get_db_path_file())
    cursor = connection.cursor()

    # Abrir e ler o conteúdo do arquivo .sql
    with SCHEMA_FILE.open('r') as sql_file:
        sql_script = sql_file.read()

    # Executar o script SQL
    cursor.executescript(sql_script)

    # Commit das alterações e fechar a conexão
    connection.commit()
    connection.close()