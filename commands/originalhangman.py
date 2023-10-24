import discord
import random
from discord.ext import commands

# Function for game to select word
word_list = ['python', 'java', 'javascript', 'discord', 'hangman']
def get_hangman_word():
    return random.choice(word_list)

# Word is displayed with guessed letters        
def get_display_word(word, guessed_letters):
    display_word = ''
    for letter in word:
        if letter in guessed_letters:
            display_word += letter
        else:
            display_word += '-'
    return display_word

# Function to register the hangman command
def register_hangman_command(client):
    @client.tree.command(name="hangman", description="Starts a game of Hangman")
    async def hangman(interaction: discord.Interaction):

        # Defer the response to the interaction
        await interaction.response.defer()

        # Send a temporary message to clear the "thinking" status
        message = await interaction.followup.send('Starting game...')

        # Assuming that the word to guess and the guessed letters are known
        word_to_guess = get_hangman_word()
        guessed_letters = []  # Initially no letters are guessed; update this list as the game progresses

        # Get the displayed word
        display_word = get_display_word(word_to_guess, guessed_letters)

        # Print the displayed word to the console
        print(display_word)

        # Creating the initial embed with instructions
        embed = discord.Embed(
            title="Hangman",
            description=f"Word to guess: {display_word}",
            color=0x00FF00)

        # Edit the temporary message with the game embed
        await message.edit(content='', embed=embed)  # Update the temporary message with the game embed