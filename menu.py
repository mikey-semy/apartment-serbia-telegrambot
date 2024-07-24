import os
import json
import telebot

class CreateMenu:
    def __init__(self, bot, lang):
        self.bot = bot
        self.lang = lang
        '''Конструктор класса. Определяет файл json'''
        self.name_json_file = 'menu.json'
         # Получаем текущий путь к директории
        self.__db_path = os.getcwd()
        # Формируем путь к файлу json                                       
        self.__json_file = os.path.join(self.__db_path, self.name_json_file)
        # Загружаем данные из json файла      
        self.menu = self.__load_json()

    def __load_json(self):
        '''Функция загрузки JSON файла'''
        try:
            with open(self.__json_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading JSON file: {e}")
            return {}
            
    def __get_menu_item(self, menu_id):
        return self.menu[menu_id]

    def __create_markup(self, menu_item):
        markup = telebot.types.InlineKeyboardMarkup()
        print('Menu: ', self.lang.selected_language)
        for button in menu_item['buttons']:
            markup.add(telebot.types.InlineKeyboardButton(text=self.lang.get_language(button['label']), callback_data=button['callback_data']))
        return markup

    def callback(self, call, data=None):
        menu_id = call.data if data == None else data
        menu_item = self.menu[menu_id]
        if menu_item:
            markup = self.__create_markup(menu_item)
            self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=self.lang.get_language(menu_item['label']), reply_markup=markup)
        else:
            self.bot.answer_callback_query(call.id, text=self.lang.get_language('error_message_not_menu_item'))

    def create_menu(self, message, type_menu='menu_main'):
        menu_item = self.__get_menu_item(type_menu)
        markup = self.__create_markup(menu_item)
        self.bot.send_message(message.from_user.id, text=self.lang.get_language(menu_item['label']), reply_markup=markup)
