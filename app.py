from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import requests
import json

app = Dash(__name__)

app.layout = html.Div([
    
    html.H1(id="count-up"),
    dcc.Graph(id="candles"),
    dcc.Graph(id="indicator"),


    dcc.Interval(id="interval", interval = 2000),
    
    ])

@app.callback(
        Output("candles","figure"),
        Output("indicator","figure"),
        Input("interval","n_intervals"),
)
def update_figure(n_intervals):

    url = "https://www.bitstamp.net/api/v2/ohlc/btcusd/"

    params = {"step":"60","limit":"30"}

    data = requests.get(url, params=params).json()["data"]["ohlc"]
    data = pd.DataFrame(data)
    data.timestamp = pd.to_datetime(data.timestamp, unit = "s")


    
    candles = go.Figure(
                    data = [
                        go.Candlestick(
                            x = data.timestamp,
                            open = data.open,
                            high = data.high,
                            low = data.low,
                            close = data.close
                            )])
    
    candles.update_layout(xaxis_rangeslider_visible= False, 
            height = 400, template= "plotly_dark")

    candles.update_layout(transition_duration = 500)
    
    indicator = px.line(x=data.timestamp, y=data.high, height = 300, template = "plotly_dark")
    indicator.update_layout(transition_duration = 500)

    return candles, indicator

if __name__ == "__main__":
    app.run_server(debug=True)