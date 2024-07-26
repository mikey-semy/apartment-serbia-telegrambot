from collections import OrderedDict

from jsonloader import JsonLoader

JSON_FILE_NAME = 'filter.json'

class UrlCreater:
    def __init__(self):
        json_loader = JsonLoader(JSON_FILE_NAME)
        self.filter = json_loader.load_json()

    def get_type(self, call, value):
        
        self.value = value

    
    def __get_menu_item(self, menu_id):
        return self.menu[menu_id]
    
class UrlNekretnine(UrlCreater):

    def __init__(self, url) -> None:
        super().__init__()
        self.name = "nekretnine"
        self.url = url
        self.filter = self.filter[self.name]

    def create_url(type_housing, city, area, price):
        path_url = filter['base'] + "/".join()
    


odNekretnine = OrderedDict([
            ('path_base', 'https://www.nekretnine.rs'),
            ('path_type', 'stambeni-objekti'),
            ('path_base_city', 'grad'),
            ('path_city', 'beograd'),
            ('path_base_area', 'kvadratura'),
            ('path_area', '1_500'),
            ('path_base_price', 'cena'),
            ('path_price', '1_1000000'),
        ])
odFourzida = OrderedDict([
            ('path_base', 'https://www.4zida.rs'),
            ('path_type', 'prodaja-stanova'),
            ('path_city', 'beograd'),
            ('path_rooms', 'garsonjera'),
            ('path_price_max', 'do-1000000-evra'),
            ('param_base_room', 'struktura'),
            ('param_room', 'jednosoban'),
            ('param_base_area_min', 'vece_od'),
            ('param_area_min', '1m2'),
            ('param_base_area_max', 'manje_od'),
            ('param_area_max', '500m2'),
            ('param_base_price_min', '1eur'),
        ])
odCityexpert = OrderedDict([
            ('path_base', 'https://cityexpert.rs'),
            ('path_base_type', 'prodaja-nekretnina'),
            ('path_city', 'beograd'),
            ('param_base_type', 'ptId'),
            ('param_type', '1'),
            ('param_base_room', 'structure'),
            ('param_type', '0.1'),
            ('param_base_area_min', 'minSize'),
            ('param_area_min', '1'),
            ('param_base_area_max', 'maxSize'),
            ('param_area_max', '500'),
            ('param_base_price_min', 'minPrice'),
            ('param_area_min', '1'),
            ('param_base_price_max', 'maxPrice'),
            ('param_area_max', '1000000'),
        ])

objects = [odNekretnine, odFourzida, odCityexpert]

def func_update_value(city):
    for obj in objects:
        obj.update_value(city)

#update_value('beograd')
func_update_value('nis')

list_values = []
for obj in objects:
    values = list(obj.values())
    list_values.append(values)

for values in list_values:
    print(values)