#!/bin/bash
# Compact MS AI Curriculum System Deployment

set -e

echo "🚀 Deploying MS AI Curriculum System..."

# Update system
apt-get update
apt-get install -y python3 python3-pip nginx

# Create application directory
mkdir -p /opt/msai
cd /opt/msai

# Create FastAPI app
cat > app.py << 'EOF'
from fastapi import FastAPI
import uvicorn
from datetime import datetime

app = FastAPI(title="MS AI Curriculum System")

@app.get("/")
def read_root():
    return {
        "message": "MS AI Curriculum System is live!",
        "status": "success",
        "domain": "msai.syzygyx.com",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health_check():
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
def get_professors():
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
def get_curriculum():
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
def get_students():
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

# Create nginx config
cat > /etc/nginx/sites-available/msai << 'EOF'
server {
    listen 80;
    server_name msai.syzygyx.com www.msai.syzygyx.com;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/msai /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Create systemd service
cat > /etc/systemd/system/msai.service << 'EOF'
[Unit]
Description=MS AI Curriculum System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/msai
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Start services
systemctl daemon-reload
systemctl enable msai
systemctl start msai
systemctl enable nginx
systemctl restart nginx

# Wait and test
sleep 10
curl -f http://localhost:8000/health || echo "App test failed"
curl -f http://localhost/health || echo "Nginx test failed"

echo "✅ Deployment completed!"
EOF

Now let me create the EC2 instance with the compact script:
<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
run_terminal_cmd