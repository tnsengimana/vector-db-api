from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chunks, documents, libraries


app = FastAPI(
    title="Vector Database API",
    description="A REST API for indexing and querying documents in a Vector Database",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chunks.router)
app.include_router(documents.router)
app.include_router(libraries.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Vector Database API",
        "docs": "/docs",
        "endpoints": {
            "chunks": "/chunks",
            "documents": "/documents",
            "libraries": "/libraries"
        }
    } 
