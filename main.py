import tkinter as tk
from tkinter import messagebox, filedialog
import json
import requests
import csv
import os
import ttkbootstrap as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AirPollutionApp:
    def __init__(self, root):
        self.root = root
        self.api_key = "988e37e63684135f6d0f6e471e066257"
        self.setup_gui()
        self.load_city_data()

    def setup_gui(self):
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.title("Air Pollution")
        style = ttk.Style("superhero")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Main")

        self.file_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.file_tab, text="Functions")

        header_frame = ttk.Frame(self.main_tab, bootstyle="dark")
        header_frame.pack(fill="x")
        title_label = ttk.Label(
            header_frame, text="Air Pollution", font=('Arial', 20, 'bold'),
            bootstyle="inverse-dark")
        title_label.pack(pady=10)

        io_frame = ttk.Frame(self.main_tab, padding=10)
        io_frame.pack(expand=True, fill="both")

        input_frame = ttk.Labelframe(io_frame, text="City info", padding=10)
        input_frame.pack(fill="x", pady=10)

        ttk.Label(input_frame, text="City:", font=('Arial', 12)).grid(
            row=0, column=0, sticky="w", padx=10, pady=5)
        self.city_entry = ttk.Entry(input_frame, font=('Arial', 12), width=30)
        self.city_entry.grid(row=0, column=1, pady=5)

        ttk.Label(input_frame, text="Latitude:", font=('Arial', 12)).grid(
            row=1, column=0, sticky="w", padx=10, pady=5)
        self.lat_entry = ttk.Entry(input_frame, font=('Arial', 12), width=30)
        self.lat_entry.grid(row=1, column=1, pady=5)

        ttk.Label(input_frame, text="Longitude:", font=('Arial', 12)).grid(
            row=2, column=0, sticky="w", padx=10, pady=5)
        self.lon_entry = ttk.Entry(input_frame, font=('Arial', 12), width=30)
        self.lon_entry.grid(row=2, column=1, pady=5)

        ttk.Button(
            input_frame, text="Get Details", bootstyle="primary",
            command=self.on_submit).grid(row=3, columnspan=2, pady=15)

        output_frame = ttk.Labelframe(io_frame, text="Results", padding=10)
        output_frame.pack(fill="x", pady=10)

        self.pollution_label = ttk.Label(
            output_frame, text="Status of air pollution: ", font=('Arial', 12, 'bold'))
        self.pollution_label.pack(pady=5)

        self.details_frame = ttk.Frame(output_frame)
        self.details_frame.pack()

        pollutants = ["CO", "NO", "NO2", "O3", "SO2", "NH3"]
        self.pollutant_labels = {}

        for i, pollutant in enumerate(pollutants):
            label = ttk.Label(
                self.details_frame, text=f"{pollutant}: ", font=('Arial', 11))
            label.grid(row=i, column=0, sticky="w", padx=10, pady=3)
            self.pollutant_labels[pollutant] = ttk.Label(
                self.details_frame, text="N/A", font=('Arial', 11))
            self.pollutant_labels[pollutant].grid(
                row=i, column=1, sticky="w", pady=3)

        file_frame = ttk.Labelframe(
            self.file_tab, text="Functions", padding=10)
        file_frame.pack(expand=True, fill="both", pady=20, padx=20)
        file_label = ttk.Label(
            file_frame, text="Choose option", font=('Arial', 16, 'bold'),
            bootstyle="inverse-dark")
        file_label.pack(pady=10)

        ttk.Button(
            file_frame, text="Save Results to CSV", bootstyle="success",
            command=self.save_to_csv).pack(pady=10)

        ttk.Button(
            file_frame, text="Load Results from CSV", bootstyle="info",
            command=self.load_from_csv).pack(pady=10)

        ttk.Button(
            file_frame, text="Show graphic", bootstyle="warning",
            command=self.show_pie_chart).pack(pady=10)

    def load_city_data(self):
        if os.path.exists('city.json'):
            with open('city.json', 'r', encoding='utf-8') as file:
                data_city = json.load(file)
                if data_city:
                    lat = data_city[0]['lat']
                    lon = data_city[0]['lon']
                    self.lat_entry.insert(0, lat)
                    self.lon_entry.insert(0, lon)

    def get_air_pollution(self, city=None, lat=None, lon=None):
        if city:
            city_request = requests.get(
                f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={self.api_key}")
            if city_request.status_code == 200:
                data_city = city_request.json()
                with open('city.json', 'w', encoding='utf-8') as file:
                    json.dump(data_city, file, ensure_ascii=False, indent=4)
                lat = data_city[0]['lat']
                lon = data_city[0]['lon']
                self.lat_entry.delete(0, tk.END)
                self.lon_entry.delete(0, tk.END)
                self.lat_entry.insert(0, lat)
                self.lon_entry.insert(0, lon)
            else:
                messagebox.showerror(
                    "Error", f"Error while retrieving city data: {city_request.status_code}")
                return

        if lat and lon:
            response = requests.get(
                f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.api_key}")
            if response.status_code == 200:
                data = response.json()
                with open('data.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                data_list = data['list'][0]
                data_main = data_list['main']['aqi']
                components = data_list['components']
                self.pollution_label.config(
                    text=f"Status of air pollution: {data_main}")
                for pollutant, value in components.items():
                    if pollutant.upper() in self.pollutant_labels:
                        self.pollutant_labels[pollutant.upper()].config(
                            text=value)
            else:
                messagebox.showerror(
                    "Error", f"Pollution error: {response.status_code}")
        else:
            messagebox.showwarning("Warning", "Enter city or another details")

    def on_submit(self):
        city = self.city_entry.get()
        lat = self.lat_entry.get()
        lon = self.lon_entry.get()

        if city:
            self.get_air_pollution(city=city)
        elif lat and lon:
            self.get_air_pollution(lat=lat, lon=lon)
        else:
            messagebox.showwarning("Warning", "Enter city or another details")

    def save_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Pollutant", "Value"])
                for pollutant, label in self.pollutant_labels.items():
                    writer.writerow([pollutant, label.cget("text")])
            messagebox.showinfo("Success", "Data saved successfully!")

    def load_from_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    pollutant, value = row
                    if pollutant in self.pollutant_labels:
                        self.pollutant_labels[pollutant].config(text=value)
            messagebox.showinfo("Success", "Data loaded successfully!")

    def show_pie_chart(self):
        components = {}
        for pollutant, label in self.pollutant_labels.items():
            try:
                value = float(label.cget("text"))
                components[pollutant] = value
            except ValueError:
                continue

        if components:
            labels = components.keys()
            values = components.values()
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            plt.title("Air Pollution Components")
            plt.show()
        else:
            messagebox.showwarning(
                "Warning", "No data to display in the pie chart.")


root = ttk.Window(themename="superhero")
app = AirPollutionApp(root)
root.mainloop()
