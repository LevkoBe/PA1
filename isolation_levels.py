import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime
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

def read_uncommitted_demo():
    connection1 = create_connection()
    connection2 = create_connection()
    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()
        print(f"=== READ UNCOMMITTED: Demonstrating Dirty Read ===")
        connection1.start_transaction(isolation_level='READ UNCOMMITTED')
        connection2.start_transaction(isolation_level='READ UNCOMMITTED')

        cursor1.execute("UPDATE accounts SET balance = 9999 WHERE name = 'Alice'")
        cursor2.execute("SELECT balance FROM accounts WHERE name = 'Alice'")

        balance_dirty_read = cursor2.fetchone()[0]
        print(f"Dirty Read (READ UNCOMMITTED): Alice's balance = {balance_dirty_read}")

        connection1.rollback()
        connection2.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()

def read_committed_demo():
    connection1 = create_connection()
    connection2 = create_connection()
    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()
        print(f"=== READ COMMITTED: No Dirty Read, Possible Non-repeatable Read ===")
        connection1.start_transaction(isolation_level='READ COMMITTED')
        connection2.start_transaction(isolation_level='READ COMMITTED')

        cursor1.execute("UPDATE accounts SET balance = 5000 WHERE name = 'Alice'")
        cursor2.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        
        balance_read_committed = cursor2.fetchone()[0]
        print(f"Read Committed: Alice's balance after update (before commit) = {balance_read_committed}")
        connection1.commit()
        connection2.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()

def repeatable_read_demo():
    connection1 = create_connection()
    connection2 = create_connection()
    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()
        print(f"=== REPEATABLE READ ===")
        connection1.start_transaction(isolation_level='REPEATABLE READ')
        connection2.start_transaction(isolation_level='READ COMMITTED')

        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        initial_balance = cursor1.fetchone()[0]
        print(f"Initial Balance (REPEATABLE READ): Alice's balance = {initial_balance}")

        cursor2.execute("UPDATE accounts SET balance = 7000 WHERE name = 'Alice'")
        connection2.commit()

        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        repeat_balance = cursor1.fetchone()[0]
        print(f"Repeatable Read: Alice's balance after another transaction's commit = {repeat_balance}")

        connection1.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()

def serializable_demo():
    connection1 = create_connection()
    connection2 = create_connection()
    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()
        print(f"=== SERIALIZABLE: Demonstrating Serializable ===")
        connection1.start_transaction(isolation_level='SERIALIZABLE')
        connection2.start_transaction(isolation_level='SERIALIZABLE')

        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        initial_balance = cursor1.fetchone()[0]
        print(f"Initial Balance (SERIALIZABLE): Alice's balance = {initial_balance}")
        
        cursor2.execute("UPDATE accounts SET balance = 8000 WHERE name = 'Alice'")
        # Attempting to commit the second transaction
        try:
            connection2.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            connection1.commit()
            connection2.close()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()

