#!/usr/bin/env python3
"""
Simple HTTP server to serve static HTML files
"""
import http.server
import socketserver
import os
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def do_GET(self):
        # Route requests to appropriate files
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        elif self.path == '/application' or self.path == '/apply':
            self.path = '/msai_application_form.html'
        elif self.path == '/form':
            self.path = '/msai_application_form.html'
        
        return super().do_GET()

if __name__ == "__main__":
    PORT = 8000
    os.chdir('/opt/msai/static')
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Server running at port {PORT}")
        httpd.serve_forever()
