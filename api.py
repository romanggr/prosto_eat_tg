import requests
from config import API_TOKEN_SPOONACULAR

# Об'єкт з параметрами
def get_menu_api(calories):
    # Формування запиту до Spoonacular
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_TOKEN_SPOONACULAR,
        'timeFrame': 'day',  # можна вибрати 'day', 'week'
        'targetCalories': calories,
        'diet': 'balanced',  # можна вибрати різні дієти: 'vegan', 'vegetarian', 'paleo', 'keto' і т.д.
        'exclude': '',       # список продуктів, які ви не хочете включати (через кому)
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Викликає помилку для статус-кодів 4xx та 5xx
        print(response.json())
        return response.json()  # Повертає JSON-дані при успішному запиті

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Для налагодження
        return None

    except Exception as err:
        print(f'Other error occurred: {err}')  # Для налагодження
        return None