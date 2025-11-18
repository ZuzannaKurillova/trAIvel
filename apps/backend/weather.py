# apps/backend/weather.py
import os
import requests

API_KEY = os.environ.get("OPENWEATHER_API_KEY")
if API_KEY:
    API_KEY = API_KEY.strip('"').strip("'")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str) -> dict:
    """Return current weather info for a city"""
    if not API_KEY:
        print("DEBUG - OPENWEATHER_API_KEY is not set!")
        return {"error": "OPENWEATHER_API_KEY environment variable not set"}

    print(f"DEBUG - Fetching weather for: {city}")

    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"  # Celsius
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        print(f"DEBUG - Weather API status code: {response.status_code}")

        if response.status_code != 200:
            return {"error": data.get("message", "Unknown error")}

        weather_data = {
            "temperature": round(data["main"]["temp"]),
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        print(f"DEBUG - Parsed weather data: {weather_data}")
        return weather_data
    except Exception as e:
        print(f"DEBUG - Weather exception: {e}")
        return {"error": str(e)}
