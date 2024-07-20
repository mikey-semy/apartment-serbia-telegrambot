import time
import random
import os
import requests
from bs4 import BeautifulSoup
import re
import urllib3
from configparser import ConfigParser
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Для https.


class WebScraper:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get_page(self, url):
        response = requests.get(url, headers=self.headers)
        return BeautifulSoup(response.text, 'html.parser')

    def scrape_page(self, soup):
        # Для реализации в подклассах
        raise NotImplementedError("Subclasses must implement this method")

    def scrape_pause(self, min=1, max=2):
        delay = random.uniform(min, max)
        time.sleep(delay)


class NekretnineScraper(WebScraper):

    def __init__(self, url, page_number=1):

        self.url = url
        self.constants = ConfigParser().read("constants.ini")

        if page_number > 1:
            self.url += self.constants.get("nekretnine", "NEXT_PAGE").format(optional=page_number) #f'stranica/{page_number}/'
        super().__init__(self.url, {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        })

    def scrape(self) -> list:
        soup = self.get_page(self.url)
        return self.scrape_page(soup)

    def has_next_page(self, soup) -> bool:
        next_page_link = soup.find('a', class_='next-article-button')  # Признак окончания узнать, поправить.
        return next_page_link is not None

    def scrape_page(self, soup) -> list:
        # Скрейпинг nekretnine.rs
        
        offers = []
        pattern = r"^\s+|\n|\r|\s+$"
        offer_elements = soup.findAll('div', class_=self.constants.get("nekretnine", "OFFER_CLASS"))

        for offer_element in offer_elements:
            self.scrape_pause()

            title = offer_element.find('h2', class_=self.constants.get("nekretnine", "TITLE_CLASS"))
            location = offer_element.find('p', class_=self.constants.get("nekretnine", "LOCATION_CLASS"))
            rooms = offer_element.find('div', class_=self.constants.get("nekretnine", "ROOMS_CLASS"))
            date_create = offer_element.find('div', class_=self.constants.get("nekretnine", "DATE_CREATE_CLASS"))
            price = offer_element.find('p', class_=self.constants.get("nekretnine", "PRICE_CLASS"))
            area = offer_element.find('p', class_=self.constants.get("nekretnine", "AREA_CLASS"))
            url_offer = offer_element.find('h2', class_=self.constants.get("nekretnine", "LINK_HREF_OFFER_CLASS"))
            url_image = offer_element.find('img', class_=self.constants.get("nekretnine", "IMG_SRC_OFFER_CLASS"))

            offers.append({
                'title': re.sub(pattern, '', str(title.text)),
                'location': re.sub(pattern, '', str(location.text)),
                'rooms':  re.sub(pattern, '', str(rooms.text)).split(' | ')[2], # Нужно сделать проверку 
                'date_create': re.sub(pattern, '', str(date_create.text)).split(' | ')[0],
                'price': price.find('span').text.strip(),
                'area': area.find('span').text.strip(),
                'url_offer': self.constants.get("nekretnine", "BASE_URL") + url_offer.find('a').get('href'),
                'url_image': url_image.get('data-src')
            }) if title else '' # Исключаем результат без заголовка.
        return offers
    
    
    def get_data(self, url, quantity_pages=2) -> list:
        # For get data from nekretnine.rs
        last_page_number = quantity_pages
        current_page_number = 1
        all_offers = []
        
        while True:
            scraper = NekretnineScraper(url, current_page_number)
            soup = scraper.get_page(url)
            offers_from_page = scraper.scrape_page(soup)
        
            for offer in offers_from_page:
                all_offers.append(offer)
        
            if not scraper.has_next_page(soup) or current_page_number == last_page_number:
                break
            current_page_number += 1
        
        return all_offers   
 

# To check separately:
#url = 'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/grad/beograd/lista/po-stranici/10/'
#offers = get_data(url, 2)

