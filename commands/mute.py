import discord
from discord import app_commands
import logging

logging.basicConfig(level=logging.INFO)

def register_mute_command(client):
    @client.tree.command(name="mute", description="Mute a user.")
    @app_commands.describe(user="The user to mute", reason="The reason for the mute")
    @app_commands.default_permissions(manage_roles=True)
    async def _mute(interaction: discord.Interaction, user: discord.Member, reason: str) -> None:
        await interaction.response.defer()  # Defer the response to ensure the bot has enough time to execute the command

        guild = interaction.guild
        if guild is None:
            await interaction.followup.send("This command can only be used in a guild.", ephemeral=True)
            return

        # Check if the Muted role exists
        muted_role = discord.utils.get(guild.roles, name="Muted")
        if muted_role is None:
            # If the Muted role doesn't exist, create it
            muted_role = await guild.create_role(name="Muted")

        # Ensure the Muted role has the correct permissions in all channels
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.Thread):
                overwrites = channel.overwrites_for(muted_role)
                overwrites.send_messages = False
                overwrites.send_messages_in_threads = False
                overwrites.use_external_emojis = False
                overwrites.add_reactions = False
                await channel.set_permissions(muted_role, overwrite=overwrites)

        # Apply the mute role to the user
        await user.add_roles(muted_role)

        # Send the mute reason to the user privately
        try:
            await user.send(f"You have been muted in **{guild.name}** for the following reason: {reason}")
        except discord.Forbidden:
            await interaction.followup.send(f"I couldn't send a private message to {user.mention}, but I will still log the mute in this channel.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(f"Failed to send a mute notification due to an error: {e}", ephemeral=True)
            return

        # Log the mute in the current channel
        embed = discord.Embed(title="User Muted", color=discord.Color.red())
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.set_footer(text=f"Muted by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

        await interaction.followup.send(embed=embed)

