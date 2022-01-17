import telebot
import handlers
import history
from commands import main_generator
from dotenv import load_dotenv, dotenv_values


load_dotenv()
TOKEN = dotenv_values(".env")["TOKEN"]
bot = telebot.TeleBot(TOKEN)
handlers = handlers.MainHandlers(bot=bot)

history.start_db()


@bot.message_handler(commands=['start'])
def say_hi(message) -> None:
    bot.send_message(message.chat.id, 'Привет. Я бот, помогающий искать отели по всему миру.\n'
                                      'Введи команду /help, чтобы ознакомиться с функционалом')


@bot.message_handler(commands=['help'])
def help_func(message):
    r_str = 'В данном боте содержится следующий функционал:\n\n' \
            '/lowprice - вывести список самых дешевых отелей в выбранной местности\n' \
            '/highprice - вывести список самых дорогих отелей в выбранной местности\n' \
            '/bestdeal - вывести список отелей, наиболее подходящих по цене и расположению от центра\n' \
            '/history - вывести историю поиска\n'

    bot.send_message(message.chat.id, r_str)

@bot.message_handler(commands=['lowprice'])
def lowprice_func(message) -> None:
    handlers.data_dict["command_name"] = 'lowprice'
    msg = bot.send_message(message.chat.id, 'Введите город и страну, где будет проводиться поиск (Город, Страна)')
    bot.register_next_step_handler(msg, handlers.get_city)


@bot.message_handler(commands=['highprice'])
def highprice_func(message) -> None:
    handlers.data_dict["command_name"] = 'highprice'
    handlers.reverse_price = True
    msg = bot.send_message(message.chat.id, 'Введите город и страну, где будет проводиться поиск (Город, Страна)')
    bot.register_next_step_handler(msg, handlers.get_city)


@bot.message_handler(commands=['bestdeal'])
def bestdeal_func(message) -> None:
    handlers.data_dict["command_name"] = 'bestdeal'
    msg = bot.send_message(message.chat.id, 'Введите ценовой диапазон (в руб.):')
    bot.register_next_step_handler(msg, handlers.price_range)


@bot.message_handler(commands=['history'])
def history_func(message) -> None:
    for log_data in history.get_history_data_generator():
        bot.send_message(message.chat.id, log_data)


@bot.callback_query_handler(func=lambda call: True)
def answer(call) -> None:
    if call.data == 'photo_answer_yes':
        if handlers.data_dict["command_name"] == 'highprice':
            handlers.reverse_price = True
        msg = bot.send_message(call.message.chat.id, 'Введите количество фотографий (от 2 до 10):')
        bot.register_next_step_handler(msg, handlers.photo_answer_yes_func)
    elif call.data == 'photo_answer_no':
        all_hotels_info = list()
        for hotel in main_generator(handlers.data_dict, bot=bot, chat_id=call.message.chat.id):
            hotel_data = "".join(hotel[0].values())
            all_hotels_info.append(hotel[0])
            bot.send_message(call.message.chat.id, hotel_data)

        data_for_history = [all_hotels_info, handlers.data_dict["command_name"]]
        history.add_instance(data_for_history)
        handlers.data_dict.clear()


bot.polling(none_stop=True)
