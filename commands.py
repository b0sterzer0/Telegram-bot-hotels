import custom_requests
from urllib.request import urlopen
from xml.etree.ElementTree import fromstring


reqs = custom_requests.MyReqs()

def get_data(search_location: str, price_min=1, price_max=1000, sort_order='NONE'):
    """
    This function gets data from api and returns them in json format
    :param search_location: location for search
    :param price_min: min price for hotels
    :param price_max: max price for hotels
    :param sort_order: the sort order
    """

    # get destination id
    data = reqs.req_to_api(url="https://hotels4.p.rapidapi.com/locations/v2/search",
                           querystring={"query": search_location})  # call method req_to_api from custom_requests.py
    destination = ''
    for place in data["suggestions"][0]["entities"]:
        if place["name"] == search_location.split(', ')[0]:
            destination = place["destinationId"]
            print(destination)

    # search hotels
    data_hotels = reqs.req_to_api(url="https://hotels4.p.rapidapi.com/properties/list",
                                  querystring={"destinationId": destination, "currency": "USD", "priceMin": price_min,
                                               "priceMax": price_max, "landmarkIds": "City center",
                                               "sortOrder": sort_order})  # call method req_to_api from custom_requests.py
    
    return data_hotels
    

def lowprice_and_highprice_func(location: str, command_name: str) -> list:
    """
    This function This function implements the functionality of the commands lowprice and highprice
    :param location: location for search
    :param command_name: name of command (lowprice or highprice)
    :return: sorted list of hotels
    """

    # get data from api
    hotels_data_from_api = ''
    if command_name == 'lowprice':
        hotels_data_from_api = get_data(search_location=location, sort_order='PRICE')
    elif command_name == 'highprice':
        hotels_data_from_api = get_data(search_location=location, sort_order='PRICE_HIGHEST_FIRST')

    # check data
    hotels_list = list()
    if hotels_data_from_api["data"]["body"]["searchResults"]["results"]:
        for hotel in hotels_data_from_api["data"]["body"]["searchResults"]["results"]:
            if "ratePlan" in hotel.keys():
                hotels_list.append((hotel["ratePlan"]["price"]["current"], hotel))

    return hotels_list

 
def bestdeal_func(location: str, distance_range: list, price_range: list) -> list:
    """
    This function This function implements the functionality of the command bestdeal
    :param location: location for search
    :param distance_range: min and max distance from city center
    :param price_range: min and max current price
    :return: list of hotels
    """
    hotels_list = list()

    # get data from api
    hotels_data_from_api = get_data(search_location=location, price_min=price_range[0], price_max=price_range[1],
                                    sort_order="DISTANCE_FROM_LANDMARK")

    # check and select data
    for hotel in hotels_data_from_api["data"]["body"]["searchResults"]["results"]:
        distance = float(hotel["landmarks"][0]["distance"].split()[0])
        if distance_range[0] <= distance <= distance_range[1]:
            if "ratePlan" in hotel.keys():
                hotels_list.append((hotel["ratePlan"]["price"]["current"], hotel))

    return hotels_list


def main_generator(data_dict: dict, bot, chat_id) -> str:
    """
    Generator.From here, the rest of the module's functions are launched.
    Collect all data about hotels and returns string with data about each hotel at each step
    :param data_dict: a dictionary with user data passed from the handlers.py
    :param bot: bot from main.py
    :param chat_id: id for bot.send_message
    """

    hotels_list = list()

    # select function
    if data_dict["command_name"] == 'lowprice' or data_dict["command_name"] == 'highprice':
        hotels_list = lowprice_and_highprice_func(location=data_dict["search_location"],
                                                  command_name=data_dict["command_name"])
    elif data_dict["command_name"] == 'bestdeal':
        hotels_list = bestdeal_func(location=data_dict["search_location"], distance_range=data_dict["distance_range"],
                                    price_range=data_dict[
            "price_range"
        ])

    # check returned data
    if not hotels_list:
        bot.send_message(chat_id, 'К сожалению, по вашим критериям ничего не найдено')

    point = 0
    for hotel in hotels_list:
        # address constructor
        if point != data_dict["num_hotels"]:
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

            # get distance from city center
            distance_from_center = ''

            if hotel[1]["landmarks"]:
                for landmark in hotel[1]["landmarks"]:
                    if landmark["label"] == "City center":
                        distance_from_center = round(float(landmark["distance"].split()[0]) * 1.6, 2)

            # result string with info about hotel for return
            price = reqs.currency_converter([hotel[0][1:]], "USD/RUB")[0]
            r_data_tuple = ({
                "hotel_name": f'Название отеля: {hotel[1]["name"]}\n',
                "address": f'Адресс: {" ".join(full_address)}\n',
                "distance_from_center": f'Расположение от центра: {distance_from_center} км.\n',
                "price": f'Цена: {price} руб./сутки'
                            }, hotel[1]["id"])
            point += 1
            yield r_data_tuple
