import rapidapi
from telebot import types
from translate import Translator
from lowprice_and_highprice_commands import lowprice_and_highprice_func
from bestdeal_command import bestdeal_command_func

class LowpriceHandlers:
    def __init__(self, bot):
        self.bot = bot
        self.data_list = list()
        self.reverse_price = False

    def price_range(self, message) -> None:
        """
        This method call from main.py. Adds in list price range and asks distance range
        """
        self.data_list.append([float(num) for num in message.text.split('-')])
        msg = self.bot.send_message(message.chat.id,
                                    'Введите диапозон расстояния от центра в формате цифра-цифра')
        self.bot.register_next_step_handler(msg, self.distance_range)

    def distance_range(self, message) -> None:
        """
        Next step after price_range. This method adds distance range in list and asks location for search
        """
        self.data_list.append([float(num) for num in message.text.split('-')])
        msg = self.bot.send_message(message.chat.id,
                                    'Введите город и страну, где будет проводиться поиск в формате Город, Страна')
        self.bot.register_next_step_handler(msg, self.get_city)
        
    def get_city(self, message) -> None:
        """
        This method is called from main.py. Adds location for search in list and asks number of hotels
        """
        translator = Translator(from_lang="russian", to_lang="english")
        search_location = translator.translate(message.text)
        self.data_list.append(search_location)
        msg = self.bot.send_message(message.chat.id,
                                    'Введите количество отелей, которые необходимо вывести (максимум - 15)')
        self.bot.register_next_step_handler(msg, self.get_num_hotels)

    def get_num_hotels(self, message) -> None:
        """
        Next step after get_city. Adds number of hotels in list and asks the need for photos.
        Creates InlineMarkup and attaches to post.
        """
        if int(message.text) <= 15:
            self.data_list.append(int(message.text))
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
            if self.data_list[0] == 'lowprice' or self.data_list[0] == 'highprice':
                for hotel in lowprice_and_highprice_func(search_location=self.data_list[1],
                                              num_hotels=int(self.data_list[2]),
                                              command_name=self.data_list[0]):
                    if hotel is None:
                        print('ERROR: возвращен объект None')
                    else:
                        req = rapidapi.MyReqs()
                        media_group = req.get_photos(id_hotel=hotel[1], num_photo=int(message.text), describe=hotel[0])
                        self.bot.send_media_group(message.chat.id, media=media_group)
            elif self.data_list[0] == 'bestdeal':
                pass
        else:
            self.bot.send_message(message.chat.id, "Вы ввели недопустимое количество фотографий!")
        self.data_list.clear()
