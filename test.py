import os
import json
import requests
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

# OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Define the Chroma DB Path
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_directory = os.path.join(current_dir, "db", "chroma_db")

# Load Chroma DB with HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Loading the vector store
print("Vector store already exists. Loading the vector store...")
db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)

# --- Query to see the data ---
print("\n--- Querying the vector store ---")
query = "Dinkoism emergence"  # Or any query you want to test
results = db.similarity_search(query, k=3)  # Fetching top 3 results for the query

# Display the Relevant Documents
print("\n--- Relevant Documents ---")
for i, result in enumerate(results):
    print(f"Document {i + 1}: {result.page_content[:200]}...")  # Show first 200 characters

# Combine Documents and User Query for OpenRouter API
combined_input = (
    "Here are some documents that might help answer the question: "
    + query
    + "\n\nRelevant Documents:\n"
    + "\n\n".join([doc.page_content for doc in results])
)

# Send Request to OpenRouter API
response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "google/gemma-3-4b-it:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Your task is to summarize the key points from the documents provided, focusing on providing a brief overview of the content."},
            {"role": "user", "content": combined_input}
        ]
    })
)


# Extract Response
response_data = response.json()
if "choices" in response_data:
    answer = response_data['choices'][0]['message']['content']
else:
    answer = "Error: No response from OpenRouter API."

# Output the Results
print("\n--- Generated Response ---")
print(answer)
