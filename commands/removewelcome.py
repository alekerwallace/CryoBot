import discord
import json
import os

def register_removewelcome_command(client):
    @client.tree.command(name="remove-welcome", description="Remove the welcome message.")
    async def _removewelcome(interaction: discord.Interaction) -> None:
        if os.path.exists('welcome_settings.json'):
            os.remove('welcome_settings.json')
            await interaction.response.send_message("Welcome message removed successfully.")
        else:
            await interaction.response.send_message("There is no welcome message set up.")
