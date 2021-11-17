import pymysql
import pandas as pd
import json
import sys
import datetime
import os
import sys
sys.path.append("/home/lighthouse/CovId/")

from models.db import client
from config import Config
##

def china_all():
    with open(os.path.join(Config.tencentPath, 'data_today.json'),'r') as data_file:
        d = json.load(data_file)
    chinaTotal = pd.DataFrame(d['chinaTotal'], index=[d['lastUpdateTime']])
    chinaAdd = pd.DataFrame(d['chinaAdd'], index=[d['lastUpdateTime']])
    return chinaTotal, chinaAdd


def china_province():
    with open(os.path.join(Config.tencentPath, 'data_today.json')) as data_file:
        d = json.load(data_file)

    # d[areaTree] 这个数据里第一层是国家的，children是每个省的,省里面第一层是省数据，里面还有children 是每个省的区县
    # 各个省的当前数据
    province_today_data = pd.DataFrame()
    for province in d['areaTree'][0]['children']:
        dicts = province['today']  # 这里省份只要今天的数据
        series = pd.Series(dicts, name=province['name'])
        province_today_data = province_today_data.append(series)

    # 各个省的总数据
    province_total_data = pd.DataFrame()
    for province in d['areaTree'][0]['children']:
        dicts = province['total']  # 这里省份只要今天的数据
        series = pd.Series(dicts, name=province['name'])
        province_total_data = province_today_data.append(series)
    province_total_data.dropna(subset=['confirm', 'isUpdated'], inplace=True)
    return province_today_data, province_total_data


def china_city():
    with open(os.path.join(Config.tencentPath, 'data_today.json')) as data_file:
        d = json.load(data_file)
    # 每个省 地区的总数据
    city_total_data = pd.DataFrame()
    for province in d['areaTree'][0]['children']:
        cities = province['children']  # 省份的孩子
        for city in cities:
            dicts = city['total']
            dicts['province'] = province['name']
            series = pd.Series(dicts, name=city['name'])
            city_total_data = city_total_data.append(series)

    # 每个省 地区的今日数据
    city_today_data = pd.DataFrame()
    for province in d['areaTree'][0]['children']:
        cities = province['children']  # 省份的孩子
        for city in cities:
            dicts = city['today']
            dicts['province'] = province['name']
            series = pd.Series(dicts, name=city['name'])
            city_today_data = city_total_data.append(series)
    city_today_data['city'] = city_today_data.index
    city_total_data['city'] = city_total_data.index

    city_total_data.reset_index(drop=True, inplace=True)
    city_today_data.reset_index(drop=True, inplace=True)
    return city_total_data, city_today_data


if __name__ == '__main__':
    from models.tencent_data import get_global_data,get_hist_data,get_last_data

    last_data = get_last_data()
    with open(os.path.join(Config.tencentPath,'data_today.json'), 'w') as f:
        json.dump(last_data, f)

    hist_data = get_hist_data()
    with open(os.path.join(Config.tencentPath,'hist_data.json'), 'w') as f:
        json.dump(hist_data,f)

    glob_data = get_global_data()
    with open(os.path.join(Config.tencentPath,'global_data.json'), 'w') as f:
        json.dump(glob_data, f)
        
        
    chinaTotal, chinaAdd = china_all()
    province_today_data, province_total_data = china_province()
    city_total_data, city_today_data = china_city()
    data = {
        "time": chinaTotal.index[0],
        "chinaTotal": chinaTotal.to_json(),
        "chinaAdd": chinaAdd.to_json(),
        "province_today_data": province_today_data.to_json(),
        "province_total_data": province_total_data.to_json(),
        "city_total_data": city_total_data.to_json(),
        "city_today_data": city_today_data.to_json(),
    }
    # 存入mongo
    with client:
        db = client.covId
        db.time.replace_one({"_id": 1}, {"time": chinaTotal.index[0]})
        id = db.data.insert_one(data)
    print(f"更新于{datetime.datetime.now()}")
    print("=============")
    print(f"数据时间为{chinaTotal.index[0]}\n")
