from db import user_exists
from global_variables import user_data
from keyboards import get_main_menu_keyboard, fill_personal_data


def register_start_handler(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        chat_id = message.chat.id
        user_data[chat_id] = {}  # Ініціалізуємо дані для нового користувача

        bot.send_message(chat_id, "Привіт! Я ProstoEat, я допоможу тобі збалансувати твоє харчування.")
        if user_exists(chat_id):
            menu(message)
        else:
            keyboard = fill_personal_data()
            bot.send_message(chat_id, "Натисни кнопку нижче, щоб заповнити необхідні дані:", reply_markup=keyboard)

    @bot.message_handler(commands=['menu'])
    def menu(message):
        keyboard = get_main_menu_keyboard()
        bot.send_message(message.chat.id, "Виберіть опцію:", reply_markup=keyboard)