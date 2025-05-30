import cohere
from config import COHERE_API_KEY, COHERE_MODEL
import time

client = cohere.Client(COHERE_API_KEY)

def generate_response(user_query, weather_data, retrieved_chunks):
    weather_str = (
        f"Current weather in {weather_data['location']}:\n"
        f"- Temperature: {weather_data['temperature']}°C\n"
        f"- Condition: {weather_data['condition']}\n"
        f"- Humidity: {weather_data['humidity']}%\n"
        f"- Wind Speed: {weather_data['wind']} m/s\n"
    )

    retrieved_text = "\n\n".join([chunk["text"][:500] for chunk in retrieved_chunks])

    prompt = f"""
You are a helpful assistant that answers weather-related questions with grounded, practical advice.

User Question: "{user_query}"

Weather Info:
{weather_str}

Relevant Information from Knowledge Base:
{retrieved_text}

Based on the weather and knowledge base, give a complete and clear recommendation.
"""

    try:
        start = time.time()
        response = client.chat(
            model=COHERE_MODEL,
            message=prompt.strip(),
            temperature=0.7,
            max_tokens=400,
            chat_history=[],
        )
        print("Cohere call took", time.time() - start, "seconds")
        return response.text.strip()

    except Exception as e:
        return f"Error generating response: {e}"
