#  Weather Activity & Clothing Assistant

A smart, weather-aware assistant that uses real-time weather data + PDF knowledge to help users plan what to wear and do — powered by LLMs and Retrieval-Augmented Generation (RAG).

---

##  Features

-  Real-time weather data via OpenWeatherMap
-  PDF knowledge base (multi-country weather & activity guide)
-  Semantic search via FAISS + Sentence Transformers
-  Answer generation via Cohere's Command-R+ (or Command-R)
-  Streamlit UI: simple, responsive, and user-friendly

---

## How It Works

1. **User asks a weather-related question**
2. **Weather API** fetches current conditions for the specified location
3. **Semantic search** retrieves relevant PDF chunks
4. **LLM (Cohere)** generates a final helpful answer combining:
   - Real-time weather
   - RAG search results
   - Natural language generation

---

## Project Structure
weather-activity-assistant/
├── app.py # Streamlit UI
├── weather.py # OpenWeather API logic
├── retrieval.py # FAISS search + embeddings
├── llm_response.py # Cohere-powered response generator
├── config.py # Loads API keys from .env
├── ingest_pdf.py # Chunks + embeds PDF
├── test_LLM.py # CLI test for final LLM response
├── .env # API keys (not tracked by Git)
├── .gitignore
└── vector_store/ # FAISS index + metadata
