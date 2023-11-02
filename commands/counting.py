import discord
from discord.ext import commands
import sympy

current_count = 0
last_user_id = None
counting_channel_id = None


def register_counting_command(client):
    @client.tree.command(name="counting", description="Counting game command")
    async def counting(interaction: discord.Interaction):
        global current_count, counting_channel_id
        current_count = 0
        counting_channel_id = interaction.channel_id
        
        await interaction.response.send_message(f"This channel ({counting_channel_id}) has been designated as the counting channel")
        