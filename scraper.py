import time
import random
import os
import json
import requests
from bs4 import BeautifulSoup
import re
import urllib3


from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.time()
        value = func(*args, **kwargs)
        end_time = time.time()
        print(f"Время выполнения {func.__name__!r}: {end_time - start_time} секунд")
        return value
    return wrapper_timer

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

    def scrape_pause(self, min=0.5, max=1):
        # Вводим задержку, чтобы предотвратить блокировку скрейпера
        delay = random.uniform(min, max)
        print('Pause:', delay)
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
            price = offer_element.find(self.data["PRICE_TAG"], class_=self.data["PRICE_CLASS"])
            area = offer_element.find(self.data["AREA_TAG"], class_=self.data["AREA_CLASS"])
            url_offer = offer_element.find(self.data["LINK_HREF_OFFER_TAG"], class_=self.data["LINK_HREF_OFFER_CLASS"])
            url_image = offer_element.find(self.data["IMG_SRC_OFFER_TAG"], class_=self.data["IMG_SRC_OFFER_CLASS"])

            # Очищаем данные и добавляем их в список предложений
            offers.append({
                'title': re.sub(pattern, '', str(title.text)),
                'location': re.sub(pattern, '', str(location.text)),
                'rooms': re.sub(pattern, '', str(rooms.text)).split(' | ')[2],  # Нужно сделать проверку
                'price': price.find('span').text.strip(),
                'area': area.find('span').text.strip(),
                'url_offer': self.data["BASE_URL"] + url_offer.find('a').get('href'),
                'url_image': url_image.get('data-src')
            }) if title else ''  # Исключаем результат без заголовка.
            print('! ', self.name, ' - get offers: ', str(len(offers)))
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
                'price': price.text.strip(),
                'area': re.sub(pattern, '', str(area.text)).split(' • ')[0],
                # 'floor': re.sub(pattern, '', str(floor.text)).split(' • ')[2],
                'url_offer': self.data["BASE_URL"] + url_offer.get('href'),
                'url_image': url_image.find('img').get('src')
            }) if title else ''  # Исключаем результат без заголовка.

            print('! ', self.name, ' - get offers: ', str(len(offers)))
        return offers

class CityexpertScraper(WebScraper):

    def __init__(self, url, page_number=1):
        # Инициализируем базовый скрейпер с URL и номером страницы
        super().__init__(url, {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        })
        self.name = "cityexpert"
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
            price = offer_element.find(self.data["PRICE_TAG"], class_=self.data["PRICE_CLASS"])
            area = offer_element.findAll(self.data["AREA_TAG"], class_=self.data["AREA_CLASS"])
            # floor = offer_element.find(self.data["FLOOR_TAG"], class_=self.data["FLOOR_CLASS"])
            url_offer = offer_element.find(self.data["LINK_HREF_OFFER_TAG"], class_=self.data["LINK_HREF_OFFER_CLASS"])
            url_image = offer_element.find(self.data["IMG_SRC_OFFER_TAG"], class_=self.data["IMG_SRC_OFFER_CLASS"])
            
            # Очищаем данные и добавляем их в список предложений
            offers.append({
                'title': re.sub(pattern, '', str(title.text)),
                'location': re.sub(pattern, '', str(location.text)),
                'rooms': re.sub(pattern, '', str(rooms[1].text)),  # Нужно сделать проверку
                'price': price.find('span').text.strip(),
                'area': re.sub(pattern, '', str(area[0].text)),
                # 'floor': re.sub(pattern, '', str(floor.text)).split(' • ')[2],
                'url_offer': self.data["BASE_URL"] + url_offer.find('a').get('href'),
                'url_image': url_image.find('img').get('src')
            }) if title else ''  # Исключаем результат без заголовка.
        return offers

# Функция get_scraper возвращает объект скрейпера в зависимости от URL
def get_scraper(url: str, page_number: int) -> object:
    if 'nekretnine.rs' in url:
        return NekretnineScraper(url, page_number)
    elif '4zida.rs' in url:
        return FourzidaScraper(url, page_number)
    elif 'cityexpert.rs' in url:
        return CityexpertScraper(url, page_number)
    else:
        raise ValueError("Unsupported URL")

# Функция get_data собирает данные со всех страниц сайта
@timer
def get_data(urls: list, quantity_pages: int = 2) -> list:
    last_page_number = quantity_pages
    current_page_number = 1
    all_offers = []
    for url in urls:
        while True:
            scraper = get_scraper(url, current_page_number)
            soup = scraper.get_page(url)
            offers_from_page = scraper.scrape_page(soup)

            for offer in offers_from_page:
                all_offers.append(offer)

            if not scraper.has_next_page(soup) or current_page_number == last_page_number:
                break
            current_page_number += 1

    return all_offers

urlNekretnine = 'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/grad/beograd/lista/po-stranici/10/'
urlFourzida = 'https://www.4zida.rs/prodaja-stanova/beograd/garsonjera/vlasnik/do-100000-evra?struktura=jednosoban&struktura=jednoiposoban&struktura=dvosoban&struktura=dvoiposoban&struktura=trosoban&vece_od=10m2&manje_od=60m2&skuplje_od=1000eur'
urlCityexpert = 'https://cityexpert.rs/prodaja-nekretnina/beograd?ptId=2,1&minPrice=10000&maxPrice=300000&minSize=10&maxSize=60&bedroomsArray=r1'

# urls = [urlNekretnine, urlFourzida, urlCityexpert]
urls = [urlCityexpert]
max_page = 2

offers = get_data(urls, max_page)


print(f'Количество записей: {len(offers)}')

