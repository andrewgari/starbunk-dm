import sqlite3
import os
import threading
from config import DATABASE_PATH

class DataManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                # Another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super(DataManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initializes the DataManager singleton instance."""
        if hasattr(self, '_initialized') and self._initialized:
             return
        with self._lock:
            if hasattr(self, '_initialized') and self._initialized:
                return
            self._initialize_database()
            self._initialized = True


    def _get_db_connection(self):
        """Returns a connection object to the database."""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.row_factory = sqlite3.Row # Return rows as dictionary-like objects
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def _initialize_database(self):
        """Initializes the database connection and ensures the database file exists.

        This function ensures that the directory for the database exists and connects to the
        SQLite database file, creating it if necessary. Table creation is handled separately.
        """
        conn = None
        try:
            os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
            # Connect to the database (this will create the file if it doesn't exist)
            conn = self._get_db_connection()

            conn.commit() # Commit any changes if schema modifications were made (though none are here now)
            print(f"Database checked/initialized at {DATABASE_PATH}")
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
        finally:
            if conn:
                conn.close()

    # Add other data access methods here as needed
    # e.g., get_all_users, delete_user, etc.

# Provide a way to access the singleton instance
def get_data_manager():
    """Returns the singleton instance of the DataManager."""
    return DataManager()
