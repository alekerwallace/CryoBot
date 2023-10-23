import discord
import random
from discord.ext import commands
from commands.data import user_scores

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

def build_embed(title, description, color=0x00FF00):
    return discord.Embed(title=title, description=description, color=color)

def register_blackjack_command(client):

    @client.tree.command(name="blackjack", description="Play a game of Blackjack.")
    async def blackjack(interaction: discord.Interaction):
        await interaction.response.defer()
        message = await interaction.followup.send('Starting game...')

        deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'] * 4
        random.shuffle(deck)

        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        can_split = player_hand[0] == player_hand[1]

        if hand_value(player_hand) == 21:
            embed = build_embed("Blackjack", "**Blackjack, you win!**", 0xd3f5f7)
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        description = (
            f"Click ✅ to hit or ❌ to stand\n\n"
            f"Your hand: {', '.join(player_hand)}\nTotal: {hand_value(player_hand)}\n\n"
            f"Dealer's face-up card: {dealer_hand[0]}"
        )
        embed = build_embed("Blackjack", description)
        await message.edit(content='', embed=embed)

        await message.add_reaction("✅")
        await message.add_reaction("❌")
        if can_split:
            await message.add_reaction("🪚")

        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ["✅", "❌", "🪚"] and reaction.message.id == message.id

        async def handle_hand(hand, message):
            while hand_value(hand) < 21:
                reaction, user = await client.wait_for('reaction_add', check=check)
                await message.remove_reaction(reaction, user)
                if str(reaction.emoji) == "✅":
                    hand.append(deck.pop())
                    description = (
                        f"Click ✅ to hit or ❌ to stand\n\n"
                        f"Your hand: {', '.join(hand)}\nTotal: {hand_value(hand)}\n\n"
                        f"Dealer's face-up card: {dealer_hand[0]}"
                    )
                    if hand_value(hand) > 21:
                        description += f"\n\n**You busted! Game over.**"
                        embed.description = description
                        await message.edit(embed=embed)
                        await message.clear_reactions()
                        return hand
                    embed.description = description
                    await message.edit(embed=embed)
                elif str(reaction.emoji) == "❌":
                    return hand

        while True:
            reaction, user = await client.wait_for('reaction_add', check=check)
            await message.remove_reaction(reaction, user)
            if str(reaction.emoji) == "🪚":

                hand1 = [player_hand.pop(), deck.pop()]
                hand2 = [player_hand.pop(), deck.pop()]
                embed1 = discord.Embed(
                    title="Blackjack - Hand 1",
                    description=f"Click ✅ to hit or ❌ to stand\n\n"
                                f"Your hand: {', '.join(hand1)}\nTotal: {hand_value(hand1)}",
                    color=0x00FF00
                )
                message1 = await interaction.followup.send(embed=embed1)
                await message1.add_reaction("✅")  # Reaction for "Hit"
                await message1.add_reaction("❌")  # Reaction for "Stand"

                embed2 = discord.Embed(
                    title="Blackjack - Hand 2",
                    description=f"Click ✅ to hit or ❌ to stand\n\n"
                            f"Your hand: {', '.join(hand2)}\nTotal: {hand_value(hand2)}",
                    color=0x00FF00
                )
                message2 = await interaction.followup.send(embed=embed2)
                await message2.add_reaction("✅")  # Reaction for "Hit"
                await message2.add_reaction("❌")  # Reaction for "Stand"
                
                def check1(reaction, user):
                    return user == interaction.user and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == message1.id
                
                def check2(reaction, user):
                    return user == interaction.user and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == message2.id
                
                # New gameplay loops for each split hand
                while True:
                    reaction, user = await client.wait_for('reaction_add', check=check1)

            else:
                break  # Exit the loop if the "Hit" or "Stand" reaction is received, or any other reaction that isn't "Split"
                        
        def check1(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == message1.id
        
        def check2(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == message2.id
        
        # Example: Playing one hand to completion before the other
        while True:
            reaction, user = await client.wait_for('reaction_add', check=check1)
            # ... (handle hit or stand actions for hand1)
        
        while True:
            reaction, user = await client.wait_for('reaction_add', check=check2)
            # ... (handle hit or stand actions for hand2)

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