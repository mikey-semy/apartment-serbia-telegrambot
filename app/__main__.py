import logging
from datetime import datetime
from pathlib import Path


import telebot

from app import TOKEN
from app.handlers import *

def main():
    
    log_name = f'logs/{datetime.now().strftime("%Y-%m-%d")}.log'
    Path(log_name).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        filename=log_name,
        filemode="a"
    )

    bot = telebot.TeleBot(TOKEN)

    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
    