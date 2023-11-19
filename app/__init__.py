from dash import Dash, html, dash_table
import pandas as pd
import numpy as np
from .api import data_api

app = Dash(__name__)
server = app.server

server.register_blueprint(data_api.data_api, url_prefix='/api')

app.layout = html.Div([
    html.Div('Mu First App with Data'),
    dash_table.DataTable(data=data_api.get_traceroute_dataframe().to_dict('records'), page_size=10)
])

