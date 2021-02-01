from decouple import config
import psycopg2

DB_NAME = config('DB_NAME')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')

try:
    conn = psycopg2.connect(
        "dbname={} user={} host={} password={} port={}".format(DB_NAME, DB_USER, DB_HOST, DB_PASSWORD, DB_PORT))
    print("connected to the database")
except:
    print("unable to connect to the database")
