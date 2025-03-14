import os
import argparse

import pandas as pd

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components

import plotly.express as px

from scrapping import WizzAirScrapper, RyanAirScrapper
from utils import load_monitored_flights, load_price_history, save_price


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    parser = argparse.ArgumentParser()
    parser.add_argument('--adults', default=2, help='number of adult passangers')
    parser.add_argument('--flights_file', default='data/monitored_flights.json', help='json file: list of flight dicts [\{"departure": "DDD", "arrival": "AAA", "date": "YYYY-MM-DD", "agency": "<agency>"\}, ...]')
    parser.add_argument('--data_file', default='data/price_history.csv', help='csv filepath to save and load saved data if already exists')

    args = parser.parse_args()
    adults, flights_file, data_file = args.adults, args.flights_file, args.data_file

    scrappers = {
        'wizzair': WizzAirScrapper(),
        'ryanair': RyanAirScrapper()
    }

    load_figure_template(['journal'])

    flights = load_monitored_flights(flights_file)

    initial_df = load_price_history(data_file)
    initial_df['Timestamp'] = pd.to_datetime(initial_df['Timestamp'])
    figs = {}
    for pid, info in flights.items():
        df_pid = initial_df[initial_df['FlightID'] == pid]
        figs[pid] = px.line(df_pid, x='Timestamp', y='Price', title=pid)
        figs[pid].update_layout(yaxis_title=None, xaxis_title=None)

    app = dash.Dash('Flight Monitor', external_stylesheets=[dash_bootstrap_components.themes.JOURNAL, dash_bootstrap_components.icons.FONT_AWESOME])
    app.layout = html.Div([
        html.Div(
            children=[
                html.Div(
                    dcc.Graph(
                        id=f'price-graph-{pid}', figure=figs[pid],
                        style={'border': '1px solid #34495e', 'borderRadius': '10px', 'padding': '10px'}
                    ),
                    style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}
                ) for pid in flights
            ],
            style={'textAlign': 'center'}
        ),
        html.Button('Update Prices', id='update-button', n_clicks=0,
                    style={
                        'display': 'block', 'margin': '20px auto', 'padding': '10px 20px', 'fontSize': '16px',
                        'backgroundColor': '#2980b9', 'color': 'white', 'border': 'none', 'borderRadius': '5px',
                        'cursor': 'pointer'
                    }
        ),
        dcc.Interval(id='interval-component', interval=1800000, n_intervals=0)
    ])

    @app.callback(
        [Output(f'price-graph-{pid}', 'figure') for pid in flights],
        [Input('interval-component', 'n_intervals'), Input('update-button', 'n_clicks')]
    )
    def update_prices(n_intervals: int | None, n_clicks: int | None) -> list:
        prices = {}
        for pid, info in flights.items():
            try:
                prices[pid] = scrappers[info['agency'].lower()].get_price(info['departure'], info['arrival'], info['date'])
            except NotImplementedError:
                print(f'Agency {info["agency"]} not implemented')

        df = save_price(prices, data_file)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        figs = []
        for pid in flights.keys():
            df_pid = df[df['FlightID'] == pid]
            plot = px.line(df_pid, x='Timestamp', y='Price', title=pid, template='journal')
            plot.update_layout(yaxis_title=None, xaxis_title=None)
            figs.append(plot)
        return figs

    app.run_server(debug=True)
