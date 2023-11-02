import discord
from discord import app_commands
import json
import os

def register_addwelcome_command(client):
    @client.tree.command(name="welcome", description="Set up a welcome message.")
    @app_commands.describe(
        channel="The channel to send the welcome message to", 
        title="Title of the embed", 
        description="Description of the embed", 
        color="Color of the embed", 
        footer="Footer text of the embed",
        show_avatar_thumbnail="Show the user's avatar as a thumbnail in the welcome message"
    )
    async def addwelcome(
        interaction: discord.Interaction, 
        channel: discord.TextChannel, 
        title: str, 
        description: str, 
        color: str = None, 
        footer: str = None,
        show_avatar_thumbnail: bool = False
    ):
        settings = {
            'channel_id': channel.id,
            'title': title,
            'description': description,
            'color': color,
            'footer': footer,
            'show_avatar_thumbnail': show_avatar_thumbnail
        }
        with open('welcome_settings.json', 'w') as f:
            json.dump(settings, f)
        await interaction.response.send_message(f"Welcome message set up successfully in {channel.mention}")

def register_removewelcome_command(client):
    @client.tree.command(name="remove-welcome", description="Remove the welcome message.")
    async def _removewelcome(interaction: discord.Interaction) -> None:
        if os.path.exists('welcome_settings.json'):
            os.remove('welcome_settings.json')
            await interaction.response.send_message("Welcome message removed successfully.")
        else:
            await interaction.response.send_message("There is no welcome message set up.")
