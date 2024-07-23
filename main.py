import os
import telebot
from telebot import types
from menu import CreateMenu
from telebot.util import quick_markup

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
cm = CreateMenu()

CHANNEL_IDS = ["@MikeDaily"]

# Константы выбора языка
LANG_RU = 'ru'
LANG_EN = 'en'

# Константы типов меню
START = 'start'
WELCOME = 'welcome'
MAIN = 'main'
HELP = 'help'
LANGUAGE_SELECTION = 'language_selection'
CITY_SELECTION = 'city_selection'
PROPERTY_TYPE = 'property_type'
BACK = 'back'

# CITIES = ['belgorod', 'moscow']
# TYPES = ['apartment', 'house']
# filter = []


# @bot.message_handler(content_types=['text'])
# def check_subscriptions(message):
#     subscribed_channels = []
#     for channel_id in CHANNEL_IDS:
#         chat_member = bot.get_chat_member(channel_id, message.from_user.id)
#         if chat_member.status in ['member', 'creator', 'administrator']:
#             subscribed_channels.append(channel_id)
#     if subscribed_channels:
#         bot.send_message(message.chat.id, f'You are subscribed to the following channels: {", ".join(subscribed_channels)}')
#     else:
#         bot.send_message(message.chat.id, 'You are not subscribed to any of the channels.')

# Функция для обработки команды старт
# @bot.message_handler(commands=["start"])
# def send_welcome(message):

#     # Установка языка по-умолчанию (из настроек пользователя)
#     language_code = message.from_user.language_code
#     cm.set_language(language_code)

#     #Приветствие пользователя
#     first_name = message.from_user.first_name 
#     bot.send_message(message.chat.id, text=cm.create_caption(WELCOME, first_name), reply_markup=cm.create_menu(WELCOME))

# def handle_main_selection(message):
#     bot.send_message(message.chat.id, text=cm.create_caption(MAIN), reply_markup=cm.create_menu(MAIN))
#     # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption(help), reply_markup=cm.create_menu(help))
#     # 

# # Функция для обработки языкового выбора
# def handle_language_selection(call, language):
#     cm.set_language(language)
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption(MAIN), reply_markup=cm.create_menu(MAIN))
#     #handle_start_selection()

# # Функция для обработки выбора по фильтру
# def handle_filter_selection(call, category_filter):
#     filter.append(call.data)
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption(MAIN), reply_markup=cm.create_menu(MAIN))

# # Функция для обработки выбора меню
# def handle_menu_selection(call, menu_type):
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption(menu_type), reply_markup=cm.create_menu(menu_type))

# @bot.message_handler(commands=['filter'])
# def send_filter(message):
#     bot.reply_to(message, str(filter))


lang = {
    'ru':
        {
            'Main menu': 'Главное меню',
            'Change language': 'Изменить язык',
            'Help': 'Помощь'
        }
}

# Define the menu structure
menu = {
    'main': {
        'label': lang['ru']['Main menu'],
        'buttons': [
            {'label': 'Подменю 1', 'callback_data': 'submenu1'},
            {'label': 'Подменю 2', 'callback_data': 'submenu2'},
            {'label': 'Выход', 'callback_data': 'exit'}
        ]
    },
    'submenu1': {
        'label': lang['ru']['Change language'],
        'buttons': [
            {'label': 'Опция 1', 'callback_data': 'option1'},
            {'label': 'Опция 2', 'callback_data': 'option2'},
            {'label': 'Назад', 'callback_data': 'main'}
        ]
    },
    'submenu2': {
        'label': lang['ru']['Help'],
        'buttons': [
            {'label': 'Опция 3', 'callback_data': 'option3'},
            {'label': 'Опция 4', 'callback_data': 'option4'},
            {'label': 'Назад', 'callback_data': 'main'}
        ]
    }
}

# Define the callback function
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    menu_id = call.data
    menu_item = menu.get(menu_id)
    if menu_item:
        markup = telebot.types.InlineKeyboardMarkup()
        for button in menu_item['buttons']:
            markup.add(telebot.types.InlineKeyboardButton(button['label'], callback_data=button['callback_data']))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=menu_item['label'], reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, text='Ошибка')

# Define the start command
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    for button in menu['main']['buttons']:
        markup.add(telebot.types.InlineKeyboardButton(button['label'], callback_data=button['callback_data']))
    bot.send_message(message.from_user.id, menu['main']['label'], reply_markup=markup)


# # Обработчик callback-запросов
# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     if call.data == MAIN:
#         handle_main_selection(call.message)
#     # elif call.data == HELP:
#     #     handle_help_selection(call, HELP)
#     elif call.data == LANG_RU:
#         handle_language_selection(call, LANG_RU)
#     elif call.data == LANG_EN:
#         handle_language_selection(call, LANG_EN)
#     elif call.data in CITIES:
#         handle_filter_selection(call, CITY_SELECTION)
#     elif call.data in TYPES:
#         handle_filter_selection(call, PROPERTY_TYPE)
#     elif call.data == LANGUAGE_SELECTION:
#         handle_menu_selection(call, LANGUAGE_SELECTION)
#     elif call.data == CITY_SELECTION:
#         handle_menu_selection(call, CITY_SELECTION)
#     elif call.data == PROPERTY_TYPE:
#         handle_menu_selection(call, PROPERTY_TYPE)
#     elif call.data == BACK:
#         handle_menu_selection(call, MAIN)
#     else:
#         print(f"Unknown callback data: {call.data}")

if __name__ == "__main__":
    bot.polling(none_stop=True)