# python TestApartmentSerbiaBot.py -v

import unittest

from app.modules import SelectLanguage
from app.modules import UrlCreater
from app.modules.WebScraper import CommonScraper

class TestApartmentSerbiaBot(unittest.TestCase):
    def setUp(self):
        self.lang = SelectLanguage.SelectLanguage()
        self.urlc = UrlCreater.CommonUrlCreater()
        self.scraper = CommonScraper()
    def test_valid_language_code(self):
        self.lang.set_language("ru")
        result = self.lang.selected_language
        self.assertEqual(result, "ru")
    
    def test_invalid_language_code(self):
        with self.assertRaises(ValueError) as context:
            self.lang.set_language('rs')
        self.assertEqual(str(context.exception), "Invalid language code")
    
    def test_create_url(self):
        self.urlc.set_param('city', 'beograd')
        self.urlc.set_param('price_min', '20')
        self.urlc.set_param('area_min', '100')
        self.urlc.set_param('area_max', '500')
        result = self.urlc.get_urls()
        self.assertEqual(result, ['https://www.nekretnine.rs/apartmani/grad/beograd/kvadratura/100_500/cena/20_1000000', 'https://www.4zida.rs/prodaja-stanova/beograd/do-1000000-evra?&vece_od=100m2&manje_od=500m2&skuplje_od=20eur', 'https://cityexpert.rs/prodaja-nekretnina/beograd?/prodaja-nekretnina&minSize=100&maxSize=500&minPrice=20&maxPrice=1000000'])

    def test_web_scraper_nekretnine(self):
        url = ["https://www.nekretnine.rs/apartmani/grad/beograd/kvadratura/1_500/cena/0_1000000"]
        offers = self.scraper.get_data(url)
        self.assertEqual(offers, [{'title': 'ODLIČNA PRILIKA, Kuća na vrhu Kosmaja, 316m2, 14ar', 'location': 'Sopot, Beograd, Srbija', 'price': '129 000 €', 'url_offer': 'https://www.nekretnine.rs/apartmani/vikendice-i-brvnare/odlicna-prilika-kuca-na-vrhu-kosmaja-316m2-14ar/Nk2Dt4eqNoV/'}, {'title': 'Splav - kućica za odmor na Savi', 'location': 'Surčin, Beograd, Srbija', 'price': '86 500 €', 'url_offer': 'https://www.nekretnine.rs/apartmani/vikendice-i-brvnare/splav-kucica-za-odmor-na-savi/Nkj0x5EmZrh/'}, {'title': 'Grocka - Zaklopača - 19m2+7.5a ID#21742', 'location': 'Grocka, Beograd, Srbija', 'price': '28 000 €', 'url_offer': 'https://www.nekretnine.rs/apartmani/vikendice-i-brvnare/grocka-zaklopaca-19m275a-id21742/Nk5lzY2FB6U/'}])

    def test_web_scraper_fourzida(self):
        url = ["https://www.4zida.rs/prodaja-stanova/beograd/do-1000000-evra?&vece_od=100m2&manje_od=500m2&skuplje_od=20eur"]
        offers = self.scraper.get_data(url)
        self.assertEqual(len(offers), 3)

    def test_web_scraper_cityexpert(self):
        url = ["https://cityexpert.rs/prodaja-nekretnina/beograd?/prodaja-nekretnina&minSize=100&maxSize=500&minPrice=20&maxPrice=1000000"]
        offers = self.scraper.get_data(url)
        self.assertEqual(len(offers), 3)

if __name__ == "__main__":
    unittest.main()

