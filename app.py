from dash import Dash, html, dcc, Input, Output, State, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
from graph_traceroute import Graph_Traceroute
from graph_ping import Graph_Ping

app = Dash(name=__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

traceroute_graph = Graph_Traceroute()
ping_graph = Graph_Ping()


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
        navbar,
        html.Div(id="graph-container", children=[
          # Inspect this component for any layout constraints

        ]
        )
    ],
    fluid=True,
    style=dict(height="100%", width="100%")  
)

@app.callback(
    Output('graph-container', 'children'),
    [Input('traceroute_button', 'n_clicks'),
     Input('ping_button', 'n_clicks')]
)
def display_content(btn1, btn2):
    ctx = callback_context

    if not ctx.triggered:
        return [        dcc.Graph(
            id="graph", 
            figure=traceroute_graph.get_plot(),
        ),
        dcc.Graph(
            id="graph2",
            figure=traceroute_graph.traceroute_hops_graph,
        )]
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == "traceroute_button":
            return [        dcc.Graph(
                id="graph", 
                figure=traceroute_graph.get_plot(),
            ),
            dcc.Graph(
                id="graph2",
                figure=traceroute_graph.traceroute_hops_graph,
            )]
        elif button_id == "ping_button":
            return[dcc.Graph(
                id="map",
                figure=ping_graph.create_scattermap()
            ),
            dcc.Graph(
                id="bar_graph1",
                figure=ping_graph.create_remoteAK_bar_graph()
            ),
            dcc.Graph(
                id="bar_graph2",
                figure=ping_graph.create_urbanAK_bar_graph()
            )]

 
if __name__ == '__main__':
    app.run(debug=True)