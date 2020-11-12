import psycopg2
import teradatasql

from sqldiff.comp.compare import compare

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


with psycopg2.connect(**connection_params_postgres) as postgres_connection, \
        teradatasql.connect(**connection_params_teradata) as teradata_connection:

    result = compare(
        source_connection=teradata_connection,
        source_query=query_teradata,
        target_connection=postgres_connection,
        target_query=query_postgres)

print(result)
