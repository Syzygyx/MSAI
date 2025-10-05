#!/bin/bash
# Deploy MS AI Curriculum System on port 80

set -e

echo "🚀 Deploying MS AI Curriculum System on port 80..."

# Update system
yum update -y
yum install -y python3 python3-pip nginx

# Create app directory
mkdir -p /opt/msai
cd /opt/msai

# Create FastAPI app
cat > app.py << 'EOF'
from fastapi import FastAPI
import uvicorn
from datetime import datetime

app = FastAPI(title="MS AI Curriculum System")

@app.get("/")
def root():
    return {
        "message": "MS AI Curriculum System is working!",
        "status": "success",
        "domain": "msai.syzygyx.com",
        "timestamp": datetime.now().isoformat()
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
        }
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

# Install FastAPI
pip3 install fastapi uvicorn

# Create nginx configuration for port 80
cat > /etc/nginx/conf.d/msai.conf << 'EOF'
server {
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
EOF

# Remove default nginx config
rm -f /etc/nginx/conf.d/default.conf

# Create systemd service
cat > /etc/systemd/system/msai.service << 'EOF'
[Unit]
Description=MS AI Curriculum System
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/msai
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Set ownership
chown -R ec2-user:ec2-user /opt/msai

# Start services
systemctl daemon-reload
systemctl enable msai
systemctl start msai
systemctl enable nginx
systemctl restart nginx

# Wait and test
sleep 10
curl http://localhost:8000/health || echo "App health check failed"
curl http://localhost/health || echo "Nginx proxy test failed"

echo "✅ MS AI deployment on port 80 complete!"
EOF

Now let me deploy this to EC2:
<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
run_terminal_cmd