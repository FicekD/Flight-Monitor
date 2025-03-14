import json
import os

from curl_cffi import requests


class RyanAirScrapper:
    def __init__(self, adults: int=2) -> None:
        self.adults = adults

        self.api_version = 'v4'

    def get_price(self, departure_station: str, arrival_station: str, date: str) -> float | None:
        session = requests.Session(impersonate='chrome', proxy=os.getenv('stickyproxy'))
        resp = session.get(f'https://www.ryanair.com/api/booking/{self.api_version}/en-us/availability?ADT={self.adults}&TEEN=0&CHD=0&INF=0&Origin={departure_station}&Destination={arrival_station}&promoCode=&IncludeConnectingFlights=false&DateOut={date}&DateIn=&FlexDaysBeforeOut=2&FlexDaysOut=2&FlexDaysBeforeIn=2&FlexDaysIn=2&RoundTrip=false&IncludePrimeFares=false&ToUs=AGREED')
        resp.raise_for_status()
        resp_data = resp.json()

        assert len(resp_data['trips']) == 1

        target_date = date + 'T00:00:00.000'

        price = None
        for item in resp_data['trips'][0]['dates']:
            if item['dateOut'] == target_date:
                assert len(item['flights']) == 1 and len(item['flights'][0]['regularFare']['fares']) == 1
                price = float(item['flights'][0]['regularFare']['fares'][0]['amount'])
                break
        return price
