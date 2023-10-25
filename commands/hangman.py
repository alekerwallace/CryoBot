import discord
import random
from discord.ext import commands

# Function for game to select word
word_list = ['python', 'java', 'javascript', 'discord', 'hangman']
def get_hangman_word():
    return random.choice(word_list)

# Mapping emojis to letters
emoji_to_letter = {
    "🇦": "a",
    "🇧": "b",
    "🇨": "c",
    "🇩": "d",
    "🇪": "e",
    "🇫": "f",
    "🇬": "g",
    "🇭": "h",
    "🇮": "i",
    "🇯": "j",
    "🇰": "k",
    "🇱": "l",
    "🇲": "m",
    "🇳": "n",
    "🇴": "o",
    "🇵": "p",
    "🇶": "q",
    "🇷": "r",
    "🇸": "s",
    "🇹": "t",
    "🇺": "u",
    "🇻": "v",
    "🇼": "w",
    "🇽": "x",
    "🇾": "y",
    "🇿": "z"
    }

# Word is displayed with guessed letters        
def get_display_word(word, correct_guesses):
    display_word = ''
    for letter in word:
        if letter in correct_guesses:
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

        # Get the displayed word
        display_word = get_display_word(word_to_guess, [])

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
#        await hangman_game(interaction, client, message, embed, word_to_guess)

        # Defining the check for reactions
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ["🇦", "🇧", "🇨"] and reaction.message.id == message.id

        # Checking the emoji 
        while True:
            reaction, user = await client.wait_for('reaction_add', check=check)
            
            def get_letter(emoji):
                return emoji_to_letter.get(emoji, None)

            # Call get_letter with the emoji of the reaction
            letter = get_letter(str(reaction.emoji))
            if letter:
                print(f"The letter for emoji {reaction.emoji} is {letter}")

            # Main game loop
            async def hangman_game(interaction, client, message, embed, word_to_guess):
                correct_guesses = []
                attempts_remaining = 6  # Adjust as needed
                incorrect_guesses = []  # List to keep track of incorrect guesses
                while attempts_remaining > 0:
                    display_word = get_display_word(word_to_guess, correct_guesses)
                    embed.description = f'Word: {display_word}  Attempts remaining: {attempts_remaining}\nIncorrect guesses: {", ".join(incorrect_guesses)}'
                    await message.edit(embed=embed)  # Edit the embed within the message
                    
                    def check(reaction, user):
                        return (
                            user == interaction.user and
                            reaction.message.id == message.id and
                            str(reaction.emoji) in emoji_to_letter
                        )
                    
                    reaction, user = await client.wait_for('reaction_add', check=check)

                    if guessed_letter in correct_guesses:
                        embed.description = f'You already guessed the letter {guessed_letter}. Try a different letter.'
                        await message.edit(embed=embed)  # Edit the embed within the message
                        continue  # Skip to the next iteration of the loop
                    correct_guesses.append(guessed_letter)
                    if guessed_letter not in word_to_guess:
                        incorrect_guesses.append(guessed_letter)  # Add incorrect guess to the list
                        attempts_remaining -= 1
                        embed.description = f'Incorrect guess. Attempts remaining: {attempts_remaining}\nIncorrect guesses: {", ".join(incorrect_guesses)}'
                        await message.edit(embed=embed)  # Edit the embed within the message

                embed.description = f'Sorry, the word was: {word_to_guess}'
                await message.edit(embed=embed)  # Edit the embed within the message
