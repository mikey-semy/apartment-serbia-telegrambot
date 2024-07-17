class FilterBuilder:

    def __init__(self) -> None:
        self.filter = {}

    def add_filter(self, value:str) -> set:
        self.filter.add(value)
        return self.filter

    def remove_filter(self, value:str) -> set:
        if value in self.filter:
            self.filter.remove(value)
        return self.filter
    
    def create_query_nekretnine(self, filter: set) -> str:

        # example: https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/grad/beograd/lista/po-stranici/10/
        # example: https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/grad/beograd/lista/po-stranici/10/stranica/2/
        # example: https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/grad/beograd/kvadratura/10_400/lista/po-stranici/10/


        link = "https://www.nekretnine.rs/"
        query = link + "/".join(filter) + "/po-stranici/10/"
        return query
    
    def create_query_4zida(self, filter: set) -> str:

        # example: https://www.4zida.rs/prodaja-stanova/beograd/garsonjera/vlasnik/do-100000-evra?vece_od=10m2&manje_od=60m2&skuplje_od=1000eur
        # example: https://www.4zida.rs/prodaja-stanova/beograd/garsonjera/vlasnik/do-100000-evra?oglasivac=agencija&vece_od=10m2&manje_od=60m2&strana=2&skuplje_od=1000eur
        # example: https://www.4zida.rs/prodaja-stanova/beograd/garsonjera/vlasnik/do-100000-evra?oglasivac=agencija&vece_od=10m2&manje_od=60m2&strana=3&skuplje_od=1000eur

        link = "https://www.4zida.rs/"
        query = link + "/".join(filter)
        return query
    
    
    def create_query_cityexpert(self, filter: set) -> str:

        # example: https://cityexpert.rs/prodaja-nekretnina/beograd?ptId=2,1&minPrice=10000&maxPrice=300000&minSize=10&maxSize=60&bedroomsArray=r1
        # example: https://cityexpert.rs/prodaja-nekretnina/beograd?ptId=2,1&currentPage=2&minPrice=10000&maxPrice=300000&minSize=10&maxSize=60&bedroomsArray=r1
        # example: https://cityexpert.rs/prodaja-nekretnina/beograd?ptId=2,1&currentPage=3&minPrice=10000&maxPrice=300000&minSize=10&maxSize=60&bedroomsArray=r1

        link = "https://cityexpert.rs/"
        query = link + "/".join(filter)
        return query