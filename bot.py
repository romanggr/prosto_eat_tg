import telebot
from db import close_db
from dotenv import load_dotenv
import os
from handlers.personal_data_handler import register_personal_data_handler
from handlers.calories_handler import register_pfc_handler
from handlers.start import register_start_handler
from handlers.unknown_command_handler import register_unknown_command

load_dotenv()
bot = telebot.TeleBot(os.getenv("API_TOKEN"))


# Реєстрація обробників
register_personal_data_handler(bot)
register_pfc_handler(bot)
register_start_handler(bot)
register_unknown_command(bot)

# Запуск бота
if __name__ == "__main__":
    try:
        bot.polling()
    except KeyboardInterrupt:
        print("Бот зупинений.")
    finally:
        close_db()