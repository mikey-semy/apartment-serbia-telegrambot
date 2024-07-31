"""Модуль для скрапинга сайтов"""

import time
import random
import re
import requests
import bs4 # для yandex cloud - иначе ругается на отсутствие bs4
#from bs4 import BeautifulSoup
import urllib3
from modules.JSONLoader import JSONLoader

# Отключаем предупреждение о небезопасном запросе
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebScraper:
    '''Скрапер'''

    JSON_FILE_NAME = 'database/scraper.json'
    HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' }
    TIMEOUT = None
    PATTERN = r"^\s+|\n|\r|\s+$"
    MIN_PAUSE = 0.5
    MAX_PAUSE = 1
    QUANTITY_PAGE = 1
    QUANTITY_OFFERS = 3

    def __init__(self) -> None:
        '''Конструктор класса. Определяет файл json'''
        json_loader = JSONLoader(self.JSON_FILE_NAME)
        self.scraper_data = json_loader.load_json()

    def get_page(self, url) -> object:
        '''Функция отправляет GET-запрос к URL и возвращает объект BeautifulSoup'''
        response = requests.get(url, headers=self.HEADERS, timeout=self.TIMEOUT)
        return bs4.BeautifulSoup(response.text, 'html.parser') # для yandex cloud - иначе ругается на отсутствие bs4

    def scrape_page(self, soup) -> list:
        '''Абстрактный метод, который должен быть реализован в подклассах'''
        raise NotImplementedError("Subclasses must implement this method")
    
    def scrape_pause(self, min_pause=MIN_PAUSE, max_pause=MAX_PAUSE) -> None:
        '''Функция вводит задержку, чтобы предотвратить блокировку скрейпера'''
        delay = random.uniform(min_pause, max_pause)
        time.sleep(delay)

    def scrape(self) -> list:
        '''Функция скрейпит страницу и возвращает список предложений на странице'''
        soup = self.get_page(self.url)
        return self.scrape_page(soup)

    def has_next_page(self, soup) -> bool:
        '''Функция проверяет, есть ли следующая страница'''
        next_page_link = soup.find(self.data["NEXT_BUTTON_TAG"], class_=self.data["NEXT_BUTTON_CLASS"])
        return next_page_link is not None
    
class NekretnineScraper(WebScraper):
    '''Скрапер для сайта nekretnine.rs'''

    def __init__(self, url, page_number=1) -> None:
        super().__init__()
        self.name = "nekretnine"
        self.url = url
        self.data = self.scraper_data[self.name]
        # Конструируем URL для следующей страницы
        if page_number > 1:
            self.url += self.data["NEXT_PAGE"].format(page_number=page_number)
    
    def scrape_page(self, soup) -> list:
        '''Функция скрейпит страницу и возвращает список предложений на странице'''
        self.scrape_pause()
        offers = []

        offer_elements = soup.findAll(self.data["OFFER_TAG"], class_=self.data["OFFER_CLASS"])

        count = 0
        for offer_element in offer_elements:

            if count == self.QUANTITY_OFFERS:
                break

            self.scrape_pause()


            title = offer_element.find(self.data["TITLE_TAG"], class_=self.data["TITLE_CLASS"])
            location = offer_element.find(self.data["LOCATION_TAG"], class_=self.data["LOCATION_CLASS"])
            # rooms = offer_element.find(self.data["ROOMS_TAG"], class_=self.data["ROOMS_CLASS"])
            price = offer_element.find(self.data["PRICE_TAG"], class_=self.data["PRICE_CLASS"])
            # area = offer_element.find(self.data["AREA_TAG"], class_=self.data["AREA_CLASS"])
            url_offer = offer_element.find(self.data["LINK_HREF_OFFER_TAG"], class_=self.data["LINK_HREF_OFFER_CLASS"])
            #url_image = offer_element.find(self.data["IMG_SRC_OFFER_TAG"], class_=self.data["IMG_SRC_OFFER_CLASS"])

            offer_cleaned = {
                'title': re.sub(self.PATTERN, '', str(title.text)),
                'location': re.sub(self.PATTERN, '', str(location.text)),
                # 'rooms': re.sub(PATTERN, '', str(rooms.text)).split(' | ')[2],
                'price': price.find('span').text.strip(),
                # 'area': area.find('span').text.strip(),
                'url_offer': self.data["BASE_URL"] + url_offer.find('a').get('href'),
                #'url_image': url_image.get('data-src')
            } if title else ''
            
            count = count + 1

            offers.append(offer_cleaned)

        return offers

class FourzidaScraper(WebScraper):
    '''Скрапер для сайта 4zida.rs'''

    def __init__(self, url, page_number=1):
        super().__init__()
        self.name = "4zida"
        self.url = url
        self.data = self.scraper_data[self.name]
        if page_number > 1:
            self.url += self.data["NEXT_PAGE"].format(page_number=page_number)
    
    def scrape_page(self, soup) -> list:
        '''Функция скрейпит страницу и возвращает список предложений на странице'''

        offers = []

        offer_elements = soup.findAll(self.data["OFFER_TAG"], class_=self.data["OFFER_CLASS"])

        count = 0

        for offer_element in offer_elements:

            if count == self.QUANTITY_OFFERS:
                break

            self.scrape_pause()

            title = offer_element.find(self.data["TITLE_TAG"], class_=self.data["TITLE_CLASS"])
            location = offer_element.find(self.data["LOCATION_TAG"], class_=self.data["LOCATION_CLASS"])
            # rooms = offer_element.find(self.data["ROOMS_TAG"], class_=self.data["ROOMS_CLASS"])
            price = offer_element.find(self.data["PRICE_TAG"], class_=self.data["PRICE_CLASS"])
            # area = offer_element.find(self.data["AREA_TAG"], class_=self.data["AREA_CLASS"])
            url_offer = offer_element.find(self.data["LINK_HREF_OFFER_TAG"], class_=self.data["LINK_HREF_OFFER_CLASS"])
            # url_image = offer_element.find(self.data["IMG_SRC_OFFER_TAG"], class_=self.data["IMG_SRC_OFFER_CLASS"])
            
            offer_cleaned = {
                'title': re.sub(self.PATTERN, '', str(title.text)),
                'location': re.sub(self.PATTERN, '', str(location.text)),
                # 'rooms': re.sub(PATTERN, '', str(rooms.text)).split(' • ')[1],
                'price': price.text.strip(),
                # 'area': re.sub(PATTERN, '', str(area.text)).split(' • ')[0],
                'url_offer': self.data["BASE_URL"] + url_offer.get('href'),
                # 'url_image': url_image.find('img').get('src')
            } if title else ''

            count = count + 1

            offers.append(offer_cleaned)
        return offers

class CityexpertScraper(WebScraper):
    '''Скрапер для сайта cityexpert.rs'''

    def __init__(self, url, page_number=1):

        super().__init__()
        self.name = "cityexpert"
        self.url = url
        self.data = self.scraper_data[self.name]

        if page_number > 1:
            self.url += self.data["NEXT_PAGE"].format(page_number=page_number)
    
    def scrape_page(self, soup) -> list:
        '''Функция скрейпит страницу и возвращает список предложений на странице'''
        offers = []
        
        offer_elements = soup.findAll(self.data["OFFER_TAG"], class_=self.data["OFFER_CLASS"])
        
        count = 0

        for offer_element in offer_elements:

            if count == self.QUANTITY_OFFERS:
                break

            self.scrape_pause()

            title = offer_element.find(self.data["TITLE_TAG"], class_=self.data["TITLE_CLASS"])
            location = offer_element.find(self.data["LOCATION_TAG"], class_=self.data["LOCATION_CLASS"])
            # rooms = offer_element.findAll(self.data["ROOMS_TAG"], class_=self.data["ROOMS_CLASS"])
            price = offer_element.find(self.data["PRICE_TAG"], class_=self.data["PRICE_CLASS"])
            # area = offer_element.findAll(self.data["AREA_TAG"], class_=self.data["AREA_CLASS"])
            url_offer = offer_element.find(self.data["LINK_HREF_OFFER_TAG"], class_=self.data["LINK_HREF_OFFER_CLASS"])
            # url_image = offer_element.find(self.data["IMG_SRC_OFFER_TAG"], class_=self.data["IMG_SRC_OFFER_CLASS"])
           
            offer_cleaned = {
                'title': re.sub(self.PATTERN, '', str(title.text)),
                'location': re.sub(self.PATTERN, '', str(location.text)),
                # 'rooms': re.sub(PATTERN, '', str(rooms[1].text if rooms is not None else '')),
                'price': price.find('span').text.strip(),
                # 'area': re.sub(PATTERN, '', str(area[0].text if area is not None else '')),
                'url_offer': self.data["BASE_URL"] + url_offer.find('a').get('href'),
                # 'url_image': url_image.find('img').get('src', '') if url_image is not None and url_image.find('img') is not None else ''
            } if title else ''
            
            count = count + 1

            offers.append(offer_cleaned)
        return offers


class CommonScraper(NekretnineScraper, FourzidaScraper, CityexpertScraper):
    ''' Класс общего скрапера для трех сайтов с методом получения данных постранично'''
   
    def __init__(self):
        super().__init__()
  
    def scrape_page(self, soup):
        pass

    def __get_scraper(self, url: str, page_number: int) -> object:
        ''' Функция возвращает объект скрейпера в зависимости от URL'''

        if 'nekretnine.rs' in url:
            return NekretnineScraper(url, page_number)
        elif '4zida.rs' in url:
            return FourzidaScraper(url, page_number)
        elif 'cityexpert.rs' in url:
            return CityexpertScraper(url, page_number)
        else:
            raise ValueError("Unsupported URL")

    def get_data(self, urls: list, current_page_number: int = 1, quantity_pages: int = WebScraper.QUANTITY_PAGE) -> list:
        '''Функция get_data собирает данные со всех страниц сайта'''
       
        last_page_number = quantity_pages

        all_offers = []

        for url in urls:
            while True:

                scraper = self.__get_scraper(url, current_page_number)

                soup = scraper.get_page(url)

                offers_from_page = scraper.scrape_page(soup)

                for offer in offers_from_page:
                    all_offers.append(offer)

                if not scraper.has_next_page(soup) or current_page_number == last_page_number:
                    break

                current_page_number += 1

        return all_offers