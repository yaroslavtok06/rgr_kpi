import json
import tkinter as tk
from tkinter import ttk
import requests


api_key = "988e37e63684135f6d0f6e471e066257"
lat = 10
lon = 50

response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}")
if response.status_code == 200:
    data = response.json()

    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    list_data = data['list']
    first_item = list_data[0]
    main = first_item['main']
    aqi_list = main['aqi']

    root = tk.Tk()
    root.title("JSON Viewer")

    ttk.Label(root, text="Status of air pollution:").grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)
    ttk.Label(root, text=aqi_list).grid(column=1, row=0, sticky=tk.W, padx=10, pady=5)

    root.mainloop()

else:
    print(response.status_code)