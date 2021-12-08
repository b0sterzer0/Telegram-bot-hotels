import rapidapi
from telebot import types
from translate import Translator
from lowprice_and_highprice_commands import lowprice_and_highprice_func

class LowpriceHandlers:
    def __init__(self, bot):
        self.bot = bot
        self.lowprice_data_list = list()
        self.reverse_price = False

    def get_city(self, message) -> None:
        """
        This method is called from main.py. Adds location for search in list and asks number of hotels
        """
        translator = Translator(from_lang="russian", to_lang="english")
        search_location = translator.translate(message.text)
        self.lowprice_data_list.append(search_location)
        msg = self.bot.send_message(message.chat.id,
                                    'Введите количество отелей, которые необходимо вывести (максимум - 15)')
        self.bot.register_next_step_handler(msg, self.get_num_hotels)

    def get_num_hotels(self, message) -> None:
        """
        Next step after get_city. Adds number of hotels in list and asks the need for photos.
        Creates InlineMarkup and attaches to post.
        """
        if int(message.text) <= 15:
            self.lowprice_data_list.append(int(message.text))
            inline_markup = types.InlineKeyboardMarkup()
            answer_yes = types.InlineKeyboardButton('Да', callback_data='photo_answer_yes')
            answer_no = types.InlineKeyboardButton('Нет', callback_data='photo_answer_no')
            inline_markup.add(answer_yes, answer_no)
            msg = self.bot.send_message(message.chat.id, 'Нужно ли выводить фотографии?', reply_markup=inline_markup)
        else:
            self.bot.send_message(message.chat.id, 'Вы превысили лимит отелей!')

    def photo_answer_yes_func(self, message) -> None:
        """
        This method is called from main.py. Calls lowprice_and_highprice.py
        """
        num = message
        if 2 <= int(num.text) <= 10:
            for hotel in lowprice_and_highprice_func(search_location=self.lowprice_data_list[0],
                                          num_hotels=int(self.lowprice_data_list[1]),
                                          photo_answer=True, highprice=self.reverse_price):
                req = rapidapi.MyReqs()
                media_group = req.get_photos(id_hotel=hotel[1], num_photo=int(message.text), describe=hotel[0])
                self.bot.send_media_group(message.chat.id, media=media_group)
                self.lowprice_data_list.clear()
        else:
            self.bot.send_message(message.chat.id, "Вы ввели недопустимое количество фотографий!")
            self.lowprice_data_list.clear()
