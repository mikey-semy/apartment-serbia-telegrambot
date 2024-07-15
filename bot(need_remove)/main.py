import os
import random
import telebot

import configparser

config = configparser.ConfigParser()
config.read("messages.ini")

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


# ---------------- dialog params ----------------
dialog = {
    'hello': {
        'in': ['/hello', 'привет', 'hello', 'hi', 'privet', 'hey'],
        'out': ['Приветствую', 'Здравствуйте', 'Привет!']
    },
    'how r u': {
        'in': ['/howru', 'как дела', 'как ты', 'how are you', 'дела', 'how is it going'],
        'out': ['Хорошо', 'Отлично', 'Good. And how are u?']
    },
    'name': {
        'in': ['/name', 'зовут', 'name', 'имя'],
        'out': [
            'Я telegram-template-bot',
            'Я бот шаблон, но ты можешь звать меня в свой проект',
            'Это секрет. Используй команду /help, чтобы узнать'
        ]
    }
}


# --------------------- bot ---------------------
# @bot.message_handler(commands=['help', 'start'])
# def say_welcome(message):
#     user_first_name = str(message.chat.first_name)
#     #bot.reply_to(message, f"Привет! {user_first_name} \n Добро пожаловать!")
#     bot.send_message(message.chat.id,
#                      'Добро пожаловать, ', user_first_name, '!\n',
#                      parse_mode='markdown')

@bot.message_handler(commands=["start"])
def send_start(message):
    username = message.from_user.username
    start_message = config.get("Messages", "start")
    bot.send_message(message.chat.id, start_message.format(username=username))


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(message.chat.id, config.get("Messages", "help"))


@bot.message_handler(func=lambda message: True)
def echo(message):
    for t, resp in dialog.items():
        if sum([e in message.text.lower() for e in resp['in']]):
            bot.send_message(message.chat.id, random.choice(resp['out']))
            return

    bot.send_message(message.chat.id, 'Проблемы?. Воспользуйтесь /help.')


# ---------------- local testing ----------------
if __name__ == '__main__':
    bot.infinity_polling()
