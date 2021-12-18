import telebot
import handlers
from lowprice_and_highprice_commands import lowprice_and_highprice_func
from bestdeal_command import bestdeal_command_func
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
    handlers.data_list.append('lowprice')
    msg = bot.send_message(message.chat.id, 'Введите город и страну, где будет проводиться поиск (Город, Страна)')
    bot.register_next_step_handler(msg, handlers.get_city)


@bot.message_handler(commands=['highprice'])
def highprice_func(message):
    handlers.data_list.append('highprice')
    handlers.reverse_price = True
    msg = bot.send_message(message.chat.id, 'Введите город и страну, где будет проводиться поиск (Город, Страна)')
    bot.register_next_step_handler(msg, handlers.get_city)


@bot.message_handler(commands=['bestdeal'])
def bestdeal_func(message):
    handlers.data_list.append('bestdeal')
    msg = bot.send_message(message.chat.id, 'Введите ценовой диапазон в формате мин. цена - макс. цена')
    bot.register_next_step_handler(msg, handlers.price_range)


@bot.callback_query_handler(func=lambda call: True)
def answer(call) -> None:
    if call.data == 'photo_answer_yes':
        if handlers.data_list[0] == 'highprice':
            handlers.reverse_price = True
        msg = bot.send_message(call.message.chat.id, 'Введите количество фотографий (от 2 до 10):')
        bot.register_next_step_handler(msg, handlers.photo_answer_yes_func)
    elif call.data == 'photo_answer_no':
        if handlers.data_list[0] == 'lowprice' or handlers.data_list[0] == 'highprice':
            for hotel in lowprice_and_highprice_func(search_location=handlers.data_list[1],
                                          num_hotels=int(handlers.data_list[2]),
                                          command_name=handlers.data_list[0]):
                if hotel is None:
                    print('ERROR: возвращен объект None')
                else:
                    bot.send_message(call.message.chat.id, hotel[0])
        elif handlers.data_list[0] == 'bestdeal':
            for hotel in bestdeal_command_func(price_range=handlers.data_list[1],
                                               distance_range=handlers.data_list[2],
                                               search_location=handlers.data_list[3],
                                               num_hotels=handlers.data_list[4]):
                if hotel is None:
                    print('ERROR: возвращен объект None')
                else:
                    bot.send_message(call.message.chat.id, hotel[0])
        handlers.data_list.clear()


bot.polling(none_stop=True)
