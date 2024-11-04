from db import user_exists, get_user_calories
from api import get_menu_api
from keyboards import fill_personal_data


def register_menu_handler(bot):
    @bot.message_handler(func=lambda message: message.text == "Меню На День")
    def get_menu(message):
        chat_id = message.chat.id

        # get data from db
        if user_exists(chat_id):
            calories = get_user_calories(chat_id)
            api_data = get_menu_api(calories)

            if api_data:  # Перевірка, що api_data не None
                recipes = api_data.get('results', [])  # Отримуємо список рецептів

                if recipes:
                    # Формуємо повідомлення з рецептами
                    response_message = "Here's a menu based on your calories:\n\n"
                    for recipe in recipes:
                        title = recipe.get('title', 'No Title')
                        url = recipe.get('sourceUrl', '#')
                        response_message += f"- {title}: {url}\n"
                    bot.send_message(message.chat.id, response_message)
                else:
                    bot.send_message(message.chat.id, "Помилка на сервері")
            else:
                # Якщо api_data None, повідомляємо про помилку на сервері
                bot.send_message(message.chat.id, "Помилка на сервері")
        else:
            go_back(message)
            return


    def go_back(message):
        chat_id = message.chat.id
        keyboard = fill_personal_data()
        bot.send_message(chat_id, "На початку ти повинен заповнити особисті дані такі як: вага, зріст, стать...",
                         reply_markup=keyboard)





