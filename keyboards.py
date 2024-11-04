from telebot import types


def get_main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton("Оновити дані"), types.KeyboardButton("Мої Калорії"))
    keyboard.add(types.KeyboardButton("Меню На День"))
    return keyboard


def fill_personal_data():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton("Заповнити необхідні дані"))
    return keyboard
