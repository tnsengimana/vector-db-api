# Vector Database REST API

A REST API for indexing and querying documents in a Vector Database. This project allows users to create, read, update, and delete libraries, documents, and chunks, indexing a library, as well as performing k-Nearest Neighbor vector searches.

## Features

- CRUD operations for libraries, documents, and chunks
- Integration with Cohere to compute embeddings
- Multiple indexing algorithms:
  - Linear search (brute force). It's the baseline to understand vector db in general. Generally not ideal!
  - Locality-sensitive Hashing (LSH). Ideal for high dimensional and sparse data, and when approximating nearest neighor is acceptable. Also, it illustrates how ANN algorithms can sometimes be a hit and miss.
  - TODO: Hierarchical Navigable Small World (HNSW). State-of-the art algorithm, adopted throughout the industry. Strikes the right balance between retrieval precision and speed.
- In-memory database and vector db index
- Thread-safety for database and vector db index
  - Read-write locks for individual operations
  - Copy-on-read/write to prevent shared state issues

## Installation

### Using Docker

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/vector-db-api.git
   cd vector-db-api
   ```

2. Run the container:
   ```
   docker compose up --build
   ```

### Manual Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/vector-db-api.git
   cd vector-db-api
   ```

2. Create and activate a virtual environment:
   ```
   uv sync
   source venv/bin/activate
   ```

3. Run the API server:
   ```
   fastapi dev app/main.py
   ```

## API Documentation

The API documentation is available at `http://localhost:8000/docs` when the server is running.


