import json
import requests


api_key = "988e37e63684135f6d0f6e471e066257"
#London
lat = 37.1289771
lon = -84.0832646

response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}")
if response.status_code == 200:
    data = response.json()

    #write in file data.json
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    #read file data.json
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    data_list = data['list'][0]
    data_main = data_list['main']['aqi']

    print(data_main)
else:
    print(response.status_code)