import requests
import json
from telebot import types
from dotenv import dotenv_values


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
        response = requests.request("GET", url, headers=self.headers, params=querystring, timeout=10)
        if response.status_code: #check request
            return json.loads(response.text)
        else:
            print(f'ERROR: ошибка запроса по url: {url}')

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
        response = requests.request("GET", url, headers=self.headers, params=querystring, timeout=10)
        if response.status_code:  # check request
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
            print(f'ERROR: ошибка запроса по url: {url}')

