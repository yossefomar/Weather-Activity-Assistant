# weather.py
#Handles fetching weather data from OpenWeatherMap API
import requests
from config import OPENWEATHER_API_KEY

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Failed to get weather for {city}."}
    
    data = response.json()
    return {
        "location": data["name"],
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["description"].capitalize(),
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"]
    }
