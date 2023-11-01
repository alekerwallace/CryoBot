import discord
from datetime import timezone


def register_annihilate_command(client):
    @client.tree.command(name='annihilate', description='Duplicating the channel, re-pinning messages, and deleting the original.')
    @discord.app_commands.guild_only()
    @discord.app_commands.default_permissions(manage_channels=True)
    async def _annihilate(interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        
        original_channel = interaction.channel
        if not isinstance(original_channel, discord.TextChannel):
            await interaction.followup.send("This command can only be used in text channels.", ephemeral=True)
            return

        guild = interaction.guild
        if guild is None:
            await interaction.followup.send("This command can only be used in a guild.", ephemeral=True)
            return
        
        # Step 1: Duplicate the channel
        new_channel = await guild.create_text_channel(
            name=original_channel.name,
            category=original_channel.category,
            position=original_channel.position,
            topic=original_channel.topic,
            slowmode_delay=original_channel.slowmode_delay,
            nsfw=original_channel.nsfw,
            overwrites=original_channel.overwrites
        )

        # Step 2: Copy pinned messages
        pinned_messages = await original_channel.pins()
        for message in pinned_messages:
            # Format the time
            formatted_time = message.created_at.astimezone(timezone.utc).strftime('%B %d, %Y at %H:%M %Z')
            
            # Copy text content
            if message.content:
                embed = discord.Embed(
                    title=f"{message.author.name} sent on {formatted_time}",
                    description=message.content,
                    color=0x3498db  # You can change this to your preferred color
                )
                embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
                new_message = await new_channel.send(embed=embed)
                await new_message.pin()
            
            # Copy embeds
            for embed in message.embeds:
                # You need to create a new Embed and copy over the fields
                new_embed = discord.Embed(
                    title=embed.title,
                    description=embed.description,
                    color=embed.color
                )
                for field in embed.fields:
                    new_embed.add_field(name=field.name, value=field.value, inline=field.inline)
                
                new_embed.set_author(name=embed.author.name, icon_url=embed.author.icon_url)
                new_embed.set_footer(text=embed.footer.text, icon_url=embed.footer.icon_url)
                new_embed.set_thumbnail(url=embed.thumbnail.url)
                new_embed.set_image(url=embed.image.url)
                
                new_message = await new_channel.send(embed=new_embed)
                await new_message.pin()


        # Step 3: Delete the original channel
        await original_channel.delete(reason="Annihilated by command")
        
        await new_channel.send(f"Channel {original_channel.name} has been annihilated and replaced with {new_channel.mention}.")
