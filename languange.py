import os
import json

class SelectLanguage:
    def __init__(self) -> None:
        '''Конструктор класса. Определяет файл json'''
        self.name_json_file = 'language.json'
         # Получаем текущий путь к директории
        self.__db_path = os.getcwd()
        # Формируем путь к файлу json                                       
        self._json_file = os.path.join(self.__db_path, self.name_json_file)
        # Загружаем данные из json файла      
        self.language = self.__load_json()
        
        self.selected_language = self.language["default_language"]

    def __load_json(self):
        '''Функция загрузки JSON файла'''
        with open(self._json_file, 'r') as f:
            return json.load(f)
        
    def set_language(self, language_code):
        if language_code in self.language["languages"]:
            # Проверяем, является ли язык допустимым
            self.selected_language = language_code                          
        else:
            # Выбрасываем ошибку, если языковой код недопустимый
            # raise ValueError("Invalid language code")
            # Устанавливаем язык по-умолчанию
            self.selected_language = self.language["default_language"]                     
    
    def get_language(self, text):
        return self.language[self.selected_language][text]