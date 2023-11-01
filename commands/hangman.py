import discord
import random
from discord.ext import commands

def load_common_words():
    with open('common_words.txt', 'r') as f:
        return [line.strip() for line in f]

common_words = load_common_words()

def get_hangman_word():
    return random.choice(common_words)

# Function for game to select word
#word_list = ['python', 'java', 'javascript', 'discord', 'hangman']
#def get_hangman_word():
#    return random.choice(word_list)

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

emoji_list = list(emoji_to_letter.keys())

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

        def letter_in_word(letter):
            if letter.lower() in word_to_guess.lower():
                return True
            else:
                return False

        attempts_remaining = 6

        # Get the displayed word
        correct_guesses = []
        display_word = get_display_word(word_to_guess, correct_guesses)

        # Print the displayed word to the console
        print(display_word)

        def get_description(message):
            display_word = get_display_word(word_to_guess, correct_guesses)
            return f"**To play**\nReact with the region_indicator letter emoji for the letter you would like to guess. For example, to guess 'a' you would react with 'regional_indicator_a' or :regional_indicator_a:. You can type 'regional' into the emoji search bar to quickly bring up a list of letter emojis.\n\nWord to guess: {display_word}\n\n**{message} Attempts remaining: {attempts_remaining}**"

        # Creating the initial embed with instructions
        embed = discord.Embed(
            title="Hangman",
            description=get_description("New game!"),
            color=0xfdfdfd)

        # Edit the temporary message with the game embed
        await message.edit(content='', embed=embed)  # Update the temporary message with the game embed

        # Now call the hangman_game function, passing the interaction and client objects
#        await hangman_game(interaction, client, message, embed, word_to_guess)

        # Defining the check for reactions
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in emoji_list and reaction.message.id == message.id

        # Checking the emoji 
        while True:
            reaction, user = await client.wait_for('reaction_add', check=check)
            
            def get_letter(emoji):
                return emoji_to_letter.get(emoji, None)

            # Call get_letter with the emoji of the reaction
            letter = get_letter(str(reaction.emoji))
            if letter:
                print(f"The letter for emoji {reaction.emoji} is {letter}")
                if letter_in_word(letter):
                    correct_guesses.append(letter)
                    display_word = get_display_word(word_to_guess, correct_guesses)
                    if '-' in display_word:
                        embed.description=get_description("Correct guess!")
                    else:
                        embed.description=get_description("YOU WIN!")
                        attempts_remaining=0
                else:
                    if attempts_remaining < 0:
                        await message.remove_reaction(reaction, user)
                    else:
                        attempts_remaining -= 1
                    if attempts_remaining < 1:
                        embed.description=get_description(f"You lose.\n\nThe word was {word_to_guess}")
                    else:
                        embed.description=get_description("WRONG!")
                await message.edit(embed=embed)
