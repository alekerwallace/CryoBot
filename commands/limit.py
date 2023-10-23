import sympy as sp
import discord

def register_limit_command(client):
    @client.tree.command(name="limit", description="Calculate the limit of a given expression at a specified point.")
    async def _limit(interaction: discord.Interaction, expression: str, limit_point: str):
        # Define the variable
        x = sp.symbols('x')

        # Parse the user-input expression
        try:
            expr = sp.sympify(expression)
        except sp.SympifyError:
            await interaction.response.send_message("Invalid input. Please enter a valid mathematical expression.")
            return

        # Check if the limit point is 'infinity' (case-insensitive)
        if limit_point.lower() == 'infinity':
            limit_point = sp.oo
        else:
            # Parse the limit point as a float
            try:
                limit_point = float(limit_point)
            except ValueError:
                await interaction.response.send_message("Invalid limit point. Please enter a valid number or 'infinity'.")
                return

        # Calculate the limit
        try:
            limit_result = sp.limit(expr, x, limit_point)
            await interaction.response.send_message(f"Limit Answer: {limit_result}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")
