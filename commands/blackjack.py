import discord
import random
import asyncio
from discord.ext import commands
from commands.data import user_scores  # Importing user scores from a data module

# Function to calculate the value of a hand
def hand_value(hand):
    value = 0  # Initialize total value
    aces = 0  # Track the number of aces
    for card in hand:  # Loop through each card in the hand
        if card in ['Jack', 'Queen', 'King']:
            value += 10  # Face cards are worth 10
        elif card == 'Ace':
            value += 11  # Ace initially counts as 11
            aces += 1  # Increment ace count
        else:
            value += int(card)  # Numeric cards are worth their face value
    while value > 21 and aces:  # Adjust value for aces if total value is over 21
        value -= 10
        aces -= 1
    return value  # Return the final hand value

# Function to create a Discord embed
def build_embed(title, description, color=0x6d6482):
    return discord.Embed(title=title, description=description, color=color)

# Function to register the blackjack command with the client
def register_blackjack_command(client):

    @client.tree.command(name="blackjack", description="Play a game of Blackjack.")
    async def blackjack(interaction: discord.Interaction):
        await interaction.response.defer()  # Defer the response to the interaction
        message = await interaction.followup.send('Starting game...')  # Send a follow-up message to indicate the game is starting

        # Initialize and shuffle the deck
        deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'] * 4
        random.shuffle(deck)

        # Draw initial hands for player and dealer
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        # Check if the player can split their hand
        can_split = player_hand[0] == player_hand[1]

        # Build the game message description
        description = (
            f"Click ✅ to hit or ❌ to stand\n\n"
            f"Your hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"
            f"Dealer's face-up card: {dealer_hand[0]}"
        )
        embed = build_embed("Blackjack", description)
        await message.edit(content='', embed=embed)  # Update the game message with the embed

        # Add reactions for player actions
        await message.add_reaction("✅")  # Reaction for "Hit"
        await message.add_reaction("❌")  # Reaction for "Stand"
        if can_split:
            await message.add_reaction("🪚")  # Reaction for "Split" if applicable

        # Define a check function for reaction events
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ["✅", "❌", "🪚"] and reaction.message.id == message.id

        # Define an asynchronous function to handle player actions for a hand
        async def handle_hand(hand, message, dealer_hand, title):
            while hand_value(hand) < 21:
                reaction, user = await client.wait_for('reaction_add', check=check)  # pass check directly
                await message.remove_reaction(reaction, user)  # Remove the user's reaction
                
                if str(reaction.emoji) == "✅":  # Player chose to hit
                    hand.append(deck.pop())  # Draw a card from the deck
                    description = (
                        f"Click ✅ to hit or ❌ to stand\n\n"
                        f"Your hand: {', '.join(hand)}\nTotal: {hand_value(hand)}\n\n"
                        f"Dealer's face-up card: {dealer_hand[0]}"
                    )
                    if hand_value(hand) > 21:  # Check for bust
                        description += f"\n\n**You busted! Game over.**"
                        embed = discord.Embed(
                            title=title,
                            description=description,
                            color=0x6d6482
                        )
                        await message.edit(embed=embed)
                        await message.clear_reactions()  # Clear reactions if busted
                        return  # Return if the player busts
                    else:
                        embed = discord.Embed(
                            title=title,
                            description=description,
                            color=0x6d6482
                        )
                        await message.edit(embed=embed)  # Update the game message
                elif str(reaction.emoji) == "❌":  # Player chose to stand
                    description = (
                        f"You chose to stand.\n\n"
                        f"Your hand: {', '.join(hand)}\nTotal: {hand_value(hand)}\n\n"
                        f"Dealer's face-up card: {dealer_hand[0]}"
                    )
                    embed = discord.Embed(
                        title=title,
                        description=description,
                        color=0x6d6482
                    )
                    await message.edit(embed=embed)  # Update the game message to reflect stand choice
                    return  # Return if the player stands
        
        # Main gameplay loop
        while True:
            reaction, user = await client.wait_for('reaction_add', check=check)

            # Player chose to split
            if str(reaction.emoji) == "🪚":  

                # Splitting the player's hand into two new hands
                hand1 = [player_hand.pop(), deck.pop()]
                hand2 = [player_hand.pop(), deck.pop()]
                
                # Creating and sending messages for each new hand
                embed1 = discord.Embed(
                    title="Blackjack - Hand 1",
                    description=f"Click ✅ to hit or ❌ to stand\n\n"
                                f"Your hand: {', '.join(hand1)}\nTotal: {hand_value(hand1)}",
                    color=0x6d6482
                )
                message1 = await interaction.followup.send(embed=embed1)
                await message1.add_reaction("✅")  # Reaction for "Hit"
                await message1.add_reaction("❌")  # Reaction for "Stand"

                embed2 = discord.Embed(
                    title="Blackjack - Hand 2",
                    description=f"Click ✅ to hit or ❌ to stand\n\n"
                                f"Your hand: {', '.join(hand2)}\nTotal: {hand_value(hand2)}",
                    color=0x6d6482
                )
                message2 = await interaction.followup.send(embed=embed2)
                await message2.add_reaction("✅")  # Reaction for "Hit"
                await message2.add_reaction("❌")  # Reaction for "Stand"
                
                # Defining check functions for each new hand
                def check(message):
                    def _check(reaction, user):
                        return (
                            user == interaction.user and 
                            str(reaction.emoji) in ["✅", "❌"] and 
                            reaction.message.id == message.id
                        )
                    return _check

                # Handling each new hand individually
                task1 = asyncio.create_task(handle_hand(hand1, message1, dealer_hand, "Blackjack - Hand 1")) # Pass title here
                task2 = asyncio.create_task(handle_hand(hand2, message2, dealer_hand, "Blackjack - Hand 2")) # And here
                
                # Wait for both tasks to complete
                await asyncio.gather(task1, task2)
                
                await message.remove_reaction(reaction, user)  # Remove the reaction after processing
                break  # Exit the loop after handling both hands

            # Player chose to hit or stand
            elif str(reaction.emoji) in ["✅", "❌"]:  
                await message.remove_reaction(reaction, user)  # Remove the reaction after processing
                if str(reaction.emoji) == "✅":  # Player chose to hit
                    player_hand.append(deck.pop())  # Draw a card from the deck
                    description = (
                        f"Click ✅ to hit or ❌ to stand\n\n"
                        f"Your hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"
                        f"Dealer's face-up card: {dealer_hand[0]}"
                    )
                    if hand_value(player_hand) > 21:  # Check for bust
                        description += (
                            f"\n\n**You busted! Game over.**"
                        )
                        embed.description = description
                        await message.edit(embed=embed)
                        await message.clear_reactions()  # Clear reactions if busted
                        return  # Exit the function if player busts
                    embed.description = description
                    await message.edit(embed=embed)  # Update the game message
                else:  # Player chose to stand
                    break  # Exit the loop if the "Stand" reaction is received
            else:
                await message.remove_reaction(reaction, user)  # Remove the reaction if it's not one of the expected emojis
                pass  # Placeholder for handling other reactions if necessary

            # Determine the title for standard game scenario
            if message.embeds:
                title = message.embeds[0].title
            else:
                title = "Blackjack"  # Default title if no embeds are found

            # Call handle_hand with the determined title
            await handle_hand(player_hand, message, dealer_hand, title)  # Pass title here

        # Dealer's turn to draw cards
        while hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.pop())  # Dealer draws until hand value is 17 or higher

        if hand_value(player_hand) > 21:  # Check for bust
            outcome = "You busted! Game over."
        else:
            dealer_total = hand_value(dealer_hand)
            player_total = hand_value(player_hand)
            if dealer_total > 21:
                outcome = "Dealer bust, you win!"
            elif player_total > dealer_total:
                outcome = "You win!"
            elif player_total < dealer_total:
                outcome = "You lose."
            else:
                outcome = "It's a tie."

        description = (
            f"Your hand: {', '.join(player_hand)}\nTotal: {player_total}\n\n"
            f"Dealer's hand: {', '.join(dealer_hand)}\nTotal: {dealer_total}\n\n{outcome}"
        )
        embed = discord.Embed(
            title=message.embeds[0].title,
            description=description,
            color=0x6d6482 if "win" in outcome else 0x6d6482
        )
        await message.edit(embed=embed)
        await message.clear_reactions()  # Clear reactions since the game for this hand is over

        # Update user_scores in the blackjack command
        user_id = str(interaction.user.id)
        if user_id not in user_scores:
            user_scores[user_id] = {'wins': 0, 'losses': 0}
        if outcome == "**You win!**" or outcome == "**Dealer bust, you win!**":
            user_scores[user_id]['wins'] += 1
        elif outcome == "**You lose.**":
            user_scores[user_id]['losses'] += 1

        print(user_scores)  # Debug print for checking user scores
        
        # Update the game message with the outcome
        description = (
            f"Your hand: {', '.join(player_hand)}\nTotal: {player_total}\n\n"
            f"Dealer's hand: {', '.join(dealer_hand)}\nTotal: {dealer_total}\n\n{outcome}"
        )
        embed.description = description  
        await message.edit(embed=embed)  # Updating the embed with the game outcome
        
        # Clear all reactions after the game has concluded
        await message.clear_reactions()
