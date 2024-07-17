import os
import json
from telebot import types

'''В классе CreateMenu реализованы следующие функции:

    Загрузка данных из JSON файла
    Установка и получение языка для меню
    Выбор кнопок для заданного типа меню
    Создание заголовка для заданного типа меню
    Создание меню для Telegram бота с кнопками и заголовком, соответствующими выбранному языку.'''

class CreateMenu:


    def __init__(self):
        '''Конструктор класса. Определяет файл json'''
         # Получаем текущий путь к директории
        self.__db_path = os.getcwd()
        # Формируем путь к файлу json                                       
        self.json_file = os.path.join(self.__db_path, 'elements.json')
        # Загружаем данные из json файла      
        self.elements = self.__load_json()
        # Устанавливаем язык по умолчанию !!!нужно сделать запоминание выбранного ранее языка   
        self.selected_language = 'en'    

    def set_language(self, language_code):
        '''Установка языка для меню'''
        if language_code in ['ru', 'en']:
            # Проверяем, является ли язык допустимым
            self.selected_language = language_code                          
        else:
            # Выбрасываем ошибку, если языковой код недопустимый
            raise ValueError("Invalid language code")                       
    
    def get_language(self):
        '''Получение текущего языка'''
        return self.selected_language

    def __load_json(self):
        '''Функция загрузки JSON файла'''
        with open(self.json_file, 'r') as f:
            return json.load(f)
    
    def __select_button(self, type_menu: str) -> dict:
        '''Выбор кнопок для заданного типа меню'''
        buttons = self.elements['buttons']
        result = {}
        for button in buttons:
            if button['type_menu'] == type_menu:
                # Добавляем кнопку в словарь результатов с переведенным именем кнопки
                result[button['btn_name'][self.selected_language]] = button['btn_callback']
        return result

    def create_caption(self, type_menu: str) -> str:
        '''Создание заголовка для заданного типа меню'''
        captions = self.elements['captions']
        for caption in captions:
            if caption['type_menu'] == type_menu:
                return caption['cpt_name'][self.selected_language]

    def create_menu(self, type_menu: str) -> types.InlineKeyboardMarkup:
        '''Создание меню для Telegram бота'''
        markup = types.InlineKeyboardMarkup()
        btn_list = self.__select_button(type_menu)
        for btn_name, btn_callback in btn_list.items():
            btn = types.InlineKeyboardButton(text=btn_name, callback_data=btn_callback)
            markup.add(btn)
        return markup