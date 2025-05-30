from retrieval import search_chunks
from weather import get_weather
from llm_response import generate_response

query = "What should I wear in Giza now?"
weather = get_weather("Japan")
chunks = search_chunks(query)
answer = generate_response(query, weather, chunks)

print("\n💬 Assistant Answer:\n", answer)
