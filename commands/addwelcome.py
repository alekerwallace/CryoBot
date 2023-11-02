import discord
from discord import app_commands
import json

def register_addwelcome_command(client):
    @client.tree.command(name="welcome", description="Set up a welcome message.")
    @app_commands.describe(channel="The channel to send the welcome message to", title="Title of the embed", description="Description of the embed", color="Color of the embed", footer="Footer text of the embed")
    async def addwelcome(interaction: discord.Interaction, channel: discord.TextChannel, title: str, description: str, color: str = None, footer: str = None):
        settings = {
            'channel_id': channel.id,
            'title': title,
            'description': description,
            'color': color,
            'footer': footer
        }
        with open('welcome_settings.json', 'w') as f:
            json.dump(settings, f)
        await interaction.response.send_message(f"Welcome message set up successfully in {channel.mention}")
