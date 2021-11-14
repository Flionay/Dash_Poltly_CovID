# 主要依赖
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

from callbacks.china import china

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

province_list = [
    '台湾',
    '黑龙江',
    '香港',
    '河北',
    '甘肃',
    '云南',
    '辽宁',
    '河南',
    '上海',
    '北京',
    '广西',
    '四川',
    '广东',
    '内蒙古',
    '山东',
    '宁夏',
    '浙江',
    '福建',
    '陕西',
    '天津',
    '江西',
    '青海',
    '重庆',
    '湖北',
    '吉林',
    '湖南',
    '江苏',
    '贵州',
    '山西',
    '澳门',
    '海南',
    '安徽',
    '新疆',
    '西藏', ]

china_fig = dcc.Graph(id='china', figure=china())  # 右上

card_china = dbc.Card([
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000 * 15,  # in milliseconds / refresh the webpage in every 60 seconds 15分钟
        n_intervals=0
    ),
    dbc.CardHeader(html.Div([html.H3("全国疫情", style={"color": "#294c80"}),
                             html.H6(id="update_time")])),
    dbc.CardBody(
        html.Div(id="china_card_total",
                 )
    ),

], style={"margin-left": "30px"})  # 左上

#  市地图
province_fig = dcc.Graph(id='province_fig', figure={}, style={"margin-left": "30px"})

#  市区 表格
table_province = html.Div(id="province_table", style={"height": "400px", })

province_card = dbc.Card([
    dbc.CardHeader(html.H3("各省份疫情")),
    dbc.CardBody([dcc.Dropdown(
        id='province-dropdown',
        options=[{'label': key, 'value': key} for key in province_list],
        value='山西'
    ),
    table_province
    ])]
)

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
        dbc.Col([province_card],
                lg={'size': 6, "order": 2}, align='center')
    ])
])
