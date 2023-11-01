import discord
import random
from discord.ext import commands
from discord.ui import View, Button

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

class HangmanView(View):
    def __init__(self, word_to_guess, embed, interaction):
        super().__init__()
        self.word_to_guess = word_to_guess
        self.attempts_remaining = 6
        self.correct_guesses = []
        self.incorrect_guesses = []
        self.display_word = '-' * len(word_to_guess)
        self.embed = embed
        self.interaction = interaction

        # Example grouping: vowels and consonants
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"

        self.add_item(HangmanButton(letters=vowels, label="Vowels", view=self))
        self.add_item(HangmanButton(letters=consonants, label="Consonants", view=self))

        for emoji, letter in emoji_to_letter.items():
            self.add_item(HangmanButton(letter=letter, emoji=emoji, view=self))

    async def disable_buttons(self):
        for item in self.children:
            item.disabled = True
        await self.interaction.edit_original_message(view=self)

    async def update_embed(self, status_message):
        self.display_word = get_display_word(self.word_to_guess, self.correct_guesses)
        self.embed.description = (f"**{status_message}**\n\n"
                                  f"Word to guess: {self.display_word}\n\n"
                                  f"Attempts remaining: {self.attempts_remaining}\n\n"
                                  f"Guessed Letters: {', '.join(self.incorrect_guesses) if self.incorrect_guesses else 'None'}")
        await self.interaction.edit_original_message(embed=self.embed)

class HangmanButton(Button):
    def __init__(self, letter, emoji, view):
        super().__init__(label=letter.upper(), style=discord.ButtonStyle.primary, emoji=emoji, custom_id=letter)
        self.letter = letter

    async def callback(self, interaction):
        view = self.view
        if self.letter in view.correct_guesses or self.letter in view.incorrect_guesses:
            return

        if self.letter in view.word_to_guess:
            view.correct_guesses.append(self.letter)
            if '-' not in view.display_word:
                await view.update_embed("Congratulations, YOU WIN!")
                await view.disable_buttons()
            else:
                await view.update_embed("Correct guess!")
        else:
            view.incorrect_guesses.append(self.letter)
            view.attempts_remaining -= 1
            if view.attempts_remaining <= 0:
                view.embed.description = f"You lose. The word was {view.word_to_guess}"
                await view.disable_buttons()
                await interaction.edit_original_message(embed=view.embed, view=view)
            else:
                await view.update_embed("Wrong guess!")
        self.disabled = True
        await interaction.edit_original_message(view=view)

def register_multiplayer_command(client):
    @client.tree.command(name="multiplayer", description="Starts a game of Hangman")
    async def multiplayer(interaction: discord.Interaction):
        await interaction.response.defer()
        word_to_guess = get_hangman_word().lower()
        embed = discord.Embed(title="Hangman", color=0xfdfdfd)
        view = HangmanView(word_to_guess, embed, interaction)
        await view.update_embed("New game!")
        await interaction.followup.send(embed=embed, view=view)

