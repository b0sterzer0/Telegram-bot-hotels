import rapidapi


def lowprice_and_highprice_func(search_location: str, num_hotels: int, photo_answer: bool = False,
                                highprice: bool = False) -> str:
    """
    This generator finds the cheapest hotels
    :param search_location: str -> location to search
    :param num_hotels: int -> number of hotels
    :param photo_answer: bool -> need photos
    :yield: information about each hotel
    """

    reqs = rapidapi.MyReqs()

    # get destination id
    data = reqs.req_to_api(url="https://hotels4.p.rapidapi.com/locations/v2/search",
                              querystring={"query": search_location})
    destination = ''
    for place in data["suggestions"][0]["entities"]:
        if place["name"] == search_location.split(', ')[0]:
            destination = place["destinationId"]
            print(destination)

    # search hotels
    data_hotels = reqs.req_to_api(url="https://hotels4.p.rapidapi.com/properties/list",
                                                 querystring={"destinationId": destination})
    unsorted_hotels_list = list()
    for hotel in data_hotels["data"]["body"]["searchResults"]["results"]:
        if "ratePlan" in hotel.keys():
            unsorted_hotels_list.append((hotel["ratePlan"]["price"]["current"], hotel))

    if highprice is False:
        hotels_list = sorted(unsorted_hotels_list, key=lambda elem: elem[0])  #sort by price
    else:
        hotels_list = sorted(unsorted_hotels_list, key=lambda elem: elem[0], reverse=True)

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

            r_data_str = (f'\nНазвание отеля: {hotel[1]["name"]}\nАдресс: {" ".join(full_address)}\nЦена: {hotel[0]}',
                          hotel[1]["id"])
            point += 1
            yield r_data_str
