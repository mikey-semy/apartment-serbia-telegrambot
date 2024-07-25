import os
import telebot
from menu import CreateMenu
from language import SelectLanguage
from filter import UrlBuilder
from scraper import CommonScraper

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
lang = SelectLanguage()
menu = CreateMenu(bot, lang)

# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if "menu" in call.data:

        menu.callback(call)

    elif "action" in call.data:
            
            if call.data == "action_ru":
                handle_language_selection(call, "ru")             
            elif call.data == "action_en":
                handle_language_selection(call, "en")
            elif call.data == "beograd":
                handle_city_selection(call, "beograd")
            elif call.data == "novi_sad":
                handle_city_selection(call, "novi_sad")
            elif call.data == "nis":
                handle_city_selection(call, "nis")
            elif call.data == "apartaments":
                handle_type_selection(call, "apartaments")
            elif call.data == "houses":
                handle_type_selection(call, "houses")
            elif call.data == "from_area":
                handle_area_selection(call, "from_area")
            elif call.data == "to_area":
                handle_area_selection(call, "to_area")
            elif call.data == "from_price":
                handle_type_selection(call, "from_price")
            elif call.data == "to_price":
                handle_type_selection(call, "to_price")
            elif call.data == "action_search":
                handle_search_selection(call)
            else:
                 print(f"Unknown action callback data: {call.data}")
    else:
        print(f"Unknown menu callback data: {call.data}")

@bot.message_handler(commands=['start'])
def start(message):
    # Установка языка по-умолчанию (из настроек пользователя)
    lang.set_language(message.from_user.language_code)
    # Создание главного меню
    menu.create_menu(message)

# Функция для обработки языкового выбора
def handle_language_selection(call, language):
    lang.set_language(language)
    menu.callback(call, "menu_change_language")
    #menu.callback(call, "menu_main")

def handle_city_selection(call, city):
    pass

def handle_type_selection(call, type):
    pass

def handle_rooms_selection(call, rooms):
    pass

def handle_area_selection(call, area):
    pass

def handle_price_selection(call, price):
    pass

def handle_search_selection(call):
    #urlNekretnine = UrlBuilder("https://www.nekretnine.rs", path_style=True)
    #urlFourzida = UrlBuilder("https://www.4zida.rs", path_style=True)
    #urlCityexpert = UrlBuilder("https://cityexpert.rs", path_style=True)

    urlNekretnine = 'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/grad/beograd/lista/po-stranici/10/'
    #urlFourzida = 'https://www.4zida.rs/prodaja-stanova/beograd/garsonjera/vlasnik/do-100000-evra?struktura=jednosoban&struktura=jednoiposoban&struktura=dvosoban&struktura=dvoiposoban&struktura=trosoban&vece_od=10m2&manje_od=60m2&skuplje_od=1000eur'
    #urlCityexpert = 'https://cityexpert.rs/prodaja-nekretnina/beograd?ptId=2,1&minPrice=10000&maxPrice=300000&minSize=10&maxSize=60&bedroomsArray=r1'
    urls = [urlNekretnine]#, urlFourzida, urlCityexpert]
    scraper = CommonScraper()
    offers = scraper.get_data(urls)

if __name__ == "__main__":
    bot.polling(none_stop=True)



# @bot.message_handler(content_types=['text'])
# def check_subscriptions(message):
#     subscribed_channels = ["@MikeDaily"]
#     for channel_id in subscribed_channels:
#         chat_member = bot.get_chat_member(channel_id, message.from_user.id)
#         if chat_member.status in ['member', 'creator', 'administrator']:
#             subscribed_channels.append(channel_id)
#     if subscribed_channels:
#         bot.send_message(message.chat.id, f'You are subscribed to the following channels: {", ".join(subscribed_channels)}')
#     else:
#         bot.send_message(message.chat.id, 'You are not subscribed to any of the channels.')