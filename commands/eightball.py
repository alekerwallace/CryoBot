import random
import discord

def register_eight_ball_command(client):
    @client.tree.command(name="8-ball", description="Responds with a magic 8 ball answer.")
    async def _eight_ball(interaction: discord.Interaction):
        eight_ball_quotes = [
            "it is certain",
            "it is decidedly so",
            "without a doubt"
            "yes definitely"
            "you may rely on it"
            "as I see it, yet"
            "most likely"
            "outlook good"
            "yes"
            "signs point to yes"
            "reply hazy, try again"
            "ask again later"
            "better not tell you now"
            "cannot predict now"
            "concentrate and ask again"
            "don't count on it"
            "my reply is no"
            "my sources say no"
            "outlook not so good"
            "very doubtful"
        ]
        response = random.choice(eight_ball_quotes)
        await interaction.response.send_message(f"The answer to your question is: {response}")