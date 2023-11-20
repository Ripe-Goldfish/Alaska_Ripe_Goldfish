from dash import Dash, html, dcc, Input, Output, State, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
from graph_traceroute import Graph_Traceroute

app = Dash(name=__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

traceroute_graph = Graph_Traceroute()


navbar = dbc.NavbarSimple(
    brand="Team Goldfish",
    children=[
        dbc.Button(
            "Traceroute",
            id="traceroute_button",
            style={"background": "none", "border": "none"},
        ),
        dbc.Button(
            "Ping",
            id="ping_button",
            style={"background": "none", "border": "none"},
        )
    ],
    color="dark",
    dark=True,
    fluid=True,
)


app.layout = dbc.Container(children=
    [
        navbar,  # Inspect this component for any layout constraints
        dcc.Graph(
            id="graph", 
            figure=traceroute_graph.get_plot(),
        ),
        dcc.Graph(
            id="graph2",
            figure=traceroute_graph.traceroute_hops_graph,
        )
    ],
    fluid=True,
    style=dict(height="100%", width="100%")  
)


 
if __name__ == '__main__':
    app.run(debug=True)