#!/usr/bin/env python3
"""
MS AI Static Site Server
Serves our updated HTML content on msai.syzygyx.com
"""

import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Create FastAPI application
app = FastAPI(
    title="MS AI Program - AURNOVA University",
    description="Master of Science in Artificial Intelligence Program",
    version="2.0.0"
)

# Serve static files if they exist
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Serve the main index page"""
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    else:
        return HTMLResponse(content="<h1>MS AI Program - AURNOVA University</h1><p>Site under maintenance</p>")

@app.get("/application", response_class=HTMLResponse)
async def read_application():
    """Serve the application form"""
    if os.path.exists("msai_application_form.html"):
        with open("msai_application_form.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    else:
        return HTMLResponse(content="<h1>Application Form</h1><p>Form not available</p>")

@app.get("/apply", response_class=HTMLResponse)
async def read_apply():
    """Alias for application form"""
    return await read_application()

@app.get("/form", response_class=HTMLResponse)
async def read_form():
    """Alias for application form"""
    return await read_application()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "MS AI Static Site"}

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "status": "operational",
        "service": "MS AI Program Site",
        "version": "2.0.0",
        "endpoints": {
            "main": "/",
            "application": "/application",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)