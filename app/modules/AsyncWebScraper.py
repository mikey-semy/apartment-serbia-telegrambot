"""Модуль для скрапинга сайтов"""

# import time
import random
import re
# import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import urllib3
from app.modules.JSONLoader import JSONLoader
from app.config import Config
# from app.utils.timer import timer


# Отключаем предупреждение о небезопасном запросе
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebScraper:
    '''Скрапер'''

    def __init__(self) -> None:
        '''Конструктор класса. Определяет файл json'''
        json_loader = JSONLoader(Config.WebScraper.JSON_FILE_NAME)
        self.scraper_data = json_loader.load_json()

    async def aget_page(self, url) -> object:
        '''Асинхронная функция отправляет GET-запрос к URL и возвращает объект BeautifulSoup'''
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, 
                headers=Config.WebScraper.HEADERS, 
                timeout=Config.WebScraper.TIMEOUT) as response:
                html = await response.text()
                return BeautifulSoup(html, 'html.parser')
            
    def scrape_page(self, soup) -> list:
        '''Абстрактный метод, который должен быть реализован в подклассах'''
        raise NotImplementedError("Subclasses must implement this method")

    async def ascrape_pause(self, 
                     min_pause=Config.WebScraper.MIN_PAUSE, 
                     max_pause=Config.WebScraper.MAX_PAUSE) -> None:
        '''Асинхронная функция вводит задержку, чтобы предотвратить блокировку скрейпера'''
        delay = random.uniform(min_pause, max_pause)
        await asyncio.sleep(delay)
    
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

    async def ascrape(self) -> list:
        '''Асинхронная функция скрейпит страницу и возвращает список предложений на странице'''
        soup = await self.aget_page(self.url)
        return await self.ascrape_page(soup)
    
    def has_next_page(self, soup) -> bool:
        '''Функция проверяет, есть ли следующая страница'''
        next_page_link = soup.find(self.data["NEXT_BUTTON_TAG"], class_=self.data["NEXT_BUTTON_CLASS"])
        return next_page_link is not None

    async def ascrape_page(self, soup) -> list:
        '''Асинхронная функция скрейпит страницу и возвращает список предложений на странице'''

        offers = []
        offer_elements = soup.findAll(self.data["OFFER_TAG"], class_=self.data["OFFER_CLASS"])

        count = 0
        #for offer_element in offer_elements:
        for index in range(len(offer_elements)):
            if count == Config.WebScraper.QUANTITY_OFFERS:
                break

            await self.ascrape_pause()

            title = offer_elements[index].find(self.data["TITLE_TAG"], class_=self.data["TITLE_CLASS"])
            location = offer_elements[index].find(self.data["LOCATION_TAG"], class_=self.data["LOCATION_CLASS"])
            # rooms = offer_element[index].find(self.data["ROOMS_TAG"], class_=self.data["ROOMS_CLASS"])
            price = offer_elements[index].find(self.data["PRICE_TAG"], class_=self.data["PRICE_CLASS"])
            # area = offer_element[index].find(self.data["AREA_TAG"], class_=self.data["AREA_CLASS"])
            url_offer = offer_elements[index].find(self.data["LINK_HREF_OFFER_TAG"], class_=self.data["LINK_HREF_OFFER_CLASS"])
            #url_image = offer_element[index].find(self.data["IMG_SRC_OFFER_TAG"], class_=self.data["IMG_SRC_OFFER_CLASS"])

            offer_cleaned = {
                'title': re.sub(Config.WebScraper.PATTERN, '', str(title.text)),
                'location': re.sub(Config.WebScraper.PATTERN, '', str(location.text)),
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

    async def ascrape(self) -> list:
        '''Асинхронная функция скрейпит страницу и возвращает список предложений на странице'''
        soup = await self.aget_page(self.url)
        return await self.ascrape_page(soup)
    
    def has_next_page(self, soup) -> bool:
        '''Функция проверяет, есть ли следующая страница'''
        next_page_link = soup.find(self.data["NEXT_BUTTON_TAG"], class_=self.data["NEXT_BUTTON_CLASS"])
        return next_page_link is not None

    async def ascrape_page(self, soup) -> list:
        '''Функция скрейпит страницу и возвращает список предложений на странице'''

        offers = []
        offer_elements = soup.findAll(self.data["OFFER_TAG"], class_=self.data["OFFER_CLASS"])

        count = 0

        for offer_element in offer_elements:

            if count == Config.WebScraper.QUANTITY_OFFERS:
                break

            await self.ascrape_pause()

            title = offer_element.find(self.data["TITLE_TAG"], class_=self.data["TITLE_CLASS"])
            location = offer_element.find(self.data["LOCATION_TAG"], class_=self.data["LOCATION_CLASS"])
            # rooms = offer_element.find(self.data["ROOMS_TAG"], class_=self.data["ROOMS_CLASS"])
            price = offer_element.find(self.data["PRICE_TAG"], class_=self.data["PRICE_CLASS"])
            # area = offer_element.find(self.data["AREA_TAG"], class_=self.data["AREA_CLASS"])
            url_offer = offer_element.find(self.data["LINK_HREF_OFFER_TAG"], class_=self.data["LINK_HREF_OFFER_CLASS"])
            # url_image = offer_element.find(self.data["IMG_SRC_OFFER_TAG"], class_=self.data["IMG_SRC_OFFER_CLASS"])
            
            offer_cleaned = {
                'title': re.sub(Config.WebScraper.PATTERN, '', str(title.text)),
                'location': re.sub(Config.WebScraper.PATTERN, '', str(location.text)),
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
    
    async def ascrape(self) -> list:
        '''Асинхронная функция скрейпит страницу и возвращает список предложений на странице'''
        soup = await self.aget_page(self.url)
        return await self.ascrape_page(soup)

    def has_next_page(self, soup) -> bool:
        '''Функция проверяет, есть ли следующая страница'''
        next_page_link = soup.find(self.data["NEXT_BUTTON_TAG"], class_=self.data["NEXT_BUTTON_CLASS"])
        return next_page_link is not None
    
    async def ascrape_page(self, soup) -> list:
        '''Асинхронная функция скрейпит страницу и возвращает список предложений на странице'''
        
        offers = []
        
        offer_elements = soup.findAll(self.data["OFFER_TAG"], class_=self.data["OFFER_CLASS"])
        
        count = 0

        for offer_element in offer_elements:

            if count == Config.WebScraper.QUANTITY_OFFERS:
                break

            await self.ascrape_pause()

            title = offer_element.find(self.data["TITLE_TAG"], class_=self.data["TITLE_CLASS"])
            location = offer_element.find(self.data["LOCATION_TAG"], class_=self.data["LOCATION_CLASS"])
            # rooms = offer_element.findAll(self.data["ROOMS_TAG"], class_=self.data["ROOMS_CLASS"])
            price = offer_element.find(self.data["PRICE_TAG"], class_=self.data["PRICE_CLASS"])
            # area = offer_element.findAll(self.data["AREA_TAG"], class_=self.data["AREA_CLASS"])
            url_offer = offer_element.find(self.data["LINK_HREF_OFFER_TAG"], class_=self.data["LINK_HREF_OFFER_CLASS"])
            # url_image = offer_element.find(self.data["IMG_SRC_OFFER_TAG"], class_=self.data["IMG_SRC_OFFER_CLASS"])
           
            offer_cleaned = {
                'title': re.sub(Config.WebScraper.PATTERN, '', str(title.text)),
                'location': re.sub(Config.WebScraper.PATTERN, '', str(location.text)),
                # 'rooms': re.sub(PATTERN, '', str(rooms[1].text if rooms is not None else '')),
                'price': price.find('span').text.strip(),
                # 'area': re.sub(PATTERN, '', str(area[0].text if area is not None else '')),
                'url_offer': url_offer.find('a').get('href'),
                # 'url_image': url_image.find('img').get('src', '') if url_image is not None and url_image.find('img') is not None else ''
            } if title else ''
            
            count = count + 1

            offers.append(offer_cleaned)
        return offers


class CommonScraper(WebScraper):
    ''' Класс общего скрапера для трех сайтов с методом получения данных постранично'''
   
    def __init__(self):
        super().__init__()
  
    def ascrape_page(self, soup):
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
    # @timer
    async def aget_data(self, urls: list, current_page_number: int = 1, quantity_pages: int = Config.WebScraper.QUANTITY_PAGE) -> list:
        '''Асинхронная функция get_data собирает данные со всех страниц сайта'''
       
        last_page_number = quantity_pages

        all_offers = []

        for url in urls:
            while True:

                scraper = self.__get_scraper(url, current_page_number)

                soup = await scraper.aget_page(url)

                offers_from_page = await scraper.ascrape_page(soup)

                for offer in offers_from_page:
                    all_offers.append(offer)

                if not scraper.has_next_page(soup) or current_page_number == last_page_number:
                    break

                current_page_number += 1

        return all_offers
    
# for check class:
# async def main():
#     scraper = CommonScraper()
#     url_ = ["https://www.nekretnine.rs/apartmani/grad/beograd/kvadratura/1_500/cena/0_1000000",
#         "https://cityexpert.rs/izdavanje-nekretnina/beograd?ptId=1&maxPrice=550&polygonsArray=Novi%20Beograd",
#         "https://www.4zida.rs/prodaja-stanova/novi-sad/do-47000-evra?vece_od=25m2&manje_od=30m2&skuplje_od=45000eur"]
#     offers = await scraper.aget_data(url_)
#     # print(offers)
#     print(len(offers))

# if __name__ == "__main__":
#     asyncio.run(main())