import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import datetime
import pandas as ps

df = ps.read_csv("owid-covid-data.csv")
print(df.describe())
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{
                    'name': 'viewpoint',
                    'content': 'width=device-width , initial-scale = 1.0'
                }])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Interactive Dashboard",
                        className="text-center text-primary mb-4"))
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='my_drop', multi=False, value='Nigeria',
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['location'].unique())
                                  ]
                         ),
            dcc.Graph(id='graph_1', figure= {})
        ]),
        dbc.Col([
            dcc.Dropdown(id='my_drop2', multi=True, value=['Nigeria', 'Turkey'],
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['location'].unique())
                                  ]
                         ),
            dcc.Graph(id='graph_2', figure = {})
        ])
    ]),
])

#single dropdown callback
@app.callback(
    Output('graph_1', 'figure'),
    Input('my_drop', 'value')
)
def update_graph(location):
    dff = df[df['location'] == location]
    figln = px.line(dff, x='new_cases', y='new_deaths')
    return figln


# Line chart - multiple
@app.callback(
    Output('graph_2', 'figure'),
    Input('my_drop2', 'value')
)
def update_graph(location_slctd):
    dff = df[df['location'].isin(location_slctd)]
    figln2 = px.line(dff, x='date', y='total_cases', color='location')
    return


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
