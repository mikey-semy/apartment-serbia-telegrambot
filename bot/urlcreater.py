from jsonloader import JsonLoader

class UrlCreater:
    JSON_FILE_NAME = 'bot/template.json'
    def __init__(self):
        self.json_loader = JsonLoader(JSON_FILE_NAME)
        self.template = self.json_loader.load_json()

class NekretnineUrlCreater(UrlCreater):
    NAME_TEMPLATE = 'nekretnine'
    
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
    
class CommonUrlCreater(UrlCreater):
    #Для проверки:
    #urlNekretnine = 'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/grad/beograd/lista/po-stranici/10/'
    #urlFourzida = 'https://www.4zida.rs/prodaja-stanova/beograd/garsonjera/vlasnik/do-100000-evra?struktura=jednosoban&struktura=jednoiposoban&struktura=dvosoban&struktura=dvoiposoban&struktura=trosoban&vece_od=10m2&manje_od=60m2&skuplje_od=1000eur'
    #urlCityexpert = 'https://cityexpert.rs/prodaja-nekretnina/beograd?ptId=2,1&minPrice=10000&maxPrice=300000&minSize=10&maxSize=60&bedroomsArray=r1'

    def __init__(self):
        super().__init__()
    
    def set_param(self, key, value):
        NekretnineUrlCreater().set_param(key, value)
        FourzidaUrlCreater().set_param(key, value)
        CityexpertUrlCreater().set_param(key, value)

    def get_urls(self) -> list:
        return [
            NekretnineUrlCreater().create_url(),
            FourzidaUrlCreater().create_url(),
            CityexpertUrlCreater().create_url()
        ]