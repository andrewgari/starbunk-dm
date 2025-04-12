from discord import Bot
from commands import example_command
from events import on_ready
import config
from database.database import initialize_database # Import the initializer

# Initialize the database
initialize_database()

# Initialize the bot with the specified command prefix
bot = Bot(command_prefix=config.PREFIX)

# Register command
bot.add_command(example_command)

# Register event
@bot.event
async def on_ready():
    await on_ready.on_ready(bot)

# Start the bot with the token from the config
bot.run(config.TOKEN)