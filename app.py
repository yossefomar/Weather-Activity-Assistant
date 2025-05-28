# app.py
#The main application file for the Weather Assistant app
#Using Data from OpenWeatherMap API to provide weather information
import streamlit as st
from weather import get_weather

st.set_page_config(page_title="Weather Assistant", layout="centered")

st.title("🌤️ Weather Info Assistant")

city = st.text_input("Enter your city:", "Cairo")

if st.button("Get Weather"):
    with st.spinner("Fetching weather..."):
        weather = get_weather(city)
        if "error" in weather:
            st.error(weather["error"])
        else:
            st.success(f"Weather for {weather['location']}")
            st.markdown(f"""
            - **Temperature:** {weather['temperature']} °C  
            - **Condition:** {weather['condition']}  
            - **Humidity:** {weather['humidity']}%  
            - **Wind Speed:** {weather['wind']} m/s  
            """)
