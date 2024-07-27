from jsonloader import JsonLoader

JSON_FILE_NAME = 'bot/template.json'
area_min = 10
area_max = 100
price_min = 100
price_max = 10000
class UrlBuilder:
    def __init__(self):
        self.json_loader = JsonLoader(JSON_FILE_NAME)
        self.template = self.json_loader.load_json()
        self.name = "nekretnine"
        self.data = self.template[self.name]
        self.params = []

    def get_values(self):
        parameters = ["type", "city", "area", "price", "pages"]
        for parameter in parameters:
            if self.data[parameter]["value"] != "None":
                self.params.extend(
                    [value.format(area_min=area_min,
                                    area_max=area_max,
                                    price_min=price_min,
                                    price_max=price_max) 
                    for key, value in self.data[parameter].items() 
                    if key in ["param", "value"]
                    ]
                )
        
        result = f"{self.data['base']}/{'/'.join(self.params)}"
        return result

ub = UrlBuilder()
print(ub.get_values())