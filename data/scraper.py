import requests
from bs4 import BeautifulSoup
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

class NekretnineScraper(WebScraper):

    def __init__(self, url, page_number = 1):
        self.url = url
        if page_number > 1:
            self.url += f'stranica/{page_number}/'
        super().__init__(self.url, {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        })
        

    def scrape(self):
        soup = self.get_page(self.url)
        return self.scrape_page(soup)
    
    def has_next_page(self, soup):
        next_page_link = soup.find('a', text='Sledeća stranica')
        return next_page_link is not None
    
    def scrape_page(self, soup):
        # Скрейпинг nekretnine.rs

        TITLE_CLASS = 'offer-title'
        LOCATION_CLASS = 'offer-location'
        ROOMS_CLASS = 'offer-meta-info'
        DATE_CREATE_CLASS = 'offer-meta-info'
        PRICE_CLASS = 'offer-price'
        AREA_CLASS = 'offer-price--invert'
        LINK_HREF_OFFER_CLASS='offer-title'
        IMG_SRC_OFFER_CLASS='img-fluid'

        offers = []
        pattern = "^\s+|\n|\r|\s+$"
        
        offer_elements = soup.findAll('div', class_='offer')

        for offer_element in offer_elements:
            title       =       offer_element.find('h2',    class_=TITLE_CLASS)
            location    =       offer_element.find('p',     class_=LOCATION_CLASS)
            rooms       =       offer_element.find('div',   class_=ROOMS_CLASS)
            date_create =       offer_element.find('div',   class_=DATE_CREATE_CLASS)
            price       =       offer_element.find('p',     class_=PRICE_CLASS)
            area        =       offer_element.find('p',     class_=AREA_CLASS)
            url_offer   =       offer_element.find('h2',    class_=LINK_HREF_OFFER_CLASS)
            url_image   =       offer_element.find('img',   class_=IMG_SRC_OFFER_CLASS)
            
            offers.append({
                'title'        : re.sub(pattern, '', str(title.text)),
                'location'     : re.sub(pattern, '', str(location.text)),
                'rooms'        : re.sub(pattern, '', str(rooms.text)).split(' | ')[2],
                'date_create'  : re.sub(pattern, '', str(date_create.text)).split(' | ')[0],
                'price'        : price.find('span').text.strip(),
                'area'         : area.find('span').text.strip(),
                'url_offer'    : url_offer.find('a').get('href'),
                'url_image'    : url_image.get('data-src')
            })
        return offers
    
    
    
#Example - one page:
#url = 'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/grad/beograd/lista/po-stranici/10/'
#scraper = NekretnineScraper(url, 1)
#offers = scraper.scrape()
#print(offers)

    
#Example - some pages
# page_number = 1
# while True:
#     scraper = NekretnineScraper(page_number)
#     soup = scraper.get_page()
#     offers = scraper.scrape_page(soup)
#     print(offers)

#     if not scraper.has_next_page(soup):
#         break

#     page_number += 1