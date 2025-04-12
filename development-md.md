# Discord RPG Campaign Bot - Development Guide

This document provides details about the project structure, architecture, and development guidelines for contributors.

## Project Structure

```
discord-rpg-bot/
├── bot.py                  # Main entry point
├── config.py               # Configuration and environment variables
├── requirements.txt        # Dependencies
├── .env                    # Environment variables (gitignored)
├── .env.example            # Example environment file
├── .gitignore              # Git ignore file
├── data/                   # Data storage directory
│   ├── campaigns.json      # Campaign data storage
│   ├── characters.json     # Character data storage
│   └── backups/            # Automatic backups
├── docs/                   # Documentation
│   ├── README.md           # Main readme
│   ├── USAGE.md            # Usage guide
│   └── DEVELOPMENT.md      # This file
└── src/                    # Source code
    ├── __init__.py
    ├── bot.py              # Bot class definition
    ├── campaign_manager.py # Campaign management
    ├── character_manager.py # Character management
    ├── dice_roller.py      # Dice rolling functionality
    ├── webhook_manager.py  # Webhook management system
    ├── commands/           # Command modules
    │   ├── __init__.py
    │   ├── campaign_commands.py
    │   ├── character_commands.py
    │   ├── dice_commands.py
    │   └── gm_commands.py
    └── utils/              # Utility functions
        ├── __init__.py
        ├── data_manager.py # Data persistence
        └── validators.py   # Input validation
```

## Architecture

The bot follows an Object-Oriented Programming (OOP) approach with clean separation of concerns:

### Core Components

1. **RPGCampaignBot**: Main bot class that initializes systems and handles events.
2. **CampaignManager**: Manages campaign creation, role assignment, and player management.
3. **CharacterManager**: Handles character creation, listing, and deletion.
4. **WebhookManager**: Creates and manages webhooks for character messages and dice rolls.
5. **DiceRoller**: Parses and executes dice rolls with various notation support.

### Data Flow

```
User Input (Slash Command) → Command Handler → Manager Class → Data Update → Persistence Layer
```

### Persistence Model

The bot uses JSON files for data storage:

#### Campaign Data Structure
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

#### Character Data Structure
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

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use type hints wherever possible
- Document all classes and methods with docstrings
- Keep methods short and focused (Single Responsibility Principle)

### Testing

- Write unit tests for all new functionality
- Run tests before submitting pull requests
- Aim for at least 80% test coverage

### Security Practices

1. **Token Management**
   - Always use environment variables for tokens and sensitive data
   - Never commit tokens or sensitive data to the repository

2. **Input Validation**
   - Validate all user input before processing
   - Sanitize inputs to prevent injection attacks

3. **Error Handling**
   - Catch and handle exceptions appropriately
   - Log errors without exposing sensitive information

### Webhook Management

The `WebhookManager` class is a central component that follows these principles:

1. **Reusability**: Create and manage webhooks in a centralized way
2. **Persistence**: Store webhook IDs in the campaign data for reuse
3. **Error Recovery**: Handle webhook deletion and recreation automatically
4. **Functionality Separation**: Provide clean interfaces for different message types

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests
5. Submit a pull request

## Design Principles

The project follows these core principles:

1. **SOLID**: Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion
2. **DRY**: Don't Repeat Yourself
3. **KISS**: Keep It Simple, Stupid
4. **Testability**: Code should be easy to test
5. **Scalability**: Design should accommodate future growth

## Adding New Features

When adding new features:

1. First add to the appropriate manager class
2. Create command handlers in the commands directory
3. Update persistence models as needed
4. Add tests for your new functionality
5. Update documentation to include your feature
