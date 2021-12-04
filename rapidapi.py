import requests
import json
import typing
from telebot import types


class MyReqs:
    def __init__(self) -> None:
        self.headers = {
            'x-rapidapi-host': "hotels4.p.rapidapi.com",
            'x-rapidapi-key': "0c4ebc1103msh46651525254b0d1p1a9a88jsn1c30f4590217"
        }

    def req_to_api(self, url: str, querystring: dict):
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        return json.loads(response.text)

    def get_photos(self, id_hotel, num_photo, describe):
        url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
        querystring = {"id": int(id_hotel)}
        response = requests.request("GET", url, headers=self.headers, params=querystring)
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
        print(return_data)
        return return_data
