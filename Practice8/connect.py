from config import config
import psycopg2

def get_connection():
    return psycopg2.connect(**config)
