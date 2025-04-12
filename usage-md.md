# Discord RPG Campaign Bot - Usage Guide

This document outlines how to use the Discord RPG Campaign Bot for managing your tabletop RPG campaigns.

## Getting Started

After inviting the bot to your server and setting it up (see [README.md](README.md)), you're ready to start using the commands.

## Command Reference

### Campaign Management

#### Creating a Campaign
```
/campaign
```
This command:
- Creates a campaign in the current text channel
- Creates "RPG Game Master" and "RPG Player" roles if they don't exist
- Assigns the GM role to the command invoker
- Configures channel permissions to restrict posting to GMs and Players only
- Sets up a webhook for the channel

#### Managing Players
```
/player add @User
```
- Adds the mentioned user to the campaign
- Assigns them the Player role
- Allows them to post in the campaign channel

```
/player remove @User
```
- Removes the mentioned user from the campaign
- Removes their Player role
- Removes any characters they've created in this campaign

### Character Management

#### Creating a Character
```
/character create "Character Name" "avatar_url"
```
- Creates a character for the player
- Each player can have one character per campaign
- GMs can create multiple NPCs

#### Listing Characters
```
/character list
```
- Shows your character in the current campaign (for players)
- Shows all NPCs you've created (for GMs)

#### Deleting a Character
```
/character delete "Character Name"
```
- Deletes the specified character

### Roleplaying Commands

#### Speaking In-Character
```
/ic "Your message"
```
- For players: Speaks as your character
- For GMs: Requires specifying an NPC name first (`/ic "NPC Name" "Message"`)

#### Character Actions/Emotes
```
/em "Your action"
```
- For players: Displays an action for your character (e.g., *Character Name raises their sword*)
- For GMs: Requires specifying an NPC name first (`/em "NPC Name" "Action"`)

### Dice Rolling

#### Standard Rolls
```
/roll 2d6+3
```
- Rolls dice using standard notation
- Results are visible to everyone via webhook
- Supports various dice types (d4, d6, d8, d10, d12, d20, etc.)
- Supports modifiers (e.g., +3, -1)

#### GM Rolls
```
/gmroll 2d6+3
```
- Same as /roll but results are only visible to the GM
- Useful for secret checks and behind-the-screen rolls

### GM Tools

#### Requesting Checks
```
/check @Player perception DC:15
```
- Requests a specific check from a player
- Automatically prompts the player to roll
- Results are posted publicly when the player responds

#### Requesting Saves
```
/save @Player dexterity DC:15
```
- Requests a saving throw from a player
- Works similarly to /check command

## Examples

### Setting Up a New Campaign

1. Create a new text channel in your Discord server (e.g., #my-campaign)
2. In that channel, use `/campaign`
3. Add your players with `/player add @PlayerName`
4. Have players create their characters with `/character create`

### Running a Game Session

GM: "As you enter the cave, it's pitch black inside."
Player: `/ic "I'll light my torch to see what's inside."`
GM: `/gmroll 1d20+2` (Secret perception check for hidden enemies)
GM: "As the torch illuminates the cave, you see glittering gems embedded in the walls."
Player: `/roll 1d20+4` (Investigation check)
GM: "You estimate the gems could be worth hundreds of gold pieces."
Player: `/em "carefully extracts a gem using their dagger"`

## Troubleshooting

- **Command Not Working**: Ensure the bot has proper permissions in your server
- **Can't Create Character**: Make sure you're in a campaign channel and are a player in that campaign
- **Webhook Messages Not Appearing**: The bot may have lost connection to the webhook. Try recreating the campaign

For more help, join our support server or open an issue on GitHub.
