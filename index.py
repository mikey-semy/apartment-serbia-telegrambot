import telebot
from main import bot # Да, временно без папки, когда на самом деле в папке.

def handler(event, _):
    message = telebot.types.Update.de_json(event['body'])
    bot.process_new_updates([message])
    return {
        'statusCode': 200,
        'body': '!',
    }
