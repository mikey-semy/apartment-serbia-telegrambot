import os
import json

from app.config import Config

class JSONLoader:
    
    def __init__(self, file_name):
        self.__db_path = os.getcwd()
        self.__json_file = os.path.join(self.__db_path, file_name)

    def load_json(self):
        try:
            with open(self.__json_file, Config.JSONLoader.MODE, encoding=Config.JSONLoader.ENCODING) as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading JSON file: {e}")
            return {}