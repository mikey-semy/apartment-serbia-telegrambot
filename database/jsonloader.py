import os
import json

class JsonLoader:
    ENCODING = 'UTF-8'
    def __init__(self, file_name):
        self.__db_path = os.getcwd()
        self.__json_file = os.path.join(self.__db_path, file_name)

    def load_json(self):
        try:
            with open(self.__json_file, 'r', encoding=self.ENCODING) as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading JSON file: {e}")
            return {}