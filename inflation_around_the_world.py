#### Inflation Around the World #### 
# Application Development in Python - Mandatory Assignment

import os
os.chdir('C:/Users/Kjell/Onedrive/Programming/github/dash/inflation_around_the_world/')

import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
from dash import dcc, html, dash_table, Dash

inflation = pd.read_csv('inflation.csv')

# Making animated map plot
map_plot = px.choropleth(
    inflation,
    locations = 'iso3c', color = 'inflation',
    hover_name = 'country', hover_data = {'iso3c' : False}, 
    animation_frame = 'year',
    color_continuous_scale = 'plasma',
    range_color = (-10, 25)
).update_layout(
    coloraxis_colorbar_title = 'Inflation', 
    font = dict(size = 16), 
    template = 'simple_white'
)

# Defining line and bar plot and making list of options for dropdown menues
line_plot = px.line()
bar_plot = px.bar()
options_line_plot = [{'label' : x, 'value' : x} for x in sorted(list(inflation['country'].unique()))]
options_bar_plot = [{'label' : x, 'value' : x} for x in sorted(list(inflation['year'].unique()), reverse = True)]

# Dash Application
load_figure_template('bootstrap')
dbc_css = 'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css'
app = Dash(__name__,external_stylesheets=[dbc.themes.QUARTZ, dbc_css])
server = app.server
app.layout = dbc.Container(
    children=[
        dcc.Markdown('# Inflation Around the World', style={'textAlign': 'center'}),
        dcc.Markdown('*Application Development in Python - Mandatory Assignment*', style={'textAlign': 'center'}),
        dbc.Row([
            dbc.Col([
                # Dropdown for line plot
                dcc.Dropdown(
                    options = options_line_plot,
                    id = 'line_plot_input',
                    value = ['Norway', 'Denmark', 'Sweden'],
                    multi = True,
                    style = {'width': '100%'}
                ),
            ]), 
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        # Dropdown for bar plot
                        dcc.Dropdown(
                            options = options_bar_plot,
                            id = 'bar_plot_input_year',
                            value = 2021
                        )
                    ]),
                    dbc.Col([
                        # Toggle switch for bar plot
                        dcc.RadioItems(
                            options = [{'label' : 'Top 20', 'value' : 'False'}, 
                                    {'label' : 'Bottom 20', 'value' : 'True'}], 
                            id = 'bar_plot_input_ascdesc',
                            value = 'False',
                            labelStyle={'display': 'inline-block', 'margin-right': '1vh'}
                        )
                    ])
                ])
            ])
        ]),
        dbc.Row([
            dbc.Col([ # Line plot
                dcc.Graph(id = 'line_plot_output',
                            config = {'responsive' : True},
                            style = {'height' : '650px', 'padding' : '1rem'}
                )
            ]),
            dbc.Col([ # Bar plot
                dcc.Graph(id = 'bar_plot_output',
                            config = {'responsive' : True},
                            style = {'height' : '650px', 'padding' : '1rem'}
                )
            ]),
        ]),
        dbc.Row([
            dbc.Col( # Map plot
                dcc.Graph(figure = map_plot,
                            config = {'responsive' : True},
                            style = {'height' : '650px', 'padding' : '1rem'}
                )
            ),
            dbc.Col( # Table
                dash_table.DataTable(
                    id = 'table', 
                    columns = [{'name': x, 'id': x} for x in inflation.columns],
                    data = inflation[inflation['year'] == 2021].sort_values(['inflation'], ascending = False).to_dict('records'),
                    style_cell = {'textAlign': 'left'}, page_size = 17
                )
            )
        ]),
    ],
    fluid = True, 
    className = 'dbc'
)

# Callback for line plot
@app.callback(
    Output(component_id = 'line_plot_output', component_property = 'figure'),
    Input(component_id = 'line_plot_input', component_property = 'value')
)
def line_plot_func(countries, data = inflation):
    line_plot = px.line(
        data[data['country'].isin(list(countries))], 
        x='year', y='inflation', color = 'country'
    ).update_layout(
        xaxis_title = None, yaxis_title = 'Inflation', legend_title_text = None,
        font = dict(size = 16), 
        template = 'simple_white',
        margin = dict(l = 10, r = 10, t = 10, b = 10)
    ).update_xaxes(
        rangeslider_visible = True, nticks = 10
    )
    return line_plot

# Callback for bar plot
@app.callback(
    Output(component_id = 'bar_plot_output', component_property = 'figure'),
    Input(component_id = 'bar_plot_input_year', component_property = 'value'),
    Input(component_id = 'bar_plot_input_ascdesc', component_property = 'value')
)
def bar_plot_func(year, ascdesc, data = inflation):
    x = True if ascdesc == 'True' else False
    bar_plot = px.bar(
        data[data['year'] == year].sort_values(['inflation'], ascending = x)[:20].copy(), 
        'iso3c', 'inflation', hover_name = 'country'
    ).update_layout(
        xaxis_title = None, yaxis_title = 'Inflation', legend_title_text = None,
        font = dict(size = 16), 
        template = 'simple_white',
        margin = dict(l = 10, r = 10, t = 10, b = 10)
    )
    return bar_plot

if __name__ == '__main__':
    app.run_server()