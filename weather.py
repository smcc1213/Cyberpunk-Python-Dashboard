import requests
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from dotenv import load_dotenv
import os

class WeatherWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #111111; border: 2px solid #00ffcc;")
        layout = QVBoxLayout()

        self.weather_label = QLabel("Loading weather...")
        self.weather_label.setFont(QFont("Orbitron", 10))
        self.weather_label.setAlignment(Qt.AlignRight)

        layout.addWidget(self.weather_label)
        self.setLayout(layout)

        self.update_weather()

    def update_weather(self):
        try:
            load_dotenv()
            api_key = os.getenv("WEATHER_API_KEY")
            if not api_key:
                self.weather_label.setText("Missing WEATHER_API_KEY in .env")
                return

            # Get location
            ipinfo = requests.get("https://ipinfo.io/json").json()
            city = ipinfo.get("city", "Lawrence")
            loc = ipinfo.get("loc", "38.9717,-95.2353")
            lat, lon = loc.split(",")

            # Get weather data
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
            response = requests.get(url)
            data = response.json()

            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            condition = data["weather"][0]["main"]

            symbol = self.get_symbol(condition)
            self.weather_label.setText(f"{city}: {temp:.0f}°F {symbol} - {desc}")

        except Exception as e:
            self.weather_label.setText(f"Weather error: {e}")

    def get_symbol(self, condition):
        if "Clear" in condition:
            return "🌞"
        elif "Cloud" in condition:
            return "☁️"
        elif "Rain" in condition or "Drizzle" in condition:
            return "🌧️"
        elif "Snow" in condition:
            return "❄️"
        elif "Thunderstorm" in condition:
            return "⛈️"
        else:
            return "🌀"
