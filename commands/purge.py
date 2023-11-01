import discord

def register_purge_command(client):
    @client.tree.command(name='purge', description='Delete messages in the current channel')
    @discord.app_commands.guild_only()
    @discord.app_commands.default_permissions(manage_messages=True)
    @discord.app_commands.describe(number_of_messages="The number of messages to delete.")
    async def _purge(interaction: discord.Interaction, number_of_messages: int = None) -> None:
        await interaction.response.defer(ephemeral=True)  # Deferring the response

        channel = interaction.channel
        if isinstance(channel, discord.TextChannel):
            try:
                limit = None if number_of_messages is None else number_of_messages
                
                deleted = await channel.purge(limit=limit)
                await interaction.followup.send(f'Deleted {len(deleted)} message(s).', ephemeral=True)

            except discord.Forbidden:
                await interaction.followup.send("I do not have the permissions to delete messages in this channel.", ephemeral=True)
            except discord.HTTPException as e:
                await interaction.followup.send(f"Failed to delete messages due to an error: {e}", ephemeral=True)
        else:
            await interaction.followup.send("This command can only be used in text channels.", ephemeral=True)
