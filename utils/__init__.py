import os
import json
import datetime

import pandas as pd


def load_monitored_flights(path: str) -> dict:
    with open(path, 'rt') as file:
        data = json.load(file)
    flight_dict = {f'{flight["departure"]}-{flight["arrival"]}': flight for flight in data}
    return flight_dict


def load_price_history(path: str) -> pd.DataFrame:
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame(columns=['Timestamp', 'FlightID', 'Price'])


def save_price(prices: dict, path: str) -> pd.DataFrame:
    df = load_price_history()
    new_entries = pd.DataFrame(
        [[datetime.datetime.now(), pid, price] for pid, price in prices.items()],
        columns=['Timestamp', 'FlightID', 'Price']
    )
    df = pd.concat([df, new_entries], ignore_index=True)
    df.to_csv(path, index=False)
    return df
