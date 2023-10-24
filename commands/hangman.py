import discord  # Import the discord.py library
import random  # Import the random library for random number generation

# List of words for Hangman
word_list = ['python', 'java', 'javascript', 'discord', 'hangman']

def get_hangman_word():
    # Function to get a random word from the word list
    return random.choice(word_list)  # Return a random choice from the word list

def get_display_word(word, guessed_letters):
    # Function to get the word to display with guessed letters revealed and unguessed letters as dashes
    display_word = ''  # Initialize an empty string for the display word
    for letter in word:  # Loop through each letter in the word
        if letter in guessed_letters:  # If the letter has been guessed
            display_word += letter  # Add the letter to the display word
        else:
            display_word += '-'  # Otherwise, add a dash to the display word
    return display_word  # Return the display word

async def hangman_game(interaction, client):
    word_to_guess = get_hangman_word()
    guessed_letters = []
    attempts_remaining = 6  # Adjust as needed
    while attempts_remaining > 0:
        display_word = get_display_word(word_to_guess, guessed_letters)
        await interaction.response.send_message(f'Word: {display_word}  Attempts remaining: {attempts_remaining}')
        guess = await client.wait_for('message', check=lambda m: m.author == interaction.user and m.guild == interaction.guild)
        guess_content = guess.content.lower()
        if len(guess_content) == 1:
            guessed_letters.append(guess_content)
            if guess_content not in word_to_guess:
                attempts_remaining -= 1
        elif guess_content == word_to_guess:
            await interaction.followup.send('Congratulations! You guessed the word!')
            return
        else:
            await interaction.followup.send('Invalid guess. Please guess a single letter or the entire word.')
            continue
    await interaction.followup.send(f'Sorry, the word was: {word_to_guess}')

def register_hangman_command(client):
    @client.tree.command()
    async def hangman(interaction):
        await hangman_game(interaction, client)
