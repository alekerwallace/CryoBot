import discord
import random
from discord.ext import commands
from commands.data import user_scores
from datetime import datetime
from commands.data import user_scores, start_time

# Function to register the leaderboard command
def register_leaderboard_command(client):
    # Defining the leaderboard command
    @client.tree.command(name="leaderboard", description="Show the top 10 blackjack players.")
    async def leaderboard(interaction: discord.Interaction):
        print(user_scores)  # Debug print here
        hours_since_reset = (datetime.utcnow() - start_time).seconds // 3600
        
        # Sort the dictionary based on wins
        sorted_scores = sorted(user_scores.items(), key=lambda x: x[1]['wins'], reverse=True)[:10]

        leaderboard_text = ''  # Define leaderboard_text here before using it
        for i, (user_id, scores) in enumerate(sorted_scores, start=1):
            user = await client.fetch_user(int(user_id))
            leaderboard_text += f"{i}. {user.name}: {scores['wins']} wins, {scores['losses']} losses, {scores['pushes']} pushes\n"
        
        # Now you can prepend the reset information to leaderboard_text
        leaderboard_text = f"Last reset: {hours_since_reset} hours ago\n\n" + leaderboard_text

        embed = discord.Embed(
            title="Blackjack Leaderboard",
            description=leaderboard_text,
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)
