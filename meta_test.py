import psycopg2

import sqldiff.meta.postgres_meta as postgres
import teradatasql

from sqldiff import relation as teradata

connection_params_postgres = {
    'host': 'localhost',
    'port': '5432',
    'user': 'admin',
    'password': 'admin',
    'database': 'test_db'
}

connection_params_teradata = {
    'host': '192.168.1.2',
    'user': 'dbc',
    'password': 'dbc',
    'database': 'test_db'
}

query_postgres = 'select * from all_datatypes'
query_teradata = 'select * from all_datatypes'

with psycopg2.connect(**connection_params_postgres) as connection:
    meta_postgres = postgres.get_meta(connection, query_postgres)


with teradatasql.connect(**connection_params_teradata) as connection:
    meta_teradata = teradata.get_meta(connection, query_teradata)
    meta_raw_teradata = teradata.get_raw_meta(connection, query_teradata)

a=1
