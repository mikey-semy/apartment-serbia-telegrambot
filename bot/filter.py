class UrlBuilder:
    # Инициализация класса с базовым URL и стилем пути
    def __init__(self, base_site, path_style=False):
        self.base_site = base_site  # Базовый URL
        self.path_style = path_style  # Флаг для определения стиля URL (path или query)
        self.params = []  # Список для хранения параметров

    # Метод для добавления параметра
    def add_param(self, value):
        self.params.append(value)  # Добавляем параметр в список

    # Метод для удаления параметра
    def remove_param(self, value):
        if self.path_style:
            # Для path_style удаляем точное совпадение
            self.params = [p for p in self.params if p != value]
        else:
            # Для query_style удаляем параметр, начинающийся с value=
            self.params = [p for p in self.params if not p.startswith(f"{value}=")]
    
    def create_array(self, elem, sep):
        array = []
        if elem in array:
            array.remove(elem)
        else: 
            array.append(elem)
        return sep.join(array)
    
    # Метод для построения итогового URL
    def build_url(self):
        if self.path_style:
            # Для path_style соединяем параметры через '/'
            return f"{self.base_site}/{'/'.join(self.params)}"
        else:
            if not self.params:
                # Если нет параметров, возвращаем только базовый URL
                return self.base_site
            # Для query_style соединяем параметры через '&' и добавляем '?'
            return f"{self.base_site}?{'&'.join(self.params)}"

# # Пример использования:
# url_builder = UrlBuilder("https://www.nekretnine.rs", path_style=True)
# url_builder.add_param("stambeni-objekti")
# url_builder.add_param("stanovi")
# url_builder.add_param("izdavanje-prodaja")
# url_builder.add_param("prodaja")

# print(url_builder.build_url())

# url_builder.remove_param("izdavanje-prodaja")
# print(url_builder.build_url())

# # Для URL с параметрами через ? и &
# param_builder = UrlBuilder("https://www.4zida.rs")
# param_builder.add_param("ptId=2,1")
# param_builder.add_param("minPrice=10000")
# param_builder.add_param("maxPrice=300000")

# print(param_builder.build_url())

# param_builder.remove_param("minPrice")
# print(param_builder.build_url())


# url_builder = UrlBuilder("https://www.4zida.rs", path_style=True)

# # Добавляем path параметры
# url_builder.add_param("prodaja-stanova")
# url_builder.add_param("beograd")
# url_builder.add_param("garsonjera")
# url_builder.add_param("vlasnik")
# url_builder.add_param("do-100000-evra")

# # Переключаемся на обычные параметры
# url_builder.path_style = False

# # Добавляем query параметры
# url_builder.add_param("struktura=jednosoban")
# url_builder.add_param("struktura=jednoiposoban")
# url_builder.add_param("struktura=dvosoban")
# url_builder.add_param("struktura=dvoiposoban")
# url_builder.add_param("struktura=trosoban")
# url_builder.add_param("vece_od=10m2")
# url_builder.add_param("manje_od=60m2")
# url_builder.add_param("skuplje_od=1000eur")

# # Формируем итоговую ссылку
# final_url = url_builder.build_url()
# print(final_url)


# function j(e) {
#                 var t = document.querySelector(".filtergroup.offer.filter .filter-list.collap.fixed.search-list-advanced-filters");
#                 t.innerHTML = "";
#                 var r, n, a = e.filter((function(e) {
#                     return e.counts > 0
#                 }
#                 )), o = document.createDocumentFragment();
#                 a.forEach((function(e) {
#                     o.appendChild(function(e) {
#                         var t = document.createElement("li")
#                           , r = document.createElement("a");
#                         r.className = "checkbox filter-checkbox";
#                         var n = e.addressBody.split(", ")[0].toLowerCase().replace(/\s+/g, "-");
#                         return r.setAttribute("data-url", "/grad/" + n + "/lista/po-stranici/10/"),
#                         r.setAttribute("data-name", "grad"),
#                         r.setAttribute("data-key", e.id),
#                         r.textContent = e.addressBody.split(", ")[0],
#                         t.appendChild(r),
#                         t
#                     }(e))
#                 }
#                 )),
#                 t.appendChild(o),
#                 (n = null === (r = Array.from(document.querySelectorAll(".filtergroup .heading")).find((function(e) {
#                     return "Grad" === e.textContent.trim()
#                 }
#                 ))) || void 0 === r ? void 0 : r.parentNode) ? (n.addEventListener("click", C),
#                 verticalFilterAnimations.registerEvents(!1)) : console.error("Grad container not found"),
#                 document.dispatchEvent(new CustomEvent("cityOrCityPartListUpdated"))
#             }