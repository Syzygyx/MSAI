#!/usr/bin/env python3
"""
Deploy Static App to msai.syzygyx.com
This script replaces the current FastAPI app with our static site server
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
    print("🚀 Deploying Static App to msai.syzygyx.com...")
    
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
    os.makedirs("static_app_deployment", exist_ok=True)
    
    # Copy our files
    run_command("cp app_static.py static_app_deployment/app.py")
    run_command("cp index.html static_app_deployment/")
    run_command("cp msai_application_form.html static_app_deployment/")
    
    # Create requirements.txt
    requirements = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
'''
    with open("static_app_deployment/requirements.txt", "w") as f:
        f.write(requirements)
    
    # Create systemd service
    service_config = '''[Unit]
Description=MS AI Static Site Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/msai
ExecStart=/opt/msai/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
'''
    
    with open("static_app_deployment/msai.service", "w") as f:
        f.write(service_config)
    
    # Create nginx configuration
    nginx_config = '''server {
    listen 80;
    server_name msai.syzygyx.com www.msai.syzygyx.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
'''
    
    with open("static_app_deployment/nginx.conf", "w") as f:
        f.write(nginx_config)
    
    print("📦 Creating deployment archive...")
    run_command("tar -czf static_app_deployment.tar.gz -C static_app_deployment .")
    
    print("🚀 Uploading to server...")
    run_command(f"scp -i {KEY_FILE} static_app_deployment.tar.gz {SERVER_USER}@{SERVER_IP}:/tmp/")
    
    print("🔧 Deploying on server...")
    
    # Deploy on server
    deploy_commands = f'''
set -e

echo "📥 Extracting deployment package..."
cd /opt/msai
sudo tar -xzf /tmp/static_app_deployment.tar.gz

echo "🔧 Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "🔄 Stopping existing service..."
sudo systemctl stop msai || true

echo "📋 Updating systemd service..."
sudo cp msai.service /etc/systemd/system/
sudo systemctl daemon-reload

echo "🌐 Updating nginx configuration..."
sudo cp nginx.conf /etc/nginx/sites-available/msai.syzygyx.com
sudo ln -sf /etc/nginx/sites-available/msai.syzygyx.com /etc/nginx/sites-enabled/
sudo nginx -t

echo "🚀 Starting services..."
sudo systemctl start msai
sudo systemctl enable msai
sudo systemctl reload nginx

echo "⏳ Waiting for service to start..."
sleep 10

echo "🔍 Checking service status..."
sudo systemctl status msai --no-pager

echo "🌐 Testing endpoints..."
curl -f http://localhost:8000/ || echo "Main page check failed"
curl -f http://localhost:8000/application || echo "Application form check failed"

echo "✅ Static app deployment complete!"
'''
    
    run_command(f'ssh -i {KEY_FILE} {SERVER_USER}@{SERVER_IP} "{deploy_commands}"')
    
    print("🧹 Cleaning up...")
    run_command("rm -rf static_app_deployment")
    run_command("rm -f static_app_deployment.tar.gz")
    
    print("🎉 Static App Deployment Complete!")
    print("")
    print("🌐 Live URLs:")
    print("   Main Site: http://msai.syzygyx.com")
    print("   Application Form: http://msai.syzygyx.com/application")
    print("   Health Check: http://msai.syzygyx.com/health")
    print("")
    print("✅ The updated static site is now live!")

if __name__ == "__main__":
    main()