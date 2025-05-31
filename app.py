import streamlit as st
from weather import get_weather
from retrieval import search_chunks
from llm_response import generate_response

st.set_page_config(page_title="Weather Assistant", layout="centered")
st.title("🌦️ Smart Weather Activity & Clothing Assistant")

# --- Input section with separate location field
col1, col2 = st.columns([1, 2])

with col1:
    location = st.text_input(
        "📍 Location:", 
        placeholder="e.g., London, Cairo, Japan",
        help="Enter city or country name"
    )

with col2:
    user_query = st.text_input(
        "❓ Ask your question:", 
        placeholder="e.g., 'What should I wear?' or 'Best time to visit?'",
        help="Ask about weather, clothing, or activities"
    )

if st.button("Get Recommendation"):
    if not user_query or not location:
        st.warning("Please enter both location and your question.")
    else:
        with st.spinner("🔍 Retrieving weather and knowledge..."):

            # 1. Get live weather
            weather = get_weather(location.strip())
            if "error" in weather:
                st.error(f"Weather API Error: {weather['error']}")
            else:
                # 2. Search semantic PDF database
                retrieved_chunks = search_chunks(user_query)

                if not retrieved_chunks:
                    st.warning("No relevant results found in PDF knowledge base.")
                else:
                    # 3. Generate final answer
                    answer = generate_response(user_query, weather, retrieved_chunks)
                    st.success("Recommendation generated successfully!")
                    st.markdown(f"Assistant Answer:\n{answer}")
