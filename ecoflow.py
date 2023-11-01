import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime
import os

# APIのURLとヘッダー情報を設定
api_url = "https://api.ecoflow.com/iot-service/open/api/device/queryDeviceQuota?sn=XXX"
headers = {
    'Content-Type': 'application/json',
    'appKey': 'xxx',
    'secretKey': 'xxx'
}

# データをファイルに保存・読み込むためのファイル名
data_file_name = "energy_data.json"

# グラフの初期化
try:
    with open(data_file_name, "r") as data_file:
        saved_data = json.load(data_file)
        soc_data = saved_data["soc_data"]
        remain_time_data = saved_data["remain_time_data"]
        watts_out_data = saved_data["watts_out_data"]
        watts_in_data = saved_data["watts_in_data"]
        time_labels = saved_data["time_labels"]
except FileNotFoundError:
    soc_data = []
    remain_time_data = []
    watts_out_data = []
    watts_in_data = []
    time_labels = []

def fetch_data():
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            soc = data['data']['soc']
            remain_time = data['data']['remainTime']
            watts_out = data['data']['wattsOutSum']
            watts_in = data['data']['wattsInSum']
            timestamp = datetime.now().strftime('%H:%M:%S')

            soc_data.append(soc)
            remain_time_data.append(remain_time)
            watts_out_data.append(watts_out)
            watts_in_data.append(watts_in)
            time_labels.append(timestamp)

            # データの更新ごとにグラフを描画
            plot_graph()

            # データをファイルに保存
            save_data_to_file()

    except Exception as e:
        print(f"Error fetching data: {e}")

def plot_graph():
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 2, 1)
    plt.plot(time_labels, soc_data, marker='o')
    plt.title("State of Charge (SOC)")
    plt.xlabel("Time")
    plt.ylabel("SOC (%)")

    plt.subplot(2, 2, 2)
    plt.plot(time_labels, remain_time_data, marker='o', color='orange')
    plt.title("Remaining Time")
    plt.xlabel("Time")
    plt.ylabel("Time (minutes)")

    plt.subplot(2, 2, 3)
    plt.plot(time_labels, watts_out_data, marker='o', color='green')
    plt.title("Watts Out")
    plt.xlabel("Time")
    plt.ylabel("Power (W)")

    plt.subplot(2, 2, 4)
    plt.plot(time_labels, watts_in_data, marker='o', color='red')
    plt.title("Watts In")
    plt.xlabel("Time")
    plt.ylabel("Power (W)")

    plt.tight_layout()

    # グラフを画像ファイルとして保存
    plt.savefig("energy_data.png")

def save_data_to_file():
    # データをファイルに保存する
    data_to_save = {
        "soc_data": soc_data,
        "remain_time_data": remain_time_data,
        "watts_out_data": watts_out_data,
        "watts_in_data": watts_in_data,
        "time_labels": time_labels,
    }
    with open(data_file_name, "w") as data_file:
        json.dump(data_to_save, data_file)

# データを取得してグラフを生成
fetch_data()

# 生成したグラフを画像ファイルとして保存
plot_graph()
