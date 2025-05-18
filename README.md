# Vector Database REST API

A REST API for indexing and querying documents in a Vector Database. This project allows users to create, read, update, and delete libraries, documents, and chunks, as well as perform k-Nearest Neighbor vector searches.

## Features

- CRUD operations for libraries, documents, and chunks
- Multiple indexing algorithms:
  - Linear search (brute force)
  - KD-Tree
  - Hierarchical Navigable Small World (HNSW)
- Thread-safe in-memory database with locking mechanisms
- Docker support

## Installation

### Using Docker

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/vector-db-api.git
   cd vector-db-api
   ```

2. Build the Docker image:
   ```
   docker build -t vector-db-api .
   ```

3. Run the container:
   ```
   docker run -p 8000:8000 vector-db-api
   ```

### Manual Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/vector-db-api.git
   cd vector-db-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the API server:
   ```
   uvicorn app.main:app --reload
   ```

## API Documentation

The API documentation is available at `http://localhost:8000/docs` when the server is running.

### Endpoints

- **Libraries**:
  - `GET /libraries`: Get all libraries
  - `POST /libraries`: Create a new library
  - `GET /libraries/{library_id}`: Get a library by ID
  - `PUT /libraries/{library_id}`: Update a library
  - `DELETE /libraries/{library_id}`: Delete a library
  - `POST /libraries/{library_id}/documents/{document_id}`: Add a document to a library
  - `DELETE /libraries/{library_id}/documents/{document_id}`: Remove a document from a library
  - `GET /libraries/{library_id}/documents`: Get all documents in a library

- **Documents**:
  - `GET /documents`: Get all documents
  - `POST /documents`: Create a new document
  - `GET /documents/{document_id}`: Get a document by ID
  - `PUT /documents/{document_id}`: Update a document
  - `DELETE /documents/{document_id}`: Delete a document
  - `POST /documents/{document_id}/chunks/{chunk_id}`: Add a chunk to a document
  - `DELETE /documents/{document_id}/chunks/{chunk_id}`: Remove a chunk from a document
  - `GET /documents/{document_id}/chunks`: Get all chunks in a document

- **Chunks**:
  - `GET /chunks`: Get all chunks
  - `POST /chunks`: Create a new chunk
  - `GET /chunks/{chunk_id}`: Get a chunk by ID
  - `PUT /chunks/{chunk_id}`: Update a chunk
  - `DELETE /chunks/{chunk_id}`: Delete a chunk

- **Search**:
  - `POST /search/{library_id}/index`: Index all chunks in a library
  - `POST /search/{library_id}`: Search for most similar chunks in a library

## Data Models

### Chunk

A chunk is a piece of text with an associated embedding and metadata.

```json
{
  "id": "string",
  "text": "string",
  "embedding": [0.1, 0.2, 0.3, ...],
  "metadata": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

### Document

A document is made out of multiple chunks and contains metadata.

```json
{
  "id": "string",
  "chunks": ["chunk_id_1", "chunk_id_2", ...],
  "metadata": {
    "title": "Document Title",
    "author": "Author Name",
    "date": "2025-05-01"
  }
}
```

### Library

A library is made out of a list of documents and can contain other metadata.

```json
{
  "id": "string",
  "name": "Library Name",
  "documents": ["document_id_1", "document_id_2", ...],
  "metadata": {
    "description": "Library Description",
    "created_at": "2025-05-01"
  }
}
```

## Indexing Algorithms

### Linear Index

- **Time Complexity**:
  - Build: O(n) where n is the number of chunks
  - Search: O(n) where n is the number of chunks
  - Add: O(1)
  - Remove: O(1)
  - Update: O(1)

- **Space Complexity**:
  - O(n) where n is the number of chunks

- **Use Case**:
  - Small datasets
  - Simple implementation
  - Baseline for comparison

### KD-Tree

- **Time Complexity**:
  - Build: O(n log n) where n is the number of chunks
  - Search: O(log n) in the best case, O(n) in the worst case
  - Add: O(log n) for balanced tree
  - Remove: O(log n) for balanced tree
  - Update: O(log n) + O(log n) (remove + add)

- **Space Complexity**:
  - O(n) where n is the number of chunks

- **Use Case**:
  - Medium-sized datasets
  - Low-dimensional data (e.g., 2D, 3D)
  - When exact search is required

### HNSW (Hierarchical Navigable Small World)

- **Time Complexity**:
  - Build: O(n log n) where n is the number of chunks
  - Search: O(log n) in the average case
  - Add: O(log n)
  - Remove: O(1) for soft deletion
  - Update: O(log n)

- **Space Complexity**:
  - O(n * M * L) where:
    - n is the number of chunks
    - M is the maximum number of connections per node
    - L is the number of layers

- **Use Case**:
  - Large datasets
  - High-dimensional data
  - When approximate search is acceptable
  - State-of-the-art performance for similarity search

## Thread Safety

The API uses a thread-safe in-memory database with locking mechanisms to prevent data races between reads and writes. The implementation includes:

- Read-write locks for individual operations
- Global lock for operations that span multiple resources
- Copy-on-read/write to prevent shared state issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. 