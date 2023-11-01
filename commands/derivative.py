import sympy as sp
import discord
from discord.ext import commands

def register_derivative_command(client):
    @client.tree.command(name="derivative", description="Calculate the derivative of a given function.")
    async def derivative( interaction: discord.Interaction, expression: str):
        # Define the variable
        x = sp.symbols('x')

        # Parse the user-input expression
        try:
            expr = sp.sympify(expression)
        except sp.SympifyError:
            await interaction.response.send_message("Invalid input. Please enter a valid mathematical expression.")
            return

        # Calculate the limit
        try:
            derivative_result = sp.diff(expr, x)
            await interaction.response.send_message(f"Derivative: {derivative_result}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

