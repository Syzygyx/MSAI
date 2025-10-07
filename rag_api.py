#!/usr/bin/env python3
"""
FastAPI backend for RAG-powered chat agent
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import json
from pathlib import Path
from rag_system import MSRAGSystem

app = FastAPI(title="MS AI Program RAG API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system = MSRAGSystem()

# Load or create index on startup
@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    print("🚀 Starting MS AI RAG API...")
    
    # Check for OpenRouter API key
    if not os.getenv('OPENROUTER_API_KEY'):
        print("⚠️  Warning: OPENROUTER_API_KEY not found in environment variables")
        print("   RAG system will work but AI responses will be limited")
    
    # Try to load existing index
    if not rag_system.load_index():
        print("🔄 Creating new index...")
        rag_system.index_site_content()
        rag_system.save_index()
    
    print("✅ RAG system initialized successfully")

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list
    chunks_used: int
    relevance_scores: list

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint that processes questions using RAG"""
    try:
        result = rag_system.query(request.question)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "chunks_indexed": len(rag_system.content_chunks),
        "sources": list(rag_system.indexed_content.keys())
    }

@app.get("/api/stats")
async def get_stats():
    """Get RAG system statistics"""
    return {
        "total_chunks": len(rag_system.content_chunks),
        "indexed_sources": list(rag_system.indexed_content.keys()),
        "source_details": {
            source: {
                "filename": data["filename"],
                "chunk_count": data["chunk_count"]
            }
            for source, data in rag_system.indexed_content.items()
        }
    }

@app.post("/api/reindex")
async def reindex_content():
    """Reindex all content"""
    try:
        rag_system.index_site_content()
        rag_system.save_index()
        return {
            "status": "success",
            "message": "Content reindexed successfully",
            "total_chunks": len(rag_system.content_chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reindexing content: {str(e)}")

# Serve static files
app.mount("/static", StaticFiles(directory="."), name="static")

# Serve chat agent page
@app.get("/chat", response_class=HTMLResponse)
async def chat_page():
    """Serve the RAG-powered chat agent page"""
    with open("chat-agent-rag.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# Serve main site
@app.get("/", response_class=HTMLResponse)
async def main_page():
    """Serve the main site"""
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)