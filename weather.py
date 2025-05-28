# weather.py
#Handles fetching weather data from OpenWeatherMap API
# weather.py
import requests
from config import OPENWEATHER_API_KEY

"""_summary_
Handles fetching weather data from OpenWeatherMap API.
Returns a dictionary with weather information (or) an error message.
"""
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    # Debugging output of the request
    print("Status code:", response.status_code)
    print("Response text:", response.text)

    if response.status_code != 200:
        return {"error": f"API Error {response.status_code}: {response.text}"}

    # Parse the JSON response and extract relevant data
    try:
        data = response.json()
        return {
            "location": data["name"],
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"]
        }
    except Exception as e:
        return {"error": f"Failed to parse response: {e}"}
