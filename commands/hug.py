import discord
import aiohttp
import random

apikey = "AIzaSyB7MCYU7E5gP7zeczcYLOFRHTtI22W0p8k"
lmt = 8
ckey = "CryoBot"

def register_hug_command(client):
    @client.tree.command(name="hug", description="Hug someone on the server!")
    @discord.app_commands.describe(user="The username of the person you want to hug.")
    async def hug(interaction: discord.Interaction, user: discord.Member) -> None:
        async def get_random_hug_gif():
            search_term = 'hug'
            async with aiohttp.ClientSession() as session:
                response = await session.get(f"https://tenor.googleapis.com/v2/search?q={search_term}&key={apikey}&client_key={ckey}&limit={lmt}&media_filter=minimal")
                if response.status != 200:
                    print(f'Failed to retrieve gifs: {await response.text()}')
                    return None
                json_response = await response.json()
                print(json_response)  # Print the JSON response

                if 'results' not in json_response or not json_response['results']:
                    print('No results found')
                    return None

                try:
                    gif_choice = random.choice(json_response['results'])
                    gif_url = gif_choice['media_formats']['tinygif']['url']
                    return gif_url
                except (KeyError, IndexError) as e:
                    print(f'Error extracting gif URL: {str(e)}')
                    return None

        gif_url = await get_random_hug_gif()
        if gif_url:
            embed = discord.Embed(
                title="awww",
                description=f"{user.mention} {interaction.user.display_name} is sending you hugs <333", 
                color=0xfdfdfd
                )
            embed.set_image(url=gif_url)
            await interaction.response.send_message(embed=embed)

        else:
            await interaction.response.send_message("Sorry, I couldn't find a hug GIF right now. Please try again later.", ephemeral=True)

