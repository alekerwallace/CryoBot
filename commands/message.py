import discord
import random
from discord.ext import commands

def register_message_command(client):
    @client.tree.command(name="message", description="...")
    async def message(interaction: discord.Interaction):

        # Defer the response to the interaction
        await interaction.response.defer()

        # Send a temporary message to clear the "thinking" status
        message = await interaction.followup.send('Starting game...')

        guess = await client.wait_for('message', check=lambda m: m.author == interaction.user and m.guild == interaction.guild)
        guess_content = guess.content.lower().strip()
        print(f"Received guess: '{guess_content}', Length: {len(guess_content)}")

    async def on_message(message):
        print(f"Received message: {message.content}")
        