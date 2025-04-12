\
import sqlite3
import os
from config import DATABASE_PATH

def initialize_database():
    """Initializes the database connection and creates tables if they don't exist."""
    # Ensure the directory exists
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

    # Add other tables here if needed, e.g.:
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS server_settings (
    #     guild_id INTEGER PRIMARY KEY,
    #     setting_name TEXT NOT NULL,
    #     setting_value TEXT
    # )
    # """)

    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE_PATH}")

def get_db_connection():
    """Returns a connection object to the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row # Return rows as dictionary-like objects
    return conn

# Example function to add or update a user
def add_or_update_user(user_id, username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO users (user_id, username)
    VALUES (?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        username = excluded.username
    """, (user_id, username))
    conn.commit()
    conn.close()

# Example function to get user info
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user
