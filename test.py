import os
import json
import requests
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
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

# Load the vector store
db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)

# Initialize conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

print("\nChat with the AI. Type 'exit' or 'quit' to stop.\n")

# Interactive loop
while True:
    query = input("You: ")  # Get user input
    if query.lower() in ["exit", "quit"]:
        print("Exiting chat. Goodbye!")
        break  # Exit condition

    # Retrieve past conversation history
    chat_history = [
    msg.content for msg in memory.load_memory_variables({}).get("chat_history", [])
]


    # Search in vector database
    results = db.similarity_search(query, k=3)

    # Combine Documents, User Query, and Chat History
    combined_input = (
        "Here is the chat history:\n" + "\n".join(chat_history) + "\n\n"
        "New question: " + query + "\n\n"
        "Here are some documents that might help answer the question:\n"
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
        "model": "mistralai/mistral-small-3.1-24b-instruct:free",  # Using Mistral
        "messages": [
            {"role": "system", "content": "You are an AI assistant. Use past conversation history and provided documents to give relevant answers."},
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

    # Store conversation in memory
    memory.save_context({"input": query}, {"output": answer})

    # Output the Results
    print("\nAI:", answer, "\n")
