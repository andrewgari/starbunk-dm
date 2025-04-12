\
import sqlite3
import os
from config import DATABASE_PATH

def initialize_database():
    """Initializes the database connection and creates tables if they don't exist.
    
    This function ensures that the directory for the database exists, connects to the 
    SQLite database, creates the necessary tables (e.g., users), and closes the connection.
    
    Parameters:
        None
    
    Returns:
        None
    
    Exceptions:
        Raises exceptions related to file handling or database connection issues.
    """
    try:
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            first_seen TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        conn.close()
        print(f"Database initialized at {DATABASE_PATH}")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
def get_db_connection():
    """Returns a connection object to the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row # Return rows as dictionary-like objects
    return conn

# Example function to add or update a user
def add_or_update_user(user_id, username):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users (user_id, username)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username
        """, (user_id, username))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding or updating user: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()
# Example function to get user info
def get_user(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Error retrieving user: {e}")
        raise
    finally:
        if conn:
            conn.close()
