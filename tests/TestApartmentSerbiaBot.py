# python TestApartmentSerbiaBot.py -v

import unittest

from utils import menu
from utils import language
from utils import urlcreater
from utils import scraper

class TestApartmentSerbiaBot(unittest.TestCase):
    def setUp(self):
        self.menu = menu.CreateMenu()
        self.lang = language.SelectLanguage()
        self.urlc = urlcreater.CommonUrlCreater()
        self.scrp = scraper.CommonScraper()

    def test_set_language_ru(self):
        self.assertEqual(self.lang.set_language("ru"), self.lang.selected_language)
    
    def test_set_language_rs(self):
        self.assertEqual(self.lang.set_language("rs"), self.lang.selected_language)
    
    def test_get_language_simple(self):
        self.assertEqual(self.lang.get_language("message_search_wait"), "Пожалуйста, подождите...")

    def test_get_language_error(self):
        self.assertEqual(self.lang.get_language("message_search_wiat"), "Пожалуйста, подождите...")

if __name__ == "__main__":
    unittest.main()

