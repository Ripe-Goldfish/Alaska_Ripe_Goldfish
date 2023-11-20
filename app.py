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
            return html.Div([
                html.H3('Content for Button 2'),
                # Add more content here
            ])

 
if __name__ == '__main__':
    app.run(debug=True)