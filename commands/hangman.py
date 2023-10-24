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

        # Now call the hangman_game function, passing the interaction and client objects
        await hangman_game(interaction, client)

        async def hangman_game(interaction, client):
            word_to_guess = get_hangman_word()
            guessed_letters = []
            attempts_remaining = 6  # Adjust as needed
            incorrect_guesses = []  # List to keep track of incorrect guesses
            while attempts_remaining > 0:
                display_word = get_display_word(word_to_guess, guessed_letters)
                await interaction.response.send_message(f'Word: {display_word}  Attempts remaining: {attempts_remaining}\nIncorrect guesses: {", ".join(incorrect_guesses)}')
                guess = await client.wait_for('message', check=lambda m: m.author == interaction.user and m.guild == interaction.guild)
                guess_content = guess.content.lower()
                if len(guess_content) == 1:
                    if guess_content in guessed_letters:
                        await interaction.followup.send(f'You already guessed the letter {guess_content}. Try a different letter.')
                        continue  # Skip to the next iteration of the loop
                    guessed_letters.append(guess_content)
                    if guess_content not in word_to_guess:
                        incorrect_guesses.append(guess_content)  # Add incorrect guess to the list
                        attempts_remaining -= 1
                elif guess_content == word_to_guess:
                    await interaction.followup.send('Congratulations! You guessed the word!')
                    return
                else:
                    await interaction.followup.send('Invalid guess. Please guess a single letter or the entire word.')
                    continue
            await interaction.followup.send(f'Sorry, the word was: {word_to_guess}')

