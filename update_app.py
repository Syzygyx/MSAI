#!/usr/bin/env python3
"""
Update the existing FastAPI app to serve our HTML content
"""

import os
import subprocess
import sys

def run_command(cmd, check=True):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def main():
    print("🚀 Updating FastAPI app to serve our HTML content...")
    
    # Read our HTML files
    with open("index.html", "r", encoding="utf-8") as f:
        index_content = f.read()
    
    with open("msai_application_form.html", "r", encoding="utf-8") as f:
        form_content = f.read()
    
    # Create a new app.py that serves our content
    app_content = f'''#!/usr/bin/env python3
"""
MS AI Program - AURNOVA University
Updated to serve our HTML content
"""

import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

# Create FastAPI application
app = FastAPI(
    title="MS AI Program - AURNOVA University",
    description="Master of Science in Artificial Intelligence Program",
    version="2.0.0"
)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Serve the main index page"""
    return HTMLResponse(content="""{index_content}""")

@app.get("/application", response_class=HTMLResponse)
async def read_application():
    """Serve the application form"""
    return HTMLResponse(content="""{form_content}""")

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
    return {{"status": "healthy", "service": "MS AI Program Site", "version": "2.0.0"}}

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {{
        "status": "operational",
        "service": "MS AI Program Site",
        "version": "2.0.0",
        "endpoints": {{
            "main": "/",
            "application": "/application",
            "health": "/health"
        }}
    }}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    # Write the new app.py
    with open("app_updated.py", "w", encoding="utf-8") as f:
        f.write(app_content)
    
    print("✅ Created updated app.py with our HTML content")
    print("📋 Files created:")
    print("   - app_updated.py (contains our HTML content)")
    print("")
    print("🌐 To deploy this:")
    print("   1. Copy app_updated.py to the server as app.py")
    print("   2. Restart the service")
    print("")
    print("📄 Content included:")
    print(f"   - Main page: {len(index_content)} characters")
    print(f"   - Application form: {len(form_content)} characters")

if __name__ == "__main__":
    main()