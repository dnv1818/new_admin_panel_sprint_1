import datetime
from dateutil import parser
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
                sqlite_cur.execute(f"SELECT * FROM {table}")
                sqlite_records = sqlite_cur.fetchall()

            with self.pg_conn:
                pg_cur = self.pg_conn.cursor()
                pg_cur.execute(f"SELECT * FROM content.{table}")
                pg_records = pg_cur.fetchall()

            self.assertEqual(len(sqlite_records), len(pg_records), f"Table {table} row count mismatch")

            for i in range(len(sqlite_records)):
                sqlite_record = sqlite_records[i]
                pg_record = pg_records[i]
                for j in range(len(sqlite_record)):
                    if type(pg_record[j]) == datetime.datetime:
                        sqlite_record_field_value = parser.parse(sqlite_record[j])
                        self.assertEqual(
                            sqlite_record_field_value, pg_record[j],
                            f"Field value {j} for record {i} in table {table} does not match"
                            f" between SQLite and PostgreSQL.")
                    else:
                        self.assertEqual(
                            sqlite_record[j], pg_record[j],
                            f"Field value {j} for record {i} in table {table} does not match"
                            f" between SQLite and PostgreSQL.")

    def tearDown(self):
        self.sqlite_conn.close()
        self.pg_conn.close()


if __name__ == '__main__':
    unittest.main()
