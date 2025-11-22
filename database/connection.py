import mysql.connector
from config import db_config

def get_connection():
    return mysql.connector.connect(
        host=db_config.DB_HOST,
        user=db_config.DB_USER,
        password=db_config.DB_PASSWORD,
        database=db_config.DB_NAME
    )
