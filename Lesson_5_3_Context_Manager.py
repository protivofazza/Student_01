import sqlite3


class ContextManagerForDBConnect:
    """Контекстний менеджер для відкриття та закриття бази даних SQL"""
    def __init__(self, name_db):
        self.name_db = name_db

    def __enter__(self):
        self.tmp = sqlite3.connect(self.name_db)
        return self.tmp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tmp.close()


connection_db = 'db_personal'

with ContextManagerForDBConnect(connection_db) as tmp:
    cursor = tmp.cursor()
