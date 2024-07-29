# python TestApartmentSerbiaBot.py -v

import unittest

from modules import SelectLanguage
from modules import UrlCreater
from modules import WebScraper

class TestApartmentSerbiaBot(unittest.TestCase):
    def setUp(self):
        self.lang = SelectLanguage.SelectLanguage()
        self.urlc = UrlCreater.CommonUrlCreater()

    def test_valid_language_code(self):
        self.lang.set_language("ru")
        result = self.lang.selected_language
        self.assertEqual(result, "ru")
    
    def test_invalid_language_code(self):
        with self.assertRaises(ValueError) as context:
            self.lang.set_language('rs')
        self.assertEqual(str(context.exception), "Invalid language code")
    
    def test_create_url(self):
        self.urlc.set_param('city', 'Beograd')
        self.urlc.set_param('price_min', '20')
        self.urlc.set_param('area_min', '100')
        self.urlc.set_param('area_max', '500')
        result = self.urlc.get_urls()
        self.assertEqual(result, 'https://www.nekretnine.rs/')


if __name__ == "__main__":
    unittest.main()

