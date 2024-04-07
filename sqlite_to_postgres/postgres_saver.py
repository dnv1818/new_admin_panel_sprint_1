from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch
import logging as log


def get_values(fields: str):
    return ', '.join(['%s'] * len(fields.split(', ')))


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.pg_conn = pg_conn

    def save_data(self, data, table_name: str):
        try:
            match table_name:
                case 'genre':
                    fields = 'id, name, description, created, modified'
                    data = [(i.id, i.name, i.description, i.created_at, i.updated_at) for i in data]
                case 'film_work':
                    fields = 'id, title, description, creation_date, file_path, rating, type, created, modified'
                    data = [(i.id, i.title, i.description, i.creation_date, i.file_path, i.rating, i.type, i.created_at,
                             i.updated_at) for i in data]
                case 'person':
                    fields = 'id, full_name, created, modified'
                    data = [(i.id, i.full_name, i.created_at, i.updated_at) for i in data]
                case 'genre_film_work':
                    fields = 'id, film_work_id, genre_id, created'
                    data = [(i.id, i.film_work_id, i.genre_id, i.created_at) for i in data]
                case 'person_film_work':
                    fields = 'id, film_work_id, person_id, role, created'
                    data = [(i.id, i.film_work_id, i.person_id, i.role, i.created_at) for i in data]
                case _:
                    raise ValueError(f'Table name {table_name} not supported')

            query = (f"INSERT INTO content.{table_name} ({fields}) "
                     f"VALUES ({get_values(fields)}) ON CONFLICT (id) DO NOTHING;")
            self._save_data(query, data)
        except Exception as e:
            log.error(f'Error saving data to table {table_name}: {e}', exc_info=True)

    def _save_data(self, query, data, pack_size=100):
        try:
            total = len(data)
            for start_idx in range(0, total, pack_size):
                end_idx = start_idx + pack_size
                batch = data[start_idx:end_idx]
                with self.pg_conn.cursor() as cursor:
                    execute_batch(cursor, query, batch)
                    self.pg_conn.commit()
        except Exception as e:
            log.error(f'Error processing batch {start_idx}-{end_idx}: {e}', exc_info=True)
            self.pg_conn.rollback()
            raise e
