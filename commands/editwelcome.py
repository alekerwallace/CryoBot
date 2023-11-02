import discord
from discord import app_commands
import json
import os

def register_editwelcome_command(client):
    @client.tree.command(name="edit-welcome", description="Edit the welcome message.")
    @app_commands.describe(
        channel="The channel to send the welcome message to",
        title="The title of the welcome embed",
        description="The description of the welcome embed"
    )
    async def _editwelcome(interaction: discord.Interaction, channel: discord.TextChannel, title: str, description: str) -> None:
        if not os.path.exists('welcome_settings.json'):
            await interaction.response.send_message("Welcome message is not set up yet. Use /add-welcome to set it up first.")
            return
        
        with open('welcome_settings.json', 'r') as f:
            settings = json.load(f)
        
        settings['channel_id'] = channel.id
        settings['title'] = title
        settings['description'] = description
        
        with open('welcome_settings.json', 'w') as f:
            json.dump(settings, f)
        
        await interaction.response.send_message("Welcome message updated successfully.")
