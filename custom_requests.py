import requests
import json
from telebot import types
from dotenv import dotenv_values
from requests import exceptions
from urllib.request import urlopen
from xml.etree.ElementTree import fromstring


class MyReqs:
    def __init__(self) -> None:
        self.headers = {
            'x-rapidapi-host': "hotels4.p.rapidapi.com",
            'x-rapidapi-key': dotenv_values(".env")["APIKey"]
        }

    def req_to_api(self, url: str, querystring: dict):
        """
        This method finds and returns json data with the requested information
        :param url: url for search
        :param querystring: data for search
        :return: data in format JSON
        """
        try:
            response = requests.request("GET", url, headers=self.headers, params=querystring, timeout=10)
            if response.status_code == 200:  # check request
                if response is not None:
                    return json.loads(response.text)
                else:
                    raise ValueError('Запрос к api вернул пустой объект')
            else:
                raise ValueError(f'Неудачный запрос к api (ошибка {response.status_code})')
        except exceptions.ConnectTimeout:
            raise RuntimeError('Превышено время ожидания ответа на запрос')

    def get_photos(self, id_hotel, num_photo, describe):
        """
        This method finds photos and returns data in format InputMediaPhoto
        :param id_hotel: hotel's id
        :param num_photo: number of photos
        :param describe: information about hotel
        :return: list of InputMediaPhoto
        """
        url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
        querystring = {"id": int(id_hotel)}
        try:
            response = requests.request("GET", url, headers=self.headers, params=querystring, timeout=10)
            if response.status_code == 200:  # check request
                if response is not None:
                    data = json.loads(response.text)
                    return_data = list()
                    point = 0
                    for photo_data in data["hotelImages"]:
                        if point != num_photo:
                            if point == 0:
                                url_list = photo_data["baseUrl"].split('{size}')
                                url_str = url_list[0] + 'z' + url_list[1]
                                return_data.append(types.InputMediaPhoto(url_str, caption=describe))
                                point += 1
                            else:
                                url_list = photo_data["baseUrl"].split('{size}')
                                url_str = url_list[0] + 'z' + url_list[1]
                                return_data.append(types.InputMediaPhoto(url_str))
                                point += 1
                    return return_data
                else:
                    raise ValueError('Запрос к api вернул пустой объект')
            else:
                raise ValueError(f'Неудачный запрос к api (ошибка {response.status_code})')
        except exceptions.ConnectTimeout:
            raise RuntimeError('Превышено время ожидания ответа на запрос')

    def currency_converter(self, price_nums_list: list, mod: str):
        response = urlopen('https://www.cbr-xml-daily.ru/daily_utf8.xml')
        xml_tree = fromstring(response.read())
        result = [float(price.text.replace(',', '.'))
                  for name, price in zip(xml_tree.iter('Name'), xml_tree.iter('Value'))
                  if name.text == 'Доллар США']

        r_list = list()
        for price_num in price_nums_list:
            if mod == "RUB/USD":
                r_list.append(int(float(price_num) / result[0]))
            elif mod == "USD/RUB":
                r_list.append(int(float(price_num) * result[0]))

        return r_list
