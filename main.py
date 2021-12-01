import telebot
from lowprice_command import lowprice_command
from telebot import types

TOKEN = '2134033552:AAFZu00_lp2A7V2G-BKibLbjPpAhrONgOWk'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def say_hi(message) -> None:
    bot.send_message(message.chat.id, 'Привет. Я бот, помогающий искать отели по всему миру')


@bot.message_handler(commands=['lowprice'])
def start_func(message) -> None:
    msg = bot.send_message(message.chat.id, 'Введите город и страну, где будет проводиться поиск (Город, Страна)')
    bot.register_next_step_handler(msg, input_num)


lowprice_data_list = list()


def input_num(message) -> None:
    lowprice_data_list.append(message.text)
    msg = bot.send_message(message.chat.id, 'Введите количество отелей, которые необходимо вывести (максимум - 15)')
    bot.register_next_step_handler(msg, input_num_hotels)


def input_num_hotels(message) -> None:
    if int(message.text) <= 15:
        lowprice_data_list.append(int(message.text))
        inline_markup = types.InlineKeyboardMarkup()
        answer_yes = types.InlineKeyboardButton('Да', callback_data='photo_answer_yes')
        answer_no = types.InlineKeyboardButton('Нет', callback_data='photo_answer_no')
        inline_markup.add(answer_yes, answer_no)
        msg = bot.send_message(message.chat.id, 'Нужно ли выводить фотографии?', reply_markup=inline_markup)
    else:
        bot.send_message(message.chat.id, 'Вы превысили лимит отелей!')


@bot.callback_query_handler(func=lambda call: True)
def answer(call) -> None:
    if call.data == 'photo_answer_yes':
        for hotel in lowprice_command(search_location=lowprice_data_list[0], num_hotels=int(lowprice_data_list[1]),
                                      photo_answer=True):
            bot.send_message(call.message.chat.id, hotel)
        lowprice_data_list.clear()
    elif call.data == 'photo_answer_no':
        for hotel in lowprice_command(search_location=lowprice_data_list[0], num_hotels=int(lowprice_data_list[1])):
            bot.send_message(call.message.chat.id, hotel)
        lowprice_data_list.clear()


bot.polling(none_stop=True)
