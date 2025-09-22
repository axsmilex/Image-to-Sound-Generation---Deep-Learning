# -*- encoding: utf-8 -*-

import random
import time
import traceback
import requests
import csv
from itertools import product
from copy import deepcopy
import os
from utils import TOKEN_LIST

# set current working directory to the directory of this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# begin code
session = requests.session()

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "authorization": "Bearer 20230612bpun02f8s6058r8ncbbukpi6u0",
    "content-type": "application/json;charset=UTF-8",
    "referer": "https://housesigma.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
data = {
    "listing_days": 0,
    "sold_days": "90",
    "de_list_days": "90",
    "list_type": [
        2,
        4,
        6
    ],
    "house_type": [
        "all"
    ],
    "listing_price": [
        0,
        6000000
    ],
    "rent_price": [
        0,
        10000
    ],
    "bedroom_range": [
        0
    ],
    "bathroom_min": 0,
    "garage_min": 0,
    "basement": [],
    "open_house_date": 0,
    "max_maintenance_fee": 0,
    "square_footage": [
        0,
        4000
    ],
    "front_feet": [
        0,
        100
    ],
    "show_comparision": 1,
    "description": "",
    "lat1": 43.85450000000000,
    "lon1": -79.33330000000000,
    "lat2": 43.85260000000000,
    "lon2": -79.34240000000000,
    "price": [],
    "zoom": 17.87,
    "lang": "en_US",
    "province": "ON"
}


def split_area(lat1: float, lon1: float, lat2: float, lon2: float):
    """
    lat1 > lat2 > 0, 0 > lon1 > lon2
    :param lat1:
    :param lon1:
    :param lat2:
    :param lon2:
    :return:
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    (a, b) + (b, c) = (a, b, b, c)
    """
    lat_list = []
    lon_list = []
    while lat1 > lat2:
        lat_list.append((lat1, lat1 - 0.0019))
        lat1 -= 0.0019
    while lon1 > lon2:
        lon_list.append((lon1, lon1 - 0.0091))
        lon1 -= 0.0091
    for lat_tuple, lon_tuple in product(lat_list, lon_list):
        yield lat_tuple + lon_tuple


def search_houses(index: int, data: dict):
    global headers
    url = "https://housesigma.com/bkv2/api/search/mapsearchv3/listing"
    while True:
        try:
            headers["authorization"] = random.choice(TOKEN_LIST)
            response = session.post(url, headers=headers, json=data, timeout=10)
            if response.json().get("status"):
                print(f"Area number {index} - request success")
                break
        except requests.exceptions.Timeout:
            print(f"Area number {index} - request time-out")
        except requests.exceptions.JSONDecodeError:
            print(f"Area number {index} - json request error-> {response.text}")
            # print
        except:
            traceback.print_exc()
        time.sleep(1)
    data_dict_list = response.json().get("data").get("list")
    if not data_dict_list:
        print(f"Area number {index} with coordinate({data['lat1']},{data['lon1']},{data['lat2']},{data['lon2']}) contains NO DATA -> {response.json().get('data').get('message')}")
        return
    with open("house_ids_type4_rr.csv", "a+", newline="", encoding="utf-8")as f:
        writer = csv.writer(f)
        for data_dict in data_dict_list:
            count = data_dict.get("count")
            house_ids = data_dict.get("ids")
            lat = data_dict.get("location").get("lat")
            lon = data_dict.get("location").get("lon")
            for house_id in house_ids:
                writer.writerow([
                    data["province"], house_id, count, lat, lon, data["lat1"], data["lon1"], data["lat2"], data["lon2"]
                ])


def main():
    form_data = deepcopy(data)
    form_data["province"] = "ON"

    # list type:
    # To find, 打开network 搜索listing2 然后点payload 看第一行的list_type
    # 不要拖动地图区域，直接选择别的criteria，点击新产生的listing2，然后点payload，看第一行的list_type
    # 会发现 for lease还是for sale一定是前提，然后active/sold/delisted是后面的条件
    # 对应了6种情况：

    # 2: for lease and active
    # 4: for lease and leased
    # 6: for lease and de-listed

    # 5: for sale and delisted
    # 1: for sale and active
    # 3: for sale and sold

    #form_data["list_type"] = "2"

    # 时间：记得改变both sold_days 和 de_list_days
    form_data["sold_days"] = "Y2017"
    form_data["list_type"] = [4]
    # form_data["de_list_days"] = "Y2017"

    index = 1
    lat1 = 44.2
    lon1 = -78
    lat2 = 43.2
    lon2 = -80


    # Loop through all the years
    for year in range(2017, 2023):
        form_data["sold_days"] = "Y" + str(year)
        # Loop through all the areas
        for lat_lon_tuple in split_area(lat1, lon1, lat2, lon2):
            # if index <= 43441:
            #     index += 1
            #     continue
            form_data["lat1"], form_data["lat2"], form_data["lon1"], form_data["lon2"] = lat_lon_tuple
            search_houses(index, form_data)
            index += 1


if __name__ == '__main__':
    main()


