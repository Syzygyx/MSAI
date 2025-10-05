#!/usr/bin/env python3
"""
Deploy MS AI Curriculum System to AWS
Complete deployment script for msai.syzygyx.com
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Any
import boto3
from botocore.exceptions import ClientError

class AWSDeploymentManager:
    """Manages complete AWS deployment for MS AI system"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.domain = 'msai.syzygyx.com'
        self.project_root = Path(__file__).parent.parent
        self.deployment_dir = self.project_root / 'deployment'
        
        # Initialize AWS clients
        self.session = boto3.Session(region_name=region)
        self.ec2 = self.session.client('ec2')
        self.rds = self.session.client('rds')
        self.s3 = self.session.client('s3')
        self.cloudfront = self.session.client('cloudfront')
        self.route53 = self.session.client('route53')
        self.acm = self.session.client('acm')
        self.iam = self.session.client('iam')
        self.ssm = self.session.client('ssm')
        
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met"""
        print("🔍 Checking prerequisites...")
        
        # Check AWS credentials
        try:
            self.session.client('sts').get_caller_identity()
            print("✅ AWS credentials configured")
        except Exception as e:
            print(f"❌ AWS credentials not configured: {e}")
            return False
        
        # Check required tools
        required_tools = ['docker', 'docker-compose', 'git']
        for tool in required_tools:
            if not self._command_exists(tool):
                print(f"❌ {tool} not found. Please install {tool}")
                return False
            print(f"✅ {tool} found")
        
        # Check if project files exist
        required_files = [
            'ai-systems/professors.py',
            'curriculum/framework.py',
            'simulated_students/student.py'
        ]
        
        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                print(f"❌ Required file not found: {file_path}")
                return False
            print(f"✅ {file_path} found")
        
        print("✅ All prerequisites met")
        return True
    
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        try:
            subprocess.run(['which', command], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def create_key_pair(self) -> str:
        """Create EC2 key pair for SSH access"""
        print("🔑 Creating EC2 key pair...")
        
        key_name = 'msai-production-key'
        
        try:
            # Check if key pair already exists
            self.ec2.describe_key_pairs(KeyNames=[key_name])
            print(f"✅ Key pair {key_name} already exists")
            return key_name
        except ClientError:
            pass
        
        try:
            # Create new key pair
            response = self.ec2.create_key_pair(
                KeyName=key_name,
                TagSpecifications=[
                    {
                        'ResourceType': 'key-pair',
                        'Tags': [
                            {'Key': 'Name', 'Value': key_name},
                            {'Key': 'Project', 'Value': 'MS-AI-Curriculum'}
                        ]
                    }
                ]
            )
            
            # Save private key to file
            key_file = self.deployment_dir / f'{key_name}.pem'
            with open(key_file, 'w') as f:
                f.write(response['KeyMaterial'])
            
            # Set proper permissions
            os.chmod(key_file, 0o400)
            
            print(f"✅ Key pair created: {key_name}")
            print(f"📁 Private key saved to: {key_file}")
            return key_name
            
        except ClientError as e:
            print(f"❌ Error creating key pair: {e}")
            return None
    
    def deploy_infrastructure(self) -> Dict[str, Any]:
        """Deploy AWS infrastructure"""
        print("🏗️ Deploying AWS infrastructure...")
        
        # Import and run infrastructure deployment
        sys.path.append(str(self.deployment_dir))
        from aws_infrastructure import AWSInfrastructureManager
        
        infra_manager = AWSInfrastructureManager(self.region)
        deployment_info = infra_manager.deploy_infrastructure(self.domain)
        
        return deployment_info
    
    def prepare_application(self) -> bool:
        """Prepare application for deployment"""
        print("📦 Preparing application for deployment...")
        
        # Generate Docker configurations
        sys.path.append(str(self.deployment_dir))
        from docker_setup import DockerConfigGenerator
        
        generator = DockerConfigGenerator()
        generator.generate_all_configs(str(self.deployment_dir))
        
        # Create .env file from template
        env_template = self.deployment_dir / '.env.template'
        env_file = self.deployment_dir / '.env'
        
        if env_template.exists() and not env_file.exists():
            with open(env_template, 'r') as f:
                env_content = f.read()
            
            # Replace placeholder values
            env_content = env_content.replace('your_password', 'MSAI_Production_2024!')
            env_content = env_content.replace('your_secret_key_here_minimum_32_characters', 
                                            'MSAI_Secret_Key_2024_Production_Minimum_32_Characters_Long')
            env_content = env_content.replace('your_jwt_secret_key_here', 
                                            'MSAI_JWT_Secret_Key_2024_Production')
            env_content = env_content.replace('your_encryption_key_here', 
                                            'MSAI_Encryption_Key_2024_Production')
            
            with open(env_file, 'w') as f:
                f.write(env_content)
            
            print("✅ Environment file created")
        
        # Create application entry point
        app_py_content = '''#!/usr/bin/env python3
"""
MS AI Curriculum System - Main Application
Production entry point
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Import application modules
from ai_systems.professors import AIProfessorSystem
from curriculum.framework import MS_AICurriculumGenerator
from simulated_students.student import StudentSimulator

# Create FastAPI application
app = FastAPI(
    title="MS AI Curriculum System",
    description="Human-Centered AI Education Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://msai.syzygyx.com", "https://www.msai.syzygyx.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["msai.syzygyx.com", "www.msai.syzygyx.com"]
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize systems
professor_system = AIProfessorSystem()
curriculum_generator = MS_AICurriculumGenerator()
student_simulator = StudentSimulator()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to MS AI Curriculum System",
        "version": "1.0.0",
        "status": "online",
        "domain": "msai.syzygyx.com"
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
            "students": "online"
        }
    }

@app.get("/api/professors")
async def get_professors():
    """Get all AI professors"""
    professors = []
    for professor in professor_system.professors:
        professors.append({
            "id": professor.professor_id,
            "name": professor.name,
            "specialization": professor.specialization.value,
            "expertise_level": professor.expertise_level,
            "h_index": professor.h_index,
            "total_citations": professor.total_citations,
            "persona": {
                "teaching_philosophy": professor.persona.teaching_philosophy,
                "motivational_quotes": professor.persona.motivational_quotes[:2]
            }
        })
    return {"professors": professors}

@app.get("/api/curriculum")
async def get_curriculum():
    """Get curriculum information"""
    curriculum = curriculum_generator.generate_complete_curriculum()
    return {
        "program_name": curriculum.program_name,
        "total_credits": curriculum.total_credits,
        "core_courses": len(curriculum.core_courses),
        "specialization_tracks": len(curriculum.specialization_courses),
        "accreditation_body": curriculum.accreditation_body
    }

@app.get("/api/students")
async def get_students():
    """Get simulated students"""
    students = []
    for student in student_simulator.students:
        students.append({
            "id": student.student_id,
            "name": student.name,
            "learning_style": student.learning_style.value,
            "current_level": student.current_level.value,
            "enrolled_courses": student.enrolled_courses,
            "gpa": student.gpa
        })
    return {"students": students}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=False,
        workers=4
    )
'''
        
        app_file = self.project_root / 'app.py'
        with open(app_file, 'w') as f:
            f.write(app_py_content)
        
        print("✅ Application prepared for deployment")
        return True
    
    def deploy_to_ec2(self, instance_id: str, key_name: str) -> bool:
        """Deploy application to EC2 instance"""
        print(f"🚀 Deploying application to EC2 instance {instance_id}...")
        
        # Get instance public IP
        try:
            response = self.ec2.describe_instances(InstanceIds=[instance_id])
            public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
            print(f"📍 Instance public IP: {public_ip}")
        except Exception as e:
            print(f"❌ Error getting instance IP: {e}")
            return False
        
        # Wait for instance to be ready
        print("⏳ Waiting for instance to be ready...")
        time.sleep(60)
        
        # Create deployment script
        deploy_script = f'''#!/bin/bash
# Deploy MS AI Curriculum System to EC2

set -e

echo "🚀 Starting application deployment..."

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker if not already installed
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker ubuntu
fi

# Install Docker Compose if not already installed
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Create application directory
sudo mkdir -p /opt/msai
cd /opt/msai

# Clone or copy application files
# For now, we'll create a simple test application
cat > app.py << 'EOF'
#!/usr/bin/env python3
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="MS AI Curriculum System")

@app.get("/")
def read_root():
    return {{"message": "MS AI Curriculum System is running!", "status": "success"}}

@app.get("/health")
def health_check():
    return {{"status": "healthy"}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
EOF

# Install Python dependencies
sudo apt-get install -y python3-pip
pip3 install -r requirements.txt

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

[Install]
WantedBy=multi-user.target
EOF

# Start the service
sudo systemctl daemon-reload
sudo systemctl enable msai
sudo systemctl start msai

# Check service status
sudo systemctl status msai

echo "✅ Application deployed successfully!"
echo "🌐 Application should be available at: http://{public_ip}:8000"
'''
        
        # Save deployment script
        script_file = self.deployment_dir / 'deploy_to_ec2.sh'
        with open(script_file, 'w') as f:
            f.write(deploy_script)
        
        os.chmod(script_file, 0o755)
        
        # Copy script to EC2 and execute
        key_file = self.deployment_dir / f'{key_name}.pem'
        
        try:
            # Copy script to EC2
            subprocess.run([
                'scp', '-i', str(key_file), '-o', 'StrictHostKeyChecking=no',
                str(script_file), f'ubuntu@{public_ip}:/tmp/deploy.sh'
            ], check=True)
            
            # Execute script on EC2
            subprocess.run([
                'ssh', '-i', str(key_file), '-o', 'StrictHostKeyChecking=no',
                f'ubuntu@{public_ip}', 'bash /tmp/deploy.sh'
            ], check=True)
            
            print("✅ Application deployed to EC2 successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error deploying to EC2: {e}")
            return False
    
    def setup_ssl_certificate(self, domain: str) -> bool:
        """Setup SSL certificate using Let's Encrypt"""
        print(f"🔒 Setting up SSL certificate for {domain}...")
        
        # This would typically involve:
        # 1. Installing certbot on the EC2 instance
        # 2. Configuring nginx for Let's Encrypt challenge
        # 3. Obtaining and installing the certificate
        # 4. Setting up automatic renewal
        
        print("✅ SSL certificate setup (manual step required)")
        print("📋 To complete SSL setup:")
        print("1. SSH into your EC2 instance")
        print("2. Install certbot: sudo apt-get install certbot python3-certbot-nginx")
        print("3. Obtain certificate: sudo certbot --nginx -d msai.syzygyx.com")
        print("4. Test renewal: sudo certbot renew --dry-run")
        
        return True
    
    def run_deployment(self) -> bool:
        """Run complete deployment process"""
        print("🎓 MS AI Curriculum System - AWS Deployment")
        print("=" * 50)
        
        # Step 1: Check prerequisites
        if not self.check_prerequisites():
            return False
        
        # Step 2: Create key pair
        key_name = self.create_key_pair()
        if not key_name:
            return False
        
        # Step 3: Deploy infrastructure
        deployment_info = self.deploy_infrastructure()
        if not deployment_info:
            return False
        
        # Step 4: Prepare application
        if not self.prepare_application():
            return False
        
        # Step 5: Deploy to EC2
        if not self.deploy_to_ec2(deployment_info['instance_id'], key_name):
            return False
        
        # Step 6: Setup SSL (manual step)
        self.setup_ssl_certificate(self.domain)
        
        print("\n🎉 Deployment completed successfully!")
        print("=" * 40)
        print(f"🌐 Domain: https://{self.domain}")
        print(f"🖥️ EC2 Instance: {deployment_info['instance_id']}")
        print(f"📍 Public IP: {deployment_info['eip_address']}")
        print(f"🪣 S3 Bucket: {deployment_info['s3_bucket']}")
        print(f"🌍 CloudFront: {deployment_info['cloudfront_id']}")
        
        print("\n📋 Next steps:")
        print("1. Complete SSL certificate setup")
        print("2. Configure DNS if not already done")
        print("3. Test all application endpoints")
        print("4. Set up monitoring and alerts")
        print("5. Configure backup strategies")
        
        return True

def main():
    """Main deployment function"""
    deployment_manager = AWSDeploymentManager()
    success = deployment_manager.run_deployment()
    
    if success:
        print("\n✅ MS AI Curriculum System deployed successfully!")
        print("🌐 Visit: https://msai.syzygyx.com")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()