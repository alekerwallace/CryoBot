import discord
from discord.ext import commands

current_count = 0
last_user_id = None

def register_counting_command(client):
    @client.tree.command(name="counting", description="Counting game command")
    async def counting(interaction: discord.Interaction, number: int):
        global current_count, last_user_id

        if number == current_count + 1 and interaction.user.id != last_user_id:
            current_count += 1
            last_user_id = interaction.user.id
            await interaction.response.send_message(f"Count is now {current_count}.")
        else:
            await interaction.response.send_message("Invalid count or same user repeating.")
