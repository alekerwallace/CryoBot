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
        deck: deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'] * 4
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
        player_hand_2 = []
        dealer_hand = [deck.pop(), deck.pop()]

        # Check if the player can split their hand
        can_split = player_hand[0] == player_hand[1]
        split_hand = False

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
        if can_split:
            await message.add_reaction("🪚")  # Reaction for "Split" if applicable

        # Defining the check for reactions
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ["✅", "❌", "🪚"] and reaction.message.id == message.id

        # Loop for handling Hit or Stand reactions
        while True:
            # Check if the player's hand value is 21, if so, break out of the loop
            if hand_value(player_hand) == 21:
                break

            reaction, user = await client.wait_for('reaction_add', check=check)
            await message.remove_reaction(reaction, user)  # Remove the user's reaction
            if can_split:
                await message.remove_reaction("🪚", client.user)

            if str(reaction.emoji) == "🪚": # player wants to split
                player_hand_2 = [ player_hand.pop(1) ]
                split_hand = True
                description =  f"Click ✅ to hit or ❌ to stand\n\n"
                description += f"Your hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"
                description += f"Your second hand: {', '.join(player_hand_2)}\nTotal: {hand_value(player_hand_2)}\n\n"
                description += f"Dealer's face-up card: {dealer_hand[0]}"
                embed.description = description
                await message.edit(embed=embed)

            elif str(reaction.emoji) == "✅":
                player_hand.append(deck.pop())
                if hand_value(player_hand) > 21:
                    description =  f"Your hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"
                    if split_hand:
                        description += f"Your second hand: {', '.join(player_hand_2)}\nTotal: {hand_value(player_hand_2)}\n\n"
                    description += f"Dealer's face-up card: {dealer_hand[0]}\n\n**You busted! Game over.**"

                    embed.description = description
                    await message.edit(embed=embed)
                    await message.clear_reactions()  # Clear reactions here
                    if split_hand:
                        break
                    return  # Exit the function if the player busts
                else:
                    description =  f"Click ✅ to hit or ❌ to stand\n\n"
                    description += f"Your hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"
                    if split_hand:
                        description += f"Your second hand: {', '.join(player_hand_2)}\nTotal: {hand_value(player_hand_2)}\n\n"
                    description += f"Dealer's face-up card: {dealer_hand[0]}"
                    embed.description = description
                    await message.edit(embed=embed)
                                      
            else:
                if split_hand:
                    description = (f"**Playing the second hand** \n\nClick ✅ to hit or ❌ to stand\n\n"
                                f"Your first hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"
                                f"Your second hand: {', '.join(player_hand_2)}\nTotal: {hand_value(player_hand_2)}\n\n"
                                f"Dealer's face-up card: {dealer_hand[0]}")  
                    embed.description = description
                    await message.edit(embed=embed)

                break  # Exit the loop if the "Stand" reaction is received

        while split_hand:
            # Check if the player's hand value is 21, if so, break out of the loop
            if hand_value(player_hand_2) == 21:
                break

            reaction, user = await client.wait_for('reaction_add', check=check)
            await message.remove_reaction(reaction, user)  # Remove the user's reaction
            if str(reaction.emoji) == "✅":
                player_hand_2.append(deck.pop())
                description = (f"**Playing the second hand** \n\nClick ✅ to hit or ❌ to stand\n\n"
                            f"Your first hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"
                            f"Your second hand: {', '.join(player_hand_2)}\nTotal: {hand_value(player_hand_2)}\n\n"
                            f"Dealer's face-up card: {dealer_hand[0]}")
                if hand_value(player_hand_2) > 21:
                    description = (f"Your first hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"
                                   f"Your second hand: {', '.join(player_hand_2)}\nTotal: {hand_value(player_hand_2)}\n\n"
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
        player_total_2 = hand_value(player_hand_2)
        dealer_total = hand_value(dealer_hand)
        outcome = ""

        # Update user_scores in the blackjack command
        user_id = str(interaction.user.id)
        if user_id not in user_scores:
            user_scores[user_id] = {'wins': 0, 'losses': 0}

        # Split hand score logic & update user_scores for leaderboard.py
        if split_hand:
            if dealer_total > 21:
                outcome = "**Dealer bust, you win both hands!**"
                user_scores[user_id]['wins'] += 2
            elif dealer_total < player_total and dealer_total < player_total_2:
                outcome = "**You win both hands!**"
                user_scores[user_id]['wins'] += 2
            elif dealer_total < player_total and dealer_total == player_total_2:
                outcome = "**You win the first hand and tie the second.**"
                user_scores[user_id]['wins'] += 1
                # Could add something to document number of ties here
            elif dealer_total < player_total and dealer_total > player_total_2:
                outcome = "**You win the first hand and lose the second.**"
                user_scores[user_id]['wins'] += 1
                user_scores[user_id]['losses'] += 1
            elif dealer_total == player_total and dealer_total < player_total_2:
                outcome = "**You tie the first hand and win the second**"
                user_scores[user_id]['wins'] += 1
            elif dealer_total == player_total and dealer_total == player_total_2:
                outcome = "**You tie both hands**"
            elif dealer_total == player_total and dealer_total > player_total_2:
                outcome = "**You tie the first hand and lose the second.**"
                user_scores[user_id]['wins'] += 1
            elif dealer_total > player_total and dealer_total > player_total_2:
                outcome = "**You lose both hands.**"
                user_scores[user_id]['losses'] += 2
            elif dealer_total > player_total and dealer_total == player_total_2:
                outcome = "**You lose the first hand and tie the second.**"
                user_scores[user_id]['losses'] += 1
            elif dealer_total > player_total and dealer_total < player_total_2:
                outcome = "**You lose the first hand and win the second.**"
                user_scores[user_id]['wins'] += 1
                user_scores[user_id]['losses'] += 1
            else: 
                outcome = "**Message cryopumpkin.**"

        # Not split hand score logic & update user_scores for leaderboard.py
        else:
            if dealer_total > 21:
                outcome = "**Dealer bust, you win!**"
                user_scores[user_id]['wins'] += 1
            elif dealer_total < player_total:
                outcome = "**You win!**"
                user_scores[user_id]['wins'] += 1
            elif dealer_total == player_total:
                outcome = "**You tie.**"
            elif dealer_total > player_total:
                outcome = "**You lose.**"
                user_scores[user_id]['losses'] += 1
            else: 
                outcome = "**Message cryopumpkin.**"

        print(user_scores)  # Debug print here        

        # Update the game message with the outcome
        description = f"Your hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"
        if split_hand:
            description += f"Your second hand: {', '.join(player_hand_2)}\nTotal: {hand_value(player_hand_2)}\n\n"              
        description += f"Dealer's hand: {', '.join(dealer_hand)}\nTotal: {dealer_total}\n\n{outcome}"
        embed.description = description  


        await message.edit(embed=embed)  # Updating the embed with the game outcome
        
        # Clear all reactions after the game has concluded
        await message.clear_reactions()

        # The following line is removed as it sends a 'Game over.' message at the end
        # await interaction.channel.send("Game over.")