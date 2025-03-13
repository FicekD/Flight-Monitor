import json

from curl_cffi import requests


class RyanAirScrapper:
    def __init__(self) -> None:
        pass

    def get_price(self, departure_station: str, arrival_station: str, date: str) -> float | None:
        raise NotImplementedError()

