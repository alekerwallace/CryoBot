import discord
import os
from dotenv import load_dotenv
from datetime import datetime

# For tracking how long the bot has been running for (for leaderboard.py)
start_time = datetime.utcnow()
from datetime import datetime
from commands.data import set_start_time
set_start_time(datetime.utcnow())


# Import the command files
from commands import ping
from commands import limit
from commands import eightball
from commands import blackjack
from commands import hangman
from commands import leaderboard
from commands import counting
from commands import message

# Load environment variables from .env file
load_dotenv()

# Slash commands
class SlashClient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=discord.Object(id=12345678900987654))
        await self.tree.sync()
    
    # Set bot status
    async def on_connect(self):
        print(f'Logged in as {client.user}')
        
        # Error: coffee.exe not found
#        custom_activity = discord.CustomActivity(name="error: coffee.exe not found")
#        await client.change_presence(activity=custom_activity)

        # Listening to humans 😬
        music = discord.Activity(type=discord.ActivityType.listening, name="to humans 😬")
        await client.change_presence(activity=music)

        # Playing with the API
#        game = discord.Game("with the API")
#        await client.change_presence(status=discord.Status.online, activity=game)

# Create an instance of SlashClient
client = SlashClient()

# Register commands
ping.register_ping_command(client)
limit.register_limit_command(client)
eightball.register_eight_ball_command(client)
blackjack.register_blackjack_command(client)
hangman.register_hangman_command(client)
leaderboard.register_leaderboard_command(client)
counting.register_counting_command(client)
message.register_message_command(client)

# Retrieve the DISCORD_TOKEN environment variable
token = os.environ.get('DISCORD_TOKEN')

# Run the client using the retrieved token
client.run(token)
