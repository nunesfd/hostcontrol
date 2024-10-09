# repository.py
import os
import sqlite3

from config import config

class Repository:
    def __init__(self):
        self.db_path = config.get_db_path_file()

    def _connect(self):
        # Método comum para conectar ao banco de dados
        return sqlite3.connect(self.db_path)

    def _execute(self, query, params=(), fetch=False, lastId=False):
        # Método comum para executar queries no banco de dados
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            connection.commit()

            if lastId:
                return cursor.lastrowid