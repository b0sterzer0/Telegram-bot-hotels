import requests
import json
from translate import Translator

print('Я перешел')


def lowprice_command(search_location: str, num_hotels: int, photo_answer: bool = False) -> str:
    """
    This generator finds the cheapest hotels
    :param search_location: str -> location to search
    :param num_hotels: int -> number of hotels
    :param photo_answer: bool -> need photos
    :yield: information about each hotel
    """

    translator = Translator(from_lang="russian", to_lang="english")
    search_location = translator.translate(search_location)

    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": search_location}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "0c4ebc1103msh46651525254b0d1p1a9a88jsn1c30f4590217"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)

    destination = ''

    #get destination id
    for place in data["suggestions"][0]["entities"]:
        if place["name"] == search_location.split(', ')[0]:
            destination = place["destinationId"]

    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": destination}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data_hotels = json.loads(response.text)

    #search hotels
    start_hotels_list = list()
    for hotel in data_hotels["data"]["body"]["searchResults"]["results"]:
        start_hotels_list.append((hotel["ratePlan"]["price"]["current"], hotel))

    hotels_list = sorted(start_hotels_list, key=lambda elem: elem[0]) #sort by price

    #construct answer and return it
    point = 0
    for hotel in hotels_list:
        if point != num_hotels:
            address = hotel[1]["address"]
            full_address = list()
            if "postalCode" in address.keys():
                full_address.append(address["postalCode"])
            if "streetAddress" in address.keys():
                full_address.append(address["streetAddress"])
            if "locality" in address.keys():
                full_address.append(address["locality"])
            if "region" in address.keys():
                full_address.append(address["region"])

            r_data_str = f'\nНазвание отеля: {hotel[1]["name"]}\nАдресс: {" ".join(full_address)}\nЦена: {hotel[0]}'
            point += 1
            yield r_data_str
        else:
            break
