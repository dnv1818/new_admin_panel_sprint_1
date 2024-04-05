import sqlite3


class SQLiteExtractor:
    def __init__(self, sqlite_conn: sqlite3.Connection):
        self.sqlite_conn = sqlite_conn

    def extract_data(self, data_class, table_name: str):
        """Извлекает данные из SQLite базы данных."""
        try:
            return list(self.extract_data_per_pack(data_class, table_name))
        except Exception as e:
            print(f'Error extracting {table_name}: {e}')
            raise e

    def extract_data_per_pack(self, data_class, table_name: str, pack_size=100):
        try:
            with self.sqlite_conn:
                cursor = self.sqlite_conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name}")
                while True:
                    records = cursor.fetchmany(pack_size)
                    if not records:
                        break
                    for row in records:
                        yield data_class(*row)
        except Exception as e:
            print(f'Error extracting {table_name}: {e}')
            raise e
