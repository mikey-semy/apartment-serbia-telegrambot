# python TestApartmentSerbiaBot.py -v

import unittest

from utils import CreateMenu
from utils import SelectLanguage
from utils import UrlCreater
from utils import WebScraper

class TestApartmentSerbiaBot(unittest.TestCase):
    def setUp(self):
        self.menu = CreateMenu.CreateMenu()
        self.lang = SelectLanguage.SelectLanguage()
        self.urlc = UrlCreater.CommonUrlCreater()
        self.scrp = WebScraper.CommonScraper()

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

