import json
import requests

#API air pollution
api_key = "988e37e63684135f6d0f6e471e066257"

#get city from api
city = "Paris"

city_request = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}")
if city_request.status_code == 200:
    data_city = city_request.json()

    #write in file data.json
    with open('city.json', 'w', encoding='utf-8') as file:
        json.dump(data_city, file, ensure_ascii=False, indent=4)

    with open('city.json', 'r', encoding='utf-8') as file:
        data_city = json.load(file)

    contry = data_city[0]['name']
    lat = data_city[0]['lat']
    lon = data_city[0]['lon']

    print(contry)
    print(lat)
    print(lon)
    
else:
    print(city_request.status_code)

#status pollution

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