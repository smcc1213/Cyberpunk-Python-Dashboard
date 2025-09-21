# Cyberpunk Dashboard

A neon cyberpunk-themed system dashboard built with **Python (PyQt5)** that integrates:

- 🕶️ Zeek log viewer with syntax highlighting  
- 🌤️ Live weather with automatic location detection  
- 💻 System performance monitor  
- 📈 Real-time graphing widget  
- 🕒 Full-screen cyberpunk layout with neon accents  

---

## 🚀 Features

- Zeek integration: View live network logs with suspicious activity highlighted  
- System monitor: CPU, RAM, and system stats  
- Weather: Live weather for your location via OpenWeatherMap  
- Cyberpunk UI: Bold neon colors, borders, fonts, and fullscreen layout  

---

## 📦 Requirements

- Python 3.10+  
- Zeek (Linux/macOS; Windows not supported natively)  
- `pip install -r requirements.txt`

---

## ⚙️ Configuration

This app uses a **`.env` file** for custom settings. Create a `.env` file in the project root:

```env
# .env
USER_NAME="YOUR NAME"
ZEEK_LOG_DIR="/home/cyberpunk_dashboard/zeek_logs"
ZEEK_INTERFACE="wlp4s0"
WEATHER_API_KEY="your_openweathermap_api_key"
