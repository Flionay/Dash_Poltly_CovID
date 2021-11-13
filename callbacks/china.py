import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from dash.dependencies import Input, Output,State
import sys
from server import app
sys.path.append('/Users/angyi/PycharmProjects/CovIdVis')
from data.data_dump import data_proc

def china():

    province_today_data, city_today_data, province_hist_data, city_hist_data, chinaTotal, chinaAdd = data_proc()
    token = open("./utils/mapbox").read()  # you will need your own token

    with open('./data/china_province.geojson', 'r') as response:
        provinces_map = json.load(response)

    # counties = json.load('./data/geojson.json')
    df = province_today_data
    df['location'] = df.index

    fig = px.choropleth_mapbox(
        df,
        geojson=provinces_map,
        color='confirm',
        hover_data={'wzz_add': True,  # remove species from hover data
                    'location': True,  # customize hover for column of y attribute
                    },
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
    fig.update_layout(mapbox_style="light", mapbox_accesstoken=token,
                      mapbox_zoom=2.9, mapbox_center={"lat": 34.0902, "lon": 113.7129})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    
    return fig



def fig_province():

    province_today_data, city_today_data, province_hist_data, city_hist_data, chinaTotal, chinaAdd = data_proc()
    token = open("./utils/mapbox").read()  # you will need your own token

    with open('./data/json/province.json', 'r') as response:
        provinces_map = json.load(response)

    province_text = "山西省"

    for pro in provinces_map:
        if pro['name']==province_text:
            province_code = pro['code']

    response = requests.get(f"https://geo.datav.aliyun.com/areas_v3/bound/{province_code}_full.json")
    province_geojson = response.json()


    df = city_today_data.loc[city_today_data['province']=='山西']
    df['location'] = df.index
        # 匹配每个市的名字
    for city in province_geojson['features']:
        # json市一列 city['properties']['name']
        # 数据 市一列 df.location
        city_j = city['properties']['name']
        for city_d in df['location']:
            if city_j in city_d or city_d in city_j:
                df.loc[df['location']==city_d,'location'] = city_j

    lon_center = province_geojson['features'][0]['properties']['center'][0]
    lat_center = province_geojson['features'][0]['properties']['center'][1]

    fig = px.choropleth_mapbox(
        df,
        geojson=province_geojson,
        color='confirm',
        # hover_data={'wzz_add': True,  # remove species from hover data
        #             'location': True,  # customize hover for column of y attribute
        #             },
        locations="location",
        # opacity=0.5,
        featureidkey="properties.name",
        # mapbox_style="Light and Dark",
        color_continuous_scale='Reds',
        # customdata=np.vstack((df.地区, df.确诊, df.疑似, df.治愈, df.死亡)).T,
        # hovertemplate="<b>%{customdata[0]}</b><br><br>"
        # + "确诊：%{customdata[1]}<br>"
        # + "疑似：%{customdata[2]}<br>"
        # + "治愈：%{customdata[3]}<br>"
        # + "死亡：%{customdata[4]}<br>"
        # + "<extra></extra>",
        
    )

    fig.update_layout(mapbox_style="light", mapbox_accesstoken=token,
                      mapbox_zoom=5.9, mapbox_center={"lat": lat_center, "lon":lon_center })
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


@app.callback(
    Output(component_id = "info", component_property ="children"),
    Input(component_id = "china", component_property = 'children'),
)
def update_province(china):
    print(china)
    return china


if __name__ == '__main__':
    fig = fig_province()
    # fig = china()
    fig.show()
