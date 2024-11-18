class Config:
    
    class JSONLoader:
        ENCODING = 'UTF-8'
        MODE = 'r'

    class CreateMenu:
        JSON_FILE_NAME = 'app/data/menu.json'
        ROW_WIDTH = 4

    class SelectLanguage:
        JSON_FILE_NAME = 'app/data/lang.json'
    
    class UrlCreater:
        JSON_FILE_NAME = 'app/data/urls.json'

    class WebScraper:
        JSON_FILE_NAME = 'app/data/scraper.json'
        HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' }
        TIMEOUT = None
        PATTERN = r"^\s+|\n|\r|\s+$"
        MIN_PAUSE = 0.5
        MAX_PAUSE = 1
        QUANTITY_PAGE = 1
        QUANTITY_OFFERS = 10