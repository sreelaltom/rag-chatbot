import os
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))

persistent_directory = os.path.join(current_dir, "db", "chroma_db")

# Check if the directory exists and delete it
if os.path.exists(persistent_directory):
    print(f"Vector store exists at {persistent_directory}. Deleting the existing database...")
    shutil.rmtree(persistent_directory)  # This will delete the entire directory and its contents
    print("Deleted the existing vector store.")
else:
    print("No vector store found at the specified location.")
