import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file into environment

TOKEN = os.getenv("DISCORD_TOKEN") # Load the token from environment variables
DATABASE_PATH = "data/bot_database.db"  # Path to the SQLite database file

# Add any other configuration settings as needed
