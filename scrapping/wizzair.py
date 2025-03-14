import os
import json

from curl_cffi import requests


class WizzAirScrapper:
    def __init__(self, adults: int=2) -> None:
        self.adults = adults
        session = requests.Session(impersonate='chrome', proxy=os.getenv('stickyproxy'))
        resp = session.get('https://www.wizzair.com/buildnumber')
        self.api_version = resp.text.split('/')[-1]

    def get_price(self, departure_station: str, arrival_station: str, date: str) -> float | None:
        data = {
            'adultCount': self.adults,
            'childCount': 0,
            'dayInterval': 7,
            'flightList':[
                {'departureStation': departure_station.upper(), 'arrivalStation': arrival_station.upper(), 'date': date}
            ],
            'isFlightChange': False,
            'isRescueFare': False,
            'wdc': False
        }

        session = requests.Session(impersonate='chrome', proxy=os.getenv('stickyproxy'))
        resp = session.post(f'https://be.wizzair.com/{self.api_version}/Api/asset/farechart', data=json.dumps(data), headers={'Content-type': 'application/json; charset=UTF-8'})
        resp.raise_for_status()
        resp_data = resp.json()

        target_date = date + 'T00:00:00'

        price = None
        for item in resp_data['outboundFlights']:
            if item['date'] == target_date:
                price = float(item['price']['amount'])
                break
        return price
