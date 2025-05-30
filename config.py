import streamlit as st

OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]
COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
COHERE_MODEL = st.secrets.get("COHERE_MODEL", "command-r")
TOP_K_RESULTS = int(st.secrets.get("TOP_K_RESULTS", 2))
