import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="rinet",
        user="postgres",
        password="",
        port="5432"
)