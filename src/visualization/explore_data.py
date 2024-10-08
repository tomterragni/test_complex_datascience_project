#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
explore_data:
Description
"""

__author__ = 'Tommaso Terragni, PhD.'
__date__ = '2019-05-19'
__copyright__ = 'Copyright 2019, Tommaso Terragni, PhD.'

import os
import pandas as pd
import numpy as np

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import definitions

app = dash.Dash('Premium distribution per profile')

premiums = pd.read_csv(
    os.path.join(definitions.ROOT_DIR, 'data', 'external', 'premiums.csv'),
    sep = ';')

options = [{'label': 'all_profiles', 'value': 'all'}]
options.extend(
    [{'label': 'profile_{}'.format(bid), 'value': bid} for bid in
     premiums['bid'].unique()])

colors = ['red', 'orange', 'yellow', 'green', 'blue']

app.layout = html.Div([
    html.H1('Premium analysis'),

    html.Div([
        dcc.Dropdown(
            id = 'my-dropdown',
            options = options,
            value = 'all'
        ),
        dcc.Graph(id = 'my-graph')
    ], style = {'width': '500'})
])


@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):

    if selected_dropdown_value != 'all':
        df = premiums[premiums['bid'] == int(selected_dropdown_value)]
    else:
        df = premiums

    available_ratings = [r for r in df['defaqto_rating'].dropna().unique()]
    # available_ratings.dropna()
    available_ratings.sort()
    data = [go.Histogram(
        x = df[df['defaqto_rating'] == r]['amount'],
        nbinsx = 20,
        opacity = 0.75,
        name = 'rating = {:d}'.format(int(r)),
        marker = dict(color = colors[int(r) - 1])) for r in available_ratings]

    layout = go.Layout(
        xaxis = dict(title = 'premium (GBP)'),
        yaxis = dict(title = 'number of quotations'),
        bargap = 0.2,
        bargroupgap = 0.1
    )

    return go.Figure(data = data, layout = layout)


app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server()
