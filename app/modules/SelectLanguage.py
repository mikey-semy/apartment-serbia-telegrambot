from app.modules.JSONLoader import JSONLoader
from app.config import Config

class SelectLanguage:

    def __init__(self) -> None:
        '''Конструктор класса. Определяет файл json'''
        json_loader = JSONLoader(Config.SelectLanguage.JSON_FILE_NAME)
        self.lang = json_loader.load_json()
        
        self.selected_language = self.lang["default_language"]
        
    def set_language(self, language_code) -> None:
        if language_code in self.lang["languages"]:
            # Проверяем, является ли язык допустимым
            self.selected_language = language_code                          
        else:
            # Выбрасываем ошибку, если языковой код недопустимый
            raise ValueError("Invalid language code")
            # Устанавливаем язык по-умолчанию
            # self.selected_language = self.lang["default_language"]                     
    
    def get_language(self, text) -> (None | str):
        try:
            return self.lang[self.selected_language][text]
        except KeyError:
            return f"Error: unknown text '{text}' for language '{self.selected_language}'"