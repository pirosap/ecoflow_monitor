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

output_directory = "/path/to/output_directory/"
image_file_path = os.path.join(output_directory, "energy_data.png")
data_file_path = os.path.join(output_directory, "energy_data.json")

# グラフの初期化
try:
    with open(data_file_path, "r") as data_file:
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

def set_hourly_xticks():
    timestamps = [datetime.strptime(label, '%H:%M:%S') for label in time_labels]
    hours = [timestamp.hour for timestamp in timestamps]
    hourly_labels = [timestamp.strftime('%H:%M:%S') for timestamp in timestamps if timestamp.minute == 0]
    hourly_positions = [i for i, hour in enumerate(hours) if timestamps[i].minute == 0]

    plt.xticks(hourly_positions, hourly_labels, rotation=45)

def plot_graph():
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 2, 1)
    plt.plot(time_labels, soc_data, marker='o')
    plt.title("State of Charge (SOC)")
    plt.xlabel("Time")
    plt.ylabel("SOC (%)")
    set_hourly_xticks()
    plt.ylim(bottom=0)

    plt.subplot(2, 2, 2)
    plt.plot(time_labels, remain_time_data, marker='o', color='orange')
    plt.title("Remaining Time")
    plt.xlabel("Time")
    plt.ylabel("Time (minutes)")
    set_hourly_xticks()
    plt.ylim(bottom=0)

    plt.subplot(2, 2, 3)
    plt.plot(time_labels, watts_out_data, marker='o', color='green')
    plt.title("Watts Out")
    plt.xlabel("Time")
    plt.ylabel("Power (W)")
    set_hourly_xticks()
    plt.ylim(bottom=0)

    plt.subplot(2, 2, 4)
    plt.plot(time_labels, watts_in_data, marker='o', color='red')
    plt.title("Watts In")
    plt.xlabel("Time")
    plt.ylabel("Power (W)")
    set_hourly_xticks()
    plt.ylim(bottom=0)

    plt.tight_layout()

    # グラフを画像ファイルとして保存
    plt.savefig(image_file_path)

def save_data_to_file():
    # データをファイルに保存する
    data_to_save = {
        "soc_data": soc_data,
        "remain_time_data": remain_time_data,
        "watts_out_data": watts_out_data,
        "watts_in_data": watts_in_data,
        "time_labels": time_labels,
    }
    with open(data_file_path, "w") as data_file:
        json.dump(data_to_save, data_file)

# データを取得してグラフを生成
fetch_data()

# 生成したグラフを画像ファイルとして保存
plot_graph()
