import discord
import random
import randfacts

def register_randomfact_command(client):
    @client.tree.command(name="random-fact", description="Get an interesting fact!")
    async def randomfact(interaction: discord.Interaction):
        fun_fact = randfacts.get_fact()

        embed = discord.Embed(
            title="Did you know?",
            description=f"{fun_fact}",
            color=0xfdfdfd
        )

        await interaction.response.send_message(embed=embed)
