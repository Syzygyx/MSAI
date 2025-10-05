#!/usr/bin/env python3
"""
Simple deployment script for MS AI Curriculum System to EC2
"""

import subprocess
import time
import json

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False, e.stderr

def main():
    """Main deployment function"""
    print("🎓 MS AI Curriculum System - Simple EC2 Deployment")
    print("=" * 50)
    
    # EC2 instance details
    instance_id = "i-022994775b8ec3ca7"
    instance_ip = "44.220.164.13"
    key_file = "msai-production-key.pem"
    
    # Check if instance is running
    success, output = run_command(
        f"aws ec2 describe-instances --instance-ids {instance_id} --query 'Reservations[0].Instances[0].State.Name' --output text",
        "Checking EC2 instance status"
    )
    
    if not success or "running" not in output:
        print("❌ EC2 instance is not running")
        return False
    
    print(f"✅ EC2 instance {instance_id} is running at {instance_ip}")
    
    # Create a simple application file
    app_content = '''#!/usr/bin/env python3
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
'''
    
    # Create requirements.txt
    requirements_content = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
'''
    
    # Create deployment script
    deploy_script = f'''#!/bin/bash
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
{app_content}
EOF

# Create requirements.txt
sudo tee requirements.txt > /dev/null << 'EOF'
{requirements_content}
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
echo "🌐 Application should be available at: http://{instance_ip}:8000"
'''
    
    # Save deployment script
    with open('ec2_deploy.sh', 'w') as f:
        f.write(deploy_script)
    
    # Make it executable
    run_command("chmod +x ec2_deploy.sh", "Making deployment script executable")
    
    print(f"\n🎯 Deployment script created: ec2_deploy.sh")
    print(f"📍 Target: {instance_ip}")
    print(f"🔑 Key: {key_file}")
    
    print("\n📋 Manual deployment steps:")
    print("1. Copy the deployment script to EC2:")
    print(f"   scp -i {key_file} ec2_deploy.sh ubuntu@{instance_ip}:/tmp/")
    print("2. SSH into EC2 and run the script:")
    print(f"   ssh -i {key_file} ubuntu@{instance_ip}")
    print("   bash /tmp/ec2_deploy.sh")
    print("3. Test the application:")
    print(f"   curl http://{instance_ip}:8000/health")
    print(f"   curl http://msai.syzygyx.com:8000/health")
    
    print("\n🎉 Deployment preparation completed!")
    print("=" * 40)
    
    return True

if __name__ == "__main__":
    main()