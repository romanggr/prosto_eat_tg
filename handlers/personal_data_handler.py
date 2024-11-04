from telebot import types
from db import user_exists, create_user_data, update_user_data
from global_variables import user_data
from keyboards import get_main_menu_keyboard
from utils import calculate_calories


def register_personal_data_handler(bot):
    @bot.message_handler(func=lambda message: message.text in ["Заповнити необхідні дані", "Оновити дані"])
    def fill_data(message):
        chat_id = message.chat.id
        gender_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        gender_keyboard.add(types.KeyboardButton("Чоловік"), types.KeyboardButton("Жінка"))

        bot.send_message(chat_id, "Оберіть свою стать:", reply_markup=gender_keyboard)
        bot.register_next_step_handler(message, get_gender)

    def get_gender(message):
        chat_id = message.chat.id
        gender = message.text.lower()
        if gender in ["чоловік", "жінка"]:
            user_data[chat_id]['gender'] = "MEN" if "чоловік" == gender else "WOMEN"
            bot.send_message(chat_id, "Тепер введіть свою вагу в кг (тільки число):",
                             reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_weight)
        else:
            bot.send_message(chat_id, "Будь ласка, оберіть один із варіантів: 'чоловік' або 'жінка':")
            bot.register_next_step_handler(message, get_gender)

    def get_weight(message):
        chat_id = message.chat.id
        try:
            weight = float(message.text)
            if 20 < weight < 200:
                user_data[chat_id]['weight'] = weight
                bot.send_message(chat_id, "Дякую! Тепер введіть свій зріст в см (тільки число):")
                bot.register_next_step_handler(message, get_height)
            else:
                bot.send_message(chat_id, "Вага повинна бути справжня. Спробуйте ще раз:")
                bot.register_next_step_handler(message, get_weight)
        except ValueError:
            bot.send_message(chat_id, "Будь ласка, введіть вагу числом (наприклад, 70):")
            bot.register_next_step_handler(message, get_weight)

    def get_height(message):
        chat_id = message.chat.id
        try:
            height = float(message.text)
            if 50 < height < 300:
                user_data[chat_id]['height'] = height
                bot.send_message(chat_id, "Дякую! Тепер введіть свій вік (тільки число):")
                bot.register_next_step_handler(message, get_age)
            else:
                bot.send_message(chat_id, "Зріст повинен бути справжній. Спробуйте ще раз:")
                bot.register_next_step_handler(message, get_height)
        except ValueError:
            bot.send_message(chat_id, "Будь ласка, введіть зріст числом (наприклад, 175):")
            bot.register_next_step_handler(message, get_height)

    def get_age(message):
        chat_id = message.chat.id
        try:
            age = int(message.text)
            if 0 < age < 120:
                user_data[chat_id]['age'] = age

                activity_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                activity_keyboard.add(types.KeyboardButton("Низький"), types.KeyboardButton("Середній"),
                                  types.KeyboardButton("Високий"))

                bot.send_message(chat_id, "Наскільки активний ваш спосіб життя?", reply_markup=activity_keyboard)
                bot.register_next_step_handler(message, get_activity_level)

            else:
                bot.send_message(chat_id, "Вік повинен бути в межах від 1 до 120 років. Спробуйте ще раз:")
                bot.register_next_step_handler(message, get_age)
        except ValueError:
            bot.send_message(chat_id, "Будь ласка, введіть вік числом (наприклад, 25):")
            bot.register_next_step_handler(message, get_age)

    def get_activity_level(message):
        chat_id = message.chat.id
        activity_level = message.text.lower()

        if activity_level in ["низький", "середній", "високий"]:
            # Визначаємо рівень активності користувача
            user_data[chat_id]['activity_level'] = {
                "низький": "LOW",
                "середній": "AVERAGE",
                "високий": "HIGH"
            }[activity_level]

            # Записуємо ім'я та прізвище користувача
            user_data[chat_id]['username'] = message.from_user.username
            user_data[chat_id]['user_firstname'] = message.from_user.first_name
            user_data[chat_id]['user_lastname'] = message.from_user.last_name

            # Запитуємо у користувача, чи всі дані правильні
            get_target(message)

        else:
            bot.send_message(chat_id, "Будь ласка, оберіть 'низький', 'середній' або 'високий':")
            bot.register_next_step_handler(message, get_activity_level)

    def get_target(message):
        chat_id = message.chat.id
        target = message.text.lower()

        if target not in ["схуднути", "підтримувати вагу", "набрати вагу"]:
            # Create a keyboard for target options if it's the initial prompt or if the input is invalid
            target_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            target_keyboard.add(types.KeyboardButton("Набрати вагу"), types.KeyboardButton("Підтримувати вагу"),
                                types.KeyboardButton("Схуднути"))

            bot.send_message(chat_id, "Яка ваша мета?", reply_markup=target_keyboard)
            bot.register_next_step_handler(message, get_target)
        else:
            # Save the user's target goal
            user_data[chat_id]['target'] = {
                "схуднути": "LOSE",
                "підтримувати вагу": "MAINTAIN",
                "набрати вагу": "GAIN"
            }[target]

            confirm_data(message)

    def confirm_data(message):
        chat_id = message.chat.id

        # Формування підтвердження даних
        target_text = {
            "GAIN": "Набрати вагу",
            "MAINTAIN": "Підтримувати вагу",
            "LOSE": "Схуднути"
        }

        summary = (
            f"Ось ваші дані:\n"
            f"Стать: {'Чоловік' if "MEN" == user_data[chat_id]['gender'] else "Жінка"}\n"
            f"Вага: {user_data[chat_id]['weight']} кг\n"
            f"Зріст: {user_data[chat_id]['height']} см\n"
            f"Вік: {user_data[chat_id]['age']}\n"
            f"Рівень активності: {'НИЗЬКИЙ' if user_data[chat_id]['activity_level'] == 'LOW' else 'СЕРЕДНІЙ' if user_data[chat_id]['activity_level'] == 'AVERAGE' else 'ВИСОКИЙ'}\n\n"
            f"Ціль: {target_text.get(user_data[chat_id]['target'])}\n"
            f"Чи правильні дані? Введіть 'так' або 'ні'."
        )

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(types.KeyboardButton("Так"), types.KeyboardButton("Ні"))
        bot.send_message(chat_id, summary, reply_markup=keyboard)
        bot.register_next_step_handler(message, save_data_confirmation)

    def save_data_confirmation(message):
        chat_id = message.chat.id
        confirmation = message.text.lower()

        if confirmation == 'так':
            calories = calculate_calories(user_data[chat_id])
            user_data[chat_id]['calories'] = calories


            # Збереження даних у PostgreSQL
            if user_exists(chat_id):
                update_user_data(chat_id, user_data)
            else:
                create_user_data(chat_id, user_data)

            bot.send_message(chat_id, "Дані успішно збережено! Дякую!")
            menu(message)

        elif confirmation == 'ні':
            bot.send_message(chat_id, "Будь ласка, повторіть процес введення даних.")
            fill_data(message)
        else:
            bot.send_message(chat_id, "Будь ласка, введіть 'так' або 'ні'.")
            bot.register_next_step_handler(message, save_data_confirmation)

    def menu(message):
        keyboard = get_main_menu_keyboard()
        bot.send_message(message.chat.id, "Виберіть опцію:", reply_markup=keyboard)

