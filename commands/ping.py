import discord

def register_ping_command(client):
    @client.tree.command(name="ping", description="Bot will respond with 'pong' if online.")
    async def _ping(interaction: discord.Interaction) -> None:
        await interaction.response.send_message("pong")
