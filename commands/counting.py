import discord
from discord.ext import commands

current_count = 0
last_user_id = None

def register_counting_command(client):
    @client.tree.command(name="set-up-counting", description="Counting game command")
    async def counting(interaction: discord.Interaction):
        global current_count, last_user_id

        # Parse the message to get the number
        try:
            user_number = int(interaction.message.content)
        except ValueError:
            await interaction.response.send_message("Please enter a valid number.")
            return

        # Check if the number is the next in the sequence and the user is not the same as the last user
        if user_number == current_count + 1 and interaction.user.id != last_user_id:
            current_count += 1
            last_user_id = interaction.user.id
            await interaction.response.send_message(f"Count is now {current_count}.")
        else:
            await interaction.response.send_message("Invalid count or same user repeating.")
