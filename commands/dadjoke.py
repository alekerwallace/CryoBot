import discord
import dadjokes
import random

def register_dadjoke_command(client):
    @client.tree.command(name="dad-joke", description="Get a dad joke.")
    async def dadjoke(interaction: discord.Interaction):
        dad_joke = dadjokes.Dadjoke()

        embed = discord.Embed(
            title="Dad joke incoming...",
            description=f"{dad_joke.joke}",
            color=0xfdfdfd
        )

        await interaction.response.send_message(embed=embed)
