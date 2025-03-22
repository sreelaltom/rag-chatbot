import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader, UnstructuredExcelLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Define directories
current_dir = os.path.dirname(os.path.abspath(__file__))
documents_dir = os.path.join(current_dir, "data", "documents")
persistent_directory = os.path.join(current_dir, "db", "chroma_db")

# Ensure the directory exists
if not os.path.exists(documents_dir):
    raise FileNotFoundError(f"The folder {documents_dir} does not exist. Please check the path.")

# Initialize document loaders for multiple formats
documents = []
for file_name in os.listdir(documents_dir):
    file_path = os.path.join(documents_dir, file_name)
    
    if file_name.endswith(".txt"):  # Load text files
        print(f"Loading text file: {file_name}")
        loader = TextLoader(file_path, encoding="utf-8")
        documents.extend(loader.load())

    elif file_name.endswith(".pdf"):  # Load PDFs
        print(f"Loading PDF file: {file_name}")
        loader = PyMuPDFLoader(file_path)  # Uses PyMuPDF
        documents.extend(loader.load())

    elif file_name.endswith((".xls", ".xlsx")):  # Load Excel files
        print(f"Loading Excel file: {file_name}")
        loader = UnstructuredExcelLoader(file_path)  # Handles Excel extraction
        documents.extend(loader.load())

# Split documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Display information about the split documents
print("\n--- Document Chunks Information ---")
print(f"Number of document chunks: {len(docs)}")
if docs:
    print(f"Sample chunk:\n{docs[0].page_content}\n")

# Create embeddings using HuggingFace
print("\n--- Creating embeddings ---")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("\n--- Finished creating embeddings ---")

# Create the vector store and persist it
print("\n--- Creating vector store ---")
db = Chroma.from_documents(docs, embeddings, persist_directory=persistent_directory)
print("\n--- Finished creating vector store ---")
