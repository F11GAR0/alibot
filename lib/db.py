import time
import sqlite3
import hashlib

import logging
logging.basicConfig(level=logging.DEBUG)

class DataBase:

    def __init__(self, db, uri=False):
        
        logging.debug("Initialize database.")

        try:
            self.connection = sqlite3.connect(db, uri=uri)
            self._init_cursor()
            self._init_table_if_not_exists()

            logging.debug(self.cursor.fetchall())
        except Exception as e:
            logging.debug(f"DB: {e.__str__()}")

    def _init_cursor(self):

        self.cursor = self.connection.cursor()

    def _execute_with_commit(self, __sql : str, __parameters = ()):

        self.cursor.execute(__sql, __parameters)
        self.connection.commit()

    def _init_table_if_not_exists(self):

        self._execute_with_commit('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
telegram_id INTEGER NOT NULL
)
''')
        self._execute_with_commit('''
CREATE TABLE IF NOT EXISTS Builds (
id INTEGER PRIMARY KEY,
telegram_id INTEGER NOT NULL,
json_info TEXT NOT NULL,
hash TEXT NOT NULL
)
''')
        self._execute_with_commit('''
CREATE TABLE IF NOT EXISTS BuildsPriceHistory (
id INTEGER PRIMARY KEY,
build_id INTEGER NOT NULL,
price TEXT NOT NULL,
timestamp TIMESTAMP NOT NULL
)
''')
    
    def user_exists(self, telegram_id : int):

        self._execute_with_commit('SELECT * FROM Users WHERE telegram_id = ?', (telegram_id,) )
        total_users = len(self.cursor.fetchall())

        return total_users > 0

    def register_user(self, telegram_id : int):

        self._execute_with_commit('INSERT INTO Users (telegram_id) VALUES (?)', (telegram_id,) )

    def build_exists(self, json_data : str):

        js_hash = hashlib.md5(json_data.encode()).hexdigest()

        self._execute_with_commit('SELECT * FROM Builds WHERE hash = ?', (js_hash,) )
        total_builds = len(self.cursor.fetchall())

        return total_builds > 0

    def upload_build(self, telegram_id : int, json_data : str) -> int:
        
        """
        Uploads build into database.
        Returns:
            int: inserted build_id
        """

        js_hash = hashlib.md5(json_data.encode()).hexdigest()

        self._execute_with_commit('INSERT INTO Builds (telegram_id, json_info, hash) VALUES (?, ?, ?)', (telegram_id, json_data, js_hash,) )
        self._execute_with_commit("SELECT last_insert_rowid()")
        build_id = self.cursor.fetchone()[0]

        return build_id

    def push_price_to_history(self, build_id: int, price: str):

        self._execute_with_commit('INSERT INTO BuildsPriceHistory (build_id, price, timestamp) VALUES (?, ?, ?)', (build_id, price, time.time(), ))

    def __del__(self):

        """
        Close database connection when the object is destroyed
        """
        
        self.connection.close()
