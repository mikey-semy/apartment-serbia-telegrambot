from JSONLoader import JSONLoader
import re

class UrlCreater:
    JSON_FILE_NAME = 'database/urls.json'
    def __init__(self):
        self.json_loader = JSONLoader(self.JSON_FILE_NAME)
        self.template = self.json_loader.load_json()

    def extract_number(self, value):
        if isinstance(value, int):
            return value
    
        value_str = str(value)
        match = re.search(r'\d+', value_str)
        if match:
            return int(match.group())
        return None
    

class NekretnineUrlCreater(UrlCreater):
    NAME_TEMPLATE = 'nekretnine'
    params = {
            "base": "https://www.nekretnine.rs",
            "type": "/apartmani",
            "city": "",
            "price_max": "",
            "rooms": "",
            "area_min": "",
            "area_max": "",
            "price_min": ""
        }
    
    def __init__(self):
        super().__init__()

    def check_numbers(self, key, value):
 
        # Преобразуя в число, проверяем тем самым на число, при ошибке - None
        try:
            value = int(value)
        except ValueError:
            value = None
        # Задаем по умолчанию противоположные числа, если они не указаны
        if key == "price_min" and not self.params["price_max"]:
            self.params["price_max"] = 1000000
        if key == "price_max" and not self.params["price_min"]:
            self.params["price_min"] = 0
        if key == "area_min" and not self.params["area_max"]:
            self.params["area_max"] = 500
        if key == "area_max" and not self.params["area_min"]:
            self.params["area_min"] = 1
        print(self.params)
        # Если число было не числом или вообще было меньше нуля, выставляем значения по умолчанию:
        if value is None or value < 0:
            if key.startswith("price"):
                value = 0 if key.endswith("_min") else 1000000
            else:  # area
                value = 1 if key.endswith("_min") else 500
        
        # Если min > max, то меняем их местами ибо нех...
        if key.endswith("_min"):
            max_key = key.replace("_min", "_max")
            if self.params[max_key] and self.extract_number(self.params[max_key]) < value:
                self.params[max_key], value = value, self.extract_number(self.params[max_key])
        elif key.endswith("_max"):
            min_key = key.replace("_max", "_min")
            if self.params[min_key] and self.extract_number(self.params[min_key]) > value:
                self.params[min_key], value = value, self.extract_number(self.params[min_key])

        # Шаблоним появившихся в этой функции:
        if key != "price_min" and str(self.params["price_min"]).isdigit():
            self.params["price_min"] = self.__get_template("price_min", self.params["price_min"])
        if key != "price_max" and str(self.params["price_max"]).isdigit():
            self.params["price_max"] = self.__get_template("price_max", self.params["price_max"])
        if key != "area_min" and str(self.params["area_min"]).isdigit():
            self.params["area_min"] = self.__get_template("area_min", self.params["area_min"])
        if key != "area_max" and str(self.params["area_max"]).isdigit():
            self.params["area_max"] = self.__get_template("area_max", self.params["area_max"])

        return str(value)
    
    def get_default_params(self):
        return self.template[self.NAME_TEMPLATE]["default"]
    
    def set_param(self, key, value):
        if key in ["area_min", "area_max", "price_min", "price_max"]:

            final_value = self.__get_template(key, self.check_numbers(key, value))

            # нужно подумать как ошаблонить второе число
        else:
            if value in ["apartaments", "houses", "beograd", "novi_sad", "nis"]:
                value = self.__get_template(value)
            final_value = self.__get_template(key, value)
        
        self.params.update({key: final_value})
        print(self.params)

    def __get_template(self, param, value=None):
        template = self.template[self.NAME_TEMPLATE][param]
        return template.format(p={param: value}) if value else template
    
    def create_url(self):
        return self.template[self.NAME_TEMPLATE]["all"].format(**self.params)


class FourzidaUrlCreater(UrlCreater):
    NAME_TEMPLATE = 'fourzida'

    def __init__(self):
        super().__init__()
        self.params = {}

    def set_param(self, key, value):
        #Здесь нужно обработать значения в зависимости от ключа
        #area и price проверить на число и между min и max в другом месте
        #city - объединить при больших вариантах для nekretnine
        #rooms - объединить для 4zida и cityexpert, для nekretnine ничего не делать
        #добавить в шаблон наименования для каждого сайта
        final_value = self.__get_template(key).format(key=value)
        self.params[key] = final_value

    def __get_template(self, param):
        return self.template[self.NAME_TEMPLATE][param] if param else ""
    
    def create_url(self):
        data = self.params
        
        return self.template[self.NAME_TEMPLATE]["all"].format(**data)


class CityexpertUrlCreater(UrlCreater):
    NAME_TEMPLATE = 'cityexpert'
   
    def __init__(self):
        super().__init__()
        self.params = {}
        
    def set_param(self, key, value):
    
        final_value = self.__get_template(key).format(key=value)
        self.params[key] = final_value

    def __get_template(self, param):
        return self.template[self.NAME_TEMPLATE][param] if param else ""
    
    def create_url(self):
        data = self.params
        return self.template[self.NAME_TEMPLATE]["all"].format(**data)
    
class CommonUrlCreater(UrlCreater):
    #Для проверки:
    #urlNekretnine = 'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/grad/beograd/lista/po-stranici/10/'
    #urlFourzida = 'https://www.4zida.rs/prodaja-stanova/beograd/garsonjera/vlasnik/do-100000-evra?struktura=jednosoban&struktura=jednoiposoban&struktura=dvosoban&struktura=dvoiposoban&struktura=trosoban&vece_od=10m2&manje_od=60m2&skuplje_od=1000eur'
    #urlCityexpert = 'https://cityexpert.rs/prodaja-nekretnina/beograd?ptId=2,1&minPrice=10000&maxPrice=300000&minSize=10&maxSize=60&bedroomsArray=r1'

    def __init__(self):
        super().__init__()
    
    def set_param(self, key, value):
        NekretnineUrlCreater().set_param(key, value)
        # FourzidaUrlCreater().set_param(key, value)
        # CityexpertUrlCreater().set_param(key, value)

    def get_urls(self) -> list:
        return [
            NekretnineUrlCreater().create_url(),
            # FourzidaUrlCreater().create_url(),
            # CityexpertUrlCreater().create_url()
        ]
    

# urlc = CommonUrlCreater()
# urlc.set_param('city', 'Beograd')
# urlc.set_param('price_min', 'gh')
# urlc.set_param('price_max', '2g')
# urlc.set_param('area_max', '-500')
# urlc.set_param('area_min', '-100')
# urlc.set_param('area_max', '500')
# result = urlc.get_urls()
# print(result)