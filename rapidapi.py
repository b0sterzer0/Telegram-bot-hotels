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
        try:
            response = requests.request("GET", url, headers=self.headers, params=querystring, timeout=10)
            if response.status_code == 200:  # check request
                return json.loads(response.text)
            elif response.status_code == 400:
                print(f'ERROR: ошибка синтаксиса запроса (400) URL: {url}')
            elif response.status_code == 401:
                print(f'ERROR: ошибка доступа (401) URL: {url}')
            elif response.status_code == 402:
                print(f'ERROR: нестандартная ошибка клиента (402) URL: {url}')
            elif response.status_code == 403:
                print(f'ERROR: ограничение или отсутствие доступа к материалу на странице (403) URL: {url}')
            elif response.status_code == 404:
                print(f'ERROR: ошибка запроса по url: {url} (404)')
        except requests.exceptions.RequestException.Timeout:
            print('ERROR: превышен лимит ожидания ответа')

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
            elif response.status_code == 400:
                print(f'ERROR: ошибка синтаксиса запроса (400) URL: {url}')
            elif response.status_code == 401:
                print(f'ERROR: ошибка доступа (401) URL: {url}')
            elif response.status_code == 402:
                print(f'ERROR: нестандартная ошибка клиента (402) URL: {url}')
            elif response.status_code == 403:
                print(f'ERROR: ограничение или отсутствие доступа к материалу на странице (403) URL: {url}')
            elif response.status_code == 404:
                print(f'ERROR: ошибка запроса по url: {url} (404)')
        except requests.exceptions.RequestException.Timeout:
            print('ERROR: превышен лимит ожиданния ответа')

