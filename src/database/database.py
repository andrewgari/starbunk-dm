import sqlite3
import os
import threading
from config import DATABASE_PATH
from src.utils import DiscordID, validate_discord_id, PlayerType, CharacterType

class DataManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DataManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
             return
        with self._lock:
            if hasattr(self, '_initialized') and self._initialized:
                return
            self._initialize_database()
            self._initialized = True


    def _get_db_connection(self):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.row_factory = sqlite3.Row # Return rows as dictionary-like objects
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def _initialize_database(self):
        conn = None
        try:
            os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
            conn = self._get_db_connection()
            cursor = conn.cursor()

            # Create Player table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Player (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    member_id TEXT NOT NULL,
                    guild_id TEXT NOT NULL,
                    channel_id TEXT NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('Player', 'GM')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create Campaign table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Campaign (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    guild_id TEXT NOT NULL,
                    channel_id TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create Character table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Character (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    avatar_url TEXT,
                    type TEXT NOT NULL CHECK(type IN ('Player Character', 'Player Companion', 'NPC')),
                    player_id INTEGER NOT NULL,
                    campaign_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(player_id) REFERENCES Player(id),
                    FOREIGN KEY(campaign_id) REFERENCES Campaign(id)
                )
            ''')

            conn.commit()
            print(f"Database checked/initialized at {DATABASE_PATH}")
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def create_player(self, name, member_id, guild_id, channel_id, type_):
        if isinstance(type_, PlayerType):
            type_str = type_.value
        elif str(type_) in (t.value for t in PlayerType):
            type_str = str(type_)
        else:
            raise ValueError(f"Invalid PlayerType: {type_}")

        if not (
            validate_discord_id(member_id)
            and validate_discord_id(guild_id)
            and validate_discord_id(channel_id)
        ):
            raise ValueError("Invalid Discord ID(s) for player.")

        conn = self._get_db_connection()
        # …rest of method…
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Player (name, member_id, guild_id, channel_id, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, member_id, guild_id, channel_id, type_str))
        conn.commit()
        player_id = cursor.lastrowid
        conn.close()
        return player_id

    def create_campaign(self, name, guild_id, channel_id):
        if not (validate_discord_id(guild_id) and validate_discord_id(channel_id)):
            raise ValueError("Invalid Discord ID(s) for campaign.")
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Campaign (name, guild_id, channel_id)
            VALUES (?, ?, ?)
        ''', (name, guild_id, channel_id))
        conn.commit()
        campaign_id = cursor.lastrowid
        conn.close()
        return campaign_id

    def create_character(self, name, avatar_url, type_, player_id, campaign_id):
        if isinstance(type_, CharacterType):
            type_str = type_.value
        elif str(type_) in (t.value for t in CharacterType):
            type_str = str(type_)
        else:
            raise ValueError(f"Invalid CharacterType: {type_}")
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Character (name, avatar_url, type, player_id, campaign_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, avatar_url, type_str, player_id, campaign_id))
        conn.commit()
        character_id = cursor.lastrowid
        conn.close()
        return character_id

    def get_character_by_name_and_campaign(self, name, campaign_id):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Character WHERE name = ? AND campaign_id = ?
        ''', (name, campaign_id))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None

    def get_characters_by_player_and_campaign(self, player_id, campaign_id):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Character WHERE player_id = ? AND campaign_id = ?
        ''', (player_id, campaign_id))
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]

    def get_all_characters_in_campaign(self, campaign_id):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Character WHERE campaign_id = ?
        ''', (campaign_id,))
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]

    def update_character(self, character_id, **kwargs):
        allowed_fields = {'name', 'avatar_url', 'type', 'player_id', 'campaign_id'}
        fields = []
        values = []

        for k, v in kwargs.items():
            if k in allowed_fields:
                if k == 'type' and isinstance(v, CharacterType):
                    v = v.value
                # convert enum to its raw value so the DB check constraint isn’t violated
                if k == "type" and isinstance(v, CharacterType):
                    v = v.value
                fields.append(f"{k} = ?")
                values.append(v)
            # else: silently ignore unknown keys

        # now fail fast if any completely unknown fields were passed in
        if any(k not in allowed_fields for k in kwargs):
            unknown = {k for k in kwargs if k not in allowed_fields}
            raise ValueError(f"Unknown field(s) for update: {', '.join(unknown)}")

        if not fields:
            return False

        values.append(character_id)
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE Character
               SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP
             WHERE id = ?
        ''', values)
        conn.commit()
        conn.close()
        return True

    def delete_character(self, character_id):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM Character WHERE id = ?
        ''', (character_id,))
        conn.commit()
        conn.close()
        return True

def get_data_manager():
    return DataManager()
