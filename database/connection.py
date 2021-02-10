from decouple import config
import mysql.connector

DB_NAME = config('MYSQL_DATABASE')
DB_HOST = config('MYSQL_HOST')
DB_PORT = config('MYSQL_PORT')
DB_USER = config('MYSQL_USER')
DB_PASSWORD = config('MYSQL_PASSWORD')


def create_pool():
    return mysql.connector.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

