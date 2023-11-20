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
            dcc.Dropdown(
                id='msm_id_selector',
                options=[],  # Initially empty
                style={'display': 'none'}  # Initially hidden
            ),
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
     Input('ping_button', 'n_clicks')],
     Input('msm_id_selector', 'value')
)
def display_content(btn1, btn2, selected_msm_id):
    ctx = callback_context

    if not ctx.triggered:
        return [
            dcc.Dropdown(
                    id='msm_id_selector',
                    options=[{'label': list(msm_id.keys())[0], 'value': list(msm_id.keys())[0]} for msm_id in traceroute_graph.traceroute_measurements],
                    value=list(traceroute_graph.traceroute_measurements[0].keys())[0] # Set default value
            ),
            dcc.Graph(
                id="graph", 
                figure=traceroute_graph.get_plot(),
            ),
            dcc.Graph(
                id="graph2",
                figure=traceroute_graph.traceroute_hops_graph,
            )
            ]
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "traceroute_button":
            return [
                dcc.Dropdown(
                    id='msm_id_selector',
                    options=[{'label': list(msm_id.keys())[0], 'value': list(msm_id.keys())[0]} for msm_id in traceroute_graph.traceroute_measurements],
                    value=list(traceroute_graph.traceroute_measurements[0].keys())[0] # Set default value
                ),
                dcc.Graph(
                    id="graph", 
                    figure=traceroute_graph.trace_fig,
                ),
                dcc.Graph(
                    id="graph2",
                    figure=traceroute_graph.traceroute_hops_graph,
                )
                ]
        elif button_id == "ping_button":
            return html.Div([
                html.H3('Content for Button 2'),
                # Add more content here
            ])
        elif button_id == "msm_id_selector":
            return update_graphs(selected_msm_id)


def update_graphs(selected_msm_id):
    print(f"Selected msm_id: {selected_msm_id}")
    traceroute_graph.update_trace_fig(selected_msm_id)
    traceroute_graph.update_hops_graph(selected_msm_id)

if __name__ == '__main__':
    app.run(debug=True)