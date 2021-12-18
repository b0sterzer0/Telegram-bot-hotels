import rapidapi


def bestdeal_command_func(search_location: str, num_hotels: int, distance_range: list, price_range: list) -> str:
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
    data_hotels = reqs.req_to_api(url="https://hotels4.p.rapidapi.com/properties/list", querystring={
                                        "destinationId": destination})  # call method req_to_api from rapidapi.py
    if data_hotels is None:
        return None
    else:
        print('ok2')

    hotels_list = list()

    if data_hotels["data"]["body"]["searchResults"]["results"]:
        for hotel in data_hotels["data"]["body"]["searchResults"]["results"]:
            if hotel["landmarks"] and hotel["ratePlan"]["price"]["current"]:
                for elem in hotel["landmarks"]:
                    e_keys = list(elem.keys())
                    if elem[e_keys[0]] == "City center" and elem[e_keys[1]] == "distance":
                        distance = float(distance_range.split()[0])
                        price = float(hotel["ratePlan"]["price"]["current"][1:])
                        if distance_range[0] <= distance <= distance_range[1] and price_range[0] <= price <= price_range[1]:
                            hotels_list.append((distance, price, hotel))
    
    print(hotels_list)

    point = 0
    for hotel in hotels_list:
        if point != num_hotels:
            address = hotel[-1]["address"]
            full_address = list()
            if "postalCode" in address.keys():
                full_address.append(address["postalCode"])
            if "streetAddress" in address.keys():
                full_address.append(address["streetAddress"])
            if "locality" in address.keys():
                full_address.append(address["locality"])
            if "region" in address.keys():
                full_address.append(address["region"])
    
            r_data_str = (f'\nНазвание отеля: {hotel[1]["name"]}\nАдресс: {" ".join(full_address)}\nЦена: {hotel[1]}\n'
                          f'Расстояние до центра: {hotel[0]}',
                          hotel[-1]["id"])
            print(r_data_str)
            point += 1
            yield r_data_str
