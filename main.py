import os
import json
import telebot
from telebot import types

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

class CreateMenu:

    def __init__(self):
        '''Конструктор класса. Определяет файл json'''
        self.__db_path = os.getcwd()
        self.json_file = os.path.join(self.__db_path, 'elements.json')
        self.elements = self.__load_json()
        self.selected_language = 'en'

    def set_language(self, language_code):
        if language_code in ['ru', 'en']:
            self.selected_language = language_code
        else:
            raise ValueError("Invalid language code")
    
    def get_language(self):
        return self.selected_language

    def __load_json(self):
        '''Функция загрузки JSON файла'''
        with open(self.json_file, 'r') as f:
            return json.load(f)
    
    def __select_button(self, type_menu: str) -> dict:
        '''В качестве аргумента принимает "тип меню". Возвращает словарь где ключ = текст кнопки, значение = callbackdata кнопки'''
        buttons = self.elements['buttons']
        result = {}
        for button in buttons:
            if button['type_menu'] == type_menu:
                result[button['btn_name'][self.selected_language]] = button['btn_callback']
        return result

    def create_caption(self, type_menu: str) -> str:
        captions = self.elements['captions']
        for caption in captions:
            if caption['type_menu'] == type_menu:
                return caption['cpt_name'][self.selected_language]

    def create_menu(self, type_menu: str) -> types.InlineKeyboardMarkup:
        '''Создаём меню для TG бота'''
        markup = types.InlineKeyboardMarkup()
        btn_list = self.__select_button(type_menu)
        for btn_name, btn_callback in btn_list.items():
            btn = types.InlineKeyboardButton(text=btn_name, callback_data=btn_callback)
            markup.add(btn)
        return markup

# --------------------- bot ---------------------
# @bot.message_handler(commands=['help', 'start'])
# def say_welcome(message):
#     user_first_name = str(message.chat.first_name)
#     #bot.reply_to(message, f"Привет! {user_first_name} \n Добро пожаловать!")
#     bot.send_message(message.chat.id,
#                      'Добро пожаловать, ', user_first_name, '!\n',
#                      parse_mode='markdown')

cm = CreateMenu()

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, text=cm.create_caption('Main'), reply_markup=cm.create_menu('Main'))
    # bot.send_message(message.chat.id, text=config.get(selected_language, "welcome"), reply_markup= cm.create_menu('Main'))
    #bot.send_message(message.chat.id, text=config.get(cm.selected_language, "welcome"), reply_markup= cm.create_menu('Main'))
    # bot.send_message(message.chat.id, text=config.get(selected_language, "select_language"), reply_markup= cm.create_menu('Language Selection'))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'ru':
        cm.set_language('ru')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption('Main'), reply_markup=cm.create_menu('Main'))
    if call.data == 'en':
        cm.set_language('en')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption('Main'), reply_markup=cm.create_menu('Main'))
    
    if call.data == 'language_selection':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption('Language Selection'), reply_markup=cm.create_menu('Language Selection'))
    if call.data == 'сity_selection':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption('City Selection'), reply_markup=cm.create_menu('City Selection'))
    if call.data == 'property_type':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption('Property Type'), reply_markup=cm.create_menu('Property Type'))
    if call.data == 'back':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cm.create_caption('Main'), reply_markup=cm.create_menu('Main'))

if __name__ == "__main__":
    bot.polling(none_stop=True)
    
# @bot.message_handler(commands=["start"])
# def send_start(message):

#     # Создание клавиатуры выбора языка
#     # markup = ReplyKeyboardMarkup(resize_keyboard=True)
#     # markup.add(config.get(languages.get(selected_language_code), "button_ru"))
#     # markup.add(config.get(languages.get(selected_language_code), "button_en"))

#     # # Отправка сообщения с клавиатурой
#     # bot.reply_to(message, config.get(languages.get(selected_language_code), "select_language"), reply_markup=markup)

#     # username = message.from_user.username
#     # start_message = config.get("Messages", "start")
#     # bot.send_message(message.chat.id, start_message.format(username=username))
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     button_ru = telebot.types.InlineKeyboardButton(text=config.get(languages.get(selected_language_code), "button_ru"),
#                                                      callback_data='button_ru')
#     button_en = telebot.types.InlineKeyboardButton(text=config.get(languages.get(selected_language_code), "button_en"),
#                                                      callback_data='button_en')
#     keyboard.add(button_ru, button_en)
#     bot.reply_to(message, config.get(languages.get(selected_language_code), "select_language"), reply_markup=markup)

# @bot.callback_query_handler(func=lambda call: call.data == 'button_ru')
# def button_ru(call):
#     message = call.message
#     chat_id = message.chat.id
#     selected_language_code = 'ru'
#     bot.send_message(chat_id, config.get(languages.get(selected_language_code), "selected_language"))


# @bot.callback_query_handler(func=lambda call: call.data == 'button_en')
# def button_en(call):
#     message = call.message
#     chat_id = message.chat.id
#     selected_language_code = 'en'
#     bot.send_message(chat_id, config.get(languages.get(selected_language_code), "selected_language"))

    
# @bot.message_handler(content_types='text')
# def handle_message(message):
#   if message.text == config.get(languages.get(selected_language_code), "button_ru"):
#         selected_language_code = 'ru'
#         bot.reply_to(message, config.get(languages.get(selected_language_code), "selected_language"))
#   elif message.text == config.get(languages.get(selected_language_code), "button_en"):
#         selected_language_code = 'en'
#         bot.reply_to(message, config.get(languages.get(selected_language_code), "selected_language"))


# @bot.message_handler(commands=["help"])
# def send_help(message):
#     bot.send_message(message.chat.id, config.get("Messages", "help"))


# @bot.message_handler(func=lambda message: True)
# def echo(message):
#     for t, resp in dialog.items():
#         if sum([e in message.text.lower() for e in resp['in']]):
#             bot.send_message(message.chat.id, random.choice(resp['out']))
#             return

#     bot.send_message(message.chat.id, 'Проблемы?. Воспользуйтесь /help.')


# ---------------- local testing ----------------
# if __name__ == '__main__':
#     bot.infinity_polling()
