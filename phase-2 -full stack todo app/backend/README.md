
# RAG Chatbot for Physical AI & Humanoid Robotics Textbook

This is a Retrieval-Augmented Generation (RAG) system that allows users to query the Physical AI & Humanoid Robotics textbook using natural language.

## Features

- **Document Ingestion**: Reads all .md files from the configured path, converts to plain text, chunks them, creates embeddings using Google's Gemini, and stores vectors in Qdrant.
- **Intelligent Querying**: Accepts user questions, embeds them using Gemini, performs semantic search in Qdrant to find relevant textbook chunks, and generates responses.
- **Idempotent Ingestion**: Prevents duplicate chunks from being stored in the database.
- **Source Tracking**: Provides transparency by showing which documents were used to generate responses.

## Prerequisites

- Python 3.11+
- uv package manager
- Google Gemini API key
- Qdrant vector database (cloud or local)

## Setup

1. Clone the repository
2. Navigate to the backend directory: `cd backend`
3. Install dependencies using uv:
   ```bash
   uv sync
   ```
4. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
5. Update the `.env` file with your API keys and configuration:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `QDRANT_URL`: Your Qdrant instance URL
   - `QDRANT_API_KEY`: Your Qdrant API key (if using cloud version)
   - `BOOK_DOCS_PATH`: Path to your textbook markdown files (default: ./docs)

## Usage

### Running the Application

The recommended way to run the application is with uvicorn:

```bash
# Navigate to the backend directory
cd backend

# Run the application
uv run python main.py
```

Alternatively, you can run it directly with uvicorn from the backend directory:
```bash
cd backend
uv run uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at `http://localhost:8001` with documentation at `http://localhost:8001/docs`.

### API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/ingest` - Ingest textbook documents into the vector database
- `POST /api/query` - Query the textbook knowledge base
- `GET /api/documents` - Get list of all documents in the knowledge base

### Ingesting Documents

To ingest your textbook documents, make a POST request to `/api/ingest`. This will read all .md files from the configured path, process them, and store them in the vector database.

```bash
curl -X POST http://localhost:8001/api/ingest
```

### Querying the Knowledge Base

To ask questions about the textbook content, make a POST request to `/api/query` with a JSON payload:

```bash
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type": "application/json" \
  -d '{
    "query_text": "What is Physical AI?",
    "top_k": 5
  }'
```

## Architecture

The system consists of several key components:

- **Document Processor**: Reads, parses, and chunks markdown documents
- **Embedding Service**: Creates vector embeddings using Google's Gemini API
- **Qdrant Service**: Stores and retrieves vector embeddings
- **RAG Agent**: Generates responses based on retrieved document chunks
- **API Layer**: FastAPI endpoints for ingestion and querying

## Environment Variables

- `GEMINI_API_KEY`: Google Gemini API key
- `QDRANT_URL`: Qdrant instance URL
- `QDRANT_API_KEY`: Qdrant API key (for cloud instances)
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection (default: textbook_vectors)
- `BOOK_DOCS_PATH`: Path to textbook markdown files (default: ./docs)
- `APP_HOST`: Host for the FastAPI application (default: 0.0.0.0)
- `APP_PORT`: Port for the FastAPI application (default: 8000)
- `EMBEDDING_MODEL`: Gemini embedding model to use (default: models/embedding-001)
- `CHUNK_SIZE`: Size of text chunks for embedding (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `TOP_K`: Number of top chunks to retrieve (default: 5)

## Project Structure

```
backend/