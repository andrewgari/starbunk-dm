import re
from enum import Enum

class DiscordID(str):
    """A value object for Discord snowflake IDs, always numeric as a string."""
    def __new__(cls, value):
        if not DiscordID.is_valid(value):
            raise ValueError(f"Invalid Discord ID: {value}")
        return str.__new__(cls, value)

    @staticmethod
    def is_valid(value):
        return isinstance(value, str) and value.isdigit() and len(value) > 0


def validate_discord_id(value):
    """Returns True if value is a valid Discord snowflake ID (string of digits)."""
    return DiscordID.is_valid(value)


class PlayerType(Enum):
    PLAYER = 'Player'
    GM = 'GM'

class CharacterType(Enum):
    PLAYER_CHARACTER = 'Player Character'
    PLAYER_COMPANION = 'Player Companion'
    NPC = 'NPC'