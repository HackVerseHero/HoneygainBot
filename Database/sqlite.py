import sqlite3
from Database.baseStorage import BaseStorage


class SQLiteStorage(BaseStorage):
    def __init__(self, database):
        self.database = database
        init_query = '''
        CREATE TABLE IF NOT EXISTS timestamps 
        (param_name TEXT PRIMARY KEY, timestamp DATETIME)
        '''
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute(init_query)
        connection.commit()
        connection.close()

    def set_data(self, table, param, data):
        connection = sqlite3.connect(self.database)
        set_query = f'''INSERT INTO {table} (param_name, timestamp) VALUES (?, ?)'''
        try:
            connection.execute(set_query, (param, data))
            connection.commit()
        finally:
            connection.close()

    def get_data(self, table, param):
        connection = sqlite3.connect(self.database)
        get_query = f'''SELECT timestamp FROM {table} where param_name = ?'''
        try:
            cursor = connection.cursor()
            cursor.execute(get_query, (param,))
            rows = cursor.fetchall()
            data = rows[0][0]
            connection.commit()
            return data
        finally:
            connection.close()

    def update_data(self, table, param, data):
        connection = sqlite3.connect(self.database)
        update_query = f'''UPDATE {table} SET timestamp = ? WHERE param_name = ?'''
        try:
            with connection:
                cursor = connection.cursor()
                cursor.execute(update_query, (data, param,))
                if cursor.rowcount == 0:
                    raise ValueError("Failed to update data in the database.")
            connection.commit()
        finally:
            connection.close()
