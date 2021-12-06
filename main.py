import telebot
import handlers
from lowprice_and_highprice_commands import lowprice_and_highprice_func
from dotenv import load_dotenv, dotenv_values


load_dotenv()
TOKEN = dotenv_values(".env")["TOKEN"]
bot = telebot.TeleBot(TOKEN)
handlers = handlers.LowpriceHandlers(bot=bot)


@bot.message_handler(commands=['start'])
def say_hi(message) -> None:
    bot.send_message(message.chat.id, 'Привет. Я бот, помогающий искать отели по всему миру')


@bot.message_handler(commands=['lowprice'])
def lowprice_func(message) -> None:
    msg = bot.send_message(message.chat.id, 'Введите город и страну, где будет проводиться поиск (Город, Страна)')
    bot.register_next_step_handler(msg, handlers.get_city)


@bot.message_handler(commands=['highprice'])
def highprice_func(message):
    handlers.reverse_price = True
    msg = bot.send_message(message.chat.id, 'Введите город и страну, где будет проводиться поиск (Город, Страна)')
    bot.register_next_step_handler(msg, handlers.get_city)


@bot.callback_query_handler(func=lambda call: True)
def answer(call) -> None:
    if call.data == 'photo_answer_yes':
        msg = bot.send_message(call.message.chat.id, 'Введите количество фотографий (от 2 до 10):')
        bot.register_next_step_handler(msg, handlers.photo_answer_yes_func)
    elif call.data == 'photo_answer_no':
        for hotel in lowprice_and_highprice_func(search_location=handlers.data_list[0],
                                      num_hotels=int(handlers.data_list[1]),
                                      highprice=handlers.reverse_price):
            bot.send_message(call.message.chat.id, hotel[0])
        handlers.data_list.clear()


bot.polling(none_stop=True)
