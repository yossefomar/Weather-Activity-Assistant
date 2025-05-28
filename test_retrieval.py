from retrieval import search_chunks

query = "what is the weather in USA (California) in Winter?"
results = search_chunks(query)

for i, r in enumerate(results):
    print(f"\n🔹 Result {i+1}:")
    print(r["text"])
