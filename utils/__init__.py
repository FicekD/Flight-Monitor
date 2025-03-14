import os
import json
import datetime

import numpy as np
import pandas as pd


def load_monitored_flights(path: str) -> dict:
    with open(path, 'rt') as file:
        data = json.load(file)
    flight_dict = {f'{flight["agency"].capitalize()}: {flight["departure"].upper()}-{flight["arrival"].upper()} on {flight["date"]}': flight for flight in data}
    return flight_dict


def load_price_history(path: str) -> pd.DataFrame:
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame(columns=['Timestamp', 'FlightID', 'Price'])


def save_price(prices: dict, path: str) -> pd.DataFrame:
    df = load_price_history(path)
    new_entries = pd.DataFrame(
        [[datetime.datetime.now(), pid, price] for pid, price in prices.items()],
        columns=['Timestamp', 'FlightID', 'Price']
    )
    df = pd.concat([df, new_entries], ignore_index=True)

    sub_dfs = list()
    grouped = df.groupby('FlightID')
    for _, gdf in grouped:
        prices = np.array(gdf['Price'], dtype=np.float32)
        if len(prices) < 3:
            continue
        mask = np.logical_not((prices[:-2] == prices[1:-1]) * (prices[2:] == prices[1:-1]))
        mask = np.pad(mask, 1, mode='constant', constant_values=True)
        sub_dfs.append(gdf.loc[mask])
    if len(sub_dfs) > 0:
        df = pd.concat(sub_dfs)

    df.to_csv(path, index=False)
    return df
