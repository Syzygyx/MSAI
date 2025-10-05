#!/bin/bash
set -e

echo "🚀 Deploying MS AI Curriculum System..."

# Update system
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Create application directory
sudo mkdir -p /opt/msai
cd /opt/msai

# Create app.py
sudo tee app.py > /dev/null << 'EOF'
#!/usr/bin/env python3
"""
MS AI Curriculum System - Simple Production App
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="MS AI Curriculum System",
    description="Human-Centered AI Education Platform",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to MS AI Curriculum System",
        "version": "1.0.0",
        "status": "online",
        "domain": "msai.syzygyx.com",
        "description": "Human-Centered AI Education Platform"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "services": {
            "professors": "online",
            "curriculum": "online",
            "students": "online",
            "database": "online"
        }
    }

@app.get("/api/professors")
async def get_professors():
    """Get AI professors information"""
    return {
        "professors": [
            {
                "id": "prof_001",
                "name": "Dr. Sarah Chen",
                "specialization": "Machine Learning",
                "expertise_level": "Expert",
                "h_index": 45,
                "total_citations": 1250,
                "persona": {
                    "teaching_philosophy": "Learning through hands-on experience and real-world applications",
                    "motivational_quotes": ["The future belongs to those who learn AI today", "Every algorithm tells a story"]
                }
            },
            {
                "id": "prof_002", 
                "name": "Dr. Michael Rodriguez",
                "specialization": "Natural Language Processing",
                "expertise_level": "Expert",
                "h_index": 38,
                "total_citations": 980,
                "persona": {
                    "teaching_philosophy": "Understanding language is understanding intelligence",
                    "motivational_quotes": ["Language is the bridge between human and artificial intelligence", "Words have power, algorithms amplify it"]
                }
            }
        ]
    }

@app.get("/api/curriculum")
async def get_curriculum():
    """Get curriculum information"""
    return {
        "program_name": "Master of Science in Artificial Intelligence",
        "total_credits": 36,
        "core_courses": 6,
        "specialization_tracks": 3,
        "accreditation_body": "ABET",
        "duration": "2 years",
        "specializations": [
            "Machine Learning & Data Science",
            "Natural Language Processing", 
            "Computer Vision & Robotics"
        ]
    }

@app.get("/api/students")
async def get_students():
    """Get simulated students"""
    return {
        "students": [
            {
                "id": "student_001",
                "name": "Alex Johnson",
                "learning_style": "Visual",
                "current_level": "Intermediate",
                "enrolled_courses": ["ML Fundamentals", "Data Structures"],
                "gpa": 3.7
            },
            {
                "id": "student_002",
                "name": "Maria Garcia",
                "learning_style": "Kinesthetic", 
                "current_level": "Advanced",
                "enrolled_courses": ["Deep Learning", "NLP Applications"],
                "gpa": 3.9
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

EOF

# Create requirements.txt
sudo tee requirements.txt > /dev/null << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0

EOF

# Install Python dependencies
sudo pip3 install -r requirements.txt

# Create systemd service
sudo tee /etc/systemd/system/msai.service > /dev/null << 'EOF'
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
Environment=PORT=8000
Environment=HOST=0.0.0.0

[Install]
WantedBy=multi-user.target
EOF

# Set proper ownership
sudo chown -R ubuntu:ubuntu /opt/msai

# Start the service
sudo systemctl daemon-reload
sudo systemctl enable msai
sudo systemctl start msai

# Check service status
sudo systemctl status msai

echo "✅ MS AI Curriculum System deployed successfully!"
echo "🌐 Application should be available at: http://44.220.164.13:8000"
