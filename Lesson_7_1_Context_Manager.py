import sqlite3


class ContextManagerForDBConnect:
    """Контекстний менеджер для відкриття та закриття бази даних SQL"""
    def __init__(self, name_db):
        self._name_db = name_db

    def __enter__(self):
        self._connect = sqlite3.connect(self._name_db)
        return self._connect

    def __exit__(self, *args):
        self._connect.close()


connection_db = 'db_personal'

with ContextManagerForDBConnect(connection_db) as connect:
    cursor = connect.cursor()