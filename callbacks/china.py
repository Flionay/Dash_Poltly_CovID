import json
import sys
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import requests
from dash import dash_table
from dash import html
from dash.dependencies import Input, Output
from server import app
import os
from config import Config
from models.db import client
from models.data_dump import china_province, china_city, china_all
import pandas as pd
import numpy as np


def china():
    with client:
        db = client.covId
        updatetime = db.time.find_one({"_id": 1})['time']
        province_today_data = db.data.find_one({"time": updatetime})['province_today_data']

    # 中国地图geojson
    with open(os.path.join(Config.jsonPath, 'china_province.geojson'), 'r') as response:
        provinces_map = json.load(response)

    # counties = json.load('./data/geojson.json')
    df = pd.read_json(province_today_data)
    df['location'] = df.index

    fig = px.choropleth_mapbox(
        df,
        geojson=provinces_map,
        color='confirm',
        hover_data={
            'location': True,
            "confirm": True,
            "wzz_add": True
                    },
        labels={'location': "地区",
                "confirm": "累计确诊",
                "wzz_add": "无症状感染者"},
        locations="location",
        opacity=0.5,
        featureidkey="properties.NL_NAME_1",
        # mapbox_style="Light and Dark",
        color_continuous_scale='YlOrRd',

    )
    # fig.data[0].hovertemplate =  '<b>Province</b>: <b>%{hovertext}</b>'+\
    #                               '<br> <b>确诊人数 </b>: %{z}<br>'+\
    #                               '<br> <b>治愈人数 </b>: %{text}<br>'
    fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
    fig.update_layout(mapbox_style="light", mapbox_accesstoken=Config.token,
                      mapbox_zoom=2.9, mapbox_center={"lat": 34.0902, "lon": 113.7129})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


def fig_province(province_text):
    with client:
        db = client.covId
        updatetime = db.time.find_one({"_id": 1})['time']
        city_today_data = db.data.find_one({"time": updatetime})['city_today_data']
        # 从mongo中取该省份的geojson
        province_geojson = db.province_geojson.find_one({"province_name": province_text})['geojson']

    city_today_data = pd.read_json(city_today_data)
    df = city_today_data.loc[city_today_data['province'] == province_text]
    df['location'] = df['city']
    # 匹配每个市的名字
    for city in province_geojson['features']:
        # json市一列 city['properties']['name']
        # 数据 市一列 df.location
        city_j = city['properties']['name']
        for city_d in df['location']:
            if city_j in city_d or city_d in city_j:
                df.loc[df['location'] == city_d, 'location'] = city_j

    lon_center = province_geojson['features'][0]['properties']['center'][0]
    lat_center = province_geojson['features'][0]['properties']['center'][1]

    fig = px.choropleth_mapbox(
        df,
        geojson=province_geojson,
        color='confirm',
        hover_data={
            'location': True,
            "nowConfirm": True,
            "confirm": True,
            'suspect': True,
            "wzz": True
                    },
        labels={'location': "地区",
                "nowConfirm": "当前确诊",
                "confirm": "累计确诊",
                'suspect': "疑似病例",
                "wzz": "无症状感染者"},

        locations="location",
        # opacity=0.5,
        featureidkey="properties.name",
        # mapbox_style="Light and Dark",
        color_continuous_scale='Reds',
    )

    fig.update_layout(mapbox_style="light", mapbox_accesstoken=Config.token,
                      mapbox_zoom=5, mapbox_center={"lat": lat_center, "lon": lon_center})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


@app.callback(
    Output(component_id="province_fig", component_property="figure"),
    Input(component_id="province-dropdown", component_property='value'),
)
def select_province(province):
    if not province:
        province = '山西'

    return fig_province(province)


@app.callback(
    [Output('china_card_total', "children"),
     Output('update_time', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_china_cardboard(n):
    chinaTotal, chinaAdd = china_all()
    # 全国数字看板
    card_content1 = [
        dbc.CardHeader("本土现有确诊", className="china_card_header"),
        dbc.CardBody(
            [
                html.H2(str(chinaTotal['localConfirmH5'][0]), className="china_card_data", style={"color": "red"}),
                html.P(
                    f"较上日 +{chinaAdd['localConfirmH5'][0]}",
                    className="china_card_footer",
                ),
            ]
        ),
    ]
    card_content2 = [
        dbc.CardHeader("现有确诊", className="china_card_header"),
        dbc.CardBody(
            [
                html.H2(str(chinaTotal['nowConfirm'][0]), className="china_card_data",
                        style={"color": "rgb(247, 76, 49)"}),
                html.P(
                    f"较上日 +{chinaAdd['nowConfirm'][0]}",
                    className="china_card_footer",
                ),
            ]
        ),
    ]
    card_content3 = [
        dbc.CardHeader("累计确诊", className="china_card_header"),
        dbc.CardBody(
            [
                html.H2(str(chinaTotal['confirm'][0]), className="china_card_data",
                        style={"color": "rgb(174, 33, 44)"}),
                html.P(
                    f"较上日 +{chinaAdd['confirm'][0]}",
                    className="china_card_footer",
                ),
            ]
        ),
    ]
    card_content4 = [
        dbc.CardHeader("无症状感染者", className="china_card_header"),
        dbc.CardBody(
            [
                html.H4(str(chinaTotal['noInfect'][0]), className="china_card_data",
                        style={"color": "rgb(162, 90, 78)"}),
                html.P(
                    f"较上日 +{chinaAdd['noInfect'][0]}",
                    className="china_card_footer",
                ),
            ]

        ),
    ]
    card_content5 = [
        dbc.CardHeader("境外输入", className="china_card_header"),
        dbc.CardBody(
            [
                html.H4(str(chinaTotal['importedCase'][0]), className="china_card_data",
                        style={"color": "rgb(247, 130, 7)"}),
                html.P(
                    f"较上日 +{chinaAdd['importedCase'][0]}",
                    className="china_card_footer",
                ),
            ]
        ),
    ]
    card_content6 = [
        dbc.CardHeader("累计死亡", className="china_card_header"),
        dbc.CardBody(
            [
                html.H4(str(chinaTotal['dead'][0]), className="china_card_data", style={"color": "rgb(93, 112, 146)"}),
                html.P(
                    f"较上日 +{chinaAdd['dead'][0]}",
                    className="china_card_footer",
                ),
            ]
        ),
    ]

    return [
               dbc.Row(
                   [
                       dbc.Col(dbc.Card(card_content1)),
                       dbc.Col(dbc.Card(card_content2, )),
                       dbc.Col(dbc.Card(card_content3, )),
                   ],
                   className="mb-4",
               ),
               dbc.Row(
                   [
                       dbc.Col(dbc.Card(card_content4)),
                       dbc.Col(dbc.Card(card_content5, )),
                       dbc.Col(dbc.Card(card_content6, )),
                   ],
                   className="mb-4",
               ),
           ], f"更新于{chinaTotal.index[0]}"


@app.callback(
    Output('province_table', 'children'),
    Input(component_id="province-dropdown", component_property='value'),
)
def update_dashtable(province):
    with client:
        db = client.covId
        updatetime = db.time.find_one({"_id": 1})['time']
        city_total_data = db.data.find_one({"time": updatetime})['city_total_data']
        # 从mongo中取该省份的geojson

    # city_hist_data, city_today_data = china_city()
    city_hist_data = pd.read_json(city_total_data)
    df = city_hist_data.loc[city_hist_data['province'] == province]
    df['市区'] = df['city']

    df.rename(
        columns={"province": "省份",
                 "grade": "地区",
                 "nowConfirm": "当前确诊",
                 "heal": "治愈例",
                 "confirm": "累计确诊",
                 "suspect": "疑似病例",
                 "healRate": "治愈率"
                 }, inplace=True
    ),
    dfcolumns = ['省份', '市区', '地区', '当前确诊', '累计确诊', '疑似病例', '治愈例', '治愈率']
    return dbc.Container(dash_table.DataTable(
        columns=[{'name': column, 'id': column} for column in dfcolumns],
        data=df.to_dict('records'),
        virtualization=True,
        style_cell={
            'font-family': 'Times New Roman',
            'text-align': 'left',
            # all three widths are needed
            'minWidth': '70px', 'width': '100px', 'maxWidth': '130px',
        },
        # style_as_list_view=True,
        style_data_conditional=[
            {
                'if': {
                    # 'column_id': 'grade',
                    # since using .format, escape { with {{
                    'filter_query': '{{地区}} contains {}'.format('风险')
                },
                'backgroundColor': 'rgb(247, 76, 49)',
                'color': 'white'
            },
        ],
        fixed_rows={'headers': True},
        style_header={
            'background-color': '#b3e5fc',
            'font-family': 'Times New Roman',
            'font-weight': 'bold',
            'font-size': '15px',
            'text-align': 'center'
        },
        style_data={
            'font-family': 'Times New Roman',
            'text-align': 'center'
        }, style_table={'height': '360px', 'overflowY': 'auto', 'overflowX': 'auto'}, page_size=10
    ), style={'border': '2px', "margin-top": "30px"})


if __name__ == '__main__':
    # fig = fig_province('北京')
    fig = china()
    fig.show()
