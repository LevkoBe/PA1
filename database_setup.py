import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connection settings
HOST = os.getenv('host')
USER = os.getenv('user')
PASSWORD = os.getenv('password')
DATABASE = os.getenv('database')

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

def setup_database():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS accounts;")
            cursor.execute("""
            CREATE TABLE accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                balance DECIMAL(10, 2)
            );
            """)
            cursor.execute("INSERT INTO accounts (name, balance) VALUES ('Alice', 1000.00), ('Bob', 1500.00), ('Charlie', 2000.00), ('Me', 30000.00);")
            connection.commit()
            print("Database setup completed.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    setup_database()
