import time
import json
import pandas as pd
import numpy as np
import requests


def get_global_data():
    url = r"""https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign&_={0}""".format(
        int(time.time()*1000))
    result = requests.get(url)
    data = json.loads(result.json()['data'])

    return data

def get_last_data():
    import requests
    url = r"""https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&_={0}""".format(
        int(time.time()*1000))
    result = requests.get(url)
    data = json.loads(result.json()['data'])

    return data


def get_hist_data():
    import requests
    url = r"""https://view.inews.qq.com/g2/getOnsInfo?name=disease_other&_={0}""".format(
        int(time.time()*1000))
    result = requests.get(url)
    data = json.loads(result.json()['data'])
    return data


if __name__ == '__main__':
    last_data = get_last_data()
    with open('../data/tencent/data_today.json', 'w') as f:
        json.dump(last_data, f)

    hist_data = get_hist_data()
    with open('../data/tencent/hist_data.json', 'w') as f:
        json.dump(hist_data,f)

    glob_data = get_global_data()
    with open('../data/tencent/global_data.json', 'w') as f:
        json.dump(glob_data, f)

    
