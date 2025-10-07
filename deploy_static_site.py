#!/usr/bin/env python3
"""
Deploy Static HTML Site to msai.syzygyx.com
This script deploys our updated HTML content to the live site
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def main():
    print("🚀 Deploying Static HTML Site to msai.syzygyx.com...")
    
    # Server details
    SERVER_IP = "44.220.164.13"
    SERVER_USER = "ubuntu"
    KEY_FILE = "msai-production-key.pem"
    
    # Check if key file exists
    if not os.path.exists(KEY_FILE):
        print(f"❌ Key file {KEY_FILE} not found. Please ensure the SSH key is available.")
        sys.exit(1)
    
    print("📋 Preparing deployment files...")
    
    # Create deployment package
    os.makedirs("static_deployment", exist_ok=True)
    
    # Copy our HTML files
    run_command("cp index.html static_deployment/")
    run_command("cp msai_application_form.html static_deployment/")
    
    # Create a simple Python server to serve static files
    server_script = '''#!/usr/bin/env python3
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
'''
    
    with open("static_deployment/server.py", "w") as f:
        f.write(server_script)
    
    # Create nginx configuration for static files
    nginx_config = '''server {
    listen 80;
    server_name msai.syzygyx.com www.msai.syzygyx.com;

    root /opt/msai/static;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /application {
        try_files /msai_application_form.html =404;
    }

    location /apply {
        try_files /msai_application_form.html =404;
    }

    location /form {
        try_files /msai_application_form.html =404;
    }

    # Cache static files
    location ~* \\.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
'''
    
    with open("static_deployment/nginx_static.conf", "w") as f:
        f.write(nginx_config)
    
    # Create systemd service for static server
    service_config = '''[Unit]
Description=MS AI Static Site Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/msai
ExecStart=/usr/bin/python3 /opt/msai/server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
'''
    
    with open("static_deployment/msai-static.service", "w") as f:
        f.write(service_config)
    
    print("📦 Creating deployment archive...")
    run_command("tar -czf static_site_deployment.tar.gz -C static_deployment .")
    
    print("🚀 Uploading to server...")
    run_command(f"scp -i {KEY_FILE} static_site_deployment.tar.gz {SERVER_USER}@{SERVER_IP}:/tmp/")
    
    print("🔧 Deploying on server...")
    
    # Deploy on server
    deploy_commands = f'''
set -e

echo "📥 Extracting deployment package..."
cd /opt/msai
sudo rm -rf static
sudo mkdir -p static
cd static
sudo tar -xzf /tmp/static_site_deployment.tar.gz

echo "🔧 Setting up static server..."
cd /opt/msai
sudo cp static/server.py ./
sudo chmod +x server.py

echo "🔄 Stopping existing services..."
sudo systemctl stop msai || true
sudo systemctl stop msai-static || true

echo "📋 Updating systemd service..."
sudo cp static/msai-static.service /etc/systemd/system/msai-static.service
sudo systemctl daemon-reload

echo "🌐 Updating nginx configuration..."
sudo cp static/nginx_static.conf /etc/nginx/sites-available/msai.syzygyx.com
sudo ln -sf /etc/nginx/sites-available/msai.syzygyx.com /etc/nginx/sites-enabled/
sudo nginx -t

echo "🚀 Starting services..."
sudo systemctl start msai-static
sudo systemctl enable msai-static
sudo systemctl reload nginx

echo "⏳ Waiting for service to start..."
sleep 5

echo "🔍 Checking service status..."
sudo systemctl status msai-static --no-pager

echo "🌐 Testing endpoints..."
curl -f http://localhost:8000/ || echo "Main page check failed"
curl -f http://localhost:8000/application || echo "Application form check failed"

echo "✅ Static site deployment complete!"
'''
    
    run_command(f'ssh -i {KEY_FILE} {SERVER_USER}@{SERVER_IP} "{deploy_commands}"')
    
    print("🧹 Cleaning up...")
    run_command("rm -rf static_deployment")
    run_command("rm -f static_site_deployment.tar.gz")
    
    print("🎉 Static Site Deployment Complete!")
    print("")
    print("🌐 Live URLs:")
    print("   Main Site: http://msai.syzygyx.com")
    print("   Application Form: http://msai.syzygyx.com/application")
    print("")
    print("✅ The updated static site is now live!")

if __name__ == "__main__":
    main()