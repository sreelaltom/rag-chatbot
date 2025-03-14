import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings  # Using HuggingFace instead of OpenAI

# Define the directory containing the text file and the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "data","documents", "dingan.txt")
persistent_directory = os.path.join(current_dir, "db", "chroma_db")

# Check if the Chroma vector store already exists
if not os.path.exists(persistent_directory):
    print("Persistent directory does not exist. Initializing vector store...")

    # Ensure the text file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"The file {file_path} does not exist. Please check the path."
        )

    # Read the text content from the file with proper encoding (utf-8)
    try:
        loader = TextLoader(file_path, encoding="utf-8")
        documents = loader.load()
    except UnicodeDecodeError:
        print(f"Error decoding the file with utf-8. Trying a different encoding...")
        loader = TextLoader(file_path, encoding="ISO-8859-1")  # Another commonly used encoding
        documents = loader.load()

    # Split the document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50) 
    docs = text_splitter.split_documents(documents)

    # Display information about the split documents
    print("\n--- Document Chunks Information ---")
    print(f"Number of document chunks: {len(docs)}")
    print(f"Sample chunk:\n{docs[0].page_content}\n")

    # Create embeddings using HuggingFaceEmbeddings
    print("\n--- Creating embeddings ---")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )  # A popular and free embedding model
    print("\n--- Finished creating embeddings ---")

    # Create the vector store and persist it automatically
    print("\n--- Creating vector store ---")
    db = Chroma.from_documents(
        docs, embeddings, persist_directory=persistent_directory)
    print("\n--- Finished creating vector store ---")

else:
    print("Vector store already exists. No need to initialize.")

# Questions to ask
# Who is the Ring-bearer?
# Where does Gandalf meet Frodo?
