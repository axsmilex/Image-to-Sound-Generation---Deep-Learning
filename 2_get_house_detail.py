# -*- encoding: utf-8 -*-

import csv
import random
import time
import traceback
import requests
import json
import os
from typing import Tuple, Set
from pathlib import Path
from utils import TOKEN_LIST

# set current working directory to the directory of this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Start the session
session = requests.session()

# Create a directory to store the json files
dir = "./json4_rrr"
Path(dir).mkdir(exist_ok=True, parents=True)

# Initiate Headers
headers = {
    "authority": "housesigma.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-CA,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,en-US;q=0.5",
    "authorization": "Bearer 202307043o463qeke6dof6po81mcp0g3of",
    "content-type": "application/json;charset=UTF-8",
    "referer": "https://housesigma.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# There are a total of four receivers for a single house id; therefore, we need to make four requests to get all the data
# sold is later proved redundant

# This function is used to get the detail of a house
def get_detail(id_listing: str, province: str, lang: str = "en_US") -> tuple:
    """
    detail接口
    :param id_listing: house id
    :param province: On
    :param lang: 语言 默认美英
    :return: Tuple(id_community, house_type, lat, lon)
    """
    global headers
    url = "https://housesigma.com/bkv2/api/listing/info/detail_v2"
    data = {
        "id_listing": id_listing,
        "lang": lang,
        "province": province
    }
    while True:
        try:
            headers["authorization"] = random.choice(TOKEN_LIST)
            response = session.post(url, headers=headers, json=data, timeout=10)
            json_data = response.json()
            if json_data.get("status"):
                print(f"`detail` {id_listing} - SUCCESS")
                break
            print(f"`detail` {id_listing} - FAIL -> {response.text}")
        except requests.exceptions.JSONDecodeError:
            print(f"`detail` {id_listing} - json ERROR-> {response.text}")
        except requests.exceptions.Timeout:
            print(f"`detail` {id_listing} - TIMEOUT")
        except:
            traceback.print_exc()
        time.sleep(1)
    save_json(f"{dir}/{id_listing}-detail.json", json_data)
    try:
        house_type = json_data["data"]["house"]["house_type"]
        id_community = json_data["data"]["house"]["id_community"]
    except:
        id_community = "无"
        house_type = ""
    try:
        lat = json_data["data"]["house"]["map"]["lat"]
        lon = json_data["data"]["house"]["map"]["lon"]
    except:
        lat = 0
        lon = 0
    return id_community, house_type, lat, lon

# This function is used to get the sold price stats of a house
def sold_price_stats(id_listing: str, id_community: int, house_type: str, province: str, lang: str = "en_US"):
    """
    sold_price_stats接口
    :param id_listing: house id
    :param id_community: 社区id 从detail接口来
    :param house_type: 类型 从detail接口来
    :param province: 省份
    :param lang: 语言
    :return: None
    """
    global headers
    url = "https://housesigma.com/bkv2/api/community/soldpricestats"
    data = {
        "id_community": id_community,
        "house_type": house_type,
        "lang": lang,
        "province": province
    }
    while True:
        try:
            headers["authorization"] = random.choice(TOKEN_LIST)
            response = session.post(url, headers=headers, json=data, timeout=10)
            json_data = response.json()
            if json_data.get("status"):
                print(f"`sold_price_stats` {id_listing} - SUCCESS")
                break
            print(f"`sold_price_stats` {id_listing} - FAIL -> {response.text}")
        except requests.exceptions.JSONDecodeError:
            print(f"`sold_price_stats` {id_listing} - JSON ERROR -> {response.text}")
        except requests.exceptions.Timeout:
            print(f"`sold_price_stats` {id_listing} - TIMEOUT")
        except:
            traceback.print_exc()
        time.sleep(1)
    save_json(f"{dir}/{id_listing}-sold_price_stats.json", json_data)

# This function is used to get the sold price stats of a house
def sold(id_listing: str, province: str, lang: str = "en_US"):
    """
    sold接口
    :param id_listing: house id
    :param province: 省份
    :param lang: 语言 默认美英
    :return: None
    """
    global headers
    url = "https://housesigma.com/bkv2/api/listing/nearby/sold"
    data = {
        "id_listing": id_listing,
        "lang": lang,
        "province": province
    }
    while True:
        try:
            headers["authorization"] = random.choice(TOKEN_LIST)
            response = session.post(url, headers=headers, json=data, timeout=10)
            json_data = response.json()
            if json_data.get("status"):
                print(f"`sold` {id_listing} - SUCCESS")
                break
            print(f"`sold` {id_listing} - FAIL > {response.text}")
        except requests.exceptions.Timeout:
            print(f"`sold` {id_listing} - TIMEOUT")
        except requests.exceptions.JSONDecodeError:
            print(f"`sold` {id_listing} - JSON ERROR -> {response.text}")
        except:
            traceback.print_exc()
        time.sleep(1)
    save_json(f"{dir}/{id_listing}-sold.json", json_data)


def demographic(id_listing: str, lat: float, lon: float, province: str, lang: str = "en_US"):
    """
    demographic接口
    :param id_listing: 房源id
    :param lat: 经度 detail接口来
    :param lon: 纬度 detail接口来
    :param province: 省份
    :param lang: 语言
    :return:
    """
    global headers
    url = "https://housesigma.com/bkv2/api/stats/demographic"
    data = {
        "lat": lat,
        "lon": lon,
        "lang": lang,
        "province": province
    }
    while True:
        try:
            headers["authorization"] = random.choice(TOKEN_LIST)
            response = session.post(url, headers=headers, json=data, timeout=10)
            json_data = response.json()
            if json_data.get("status"):
                print(f"`demographic` {id_listing} - SUCCESS")
                break
            print(f"`demographic` {id_listing} - FAIL -> {response.text}")
        except requests.exceptions.Timeout:
            print(f"`demographic` {id_listing} - TIME OUT")
        except requests.exceptions.JSONDecodeError:
            print(f"`demographic` {id_listing} - JSON ERROR -> {response.text}")
        except:
            traceback.print_exc()
        time.sleep(1)
    save_json(f"{dir}/{id_listing}-demographic.json", json_data)


def save_json(file_name: str, json_data: dict):
    with open(file_name, "w", encoding="utf-8")as f:
        json.dump(json_data, f)


def main():
    # 用来记录已经爬取过的house id
    record_id_dict = {}
    for file_name in os.listdir("./json"):
        record_id_dict[file_name.split("-")[0]] = 1
    with open("house_ids_type4_rr.csv", "r", encoding="utf-8")as f:
        reader = csv.reader(f)
        # De-duplicate to avoid duplicate requests
        rows: Set[Tuple[str]] = set([tuple(row[:2]) for row in reader])
    total = len(rows)
    for index, row in enumerate(rows):
        print(f" Number {index + 1} out of {total} ")
        if not row:
            continue
        id_listing: str = row[1]
        if record_id_dict.get(id_listing):
            print(f"{id_listing} has already been requested, SKIP!")
            continue
        province: str = row[0]
        id_community, house_type, lat, lon = get_detail(id_listing, province)

        # Check if not null
        if id_community != "无":
            sold_price_stats(id_listing, id_community, house_type, province)
        # sold(id_listing, province)

        # Check if both latitude and longitude can be found
        if lat and lon:
            demographic(id_listing, lat, lon, province)
        print("=" * 100)


if __name__ == '__main__':
    main()
