import discord
import random

def register_coin_flip_command(client):
    @client.tree.command(name="coin-flip", description="Bot will respond with heads or tails.")
    async def coin_flip(interaction: discord.Interaction):
        coin_flip_results = [
            "heads",
            "tails"
        ]
        response = random.choice(coin_flip_results)
        await interaction.response.send_message(f"Your result is: {response}!")