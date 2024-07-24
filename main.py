import os
import telebot
from menu import CreateMenu
from language import SelectLanguage
from filter import UrlBuilder

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
menu = CreateMenu(bot)
lang = SelectLanguage()

CHANNEL_IDS = ["@MikeDaily"]

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if "menu" in call.data:

        menu.callback(call)

    elif "action" in call.data:
            
            if call.data == "action_ru":
                handle_language_selection(call, "ru")
            elif call.data == "action_en":
                handle_language_selection(call, "ru")
            else:
                 print(f"Unknown action callback data: {call.data}")
    else:
        print(f"Unknown menu callback data: {call.data}")



@bot.message_handler(commands=['start'])
def start(message):
    
    # Установка языка по-умолчанию (из настроек пользователя)
    lang.set_language(message.from_user.language_code)
    # Создание главного меню
    menu.create_menu(message)

# Функция для обработки языкового выбора
def handle_language_selection(call, language):
    lang.set_language(language)
    menu.callback(call, "menu_change_language")
    #menu.callback(call, "menu_main")

@bot.message_handler(commands=['ru'])
def send_filter(message):
    lang.set_language("ru")
    bot.reply_to(message, lang.selected_language)

@bot.message_handler(commands=['en'])
def send_filter(message):
    lang.set_language("en")
    bot.reply_to(message, lang.selected_language)

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



# # Define the callback function
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     menu_id = call.data
#     menu_item = menu.get(menu_id)
#     if menu_item:
#         markup = telebot.types.InlineKeyboardMarkup()
#         for button in menu_item['buttons']:
#             markup.add(telebot.types.InlineKeyboardButton(button['label'], callback_data=button['callback_data']))
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=menu_item['label'], reply_markup=markup)
#     else:
#         bot.answer_callback_query(call.id, text='Ошибка')

# # Define the start command
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = telebot.types.InlineKeyboardMarkup()
#     for button in menu['main']['buttons']:
#         markup.add(telebot.types.InlineKeyboardButton(button['label'], callback_data=button['callback_data']))
#     bot.send_message(message.from_user.id, menu['main']['label'], reply_markup=markup)


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