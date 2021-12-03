from telebot import types
from translate import Translator

class LowpriceHandlers:
    def __init__(self, bot):
        self.bot = bot
        self.lowprice_data_list = list()
        self.reverse_price = False

    def get_city(self, message):
        translator = Translator(from_lang="russian", to_lang="english")
        search_location = translator.translate(message.text)
        self.lowprice_data_list.append(search_location)
        msg = self.bot.send_message(message.chat.id,
                                    'Введите количество отелей, которые необходимо вывести (максимум - 15)')
        self.bot.register_next_step_handler(msg, self.get_num_hotels)

    def get_num_hotels(self, message):
        if int(message.text) <= 15:
            self.lowprice_data_list.append(int(message.text))
            inline_markup = types.InlineKeyboardMarkup()
            answer_yes = types.InlineKeyboardButton('Да', callback_data='photo_answer_yes')
            answer_no = types.InlineKeyboardButton('Нет', callback_data='photo_answer_no')
            inline_markup.add(answer_yes, answer_no)
            msg = self.bot.send_message(message.chat.id, 'Нужно ли выводить фотографии?', reply_markup=inline_markup)
        else:
            self.bot.send_message(message.chat.id, 'Вы превысили лимит отелей!')
