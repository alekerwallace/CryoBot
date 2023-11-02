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
        
        await interaction.response.send_message(f"This channel has been designated as the counting channel")

def register_removecounting_command(client):        
    @client.tree.command(name="remove-counting", description="Remove counting game from this channel")
    async def removecounting(interaction: discord.Interaction):
        global counting_channel_id
        if counting_channel_id == interaction.channel_id:
            counting_channel_id = None
            await interaction.response.send_message("Counting game has been removed from this channel")
        else:
            await interaction.response.send_message("Counting game is not active in this channel")
