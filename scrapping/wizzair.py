import os
import json

from curl_cffi import requests

from .utils import InvalidFLightException


class WizzAirScrapper:
    def __init__(self, adults: int=2) -> None:
        self.adults = adults
        
        self.api_version = self.get_api_version()

    def get_api_version(self) -> str:
        session = requests.Session(impersonate='chrome', proxy=os.getenv('stickyproxy'))
        resp = session.get('https://www.wizzair.com/buildnumber')
        api_version = resp.text.split('/')[-1]
        return api_version

    def get_price(self, departure_station: str, arrival_station: str, date: str) -> float | None:
        data = {
            'adultCount': self.adults,
            'childCount': 0,
            'dayInterval': 3,
            'flightList':[
                {'departureStation': departure_station.upper(), 'arrivalStation': arrival_station.upper(), 'date': date}
            ],
            'isFlightChange': False,
            'isRescueFare': False,
            'wdc': False
        }

        session = requests.Session(impersonate='chrome', proxy=os.getenv('stickyproxy'))
        try:
            resp = session.post(f'https://be.wizzair.com/{self.api_version}/Api/asset/farechart', data=json.dumps(data), headers={'Content-type': 'application/json; charset=UTF-8'})
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            new_api_version = self.get_api_version()
            if new_api_version != self.api_version:
                self.api_version = new_api_version
                resp = session.post(f'https://be.wizzair.com/{self.api_version}/Api/asset/farechart', data=json.dumps(data), headers={'Content-type': 'application/json; charset=UTF-8'})
                resp.raise_for_status()
            else:
                raise e
            
        resp_data = resp.json()

        target_date = date + 'T00:00:00'

        price = None
        for item in resp_data['outboundFlights']:
            if item['date'] == target_date and item['priceType'] != 'noData':
                price = float(item['price']['amount'])
                break
        
        if price is None:
            raise InvalidFLightException()
        
        return price
