import discord
import random

# List of words for Hangman
word_list = ['python', 'java', 'javascript', 'discord', 'hangman']

def get_hangman_word():
    return random.choice(word_list)

def get_display_word(word, guessed_letters):
    display_word = ''
    for letter in word:
        if letter in guessed_letters:
            display_word += letter
        else:
            display_word += '-'
    return display_word

async def hangman_game(ctx):
    word_to_guess = get_hangman_word()
    guessed_letters = []
    attempts_remaining = 6  # Adjust as needed
    while attempts_remaining > 0:
        display_word = get_display_word(word_to_guess, guessed_letters)
        await ctx.send(f'Word: {display_word}  Attempts remaining: {attempts_remaining}')
        guess = await ctx.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        guess_content = guess.content.lower()
        if len(guess_content) == 1:
            guessed_letters.append(guess_content)
            if guess_content not in word_to_guess:
                attempts_remaining -= 1
        elif guess_content == word_to_guess:
            await ctx.send('Congratulations! You guessed the word!')
            return
        else:
            await ctx.send('Invalid guess. Please guess a single letter or the entire word.')
            continue
    await ctx.send(f'Sorry, the word was: {word_to_guess}')

def register_hangman_command(client):
    @client.tree.command()
    async def hangman(ctx):
        await hangman_game(ctx)
