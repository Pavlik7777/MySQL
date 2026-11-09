import os
import sys
import time
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3307)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "rootpassword"),
    "charset": "utf8mb4"
}

DB_NAME = "demo_lesson5_db"

def create_database(db_name=DB_NAME, retries=10, delay=3):
    for attempt in range(1,retries+1):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            break
        except Error as err:
            if attempt == retries:
                raise
            print(f"Сервер MySQL недоступен ({err.msg}), попытка {attempt}/{retries}...")
            time.sleep(delay)

    try:
        cursor = connection.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
        cursor.execute("SHOW DATABASES LIKE %s;", (db_name,))
        if cursor.fetchone():
            print(f"База данных `{db_name}` готова к работе.")
        cursor.close()
    finally:
        connection.close()


if __name__ == "__main__":
    create_database()