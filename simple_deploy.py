#!/usr/bin/env python3
"""
Simple deployment script for MS AI Curriculum System to msai.syzygyx.com
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main deployment function"""
    print("🎓 MS AI Curriculum System - Simple Deployment")
    print("=" * 50)
    
    # Change to deployment directory
    deployment_dir = Path(__file__).parent / 'deployment'
    os.chdir(deployment_dir)
    
    # Check if .env file exists, create if not
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        env_content = """# MS AI Curriculum System - Production Environment
DATABASE_URL=postgresql://msai_user:MSAI_Production_2024!@db:5432/msai_db
DB_PASSWORD=MSAI_Production_2024!
SECRET_KEY=MSAI_Secret_Key_2024_Production_Minimum_32_Characters_Long
JWT_SECRET_KEY=MSAI_JWT_Secret_Key_2024_Production
ENCRYPTION_KEY=MSAI_Encryption_Key_2024_Production
DOMAIN=msai.syzygyx.com
ALLOWED_HOSTS=msai.syzygyx.com,www.msai.syzygyx.com
DEBUG=False
ENVIRONMENT=production
REDIS_URL=redis://redis:6379/0
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
    
    # Create necessary directories
    run_command("mkdir -p static media logs ssl", "Creating directories")
    
    # Set proper permissions
    run_command("chmod 755 static media logs", "Setting permissions")
    run_command("chmod 600 .env", "Securing .env file")
    
    # Build Docker images
    if not run_command("docker-compose -f docker-compose.simple.yml build --no-cache", "Building Docker images"):
        return False
    
    # Start services
    if not run_command("docker-compose -f docker-compose.simple.yml up -d", "Starting services"):
        return False
    
    # Wait for services to be ready
    print("⏳ Waiting for services to be ready...")
    import time
    time.sleep(30)
    
    # Check service health
    run_command("docker-compose -f docker-compose.simple.yml ps", "Checking service status")
    
    print("\n🎉 Deployment completed successfully!")
    print("=" * 40)
    print("🌐 Application should be available at:")
    print("   - Direct: http://localhost:8001")
    print("   - Via Nginx: http://localhost:8080")
    print("📊 Monitor logs with: docker-compose logs -f")
    print("🛠️ Access shell with: docker-compose exec web bash")
    print("\n📋 Next steps:")
    print("1. Configure domain DNS to point to your server")
    print("2. Set up SSL certificates")
    print("3. Configure reverse proxy (nginx)")
    print("4. Test all functionality")

if __name__ == "__main__":
    main()