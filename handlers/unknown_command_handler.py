from keyboards import get_main_menu_keyboard



def register_unknown_command(bot):
    @bot.message_handler(func=lambda message: True)
    def handle_unknown_command(message):
        keyboard = get_main_menu_keyboard()
        bot.send_message(message.chat.id, "Вибачте, я не розумію цю команду. Спробуйте іншу або скористайтеся меню.", reply_markup=keyboard) @bot.message_handler(func=lambda message: True)


