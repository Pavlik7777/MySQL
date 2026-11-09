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

def get_db_config_with_db():
    """Возвращает конфигурацию с указанием имени базы данных."""
    config = DB_CONFIG.copy()
    config["database"] = DB_NAME
    return config

def recreate_table():
    """Удаляет старую неправильную таблицу и создает новую с верной структурой."""
    try:
        connection = mysql.connector.connect(**get_db_config_with_db())
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users;")
        query = """
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(query)
        connection.commit()
        print("Таблица `users` успешно создана с нужными колонками (id, name, email).")
        cursor.close()
    except Error as err:
        print(f"Ошибка при подготовке таблицы: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
def insert_user(name, email):
    """Добавляет одну запись в таблицу users."""
    query = "INSERT INTO users (name, email) VALUES (%s, %s);"
    data = (name, email)
    try:
        connection = mysql.connector.connect(**get_db_config_with_db())
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        print(f"Данные успешно добавлены! Пользователь: {name} (ID: {cursor.lastrowid})")
        cursor.close()
    except Error as err:
        print(f"Не удалось добавить данные для {name}: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    recreate_table()
    insert_user("Миша Бука", "misha10@example.com")
    insert_user("Ольга Сергеевна", "olga22@example.com")
