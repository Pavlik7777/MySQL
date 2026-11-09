import mysql.connector

from main import DB_CONFIG, DB_NAME


def create_table(db_name=DB_NAME):
    connection = mysql.connector.connect(**DB_CONFIG, database= db_name)
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                last_name VARCHAR(50) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                middle_name VARCHAR(50) NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                phone VARCHAR(20) NULL
            ) ENGINE=InnoDB;
        """)
        print("Таблица 'users'готова к работе. ")
        cursor.close()
    finally:
        connection.close()



if __name__ == "__main__":
    create_table()