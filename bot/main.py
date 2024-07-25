import os
import telebot
from menu import CreateMenu
from language import SelectLanguage
from filter import UrlBuilder

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
lang = SelectLanguage()
menu = CreateMenu(bot, lang)

# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if "menu" in call.data:

        menu.callback(call)

    elif "action" in call.data:
            
            if call.data == "action_ru":
                handle_language_selection(call, "ru")               
            elif call.data == "action_en":
                handle_language_selection(call, "en")
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

if __name__ == "__main__":
    bot.polling(none_stop=True)



# @bot.message_handler(content_types=['text'])
# def check_subscriptions(message):
#     subscribed_channels = ["@MikeDaily"]
#     for channel_id in subscribed_channels:
#         chat_member = bot.get_chat_member(channel_id, message.from_user.id)
#         if chat_member.status in ['member', 'creator', 'administrator']:
#             subscribed_channels.append(channel_id)
#     if subscribed_channels:
#         bot.send_message(message.chat.id, f'You are subscribed to the following channels: {", ".join(subscribed_channels)}')
#     else:
#         bot.send_message(message.chat.id, 'You are not subscribed to any of the channels.')