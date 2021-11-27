import telebot
from telebot import types

TOKEN = '2134033552:AAFZu00_lp2A7V2G-BKibLbjPpAhrONgOWk'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def say_hi(message):
    bot.send_message(message.chat.id, 'Привет. Я твой первый серьезный бот.')


bot.polling(none_stop=True)
