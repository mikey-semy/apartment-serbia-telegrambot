import os
import telebot
from telebot import types
from menu import CreateMenu
from telebot.util import quick_markup


user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.subscribeyet = False
        self.language = 'ru'

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
cm = CreateMenu()

CHANNEL_IDS = ["@MikeDaily"]

# Константы выбора языка
LANG_RU = 'ru'
LANG_EN = 'en'

# Константы типов меню
MAIN = 'main'
START = 'start'
LANGUAGE_SELECTION = 'language_selection'
CITY_SELECTION = 'city_selection'
PROPERTY_TYPE = 'property_type'
BACK = 'back'

CITIES = ['belgorod', 'moscow']
TYPES = ['apartment', 'house']
filter = []

subscribe = quick_markup({
    'VKontakte': {'url': 'https://vk.com/toshkin_mikhail', 'callback_data': 'scribe_vk'},
    'Github': {'url': 'https://github.com/MikhailTo', 'callback_data': 'scribe_gh'},
    'Уже подписан': {'callback_data': 'start'}
}, row_width=2)

@bot.message_handler(content_types=['text'])
def check_subscriptions(message):
    subscribed_channels = []
    for channel_id in CHANNEL_IDS:
        chat_member = bot.get_chat_member(channel_id, message.from_user.id)
        if chat_member.status in ['member', 'creator', 'administrator']:
            subscribed_channels.append(channel_id)
    if subscribed_channels:
        bot.send_message(message.chat.id, f'You are subscribed to the following channels: {", ".join(subscribed_channels)}')
    else:
        bot.send_message(message.chat.id, 'You are not subscribed to any of the channels.')

# Функция для обработки команды старт
@bot.message_handler(commands=["start"])
def send_welcome(message):

    # Установка языка по-умолчанию (из настроек пользователя)
    language_code = message.from_user.language_code
    cm.set_language(language_code)

    #Приветствие пользователя
    first_name = message.from_user.first_name 
    bot.send_message(message.chat.id, text=cm.create_caption(MAIN, first_name), reply_markup=cm.create_menu(MAIN))

# Функция для обработки команды старт после подписок
def handle_start_selection():
    bot.send_message(message.chat.id, text=cm.create_caption(MAIN), reply_markup=cm.create_menu(MAIN))

# Функция для обработки языкового выбора
def handle_language_selection(call, language):
    cm.set_language(language)
    handle_start_selection()

# Функция для обработки выбора по фильтру
def handle_filter_selection(call, category_filter):
    filter.append(call.data)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption(MAIN), reply_markup=cm.create_menu(MAIN))

# Функция для обработки выбора меню
def handle_menu_selection(call, menu_type):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption(menu_type), reply_markup=cm.create_menu(menu_type))

@bot.message_handler(commands=['filter'])
def send_filter(message):
    bot.reply_to(message, str(filter))

# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == START:
        handle_start_selection()
        # handle_language_selection(call, LANGUAGE_SELECTION)
    elif call.data == LANG_RU:
        handle_language_selection(call, LANG_RU)
    elif call.data == LANG_EN:
        handle_language_selection(call, LANG_EN)
    elif call.data in CITIES:
        handle_filter_selection(call, CITY_SELECTION)
    elif call.data in TYPES:
        handle_filter_selection(call, PROPERTY_TYPE)
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