#!/bin/bash
# Debug deployment script with logging

set -e

# Enable logging
exec > >(tee /var/log/msai-deploy.log) 2>&1

echo "🚀 Starting MS AI deployment with debug logging..."
echo "Timestamp: $(date)"
echo "Instance ID: $(curl -s http://169.254.169.254/latest/meta-data/instance-id)"

# Update system
echo "Updating system packages..."
apt-get update
apt-get install -y python3 python3-pip curl wget

# Create app directory
echo "Creating application directory..."
mkdir -p /opt/msai
cd /opt/msai

# Create simple FastAPI app
echo "Creating FastAPI application..."
cat > app.py << 'EOF'
from fastapi import FastAPI
import uvicorn
from datetime import datetime
import os

app = FastAPI(title="MS AI Curriculum System")

@app.get("/")
def root():
    return {
        "message": "MS AI Curriculum System is working!",
        "status": "success",
        "domain": "msai.syzygyx.com",
        "timestamp": datetime.now().isoformat(),
        "instance_id": os.getenv("INSTANCE_ID", "unknown")
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "professors": "online",
            "curriculum": "online",
            "students": "online"
        },
        "instance_id": os.getenv("INSTANCE_ID", "unknown")
    }

@app.get("/api/professors")
def professors():
    return {
        "professors": [
            {
                "id": "prof_001",
                "name": "Dr. Sarah Chen",
                "specialization": "Machine Learning",
                "expertise_level": "Expert"
            },
            {
                "id": "prof_002",
                "name": "Dr. Michael Rodriguez",
                "specialization": "Natural Language Processing",
                "expertise_level": "Expert"
            }
        ]
    }

@app.get("/api/curriculum")
def curriculum():
    return {
        "program_name": "Master of Science in Artificial Intelligence",
        "total_credits": 36,
        "specializations": [
            "Machine Learning & Data Science",
            "Natural Language Processing",
            "Computer Vision & Robotics"
        ]
    }

@app.get("/api/students")
def students():
    return {
        "students": [
            {
                "id": "student_001",
                "name": "Alex Johnson",
                "learning_style": "Visual",
                "gpa": 3.7
            },
            {
                "id": "student_002",
                "name": "Maria Garcia",
                "learning_style": "Kinesthetic",
                "gpa": 3.9
            }
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting MS AI Curriculum System...")
    print(f"🌐 Host: 0.0.0.0")
    print(f"🔌 Port: 8000")
    print(f"📊 Domain: msai.syzygyx.com")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
EOF

# Install FastAPI
echo "Installing FastAPI..."
pip3 install fastapi uvicorn

# Create systemd service
echo "Creating systemd service..."
cat > /etc/systemd/system/msai.service << 'EOF'
[Unit]
Description=MS AI Curriculum System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/msai
Environment=INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Set proper ownership
echo "Setting ownership..."
chown -R ubuntu:ubuntu /opt/msai

# Start service
echo "Starting MS AI service..."
systemctl daemon-reload
systemctl enable msai
systemctl start msai

# Wait for service to start
echo "Waiting for service to start..."
sleep 10

# Check service status
echo "Checking service status..."
systemctl status msai --no-pager

# Test the application
echo "Testing application..."
curl -f http://localhost:8000/health || echo "Health check failed"

# Show running processes
echo "Running processes on port 8000:"
netstat -tlnp | grep :8000 || echo "No processes on port 8000"

echo "✅ MS AI deployment complete!"
echo "📋 Log file: /var/log/msai-deploy.log"
echo "🔍 Service status: systemctl status msai"
echo "📊 Application: http://localhost:8000"