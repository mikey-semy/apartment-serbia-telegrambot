from bs4 import BeautifulSoup
import requests

class GetData:

    def __init__(self, data_url):
        # Получаем текущий путь к директории
        self.__db_path = os.getcwd()
        # Формируем путь к файлу json                                       
        self.json_file = os.path.join(self.__db_path, 'data.json')
        # Загружаем данные из json файла      
        self.data = self.__load_json()
        self.data_url = data_url
        self.data_value_class = data_value_class
    def __get_data_url(self):

        current_page = self.get_current_page(self.data_url)
        sign_last_page = self.get_last_page(self.data_url)
        data_value_class = self.data[self.get_site_name(self.data_ur)]
        while sign_last_page:
            with requests.Session() as s:
                data_page = s.get(self.data_url)
                data_soup = BeautifulSoup(data_page.text, 'html.parser')
                data_value.append(soup.findAll('div', class_=data_value_class))

    def __load_json(self):
        '''Функция загрузки JSON файла'''
        with open(self.json_file, 'r') as f:
            return json.load(f)