import discord
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import re
import sympy

# For tracking how long the bot has been running for (for leaderboard.py)
start_time = datetime.utcnow()
from datetime import datetime
from commands.data import set_start_time
set_start_time(datetime.utcnow())


# Import the command files
from commands import ping
from commands import limit
from commands import derivative
from commands import eightball
from commands import blackjack
from commands import hangman
#from commands import multiplayer
from commands import leaderboard
from commands import counting
from commands import coinflip
from commands import randomfact
from commands import dadjoke
from commands import hug
from commands import hit
from commands import purge
from commands import annihilate
from commands import warn
from commands import mute
from commands import addwelcome
#from commands import editwelcome
from commands import removewelcome

# Load environment variables from .env file
load_dotenv()

# Replace channel mentions for welcome command
async def replace_channel_mentions(guild, text):
    matches = re.findall(r'\{channel:([^}]+)\}', text)
    for match in matches:
        channel = discord.utils.get(guild.text_channels, name=match)
        if channel:
            text = text.replace(f'{{channel:{match}}}', channel.mention)
        else:
            text = text.replace(f'{{channel:{match}}}', f'`{match}` (channel not found)')
    return text

# Counting
def sympy_eval(expression):
    try:
        # Parse the expression
        expr = sympy.sympify(expression)
        
        # Evaluate the expression
        result = expr.evalf()
        
        # Check if the result is very close to an integer
        if result.is_real and abs(result - round(result)) < 1e-4:
            integer_result = int(round(result))
            
            # Check if the integer result is positive
            if integer_result > 0:
                return integer_result
                
    except (sympy.SympifyError, TypeError) as e:
        print(f"An error occurred: {e}")
    
    print(f"Not a positive integer {result}")    
    return False

# Slash commands
class SlashClient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        intents.members = True
        super().__init__(intents=intents)
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

                # Fishing for laughs
        #        custom_activity = discord.CustomActivity(name="fishing for laughs 🐟")
        #        await client.change_presence(activity=custom_activity)

                # Byte me
        #        custom_activity = discord.CustomActivity(name="byte me")
        #        await client.change_presence(activity=custom_activity)

                # Zero Kelvin cool
        custom_activity = discord.CustomActivity(name="zero Kelvin cool")
        await client.change_presence(activity=custom_activity)

                # Listening to humans 😬
        #       music = discord.Activity(type=discord.ActivityType.listening, name="humans 😬")
        #       await client.change_presence(activity=music)

                # Playing with the API
        #       game = discord.Game("with the API")
        #       await client.change_presence(status=discord.Status.online, activity=game)

        # For triggering the welcome message
    async def on_member_join(self, member):
        if not os.path.exists('welcome_settings.json'):
            return
        
        with open('welcome_settings.json', 'r') as f:
            settings = json.load(f)

        channel = member.guild.get_channel(settings['channel_id'])
        if channel:
            description = settings['description']
            description = description.replace("{", "{{").replace("}", "}}")  # Escape curly braces
            description = description.format(
                member=member.mention,
                user=member.name,
                server=member.guild.name,
                avatar=member.avatar.url
            )
            description = await replace_channel_mentions(member.guild, description)

            embed = discord.Embed(title=settings['title'], description=description)

            # Set the color
            if settings.get('color'):
                try:
                    color_str = settings['color']
                    if not color_str.startswith('#'):
                            color_str = '#' + color_str
                    embed.color = discord.Color(int(color_str[1:], 16))
                except ValueError:
                    print("Invalid color format in welcome settings. Using default color.")
                    embed.color = discord.Color.default()

            if settings.get('footer'):
                footer_text = settings['footer'].replace("{avatar}", member.avatar.url)
                embed.set_footer(text=footer_text)

            embed.set_thumbnail(url=member.avatar.url)

            await channel.send(embed=embed)

    async def on_message(self, message: discord.Message):   
        # Ignore messages sent by the bot itself
        if message.author == self.user:
            return

        # Check if the message is from the target channel
        print(f"in on_message {message.channel.id} ?= {counting.counting_channel_id}")
        if message.channel.id == counting.counting_channel_id:
            print("in counting channel")
            expression = message.content
            value = sympy_eval(expression)
            if value != False:
                print(f"New value is: {value}")
                if counting.last_user_id != message.author.id and value == counting.current_count + 1:
                    counting.current_count = value
                    counting.last_user_id = message.author.id
                    await message.add_reaction("✅")
                else:
                    await message.add_reaction("❌")
                    await message.channel.send("Incorrect. Count has been reset.")
                    counting.current_count = 0
                    counting.last_user_id = None
                    

# Add more conditions and responses as needed

# Create an instance of SlashClient
client = SlashClient()

# Register commands
ping.register_ping_command(client)
limit.register_limit_command(client)
derivative.register_derivative_command(client)
eightball.register_eight_ball_command(client)
blackjack.register_blackjack_command(client)
hangman.register_hangman_command(client)
#multiplayer.register_multiplayer_command(client)
leaderboard.register_leaderboard_command(client)
counting.register_counting_command(client)
coinflip.register_coin_flip_command(client)
randomfact.register_randomfact_command(client)
dadjoke.register_dadjoke_command(client)
hug.register_hug_command(client)
hit.register_hit_command(client)
purge.register_purge_command(client)
annihilate.register_annihilate_command(client)
warn.register_warn_command(client)
mute.register_mute_command(client)
addwelcome.register_addwelcome_command(client)
#editwelcome.register_editwelcome_command(client)
removewelcome.register_removewelcome_command(client)

# Retrieve the DISCORD_TOKEN environment variable
token = os.environ.get('DISCORD_TOKEN')

# Run the client using the retrieved token
client.run(token)
