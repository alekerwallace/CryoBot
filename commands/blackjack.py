import discord
import random
from discord.ext import commands
from commands.data import user_scores

# Function to register the blackjack command
def register_blackjack_command(client):
    # Defining the blackjack command
    @client.tree.command(name="blackjack", description="Play a game of Blackjack.")
    async def blackjack(interaction: discord.Interaction):
        # Defer the response to the interaction
        await interaction.response.defer()
        
        # Send a temporary message to clear the "thinking" status
        message = await interaction.followup.send('Starting game...')

        # Creating and shuffling the deck
        deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'] * 4
        random.shuffle(deck)

        # Function to convert face cards and aces to their numerical values
        def hand_value(hand):
            value = 0
            aces = 0
            for card in hand:
                if card in ['Jack', 'Queen', 'King']:
                    value += 10
                elif card == 'Ace':
                    value += 11
                    aces += 1
                else:
                    value += int(card)
            # Adjust value for aces
            while value > 21 and aces:
                value -= 10
                aces -= 1
            return value

        # Initial hands for player and dealer
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        # Check for Blackjack
        if hand_value(player_hand) == 21:
            embed = discord.Embed(
                title="Blackjack",
                description="**Blackjack, you win!**",
                color=0xd3f5f7
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return  # Exit early as the game is over

        # Creating the initial embed with instructions
        embed = discord.Embed(
            title="Blackjack",
            description=f"Click ✅ to hit or ❌ to stand\n\n"
                        f"Your hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"  # Added \n here
                        f"Dealer's face-up card: {dealer_hand[0]}",
            color=0x00FF00
        )
        # Edit the temporary message with the game embed
        await message.edit(content='', embed=embed)  # Update the temporary message with the game embed
        
        # The following line is removed as it sends the initial game embed again
        # message = await interaction.channel.send(embed=embed)

        await message.add_reaction("✅")  # Reaction for "Hit"
        await message.add_reaction("❌")  # Reaction for "Stand"

        # Defining the check for reactions
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == message.id

        # Loop for handling Hit or Stand reactions
        while True:
            # Check if the player's hand value is 21, if so, break out of the loop
            if hand_value(player_hand) == 21:
                break

            reaction, user = await client.wait_for('reaction_add', check=check)
            await message.remove_reaction(reaction, user)  # Remove the user's reaction
            if str(reaction.emoji) == "✅":
                player_hand.append(deck.pop())
                description = (f"Click ✅ to hit or ❌ to stand\n\n"
                            f"Your hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"
                            f"Dealer's face-up card: {dealer_hand[0]}")
                if hand_value(player_hand) > 21:
                    description = (f"Your hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"
                                   f"Dealer's face-up card: {dealer_hand[0]}\n\n**You busted! Game over.**")  # Updated description
                    embed.description = description
                    await message.edit(embed=embed)
                    await message.clear_reactions()  # Clear reactions here
                    return  # Exit the function if the player busts
                embed.description = description
                await message.edit(embed=embed)
            else:
                break  # Exit the loop if the "Stand" reaction is received

        # Dealer's turn to draw cards
        while hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.pop())

        # Determining the outcome of the game
        player_total = hand_value(player_hand)
        dealer_total = hand_value(dealer_hand)
        outcome = ""
        if dealer_total > 21:
            outcome = "**Dealer bust, you win!**"
        else:
            outcome = "**It's a tie.**" if player_total == dealer_total else "**You win!**" if player_total > dealer_total else "**You lose.**"

        # Update user_scores in the blackjack command
        user_id = str(interaction.user.id)
        if user_id not in user_scores:
            user_scores[user_id] = {'wins': 0, 'losses': 0}
        if outcome == "**You win!**" or outcome == "**Dealer bust, you win!**":
            user_scores[user_id]['wins'] += 1
        elif outcome == "**You lose.**":
            user_scores[user_id]['losses'] += 1

        print(user_scores)  # Debug print here
        
        # Update the game message with the outcome
        description = (f"Your hand: {', '.join(player_hand)}\nTotal: {player_total}\n\n"
                       f"Dealer's hand: {', '.join(dealer_hand)}\nTotal: {dealer_total}\n\n{outcome}")
        embed.description = description  
        await message.edit(embed=embed)  # Updating the embed with the game outcome
        
        # Clear all reactions after the game has concluded
        await message.clear_reactions()

        # The following line is removed as it sends a 'Game over.' message at the end
        # await interaction.channel.send("Game over.")