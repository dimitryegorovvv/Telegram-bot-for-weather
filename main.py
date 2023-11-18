import telebot
import requests
import json

from token_file import token
from api import api
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name},'
                                      ' для получения сведений о '
                                      'погоде напишите название необходимого города')

@bot.message_handler(content_types=['text'])
def weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric')
    data = json.load(res.text)
    bot.send_message(message.chat.id, f'Сейчас в городе "{city}" {res.json()} градусов')


bot.polling(none_stop = True)