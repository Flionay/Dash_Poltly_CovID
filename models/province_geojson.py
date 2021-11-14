# 爬取每个省的geojson数据，存入mongo
import json
import requests
from pymongo import MongoClient


def get_geojson():
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
    with open('../data/json/province.json', 'r') as response:
        provinces_map = json.load(response)

        # province_text = "山西省"
    json_list = []
    for province_text in province_list:
        for pro in provinces_map:
            if province_text in pro['name']:
                province_code = pro['code']
        if province_code == "710000":
            response = requests.get(f"https://geo.datav.aliyun.com/areas_v3/bound/{province_code}.json")
        else:
            response = requests.get(f"https://geo.datav.aliyun.com/areas_v3/bound/{province_code}_full.json")
        json_list.append({"province_name": province_text, "geojson": response.json()})


    return json_list


if __name__ == '__main__':
    client = MongoClient(host="127.0.0.1", port=27017, username="admin", password="123456")
    json_list = get_geojson()
    # 存入mongo
    with client:
        db = client.covId
        db.province_geojson.insert_many(json_list)
