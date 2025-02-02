# RAG Application with Llama3 (Ollama) and Streamlit

This is a Retrieval-Augmented Generation (RAG) application that processes legal document PDFs, stores them in a vector database using Chroma, and retrieves relevant information using Llama3 from Ollama.

## Features
- **Upload Legal Documents**: Accepts PDFs and extracts text.
- **Vector Search with Chroma**: Uses embeddings to store and retrieve relevant document sections.
- **Local AI Processing with Llama3**: Runs Llama3 locally using Ollama for fast, private inference.
- **Streamlit UI**: A simple web interface to interact with the AI model.

## Installation Guide

### 1. Install Dependencies
Before running the application, install the required dependencies using the provided `requirements.txt` file:
```sh
pip install -r requirements.txt
```

### 2. Install and Run Ollama (Llama3) Locally
#### **MacOS**
```sh
# Install Ollama
brew install ollama

# Start Ollama service
ollama serve

# Pull the Llama3 model
ollama pull llama3
```
#### **Windows**
1. Download and install [Ollama for Windows](https://ollama.com/download).
2. Open PowerShell and start the service:
   ```sh
   ollama serve
   ```
3. Pull the Llama3 model:
   ```sh
   ollama pull llama3
   ```

### 3. Set Up ChromaDB
Ensure ChromaDB is set up for vector storage:
```sh
mkdir chroma
```

### 4. Run the Application
To start the Streamlit web application, run:
```sh
streamlit run app.py
```

To populate the database with legal documents:
```sh
python populate_database.py --reset
```

To query the AI through CLI:
```sh
python query.py "Your legal question here"
```



