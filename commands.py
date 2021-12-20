import rapidapi


def get_data(search_location: str):
    """
    This function gets data from api and returns them in json format
    :param search_location: location for search
    """
    reqs = rapidapi.MyReqs()

    # get destination id
    data = reqs.req_to_api(url="https://hotels4.p.rapidapi.com/locations/v2/search",
                           querystring={"query": search_location})  # call method req_to_api from rapidapi.py
    destination = ''
    for place in data["suggestions"][0]["entities"]:
        if place["name"] == search_location.split(', ')[0]:
            destination = place["destinationId"]
            print(destination)

    # search hotels
    data_hotels = reqs.req_to_api(url="https://hotels4.p.rapidapi.com/properties/list",
                                  querystring={"destinationId": destination})  # call method req_to_api from rapidapi.py
    
    return data_hotels
    

def lowprice_and_highprice_func(data, command_name: str) -> list:
    """
    This function This function implements the functionality of the commands lowprice and highprice
    :param data: json data from api
    :param command_name: name of command (lowprice or highprice)
    :return: sorted list of hotels
    """
    unsorted_hotels_list = list()
    hotels_list = list()
    if data["data"]["body"]["searchResults"]["results"]:
        for hotel in data["data"]["body"]["searchResults"]["results"]:
            if "ratePlan" in hotel.keys():
                unsorted_hotels_list.append((hotel["ratePlan"]["price"]["current"], hotel))

        if command_name == 'lowprice':
            hotels_list = sorted(unsorted_hotels_list, key=lambda elem: elem[0])  # sort by price
        elif command_name == 'highprice':
            hotels_list = sorted(unsorted_hotels_list, key=lambda elem: elem[0], reverse=True)
    
    return hotels_list

 
def bestdeal_func(data, distance_range: list, price_range: list) -> list:
    """
    This function This function implements the functionality of the command bestdeal
    :param data: json data from api
    :param distance_range: min and max distance from city center
    :param price_range: min and max current price
    :return: list of hotels
    """
    hotels_list = list()

    if data["data"]["body"]["searchResults"]["results"]:
        for hotel in data["data"]["body"]["searchResults"]["results"]:
            if hotel["landmarks"] and hotel["ratePlan"]["price"]["current"]:
                for elem in hotel["landmarks"]:
                    e_keys = list(elem.keys())
                    if elem[e_keys[0]] == "City center":
                        distance = round(float(elem["distance"].split()[0]) * 1.6, 2)
                        price = float(hotel["ratePlan"]["price"]["current"][1:])
                        if distance_range[0] <= distance <= distance_range[1] and price_range[0] <= price <= \
                                price_range[1]:
                            hotels_list.append((price, hotel))

    return hotels_list


def main_generator(data_dict: dict) -> str:
    """
    Generator.From here, the rest of the module's functions are launched.
    Collect all data about hotels and returns string with data about each hotel at each step
    :param data_dict: a dictionary with user data passed from the handlers.py
    """
    hotels_data = get_data(data_dict["search_location"])
    hotels_list = list()
    
    if data_dict["command_name"] == 'lowprice' or data_dict["command_name"] == 'highprice':
        hotels_list = lowprice_and_highprice_func(data=hotels_data, command_name=data_dict["command_name"])
    elif data_dict["command_name"] == 'bestdeal':
        hotels_list = bestdeal_func(data=hotels_data, distance_range=data_dict["distance_range"], price_range=data_dict[
            "price_range"
        ])
    
    if hotels_list is None:
        return 'NORESULTS'
    
    point = 0
    for hotel in hotels_list:
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

            distance_from_center = ''

            if hotel[1]["landmarks"]:
                for landmark in hotel[1]["landmarks"]:
                    if landmark["label"] == "City center":
                        distance_from_center = round(float(landmark["distance"].split()[0]) * 1.6, 2)

            r_data_str = (f'\nНазвание отеля: {hotel[1]["name"]}\nАдресс: {" ".join(full_address)}'
                          f'\nРасположение от центра: {distance_from_center} км.\nЦена: {hotel[0]}',
                          hotel[1]["id"])
            point += 1
            yield r_data_str
