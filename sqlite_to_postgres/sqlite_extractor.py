import sqlite3
import logging as log


class SQLiteExtractor:
    def __init__(self, sqlite_conn: sqlite3.Connection):
        self.sqlite_conn = sqlite_conn

    def extract_data(self, data_class, table_name: str):
        """Извлекает данные из SQLite базы данных."""
        try:
            return list(self.extract_data_per_pack(data_class, table_name))
        except Exception as e:
            log.error(f'Error extracting {table_name}: {e}', exc_info=True)
            raise e

    def extract_data_per_pack(self, data_class, table_name: str, pack_size=100):
        try:
            with self.sqlite_conn:
                cursor = self.sqlite_conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name}")
                while records := cursor.fetchmany(pack_size):
                    for row in records:
                        yield data_class(*row)
        except Exception as e:
            log.error(f'Error extracting {table_name}: {e}', exc_info=True)
            raise e
