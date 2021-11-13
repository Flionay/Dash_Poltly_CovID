# 主要依赖
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import dash  # (version 1.12.0) pip install dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np
from datetime import date
import os
from callbacks.china import china, fig_province, update_province

# 最上方横条
navbar = dbc.Navbar(

    dbc.Row([
        dbc.Col([
            dbc.Row(html.H3("疫情监控", style={'color': "white", 'fontWeight': 150}), style={"text-align": 'center'}),
            dbc.Row(html.H6("数据来源于腾讯，实时展现可视化结果。", style={'color': "white", 'fontWeight': 70, 'fontSize': 15}),
                    style={"text-align": 'center'}),
        ], ),
    ], style={"width": "100%"}),
    color="dark",
    dark=True,
    expand=True,
)
province_items = [
    dbc.DropdownMenuItem("Item 1"),
    dbc.DropdownMenuItem("Item 2"),
    dbc.DropdownMenuItem("Item 3"),
]

china_fig = dcc.Graph(id='china', figure=china())  # 右上
card_china = html.Div([
    dbc.CardHeader(html.H2("全国疫情", id="total_head")),
    dbc.CardBody(id="china_total", style={"height": "200px"}),
    dbc.DropdownMenu(
        label="选择省份", children=province_items, className="mb-1", color="warning",
    )
])  # 左上

#  市地图
province_fig = dcc.Graph(id='province', figure=fig_province())

#  市区 表格
table_province = html.Div(id="province_table", style={"height": "400px"})

layout_china = html.Div([
    navbar,
    html.Br(),
    dbc.Row([
        dbc.Col(card_china, lg={'size': 6, "order": 1}, align='center'),
        dbc.Col(china_fig, lg={'size': 6, "order": 2}, align='center')
    ]),
    html.Br(),
    dbc.Row([

        html.Hr(),
        dbc.Col([province_fig], lg={'size': 6, "order": 1}, align='center'),
        dbc.Col([table_province], lg={'size': 6, "order": 2}, align='center')
    ])
])
