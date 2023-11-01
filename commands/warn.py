import discord

def register_warn_command(client):
    @client.tree.command(name="warn", description="Warn a user.")
    @discord.app_commands.describe(user="The user to warn", reason="The reason for the warning")
    @discord.app_commands.default_permissions(manage_roles=True)
    async def _warn(interaction: discord.Interaction, user: discord.Member, reason: str) -> None:
        # Send the warning to the user privately
        try:
            await user.send(f"You have been warned for the following reason: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message(f"I couldn't send a private message to {user.mention}, but I will still log the warning in this channel.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Failed to send a warning due to an error: {e}", ephemeral=True)
            return

        # Log the warning in the current channel
        embed = discord.Embed(title="User Warned", color=discord.Color.red())
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.set_footer(text=f"Warned by {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)
