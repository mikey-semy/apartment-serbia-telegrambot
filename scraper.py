import time
import random
import os
import json
import requests
from bs4 import BeautifulSoup
import re
import urllib3

# Отключаем предупреждение о небезопасном запросе
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WebScraper:
    def __init__(self, base_url, headers):
        '''Конструктор класса. Определяет файл json'''
        # Инициализируем скрейпер с базовым URL и заголовками
        self.base_url = base_url
        self.headers = headers
        # Получаем текущий путь к директории
        self.__db_path = os.getcwd()
        # Формируем путь к файлу json
        self.json_file = os.path.join(self.__db_path, 'scraper.json')
        # Загружаем данные из json файла
        self.scraper_data = self.load_json()

    def load_json(self):
        '''Функция загрузки JSON файла'''
        with open(self.json_file, 'r') as f:
            return json.load(f)

    def get_page(self, url):
        # Отправляем GET-запрос к URL и возвращаем объект BeautifulSoup
        response = requests.get(url, headers=self.headers)
        return BeautifulSoup(response.text, 'html.parser')

    def scrape_page(self, soup):
        # Абстрактный метод, который должен быть реализован в подклассах
        raise NotImplementedError("Subclasses must implement this method")

    def scrape_pause(self, min=1, max=2):
        # Вводим задержку, чтобы предотвратить блокировку скрейпера
        delay = random.uniform(min, max)
        time.sleep(delay)


class NekretnineScraper(WebScraper):

    def __init__(self, url, page_number=1):
        # Инициализируем базовый скрейпер с URL и номером страницы
        super().__init__(url, {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        })
        self.name = "nekretnine"
        self.url = url
        self.data = self.scraper_data[self.name]
        # Конструируем URL для следующей страницы
        if page_number > 1:
            self.url += self.data["NEXT_PAGE"].format(page_number=page_number)

    def scrape(self) -> list:
        # Скрейпим страницу и возвращаем список предложений на странице
        soup = self.get_page(self.url)
        return self.scrape_page(soup)

    def has_next_page(self, soup) -> bool:
        # Проверяем, есть ли следующая страница
        next_page_link = soup.find(self.data["NEXT_BUTTON_TAG"], class_=self.data["NEXT_BUTTON_CLASS"])  # Признак окончания узнать, поправить.
        return next_page_link is not None

    def scrape_page(self, soup) -> list:
        # Скрейпинг nekretnine.rs
        # Скрейпим страницу и возвращаем список предложений по отдельности
        offers = []
        pattern = r"^\s+|\n|\r|\s+$"
        offer_elements = soup.findAll(self.data["OFFER_TAG"], class_=self.data["OFFER_CLASS"])

        for offer_element in offer_elements:
            self.scrape_pause()
            # Извлекаем данные из элемента предложения
            title = offer_element.find(self.data["TITLE_TAG"], class_=self.data["TITLE_CLASS"])
            location = offer_element.find(self.data["LOCATION_TAG"], class_=self.data["LOCATION_CLASS"])
            rooms = offer_element.find(self.data["ROOMS_TAG"], class_=self.data["ROOMS_CLASS"])
            date_create = offer_element.find(self.data["DATE_CREATE_TAG"], class_=self.data["DATE_CREATE_CLASS"])
            price = offer_element.find(self.data["PRICE_TAG"], class_=self.data["PRICE_CLASS"])
            area = offer_element.find(self.data["AREA_TAG"], class_=self.data["AREA_CLASS"])
            url_offer = offer_element.find(self.data["LINK_HREF_OFFER_TAG"], class_=self.data["LINK_HREF_OFFER_CLASS"])
            url_image = offer_element.find(self.data["IMG_SRC_OFFER_TAG"], class_=self.data["IMG_SRC_OFFER_CLASS"])

            # Очищаем данные и добавляем их в список предложений
            offers.append({
                'title': re.sub(pattern, '', str(title.text)),
                'location': re.sub(pattern, '', str(location.text)),
                'rooms': re.sub(pattern, '', str(rooms.text)).split(' | ')[2],  # Нужно сделать проверку
                'date_create': re.sub(pattern, '', str(date_create.text)).split(' | ')[0],
                'price': price.find('span').text.strip(),
                'area': area.find('span').text.strip(),
                'url_offer': self.data["BASE_URL"] + url_offer.find('a').get('href'),
                'url_image': url_image.get('data-src')
            }) if title else ''  # Исключаем результат без заголовка.
        return offers

class FourzidaScraper(WebScraper):

    def __init__(self, url, page_number=1):
        # Инициализируем базовый скрейпер с URL и номером страницы
        super().__init__(url, {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        })
        self.name = "4zida"
        self.url = url
        self.data = self.scraper_data[self.name]
        # Конструируем URL для следующей страницы
        if page_number > 1:
            self.url += self.data["NEXT_PAGE"].format(page_number=page_number)

    def scrape(self) -> list:
        # Скрейпим страницу и возвращаем список предложений на странице
        soup = self.get_page(self.url)
        return self.scrape_page(soup)

    def has_next_page(self, soup) -> bool:
        # Проверяем, есть ли следующая страница
        next_page_link = soup.find(self.data["NEXT_BUTTON_TAG"], class_=self.data["NEXT_BUTTON_CLASS"])  # Признак окончания узнать, поправить.
        return next_page_link is not None

    def scrape_page(self, soup) -> list:
        # Скрейпинг nekretnine.rs
        # Скрейпим страницу и возвращаем список предложений по отдельности
        offers = []
        pattern = r"^\s+|\n|\r|\s+$"
        offer_elements = soup.findAll(self.data["OFFER_TAG"], class_=self.data["OFFER_CLASS"])

        for offer_element in offer_elements:
            self.scrape_pause()
            # Извлекаем данные из элемента предложения
            title = offer_element.find(self.data["TITLE_TAG"], class_=self.data["TITLE_CLASS"])
            location = offer_element.find(self.data["LOCATION_TAG"], class_=self.data["LOCATION_CLASS"])
            rooms = offer_element.find(self.data["ROOMS_TAG"], class_=self.data["ROOMS_CLASS"])
            # date_create = offer_element.find(self.data["DATE_CREATE_TAG"], class_=self.data["DATE_CREATE_CLASS"])
            price = offer_element.find(self.data["PRICE_TAG"], class_=self.data["PRICE_CLASS"])
            area = offer_element.find(self.data["AREA_TAG"], class_=self.data["AREA_CLASS"])
            floor = offer_element.find(self.data["FLOOR_TAG"], class_=self.data["FLOOR_CLASS"])
            url_offer = offer_element.find(self.data["LINK_HREF_OFFER_TAG"], class_=self.data["LINK_HREF_OFFER_CLASS"])
            url_image = offer_element.find(self.data["IMG_SRC_OFFER_TAG"], class_=self.data["IMG_SRC_OFFER_CLASS"])

            # Очищаем данные и добавляем их в список предложений
            offers.append({
                'title': re.sub(pattern, '', str(title.text)),
                'location': re.sub(pattern, '', str(location.text)),
                'rooms': re.sub(pattern, '', str(rooms.text)).split(' • ')[1],  # Нужно сделать проверку
                # 'date_create': re.sub(pattern, '', str(date_create.text)).split(' | ')[0],
                'price': price.find('span').text.strip(),
                'area': re.sub(pattern, '', str(area.text)).split(' • ')[0],
                'floor': re.sub(pattern, '', str(floor.text)).split(' • ')[2],
                'url_offer': self.data["BASE_URL"] + url_offer.get('href'),
                'url_image': url_image.find('img').get('src')
            }) if title else ''  # Исключаем результат без заголовка.
        return offers
# To check separately:


# # Нужно сделать эту функцию общей для скрапинга всех сайтов
# def get_data(url, quantity_pages=2) -> list:
#         # For get data from nekretnine.rs
#         last_page_number = quantity_pages
#         current_page_number = 1
#         all_offers = []

#         while True:
#             scraper = NekretnineScraper(url, current_page_number)
#             soup = scraper.get_page(url)
#             offers_from_page = scraper.scrape_page(soup)

#             for offer in offers_from_page:
#                 all_offers.append(offer)

#             if not scraper.has_next_page(soup) or current_page_number == last_page_number:
#                 break
#             current_page_number += 1

#         return all_offers

# urlNekretnine = 'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/grad/beograd/lista/po-stranici/10/'
# urlFourzida = 'https://www.4zida.rs/prodaja-stanova/beograd/garsonjera/vlasnik/do-100000-evra?struktura=jednosoban&struktura=jednoiposoban&struktura=dvosoban&struktura=dvoiposoban&struktura=trosoban&vece_od=10m2&manje_od=60m2&skuplje_od=1000eur'
# offers = get_data(url, 2)
# print(offers)