import os
import re
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

index_url = 'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/grad/beograd/lista/po-stranici/10/'
url = 'https://www.nekretnine.rs'
widgets = []
pattern = "^\s+|\n|\r|\s+$"

def get_data():

    with requests.Session() as s:

        index_page = s.get(index_url, verify=False)
        soup = BeautifulSoup(index_page.text, 'html.parser')
        all_widgets = soup.findAll('div', class_='row offer')

        for widget in all_widgets:
            widgets.append({
                'title': re.sub(pattern, '', str(widget.find('h2', class_='offer-title text-truncate w-100').text)),
                'location': re.sub(pattern, '', str(widget.find('p', class_='offer-location text-truncate').text)),
                'room': re.sub(pattern, '', str(widget.find('div', class_='mt-1 mt-lg-2 mb-lg-0 d-md-block offer-meta-info offer-adress').text)).split(' | ')[2],
                'data': re.sub(pattern, '', str(widget.find('div', class_='mt-1 mt-lg-2 mb-lg-0 d-md-block offer-meta-info offer-adress').text)).split(' | ')[0],
                'price': widget.find('p', class_='offer-price').find('span').text.strip(),
                'area': widget.find('p', class_='offer-price--invert').find('span').text.strip(),
                'url_widget': url + widget.find('h2', class_='offer-title text-truncate w-100').find('a').get('href'),
                'url_image': widget.find('img', class_='img-fluid').get('data-src'),
                })

        print(widgets)
if __name__ == '__main__':
    get_data()
    os.system("pause")

