
from app.__main__ import bot

from app.modules.CreateMenu import CreateMenu
from app.modules.SelectLanguage import SelectLanguage
from app.modules.UrlCreater import CommonUrlCreater
from app.modules.WebScraper import CommonScraper
from app.modules.CallWrapper import CallWrapper

lang = SelectLanguage()
menu = CreateMenu(bot, lang)
scraper = CommonScraper()
urlc = CommonUrlCreater()


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if "menu" in call.data:

        menu.callback(call)

    elif "action" in call.data:
            
        action_handlers = {
                #types
                "action_apartaments": lambda call: handle_type_selection(call, "apartaments"),
                "action_houses": lambda call: handle_type_selection(call, "houses"),
                #cities
                "action_beograd": lambda call: handle_city_selection(call, "beograd"),
                "action_novi_sad": lambda call: handle_city_selection(call, "novi_sad"),
                "action_nis": lambda call: handle_city_selection(call, "nis"),
                #area
                "action_area_min": lambda call: handle_area_selection(call, "area_min"),
                "action_area_max": lambda call: handle_area_selection(call, "area_max"),
                #price
                "action_price_min": lambda call: handle_type_selection(call, "price_min"),
                "action_price_max": lambda call: handle_type_selection(call, "price_max"),
                #language
                "action_ru": lambda call: handle_language_selection(call, "ru"),
                "action_en": lambda call: handle_language_selection(call, "en"),
                #others
                "action_search": handle_search_selection,
                "action_search_continue": handle_search_selection,
        }
        handler = action_handlers.get(call.data, lambda call: print(f"Unknown action callback data: {call.data}"))
        handler(call)
    else:
        print(f"Unknown menu callback data: {call.data}")

@bot.message_handler(commands=['start'])
def start(message):
    lang.set_language(message.from_user.language_code)
    menu.create_menu(message)

@bot.message_handler(commands=['search'])
def search(message):
    handle_search_selection(CallWrapper(message))

def handle_language_selection(call, language):
    lang.set_language(language)
    menu.callback(call, "menu_change_language") #menu.callback(call, "menu_main")

def handle_city_selection(call, city):
    selected_city = city
    urlc.set_param("city", selected_city)
    
def handle_type_selection(call, type):
    selected_type = type
    urlc.set_param("type", selected_type)

def handle_rooms_selection(call, rooms):
    selected_rooms = rooms
    urlc.set_param("rooms", selected_rooms)

def handle_area_selection(call, area):
    if area == "area_min":
        bot.send_message(call.message.chat.id,
                         lang.get_language("label_change_area_min"))
        bot.register_next_step_handler(call.message, handle_area_min_input)
    if area == "area_max":
        bot.send_message(call.message.chat.id,
                         lang.get_language("label_change_area_max"))
        bot.register_next_step_handler(call.message, handle_area_max_input)

def handle_area_min_input(message):
    area_min = message.text
    urlc.set_param("area_min", area_min)

def handle_area_max_input(message):
    area_max = message.text
    urlc.set_param("area_max", area_max)

def handle_price_selection(call, price):
    if price == "price_min":
        bot.send_message(call.message.chat.id, 
                         lang.get_language("label_change_price_min"))
        bot.register_next_step_handler(call.message, handle_area_min_input)
    if price == "price_max":
        bot.send_message(call.message.chat.id, 
                         lang.get_language("label_change_price_max"))
        bot.register_next_step_handler(call.message, handle_area_max_input)

def handle_price_min_input(message):
    price_min = message.text
    urlc.set_param("price_min", price_min)
    
def handle_price_max_input(message):
    price_max = message.text
    urlc.set_param("price_max", price_max)
    
def handle_search_selection(call):

    bot.send_message(call.message.chat.id,
                     text=lang.get_language('message_search_wait'))
    menu.callback(call, "menu_search_break")

    offers = scraper.get_data(urlc.get_urls())

    if len(offers):
        bot.send_message(call.message.chat.id,
                         text=lang.get_language('message_found_count').format(count=len(offers)))

        for offer in offers:
            if call.data in ["menu_filter", "menu_main"]:
                break
            bot.send_message(
                call.message.chat.id,
                text=lang.get_language('message_offer')
                    .format(title=offer['title'], 
                            url=offer['url_offer'], 
                            price=offer['price'], 
                            location=offer['location']), 
                parse_mode='Markdown')
        else:
            menu.callback(call, "menu_search_finish")
    else:
        bot.send_message(call.message.chat.id,
                         text=lang.get_language('message_not_found'))