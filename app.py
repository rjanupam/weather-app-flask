import os
from datetime import datetime

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    forecast_data = None
    error = None
    city = request.form.get("city")
    if city:
        try:
            weather_data = get_weather_data(city)
            forecast_data = get_forecast_data(city)
        except requests.exceptions.RequestException as e:
            error = f"Error getting weather data: {e}"
    return render_template(
        "index.html",
        weather_data=weather_data,
        forecast_data=forecast_data,
        error=error,
    )


def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "pressure": data["main"]["pressure"],
            "visibility": data["visibility"],
        }
        return weather
    else:
        return None


def get_forecast_data(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast = []
        for day in data["list"]:
            dt = datetime.strptime(day["dt_txt"], "%Y-%m-%d %H:%M:%S")
            daily_forecast = {
                "date": dt.strftime("%b %d"),
                "time": dt.strftime("%H:%M"),
                "temp": day["main"]["temp"],
                "description": day["weather"][0]["description"],
                "icon": day["weather"][0]["icon"],
            }
            forecast.append(daily_forecast)
        return forecast
    else:
        return None


if __name__ == "__main__":
    app.run(debug=True)
