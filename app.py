from dash import Dash, html, dcc, Input, Output, State, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(name=__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


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

app.layout = html.Div([navbar,
                       dcc.Graph(id="graph"),])

@app.callback(
    Output("graph", "figure"),
    [Input("traceroute_button", "n_clicks"),
     Input("ping_button", "n_clicks")],
)
def update_graph(traceroute_button, ping_button):
        # The context of the callback to determine which button was clicked
    ctx = callback_context

    # If no button has been clicked, return an empty graph or default graph
    if not ctx.triggered:
        return {}

    # Identify which button was clicked
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'traceroute_button':
        # Generate the graph for traceroute
        return {}
    elif button_id == 'ping_button':
        # Generate the graph for ping
        return {}

    return { }  # Return an empty graph as default
 
if __name__ == '__main__':
    app.run(debug=True)