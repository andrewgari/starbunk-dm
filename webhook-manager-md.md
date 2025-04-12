# Webhook Management System

This document details the webhook management system for the Discord RPG Campaign Bot.

## Overview

The webhook system provides a centralized way to create, manage, and reuse Discord webhooks across the bot's features. This enables characters to send messages with custom names and avatars, dice rolls to appear as styled messages, and more.

## Core Functionality

### WebhookManager Class

```python
class WebhookManager:
    """Manages Discord webhooks for campaigns"""
    
    def __init__(self, bot):
        self.bot = bot
        
    async def get_or_create_webhook(self, channel, webhook_name="RPG Campaign Webhook"):
        """Get existing webhook or create a new one"""
        # Implementation details...
        
    async def get_campaign_webhook(self, guild_id, channel_id):
        """Get the webhook for a specific campaign"""
        # Implementation details...
        
    async def send_as_character(self, guild_id, channel_id, character_name, avatar_url, content):
        """Send a message as a character using the campaign webhook"""
        # Implementation details...
    
    async def send_roll_result(self, guild_id, channel_id, user_name, result_message):
        """Send a dice roll result using the campaign webhook"""
        # Implementation details...
        
    async def send_emote(self, guild_id, channel_id, character_name, avatar_url, action):
        """Send a character emote/action using the campaign webhook"""
        # Implementation details...
```

## Persistence Integration

Each campaign stores its associated webhook ID in the campaigns.json file:

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

## Webhook Creation and Recovery

1. **Initial Creation**: When a campaign is created, a webhook is also created and its ID stored
2. **Retrieval**: Before sending messages, the system attempts to use the stored webhook
3. **Recovery**: If the webhook is deleted or invalid, a new one is created automatically
4. **Cleanup**: When a campaign is deleted, associated webhooks are also removed

## Use Cases

### Character Messages

When a player uses the `/ic` command:

1. The system retrieves the player's character for the campaign
2. It calls `webhook_manager.send_as_character()` with appropriate parameters
3. The message appears with the character's name and avatar

### Dice Rolls

When a player uses the `/roll` command:

1. The dice are parsed and rolled
2. The system calls `webhook_manager.send_roll_result()` with results
3. The roll appears as a styled message in the channel

### Character Emotes

When a player uses the `/em` command:

1. The system retrieves the player's character
2. It calls `webhook_manager.send_emote()` with the action
3. The emote appears as a styled message (typically *italicized*)

## Error Handling

The webhook system includes robust error handling for common issues:

- Missing permissions
- Deleted webhooks
- Channel not found
- Rate limiting
- Network errors

Each error is caught, logged, and appropriate recovery or user feedback is provided.

## Design Principles

1. **Single Responsibility**: The WebhookManager handles only webhook-related tasks
2. **Reusability**: The same webhook is reused for multiple features
3. **Reliability**: Built-in recovery mechanisms ensure consistent operation
4. **Scalability**: One webhook per channel respects Discord's limits while providing all needed functionality

## Security Considerations

- Webhooks only have send message permissions
- No sensitive data is stored with the webhook
- Proper error handling prevents information leakage
- Input validation prevents abuse of the webhook system

## Limitations

- Discord limits servers to 10 webhooks per channel
- Webhook messages can't be edited by the bot after sending
- Custom usernames are limited to 80 characters
