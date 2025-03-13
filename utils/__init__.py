import os
import json
import datetime

import pandas as pd


FLIGHTS_FILE = 'data/monitored_flights.json'
DATA_FILE = 'data/price_history.csv'


def load_monitored_flights() -> dict:
    with open(FLIGHTS_FILE, 'rt') as file:
        data = json.load(file)
    flight_dict = {f'{flight["departure"]}-{flight["arrival"]}': flight for flight in data}
    return flight_dict


def load_price_history() -> pd.DataFrame:
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=['Timestamp', 'FlightID', 'Price'])


def save_price(prices: dict) -> pd.DataFrame:
    df = load_price_history()
    new_entries = pd.DataFrame(
        [[datetime.datetime.now(), pid, price] for pid, price in prices.items()],
        columns=['Timestamp', 'FlightID', 'Price']
    )
    df = pd.concat([df, new_entries], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return df
