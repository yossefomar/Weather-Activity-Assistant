import streamlit as st
import os

def get_secret(key, default=None):
    return st.secrets.get(key) or os.getenv(key) or default

OPENWEATHER_API_KEY = get_secret("OPENWEATHER_API_KEY")
COHERE_API_KEY = get_secret("COHERE_API_KEY")
COHERE_MODEL = get_secret("COHERE_MODEL", "command-r")
TOP_K_RESULTS = int(get_secret("TOP_K_RESULTS", 2))
