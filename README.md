# Discord Bot

A basic Discord bot built with discord.py.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a Discord application and bot:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to the "Bot" section and create a new bot
   - Copy the bot token

3. Configure the bot:
   - Copy your bot token
   - Open the `.env` file
   - Replace `your_bot_token_here` with your actual bot token

4. Invite the bot to your server:
   - Go to the "OAuth2" section in the Developer Portal
   - Select "bot" under "Scopes"
   - Select the required permissions (at minimum: "Send Messages", "Read Message History")
   - Copy the generated URL and open it in your browser
   - Select a server to invite the bot to

## Running the Bot

To start the bot, run:
```bash
python bot.py
```

## Basic Commands

- `!ping` - Check the bot's latency

## Features

- Basic command handling
- Server connection logging
- Latency checking
