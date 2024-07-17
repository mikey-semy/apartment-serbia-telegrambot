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
    'VKontakte': {'url': 'https://vk.com/toshkin_mikhail'},
    'Github': {'url': 'https://github.com/MikhailTo'},
    'Уже подписан': {'callback_data': 'start'}
}, row_width=2)

# Функция для обработки команды старт
@bot.message_handler(commands=["start"])
def send_welcome(message):
    start_message = bot.send_message(message.chat.id, text='(Бот находится в разработке) Добро пожаловать, подпишитесь перед тем как начать.', reply_markup=subscribe)
    bot.register_next_step_handler(start_message, process_name_step)

# Функция для обработки команды старт после подписок
def handle_start_selection(call):
    bot.send_message(message.chat.id, text=cm.create_caption(MAIN), reply_markup=cm.create_menu(MAIN))

# Функция для обработки языкового выбора
def handle_language_selection(call, language):
    cm.set_language(language)
    bot.register_next_step_handler(msg, handle_start_selection) 
    #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption(MAIN), reply_markup=cm.create_menu(MAIN))

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
        bot.register_next_step_handler(msg, handle_language_selection)
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

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == "__main__":
    bot.polling(none_stop=True)