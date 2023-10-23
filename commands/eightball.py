import random
import discord

def register_eight_ball_command(client):
    @client.tree.command(name="8ball", description="Responds with a magic 8 ball answer.")
    async def _eight_ball(interaction: discord.Interaction):
        eight_ball_quotes = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt"
            "Yes definitely"
            "You may rely on it"
            "As I see it, yet"
            "Most likely"
            "Outlook good"
            "Yes"
            "Signs point to yes"
            "Reply hazy, try again"
            "Ask again later"
            "Better not tell you now"
            "Cannot predict now"
            "Concentrate and ask again"
            "Don't count on it"
            "My reply is no"
            "My sources say no"
            "Outlook not so good"
            "Very doubtful"
        ]
        response = random.choice(eight_ball_quotes)
        await interaction.response.send_message(response)
