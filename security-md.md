# Security Guidelines

This document outlines security considerations and best practices for the Discord RPG Campaign Bot.

## Token Management

### Environment Variables

Discord bot tokens must be stored in environment variables, never in code:

```python
# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord bot token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise EnvironmentError("No Discord token found. Set the DISCORD_TOKEN environment variable.")
```

### .env File

Create a `.env` file at the project root:

```
DISCORD_TOKEN=your_discord_bot_token_here
```

**Important**: Add `.env` to your `.gitignore` file to prevent it from being committed to version control:

```
# .gitignore
.env
```

### Example File

Provide a `.env.example` file with placeholders:

```
# .env.example
DISCORD_TOKEN=your_discord_bot_token_here
```

## Data Security

### File Permissions

Set restrictive permissions on data files:

```python
def set_secure_permissions(file_path):
    """Set secure permissions on file (read/write for owner only)"""
    try:
        # For Unix-like systems (0o600 = read/write for owner only)
        if os.name != 'nt':  # Not Windows
            os.chmod(file_path, 0o600)
        # For Windows, could use ACLs but more complex
    except Exception as e:
        print(f"Warning: Could not set secure permissions on {file_path}: {e}")
```

### Data Validation

Always validate data before using it:

```python
def is_valid_user_id(user_id):
    """Validate that a user ID is in the correct format"""
    return isinstance(user_id, str) and user_id.isdigit()

def is_valid_avatar_url(url):
    """Validate avatar URL for security and correctness"""
    # Check for valid URL format
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IPv4
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        return False
        
    # Check for allowed image extensions
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    return any(url.lower().endswith(ext) for ext in allowed_extensions)
```

### Input Sanitization

Sanitize all user input:

```python
def sanitize_string(text):
    """Sanitize a string to prevent injection attacks"""
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32)
    
    # Limit length
    max_length = 1000  # Adjust as needed
    if len(text) > max_length:
        text = text[:max_length]
        
    return text
```

## Webhook Security

### Webhook Management

Ensure webhooks only have necessary permissions:

```python
async def create_secure_webhook(channel, name):
    """Create a webhook with minimal permissions"""
    try:
        webhook = await channel.create_webhook(
            name=name,
            reason="Created for RPG Campaign Bot"
        )
        return webhook
    except discord.Forbidden:
        raise PermissionError("Bot doesn't have 'Manage Webhooks' permission")
```

### Webhook Content Validation

Validate all content sent through webhooks:

```python
async def send_safe_webhook_message(webhook, content, username=None, avatar_url=None):
    """Send a webhook message with content validation"""
    # Sanitize content
    safe_content = sanitize_string(content)
    
    # Validate username if provided
    safe_username = None
    if username:
        safe_username = sanitize_string(username)[:80]  # Discord limit
    
    # Validate avatar URL if provided
    safe_avatar_url = None
    if avatar_url and is_valid_avatar_url(avatar_url):
        safe_avatar_url = avatar_url
    
    # Send the message
    await webhook.send(
        content=safe_content,
        username=safe_username,
        avatar_url=safe_avatar_url
    )
```

## Permission Management

### Required Bot Permissions

The bot requires these permissions, but no more:

- `manage_roles` - For creating and assigning GM/Player roles
- `manage_channels` - For setting channel permissions
- `manage_webhooks` - For creating and using webhooks
- `send_messages` - For sending messages
- `read_messages` - For reading commands

### Role Creation

When creating roles, use the principle of least privilege:

```python
async def create_player_role(guild):
    """Create a player role with minimal permissions"""
    return await guild.create_role(
        name="RPG Player",
        permissions=discord.Permissions(
            send_messages=True,
            read_messages=True,
            read_message_history=True,
            # No additional permissions
        ),
        color=discord.Color.blue(),
        mentionable=True
    )
```

## Error Handling

### Secure Error Messages

Never include sensitive information in error messages:

```python
try:
    # Some operation
    pass
except Exception as e:
    # Log the full error privately
    logging.error(f"Detailed error: {str(e)}")
    
    # Return a safe message to the user
    await interaction.response.send_message(
        "An error occurred while processing your request. Please try again later.",
        ephemeral=True
    )
```

## Deployment Security

### Service Account

Run the bot under a dedicated service account with minimal permissions:

```bash
# Create a dedicated user (Linux)
sudo useradd -r -s /bin/false discord-bot

# Set ownership of bot files
sudo chown -R discord-bot:discord-bot /path/to/bot

# Run the bot as this user
sudo -u discord-bot python bot.py
```

### Container Deployment

Consider using Docker for secure isolation:

```dockerfile
FROM python:3.9-slim

# Create a non-root user
RUN useradd -r -s /bin/false botuser

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set proper ownership
RUN chown -R botuser:botuser /app

# Switch to non-root user
USER botuser

# Run the application
CMD ["python", "bot.py"]
```

## Rate Limiting

### Discord API Rate Limits

Implement rate limiting to prevent abuse and stay within Discord's limits:

```python
class RateLimiter:
    """Simple rate limiter for Discord API calls"""
    
    def __init__(self):
        self.command_timestamps = {}
        self.user_cooldowns = {}
    
    async def check_rate_limit(self, user_id, command_name, cooldown_seconds=3):
        """Check if a user is rate limited for a command
        
        Returns:
            bool: True if the user can proceed, False if rate limited
        """
        current_time = time.time()
        
        # Create user entry if not exists
        if user_id not in self.user_cooldowns:
            self.user_cooldowns[user_id] = {}
        
        # Check if command is on cooldown
        if command_name in self.user_cooldowns[user_id]:
            last_used = self.user_cooldowns[user_id][command_name]
            if current_time - last_used < cooldown_seconds:
                return False
        
        # Update last used time
        self.user_cooldowns[user_id][command_name] = current_time
        return True
```

## Logging

### Secure Logging

Implement secure logging that doesn't expose sensitive data:

```python
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(log_dir="./logs"):
    """Set up secure logging"""
    os.makedirs(log_dir, exist_ok=True)
    
    # Set up file handler with rotation
    log_file = os.path.join(log_dir, "bot.log")
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=5
    )
    
    # Set restrictive permissions on log file
    if os.name != 'nt':  # Not Windows
        os.chmod(log_file, 0o600)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            file_handler,
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    # Sanitize sensitive data in logs
    class SensitiveFilter(logging.Filter):
        def filter(self, record):
            message = record.getMessage()
            
            # Filter out tokens, passwords, etc.
            filtered_message = re.sub(
                r'(token|password|secret)=[\w\.\-]+', 
                r'\1=[REDACTED]', 
                message, 
                flags=re.IGNORECASE
            )
            
            # Update the record
            record.msg = filtered_message
            return True
    
    # Add filter to root logger
    root_logger = logging.getLogger()
    root_logger.addFilter(SensitiveFilter())
```

## Regular Audits

### Security Audit Checklist

Perform regular security audits using this checklist:

1. **Token Security**
   - Is the Discord token stored in environment variables?
   - Are there any tokens accidentally committed to the repository?

2. **Data Storage**
   - Are data files stored with proper permissions?
   - Is sensitive user information properly sanitized?

3. **Code Review**
   - Is all user input validated and sanitized?
   - Are there any SQL injection or similar vulnerabilities?
   - Are proper error handling practices followed?

4. **Webhooks & API Calls**
   - Are webhook interactions properly secured?
   - Is rate limiting implemented for all API calls?

5. **Deployment**
   - Is the bot running with minimal required permissions?
   - Are logs securely stored and rotated?

## Additional Resources

- [Discord API Security Best Practices](https://discord.com/developers/docs/topics/security)
- [Python Security Best Practices](https://python-security.readthedocs.io/security.html)
- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
