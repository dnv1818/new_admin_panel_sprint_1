import os
import sqlite3
import psycopg2
import unittest
from dotenv import load_dotenv

load_dotenv()

dsl = {
        'dbname': os.environ.get('DB_NAME', 'movies_database'),
        'user': os.environ.get('DB_USER', 'user'),
        'password': os.environ.get('DB_PASSWORD', 'password'),
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '5432'),
}


class TestDatabaseIntegrity(unittest.TestCase):
    def setUp(self):
        self.sqlite_conn = sqlite3.connect('db.sqlite')
        self.pg_conn = psycopg2.connect(**dsl)

    def test_table_integrity(self):
        tables_to_check = ['genre', 'film_work', 'person', 'genre_film_work', 'person_film_work']
        for table in tables_to_check:
            with self.sqlite_conn:
                sqlite_cur = self.sqlite_conn.cursor()
                sqlite_cur.execute(f"SELECT COUNT(*) FROM {table}")
                sqlite_count = sqlite_cur.fetchone()[0]

            with self.pg_conn:
                pg_cur = self.pg_conn.cursor()
                pg_cur.execute(f"SELECT COUNT(*) FROM content.{table}")
                pg_count = pg_cur.fetchone()[0]

            self.assertEqual(sqlite_count, pg_count, f"Table {table} row count mismatch")

    def tearDown(self):
        self.sqlite_conn.close()
        self.pg_conn.close()


if __name__ == '__main__':
    unittest.main()
