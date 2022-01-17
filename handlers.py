import custom_requests
import re
import history
from telebot import types
from translate import Translator
from commands import main_generator


reqs = custom_requests.MyReqs()

class MainHandlers:
    def __init__(self, bot):
        self.bot = bot
        self.data_dict = dict()
        self.reverse_price = False

    def price_range(self, message) -> None:
        """
        This method call from main.py. Adds in list price range and asks distance range
        """
        price_list = re.findall(r'\d+', message.text)
        self.data_dict["price_range"] = [num for num in
                                         reqs.currency_converter(price_nums_list=price_list, mod="RUB/USD")]
        msg = self.bot.send_message(message.chat.id,
                                    'Введите диапозон расстояния от центра (в метрах):')
        self.bot.register_next_step_handler(msg, self.distance_range)

    def distance_range(self, message) -> None:
        """
        Next step after price_range. This method adds distance range in list and asks location for search
        """
        range_list = re.findall(r'\d+', message.text)
        self.data_dict["distance_range"] = [round(float(num) / 1000 / 1.6, 2) for num in range_list]
        msg = self.bot.send_message(message.chat.id,
                                    'Введите город и страну, где будет проводиться поиск в формате Город, Страна')
        self.bot.register_next_step_handler(msg, self.get_city)
        
    def get_city(self, message) -> None:
        """
        This method is called from main.py. Adds location for search in list and asks number of hotels
        """
        translator = Translator(from_lang="russian", to_lang="english")
        search_location = translator.translate(message.text)
        self.data_dict["search_location"] = search_location
        msg = self.bot.send_message(message.chat.id,
                                    'Введите количество отелей, которые необходимо вывести (максимум - 15)')
        self.bot.register_next_step_handler(msg, self.get_num_hotels)

    def get_num_hotels(self, message) -> None:
        """
        Next step after get_city. Adds number of hotels in list and asks the need for photos.
        Creates InlineMarkup and attaches to post.
        """
        if int(message.text) <= 15:
            self.data_dict["num_hotels"] = int(message.text)
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
        all_hotels_info = list()
        if 2 <= int(num.text) <= 10:
            for hotel in main_generator(self.data_dict, bot=self.bot, chat_id=message.chat.id):
                hotel_data = "".join(hotel[0].values())
                all_hotels_info.append(hotel[0])
                media_group = reqs.get_photos(id_hotel=hotel[1], num_photo=int(message.text), describe=hotel_data)
                self.bot.send_media_group(message.chat.id, media=media_group)

            data_for_history = [all_hotels_info, self.data_dict["command_name"]]
            history.add_instance(data_for_history)
        else:
            self.bot.send_message(message.chat.id, "Вы ввели недопустимое количество фотографий!"
                                                   " Введите комманду заново.")
        self.data_dict.clear()
