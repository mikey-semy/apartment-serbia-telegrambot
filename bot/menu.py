import telebot
from telebot.util import quick_markup
from jsonloader import JsonLoader

JSON_FILE_NAME = 'menu.json'


ROW_WIDTH = 4

class CreateMenu:
    def __init__(self, bot, lang):
        self.bot = bot
        self.lang = lang

        json_loader = JsonLoader(JSON_FILE_NAME)
        self.menu = json_loader.load_json()
      
    def __get_menu_item(self, menu_id):
        return self.menu[menu_id]

    def __create_markup(self, menu_item):
        
        buttons = {}

        for button in menu_item['buttons']:
            
            buttons[self.lang.get_language(button['label'])] = {
                'url':                                  button['url'],
                'callback_data':                        button['callback_data'],
                'switch_inline_query':                  button['switch_inline_query'],
                'switch_inline_query_current_chat':     button['switch_inline_query_current_chat'],
                'callback_game':                        button['callback_game'],
                'pay':                                  button['pay'],
                'login_url':                            button['login_url'],
                'web_app':                              button['web_app']
                }
            
        markup = quick_markup(buttons, row_width=ROW_WIDTH)

        return markup
    
    def callback(self, call, data=None):
        menu_id = call.data if data is None else data
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
