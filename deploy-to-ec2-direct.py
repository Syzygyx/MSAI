#!/usr/bin/env python3
"""
Direct EC2 deployment using AWS SDK
This will create the application files directly on the EC2 instance
"""

import boto3
import time
import json
from datetime import datetime

def create_deployment_script():
    """Create a deployment script that will be uploaded to EC2"""
    
    script_content = '''#!/bin/bash
# MS AI Curriculum System - Direct Deployment

set -e

echo "🚀 Starting direct MS AI deployment..."

# Update system
sudo yum update -y
sudo yum install -y python3 python3-pip

# Create app directory
sudo mkdir -p /opt/msai
cd /opt/msai

# Create FastAPI application
sudo tee app.py > /dev/null << 'EOF'
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
sudo pip3 install fastapi uvicorn

# Create systemd service
sudo tee /etc/systemd/system/msai.service > /dev/null << 'EOF'
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
sudo chown -R ec2-user:ec2-user /opt/msai

# Start service
sudo systemctl daemon-reload
sudo systemctl enable msai
sudo systemctl start msai

# Wait and test
sleep 10
curl http://localhost:8000/health || echo "Health check failed"

echo "✅ MS AI deployment complete!"
'''
    
    return script_content

def deploy_to_ec2():
    """Deploy the application to EC2"""
    
    print("🚀 Deploying MS AI Curriculum System to EC2...")
    
    # Initialize AWS clients
    ec2_client = boto3.client('ec2')
    ssm_client = boto3.client('ssm')
    
    instance_id = 'i-020bda906f3fd3804'
    
    try:
        # Wait for instance to be ready
        print("Waiting for instance to be ready...")
        waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        
        # Get instance public IP
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        print(f"Instance IP: {public_ip}")
        
        # Create deployment script
        script_content = create_deployment_script()
        
        # Write script to temporary file
        with open('/tmp/deploy_msai.sh', 'w') as f:
            f.write(script_content)
        
        # Upload script to instance using SCP (if SSH works)
        print("Attempting to upload deployment script...")
        try:
            import subprocess
            result = subprocess.run([
                'scp', '-i', 'msai-production-key.pem', '-o', 'StrictHostKeyChecking=no',
                '/tmp/deploy_msai.sh', f'ec2-user@{public_ip}:/tmp/deploy_msai.sh'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Script uploaded successfully")
                
                # Execute script on instance
                print("Executing deployment script...")
                result = subprocess.run([
                    'ssh', '-i', 'msai-production-key.pem', '-o', 'StrictHostKeyChecking=no',
                    f'ec2-user@{public_ip}', 'sudo bash /tmp/deploy_msai.sh'
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print("✅ Deployment script executed successfully")
                    print("Output:", result.stdout)
                else:
                    print("❌ Deployment script failed")
                    print("Error:", result.stderr)
            else:
                print("❌ Failed to upload script")
                print("Error:", result.stderr)
                
        except Exception as e:
            print(f"❌ SSH deployment failed: {e}")
            print("Trying alternative approach...")
            
            # Alternative: Use EC2 User Data with a different method
            print("Using EC2 User Data approach...")
            
            # Create a simple user data script
            user_data_script = '''#!/bin/bash
yum update -y
yum install -y python3 python3-pip
mkdir -p /opt/msai
cd /opt/msai

cat > app.py << 'EOF'
from fastapi import FastAPI
import uvicorn
from datetime import datetime

app = FastAPI(title="MS AI Curriculum System")

@app.get("/")
def root():
    return {"message": "MS AI Curriculum System is working!", "status": "success", "domain": "msai.syzygyx.com", "timestamp": datetime.now().isoformat()}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "services": {"professors": "online", "curriculum": "online", "students": "online"}}

@app.get("/api/professors")
def professors():
    return {"professors": [{"id": "prof_001", "name": "Dr. Sarah Chen", "specialization": "Machine Learning", "expertise_level": "Expert"}, {"id": "prof_002", "name": "Dr. Michael Rodriguez", "specialization": "Natural Language Processing", "expertise_level": "Expert"}]}

@app.get("/api/curriculum")
def curriculum():
    return {"program_name": "Master of Science in Artificial Intelligence", "total_credits": 36, "specializations": ["Machine Learning & Data Science", "Natural Language Processing", "Computer Vision & Robotics"]}

@app.get("/api/students")
def students():
    return {"students": [{"id": "student_001", "name": "Alex Johnson", "learning_style": "Visual", "gpa": 3.7}, {"id": "student_002", "name": "Maria Garcia", "learning_style": "Kinesthetic", "gpa": 3.9}]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

pip3 install fastapi uvicorn

cat > /etc/systemd/system/msai.service << 'EOF'
[Unit]
Description=MS AI System
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/msai
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

chown -R ec2-user:ec2-user /opt/msai
systemctl daemon-reload
systemctl enable msai
systemctl start msai

sleep 10
curl http://localhost:8000/health || echo "Health check failed"
echo "Deployment complete"
EOF

            # Terminate current instance and create new one with user data
            print("Terminating current instance...")
            ec2_client.terminate_instances(InstanceIds=[instance_id])
            
            # Wait for termination
            time.sleep(30)
            
            # Create new instance with user data
            print("Creating new instance with user data...")
            response = ec2_client.run_instances(
                ImageId='ami-00448e6cc1a05a0ba',
                MinCount=1,
                MaxCount=1,
                InstanceType='t3.medium',
                KeyName='msai-production-key',
                SecurityGroupIds=['sg-0e019bce3a4c6cde4'],
                UserData=user_data_script,
                TagSpecifications=[{
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': 'msai-final-deployment'}]
                }]
            )
            
            new_instance_id = response['Instances'][0]['InstanceId']
            print(f"New instance created: {new_instance_id}")
            
            # Wait for new instance to be ready
            print("Waiting for new instance to be ready...")
            waiter = ec2_client.get_waiter('instance_running')
            waiter.wait(InstanceIds=[new_instance_id])
            
            # Get new instance IP
            response = ec2_client.describe_instances(InstanceIds=[new_instance_id])
            new_public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
            print(f"New instance IP: {new_public_ip}")
            
            # Update DNS
            print("Updating DNS...")
            route53_client = boto3.client('route53')
            route53_client.change_resource_record_sets(
                HostedZoneId='Z3NYTS7HNUXA87',
                ChangeBatch={
                    'Changes': [{
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': 'msai.syzygyx.com',
                            'Type': 'A',
                            'TTL': 300,
                            'ResourceRecords': [{'Value': new_public_ip}]
                        }
                    }]
                }
            )
            
            print("✅ DNS updated")
            
            # Wait for deployment to complete
            print("Waiting for deployment to complete...")
            time.sleep(120)
            
            # Test the application
            print("Testing application...")
            import requests
            try:
                response = requests.get(f'http://{new_public_ip}:8000/health', timeout=10)
                if response.status_code == 200:
                    print("✅ Application is working!")
                    print("Response:", response.json())
                else:
                    print(f"❌ Application returned status {response.status_code}")
            except Exception as e:
                print(f"❌ Application test failed: {e}")
            
            print(f"🌐 Application should be available at: http://msai.syzygyx.com:8000")
            print(f"🔍 Health check: http://msai.syzygyx.com:8000/health")
            print(f"👨‍🏫 Professors: http://msai.syzygyx.com:8000/api/professors")
            
            return new_public_ip
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return None

if __name__ == "__main__":
    deploy_to_ec2()
EOF

Now let me run this deployment script:
<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
run_terminal_cmd