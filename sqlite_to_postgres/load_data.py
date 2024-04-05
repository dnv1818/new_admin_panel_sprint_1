import os
import sqlite3
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from postgres_saver import PostgresSaver
from sqlite_extractor import SQLiteExtractor
from data_classes import *

load_dotenv()


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(sqlite_conn)
    sqlite_psql = {
        'genre': Genre,
        'person': Person,
        'film_work': Filmwork,
        'genre_film_work': GenreFilmwork,
        'person_film_work': PersonFilmwork,
    }
    for table_name, data_class in sqlite_psql.items():
        data = sqlite_extractor.extract_data(data_class, table_name)
        postgres_saver.save_data(data, table_name)


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME', 'movies_database'),
        'user': os.environ.get('DB_USER', 'user'),
        'password': os.environ.get('DB_PASSWORD', 'password'),
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '5432'),
    }
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
