import requests
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_recipes(parameters):
    # API Key and URL
    API_KEY = os.getenv("SPOONACULAR_API_KEY")
    BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"

    # Parameters for the search
    params = {
        "query": parameters.get('query', ''),  # Default to empty string if 'query' is not provided
        "includeIngredients": parameters.get('includeIngredients', ''),  # Default to empty string
        "excludeIngredients": parameters.get('excludeIngredients', ''),  # Default to empty string
        "diet": parameters.get('diet', ''),  # Default to empty string
        "cuisine": parameters.get('cuisine', ''),  # Default to empty string
        "addRecipeInformation": parameters.get('addRecipeInformation', True),  # Default to False
        "number": parameters.get('number', 1),  # Default to 10 if 'number' is not provided
        "apiKey": API_KEY
    }

    # Make the API request
    response = requests.get(BASE_URL, params=params)

    # Check the response status and return results
    if response.status_code == 200:
        recipes = response.json()
        return recipes
    else:
        return {
            "error": f"Failed to fetch recipes: {response.status_code}",
            "details": response.json()
        }



def fetch_substitutes(parameter: dict) -> dict:
    """
    Makes an API request to fetch substitutes for a given ingredient.

    Args:
        parameter (dict): A dictionary containing 'ingredient_name' and 'api_key'.

    Returns:
        dict: A dictionary containing the substitutes or error details.
    """

    # API base URL
    BASE_URL = "https://api.spoonacular.com/food/ingredients/substitutes"
    API_KEY = os.getenv("SPOONACULAR_API_KEY")

    # Parameters for the request
    params = {
        "ingredientName": parameter["ingredient_name"],
        "apiKey": API_KEY
    }

    try:
        # Make the API request
        response = requests.get(BASE_URL, params=params)

        # Validate response status
        if response.status_code == 200:
            substitutes = response.json()
            return {
                "substitutes": substitutes.get("substitutes", []),
                "message": substitutes.get("message"),
            }
        else:
            return {
                "error": f"Failed to fetch substitutes. Status code: {response.status_code}",
                "details": response.json(),
            }
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        return {"error": f"An error occurred while making the API request: {str(e)}"}
