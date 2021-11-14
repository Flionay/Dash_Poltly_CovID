import pymysql
import pandas as pd
import json
import sys
sys.path.append('/Users/angyi/PycharmProjects/CovIdVis')

def china_all():
    with open('./data/data_today.json') as data_file:
        d = json.load(data_file)

    chinaTotal = pd.DataFrame(d['chinaTotal'], index=[d['lastUpdateTime']])
    chinaAdd = pd.DataFrame(d['chinaAdd'], index=[d['lastUpdateTime']])
    return chinaTotal, chinaAdd


def china_province():
    with open('./data/data_today.json') as data_file:
        d = json.load(data_file)

    # d[areaTree] 这个数据里第一层是国家的，children是每个省的,省里面第一层是省数据，里面还有children 是每个省的区县
    # 各个省的当前数据
    province_today_data = pd.DataFrame()
    for province in d['areaTree'][0]['children']:
        dicts = province['today']  # 这里省份只要今天的数据
        series = pd.Series(dicts, name=province['name'])
        province_today_data = province_today_data.append(series)

    # 各个省的总数据
    province_hist_data = pd.DataFrame()
    for province in d['areaTree'][0]['children']:
        dicts = province['total']  # 这里省份只要今天的数据
        series = pd.Series(dicts, name=province['name'])
        province_hist_data = province_today_data.append(series)

    return province_today_data, province_hist_data


def china_city():

    with open('./data/data_today.json') as data_file:
        d = json.load(data_file)
    # 每个省 地区的总数据

    city_hist_data = pd.DataFrame()
    for province in d['areaTree'][0]['children']:
        cities = province['children']  # 省份的孩子
        for city in cities:
            dicts = city['total']
            dicts['province'] = province['name']
            series = pd.Series(dicts, name=city['name'])
            city_hist_data = city_hist_data.append(series)

    # 每个省 地区的今日数据
    city_today_data = pd.DataFrame()
    for province in d['areaTree'][0]['children']:
        cities = province['children']  # 省份的孩子
        for city in cities:
            dicts = city['today']
            dicts['province'] = province['name']
            series = pd.Series(dicts, name=city['name'])
            city_today_data = city_hist_data.append(series)

    return city_hist_data, city_today_data


if __name__ == '__main__':
    chinaTotal, chinaAdd = china_all()
    # province_today_data, province_hist_data = china_province()
    # city_hist_data, city_today_data = china_city()
    print(chinaTotal)

