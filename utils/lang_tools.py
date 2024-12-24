import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
import os

load_dotenv()  # Load environment variables from .env


@tool
def search_recipes(
    query: str, 
    includeIngredients: str, 
    excludeIngredients: str, 
    diet: str, 
    cuisine: str, 
    addRecipeInformation: bool, 
    number: int,
) -> dict:
    """Search for recipes based on various filters and preferences.

    Args:
        query: Search term for the recipe (e.g., 'pasta').
        includeIngredients: Ingredients that must be included in the recipes (comma-separated).
        excludeIngredients: Ingredients to exclude from the recipes (comma-separated).
        diet: Dietary preference (e.g., 'vegetarian').
        cuisine: Cuisine type (e.g., 'italian').
        addRecipeInformation: Whether to include detailed recipe information (True/False).
        number: Number of results to return.

    Returns:
        A dictionary containing the search results.
    """
    result = {
        "query": query,
        "includeIngredients": includeIngredients,
        "excludeIngredients": excludeIngredients,
        "diet": diet,
        "cuisine": cuisine,
        "addRecipeInformation": addRecipeInformation,
        "number": number
    }
    return result


@tool
def search_ingredient_substitutes(
    ingredient_name: str
) -> dict:
    """Fetches ingredient substitutes from the Spoonacular API.

    Args:
        ingredient_name (str): The name of the ingredient to find substitutes for.

    Returns:
        dict: A dictionary containing the substitutes and relevant information.
    """
    # Return parameters for fetching substitutes
    result = {
        "ingredient_name": ingredient_name
    }
    return result

@tool
def conversation(query: str) -> str:
    """This function simply returns the input query as part of a normal conversation."""
    return query
