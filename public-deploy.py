#!/usr/bin/env python3
"""
Public MS AI Curriculum System Deployment
Makes the local application accessible via public URL
"""

import subprocess
import time
import requests
import json
from datetime import datetime

def check_local_app():
    """Check if local app is running"""
    try:
        response = requests.get('http://localhost:8001/health', timeout=5)
        if response.status_code == 200:
            print("✅ Local MS AI application is running")
            return True
    except:
        pass
    
    print("❌ Local MS AI application is not running")
    print("Please start it with: docker-compose up -d")
    return False

def install_ngrok():
    """Install ngrok if not present"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ngrok is already installed")
            return True
    except FileNotFoundError:
        pass
    
    print("Installing ngrok...")
    try:
        # Install ngrok via homebrew
        subprocess.run(['brew', 'install', 'ngrok/ngrok/ngrok'], check=True)
        print("✅ ngrok installed successfully")
        return True
    except:
        print("❌ Failed to install ngrok")
        print("Please install ngrok manually: https://ngrok.com/download")
        return False

def start_ngrok_tunnel():
    """Start ngrok tunnel"""
    print("🚀 Starting ngrok tunnel...")
    
    # Start ngrok in background
    process = subprocess.Popen(['ngrok', 'http', '8001'], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
    
    # Wait for ngrok to start
    time.sleep(3)
    
    # Get the public URL
    try:
        response = requests.get('http://localhost:4040/api/tunnels')
        if response.status_code == 200:
            tunnels = response.json()
            if tunnels['tunnels']:
                public_url = tunnels['tunnels'][0]['public_url']
                print(f"✅ Public URL: {public_url}")
                return public_url
    except:
        pass
    
    print("❌ Failed to get ngrok URL")
    return None

def test_public_access(public_url):
    """Test public access to the application"""
    print(f"🧪 Testing public access at {public_url}...")
    
    try:
        # Test health endpoint
        response = requests.get(f'{public_url}/health', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check successful:")
            print(json.dumps(data, indent=2))
            return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    return False

def test_api_endpoints(public_url):
    """Test all API endpoints"""
    endpoints = [
        ('/health', 'Health Check'),
        ('/api/professors', 'AI Professors'),
        ('/api/curriculum', 'Curriculum'),
        ('/api/students', 'Students')
    ]
    
    print("🧪 Testing all API endpoints...")
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f'{public_url}{endpoint}', timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: Working")
            else:
                print(f"❌ {name}: Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")

def main():
    """Main deployment function"""
    print("🚀 MS AI Curriculum System - Public Deployment")
    print("=" * 50)
    
    # Check local app
    if not check_local_app():
        return
    
    # Install ngrok
    if not install_ngrok():
        return
    
    # Start ngrok tunnel
    public_url = start_ngrok_tunnel()
    if not public_url:
        return
    
    # Test public access
    if test_public_access(public_url):
        print("\n🎉 SUCCESS! MS AI Curriculum System is now publicly accessible!")
        print(f"🌐 Public URL: {public_url}")
        print(f"🔍 Health Check: {public_url}/health")
        print(f"👨‍🏫 AI Professors: {public_url}/api/professors")
        print(f"📚 Curriculum: {public_url}/api/curriculum")
        print(f"👥 Students: {public_url}/api/students")
        
        # Test all endpoints
        test_api_endpoints(public_url)
        
        print("\n📋 Next Steps:")
        print("1. Share this URL with others to access the MS AI system")
        print("2. The tunnel will stay active as long as this script runs")
        print("3. Press Ctrl+C to stop the tunnel")
        
        # Keep the tunnel running
        try:
            print("\n⏳ Tunnel is running... Press Ctrl+C to stop")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping tunnel...")
    
    else:
        print("❌ Failed to establish public access")

if __name__ == "__main__":
    main()
EOF

Now let me also create a simple solution that uses the working local deployment and makes it accessible:
<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
run_terminal_cmd