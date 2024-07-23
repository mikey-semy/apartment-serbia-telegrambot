import os
import json
from telebot import types

class CreateMenu:

    def __init__(self):
        '''Конструктор класса. Определяет файл json'''
         # Получаем текущий путь к директории
        self.__db_path = os.getcwd()
        # Формируем путь к файлу json                                       
        self.menu_json_file = os.path.join(self.__db_path, 'menu.json')
        self.lang_json_file = os.path.join(self.__db_path, 'lang.json')
        # Загружаем данные из json файла      
        self.menu = self.__load_json()
        self.lang = self.__load_json()

        # Устанавливаем язык по умолчанию !!!нужно сделать запоминание выбранного ранее языка   
        self.selected_language = self.DEFAULT_LANGUAGE

    def set_language(self, language_code):
        '''Установка языка для меню'''
        if language_code in self.LANGUAGES:
            # Проверяем, является ли язык допустимым
            self.selected_language = language_code                          
        else:
            # Выбрасываем ошибку, если языковой код недопустимый
            # raise ValueError("Invalid language code")
            # Устанавливаем язык по-умолчанию
            self.selected_language = self.DEFAULT_LANGUAGE   

    def get_language(self):
        '''Получение текущего языка'''
        return self.selected_language

    def __load_json(self):
        '''Функция загрузки JSON файла'''
        with open(self.json_file, 'r') as f:
            return json.load(f)   
    
    def create_menu(self):