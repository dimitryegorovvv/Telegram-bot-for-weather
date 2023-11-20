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
                                      'погоде напишите название необходимого города или страны')
@bot.message_handler(content_types=['text'])
def weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&exclude=hourly,daily&appid={api}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = str(int(data['main']['temp']))
        feels_like = str(int(data['main']['feels_like']))
        humidity = str(int(data['main']['humidity']))
        wind_speed = str(int(data['wind']['speed']))
        clouds = str(int(data['clouds']['all']))
        if temp[0] == '-' and temp[1] == '0':
            temp = 0
        bot.send_message(message.chat.id, f'сейчас в "{city}" {temp} °C\n'
                                          f'ощущается как {feels_like} °C\n'
                                          f'влажность {humidity}%\n'
                                          f'скорость ветра {wind_speed} м/с\n'
                                          f'облачность {clouds}%')
    else:
        bot.send_message(message.chat.id, 'вы указали неверное название города,'
                                          ' либо его нету в базе')

bot.polling(none_stop = True)
