import requests
import json
import typing


class my_reqs:
    def __init__(self) -> None:
        self.headers = {
            'x-rapidapi-host': "hotels4.p.rapidapi.com",
            'x-rapidapi-key': "0c4ebc1103msh46651525254b0d1p1a9a88jsn1c30f4590217"
        }

    def req_to_api(self, url: str, querystring: dict):
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        return json.loads(response.text)

