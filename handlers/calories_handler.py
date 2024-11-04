import telebot
from config import API_TOKEN
from db import get_user_calories, user_exists
from keyboards import fill_personal_data, get_main_menu_keyboard

# Ініціалізація бота
bot = telebot.TeleBot(API_TOKEN)


def register_pfc_handler(bot):
    @bot.message_handler(func=lambda message: message.text == "Мої Калорії")
    def print_data(message):
        chat_id = message.chat.id

        # get data from db
        if user_exists(chat_id):
            calories = get_user_calories(chat_id)

            keyboard = get_main_menu_keyboard()
            bot.send_message(chat_id, f"Твоя добова норма це: {calories} ккал", reply_markup=keyboard)

        else:
            go_back(message)
            return


    def go_back(message):
        chat_id = message.chat.id
        keyboard = fill_personal_data()
        bot.send_message(chat_id, "На початку ти повинен заповнити особисті дані такі як: вага, зріст, стать...",
                         reply_markup=keyboard)

