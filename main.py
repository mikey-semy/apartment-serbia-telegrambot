import os
import telebot
from telebot import types
from menu import CreateMenu

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
cm = CreateMenu()

# Константы выбора языка
LANG_RU = 'ru'
LANG_EN = 'en'

# Константы типов меню
MAIN = 'main'
LANGUAGE_SELECTION = 'language_selection'
CITY_SELECTION = 'city_selection'
PROPERTY_TYPE = 'property_type'
BACK = 'back'

# Функция для обработки команды старт
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, text=cm.create_caption(MAIN), reply_markup=cm.create_menu(MAIN))

# Функция для обработки языкового выбора
def handle_language_selection(call, language):
    cm.set_language(language)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption(MAIN), reply_markup=cm.create_menu(MAIN))

# Функция для обработки выбора меню
def handle_menu_selection(call, menu_type):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption(menu_type), reply_markup=cm.create_menu(menu_type))

# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == LANG_RU:
        handle_language_selection(call, LANG_RU)
    elif call.data == LANG_EN:
        handle_language_selection(call, LANG_EN)
    elif call.data == LANGUAGE_SELECTION:
        handle_menu_selection(call, LANGUAGE_SELECTION)
    elif call.data == CITY_SELECTION:
        handle_menu_selection(call, CITY_SELECTION)
    elif call.data == PROPERTY_TYPE:
        handle_menu_selection(call, PROPERTY_TYPE)
    elif call.data == BACK:
        handle_menu_selection(call, MAIN)
    else:
        print(f"Unknown callback data: {call.data}")

if __name__ == "__main__":
    bot.polling(none_stop=True)