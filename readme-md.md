# Discord RPG Campaign Bot

A Discord bot for managing tabletop RPG campaigns, character creation, and dice rolling - all within Discord text channels.

## Features

- **Campaign Management**: Create dedicated campaign channels with role-based access control
- **Character System**: Players can create and manage their characters
- **In-Character Messaging**: Speak as your character with custom avatars via webhooks
- **Emotes/Descriptions**: Perform actions as your character
- **Dice Rolling**: Robust dice rolling system with public and private roll options
- **GM Tools**: Request checks and saves from players

## Installation

### Prerequisites

- Python 3.8 or higher
- A Discord Bot Token

### Setup

1. Clone this repository
```bash
git clone https://github.com/yourusername/discord-rpg-bot.git
cd discord-rpg-bot
```

2. Create a virtual environment and activate it
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```
DISCORD_TOKEN=your_discord_bot_token
```

5. Run the bot
```bash
python bot.py
```

## Security Notice

This bot requires the following permissions:
- Manage Roles
- Manage Channels
- Manage Webhooks
- Read/Send Messages
- Use Slash Commands

Always be careful when adding bots to your Discord server and review their permissions.

## Usage

See [USAGE.md](USAGE.md) for detailed usage instructions.

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for information on the project structure and how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
