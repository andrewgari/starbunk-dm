# Data Persistence System

This document outlines the data persistence design for the Discord RPG Campaign Bot.

## Overview

The bot uses a JSON-based persistence system to store information about campaigns, characters, and relationships between Discord entities (channels, roles, users). This design ensures that data survives bot restarts and maintains the integrity of the roleplaying environment.

## Data Structures

### Campaigns Data

```json
{
  "guild_id": {
    "channel_id": {
      "name": "Campaign Name",
      "gm_id": "user_id_of_gm",
      "player_role_id": "role_id",
      "gm_role_id": "role_id",
      "webhook_id": "webhook_id",
      "players": ["user_id1", "user_id2", ...]
    }
  }
}
```

This structure allows:
- Organization by guild (server) and channel
- Quick lookup of campaign-specific details
- Association with Discord roles for permission management
- Storage of the webhook ID for messaging features

### Characters Data

```json
{
  "guild_id": {
    "user_id": {
      "channel_id": {
        "name": "Character Name",
        "avatar_url": "URL to avatar image",
        "description": "Character description"
      }
    }
  }
}
```

This structure enables:
- One character per player per campaign channel
- Quick lookup of a player's character in a specific campaign
- Storage of character-specific details for messaging

### GM-Created NPCs

```json
{
  "guild_id": {
    "channel_id": {
      "npc_id": {
        "name": "NPC Name",
        "avatar_url": "URL to avatar image",
        "creator_id": "gm_user_id"
      }
    }
  }
}
```

This allows GMs to:
- Create multiple NPCs per campaign
- Quickly access their NPC list for storytelling
- Maintain separate NPCs for different campaigns

## Implementation

### DataManager Class

```python
class DataManager:
    """Manages persistence of bot data"""
    
    def __init__(self, data_dir="./data"):
        self.data_dir = data_dir
        self.campaigns_file = os.path.join(data_dir, "campaigns.json")
        self.characters_file = os.path.join(data_dir, "characters.json")
        self.npcs_file = os.path.join(data_dir, "npcs.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize data structures
        self.campaigns = {}
        self.characters = {}
        self.npcs = {}
        
        # Load data on initialization
        self.load_data()
    
    def load_data(self):
        """Load all data from files"""
        self.campaigns = self._load_json_file(self.campaigns_file, {})
        self.characters = self._load_json_file(self.characters_file, {})
        self.npcs = self._load_json_file(self.npcs_file, {})
    
    def save_data(self):
        """Save all data to files"""
        self._save_json_file(self.campaigns_file, self.campaigns)
        self._save_json_file(self.characters_file, self.characters)
        self._save_json_file(self.npcs_file, self.npcs)
        
    def _load_json_file(self, file_path, default_value):
        """Load JSON from file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default_value
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return default_value
    
    def _save_json_file(self, file_path, data):
        """Save JSON to file with error handling"""
        try:
            # Create a backup first
            self._create_backup(file_path)
            
            # Save the new data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            return True
        except Exception as e:
            print(f"Error saving {file_path}: {e}")
            return False
    
    def _create_backup(self, file_path):
        """Create a backup of the given file"""
        try:
            if os.path.exists(file_path):
                backup_dir = os.path.join(self.data_dir, "backups")
                os.makedirs(backup_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = os.path.basename(file_path)
                backup_path = os.path.join(backup_dir, f"{filename}.{timestamp}")
                
                shutil.copy2(file_path, backup_path)
        except Exception as e:
            print(f"Error creating backup: {e}")
```

## Integration with Bot Features

### Campaign Creation

```python
async def create_campaign(self, interaction):
    guild_id = str(interaction.guild_id)
    channel_id = str(interaction.channel_id)
    
    # Create campaign entry
    if guild_id not in self.bot.data.campaigns:
        self.bot.data.campaigns[guild_id] = {}
        
    self.bot.data.campaigns[guild_id][channel_id] = {
        "name": interaction.channel.name,
        "gm_id": str(interaction.user.id),
        "player_role_id": str(player_role.id),
        "gm_role_id": str(gm_role.id),
        "players": []
    }
    
    # Save data
    self.bot.data.save_data()
```

### Character Creation

```python
async def create_character(self, interaction, name, avatar_url):
    guild_id = str(interaction.guild_id)
    channel_id = str(interaction.channel_id)
    user_id = str(interaction.user.id)
    
    # Initialize data structure if needed
    if guild_id not in self.bot.data.characters:
        self.bot.data.characters[guild_id] = {}
    if user_id not in self.bot.data.characters[guild_id]:
        self.bot.data.characters[guild_id][user_id] = {}
        
    # Create or update character
    self.bot.data.characters[guild_id][user_id][channel_id] = {
        "name": name,
        "avatar_url": avatar_url,
        "description": ""
    }
    
    # Save data
    self.bot.data.save_data()
```

## Data Validation and Recovery

The system includes several safeguards:

1. **Backups**: Every save operation creates a backup with timestamp
2. **Error Handling**: All file operations include try/except blocks
3. **Default Values**: Missing data is handled gracefully with defaults
4. **Validation**: Data is validated before saving and after loading
5. **Recovery**: If data is corrupted, it attempts to load from backups

## Security Considerations

1. **File Permissions**: Data files have restricted permissions
2. **Sanitization**: All user input is sanitized before storage
3. **No Sensitive Data**: The system never stores tokens or credentials
4. **Guild Isolation**: Data from different Discord servers is isolated

## Limitations and Considerations

1. **Performance**: JSON is not optimized for large datasets but works well for typical use cases
2. **Concurrency**: The current design doesn't handle concurrent modifications optimally
3. **Scalability**: For very large servers, a database solution might be preferable
4. **Backup Management**: Old backups are not automatically pruned

## Future Improvements

1. **Database Migration**: Option to use SQLite or another database for larger deployments
2. **Transaction Support**: Atomic operations for better data integrity
3. **Compression**: Data compression for reduced storage needs
4. **Cloud Storage**: Option for cloud-based backup and synchronization
