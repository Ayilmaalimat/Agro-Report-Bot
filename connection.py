from decouple import config
import mysql.connector

DB_NAME = config('DB_NAME')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')

try:
    conn = mysql.connector.connect(
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    )
    print("connected to the database")
except:
    print("unable to connect to the database")
