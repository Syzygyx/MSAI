"""
Docker Configuration for MS AI Curriculum System
Production deployment with Docker containers
"""

import os
import yaml
from typing import Dict, List, Any

class DockerConfigGenerator:
    """Generates Docker configuration for MS AI system"""
    
    def __init__(self):
        self.project_name = "msai"
        self.version = "1.0.0"
        
    def create_dockerfile(self) -> str:
        """Create Dockerfile for the application"""
        dockerfile_content = """# MS AI Curriculum System - Production Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    software-properties-common \\
    git \\
    postgresql-client \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \\
    && apt-get install -y nodejs

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash msai \\
    && chown -R msai:msai /app
USER msai

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["python", "app.py"]
"""
        return dockerfile_content
    
    def create_docker_compose(self) -> str:
        """Create docker-compose.yml for production"""
        compose_content = """version: '3.8'

services:
  web:
    build: .
    container_name: msai-web
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://msai_user:${DB_PASSWORD}@db:5432/msai_db
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
      - ENVIRONMENT=production
    volumes:
      - ./static:/app/static
      - ./media:/app/media
      - ./logs:/app/logs
    depends_on:
      - db
      - redis
    networks:
      - msai-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    container_name: msai-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=msai_db
      - POSTGRES_USER=msai_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - msai-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U msai_user -d msai_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: msai-redis
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - msai-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  nginx:
    image: nginx:alpine
    container_name: msai-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
      - ./static:/var/www/static
      - ./media:/var/www/media
    depends_on:
      - web
    networks:
      - msai-network

  worker:
    build: .
    container_name: msai-worker
    restart: unless-stopped
    command: celery -A app.celery worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://msai_user:${DB_PASSWORD}@db:5432/msai_db
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./logs:/app/logs
    depends_on:
      - db
      - redis
    networks:
      - msai-network

  scheduler:
    build: .
    container_name: msai-scheduler
    restart: unless-stopped
    command: celery -A app.celery beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql://msai_user:${DB_PASSWORD}@db:5432/msai_db
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./logs:/app/logs
    depends_on:
      - db
      - redis
    networks:
      - msai-network

volumes:
  postgres_data:
  redis_data:

networks:
  msai-network:
    driver: bridge
"""
        return compose_content
    
    def create_nginx_config(self) -> str:
        """Create nginx configuration"""
        nginx_config = """events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    
    # Upstream
    upstream msai_backend {
        server web:8000;
    }
    
    # HTTP server (redirect to HTTPS)
    server {
        listen 80;
        server_name msai.syzygyx.com www.msai.syzygyx.com;
        
        # Let's Encrypt challenge
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        
        # Redirect all HTTP to HTTPS
        location / {
            return 301 https://$server_name$request_uri;
        }
    }
    
    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name msai.syzygyx.com www.msai.syzygyx.com;
        
        # SSL configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;
        
        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        
        # Static files
        location /static/ {
            alias /var/www/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        location /media/ {
            alias /var/www/media/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        # API endpoints
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://msai_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }
        
        # Login endpoint (rate limited)
        location /login/ {
            limit_req zone=login burst=5 nodelay;
            proxy_pass http://msai_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Main application
        location / {
            proxy_pass http://msai_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }
        
        # Health check
        location /health {
            proxy_pass http://msai_backend;
            access_log off;
        }
    }
}
"""
        return nginx_config
    
    def create_requirements_txt(self) -> str:
        """Create requirements.txt for Python dependencies"""
        requirements = """# MS AI Curriculum System - Production Dependencies

# Core web framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
gunicorn==21.2.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9

# Redis and caching
redis==5.0.1
celery==5.3.4

# AI/ML libraries
torch==2.1.1
torchvision==0.16.1
scikit-learn==1.3.2
numpy==1.24.4
pandas==2.1.3
matplotlib==3.8.2

# Human-centered learning
nltk==3.8.1
spacy==3.7.2
transformers==4.35.2
plotly==5.17.0
streamlit==1.28.1

# Web automation
playwright==1.40.0

# Social and collaborative features
python-socketio==5.10.0
opencv-python==4.8.1.78

# Emotional intelligence and NLP
textblob==0.17.1
empath==0.90
wordcloud==1.9.2

# Authentication and security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Environment and configuration
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.0.3

# Monitoring and logging
structlog==23.2.0
sentry-sdk[fastapi]==1.38.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Development tools
black==23.11.0
flake8==6.1.0
mypy==1.7.1
"""
        return requirements
    
    def create_package_json(self) -> str:
        """Create package.json for Node.js dependencies"""
        package_json = {
            "name": "msai-curriculum-system",
            "version": "1.0.0",
            "description": "MS AI Curriculum System - Human-Centered Learning Platform",
            "main": "index.js",
            "scripts": {
                "start": "node index.js",
                "dev": "nodemon index.js",
                "build": "webpack --mode production",
                "test": "jest",
                "lint": "eslint .",
                "format": "prettier --write ."
            },
            "dependencies": {
                "express": "^4.18.2",
                "socket.io": "^4.7.4",
                "cors": "^2.8.5",
                "helmet": "^7.1.0",
                "compression": "^1.7.4",
                "express-rate-limit": "^7.1.5",
                "express-validator": "^7.0.1",
                "jsonwebtoken": "^9.0.2",
                "bcryptjs": "^2.4.3",
                "multer": "^1.4.5-lts.1",
                "sharp": "^0.32.6",
                "nodemailer": "^6.9.7",
                "winston": "^3.11.0",
                "dotenv": "^16.3.1"
            },
            "devDependencies": {
                "nodemon": "^3.0.2",
                "webpack": "^5.89.0",
                "webpack-cli": "^5.1.4",
                "jest": "^29.7.0",
                "eslint": "^8.54.0",
                "prettier": "^3.1.0",
                "@types/node": "^20.9.0"
            },
            "engines": {
                "node": ">=18.0.0",
                "npm": ">=9.0.0"
            },
            "keywords": [
                "ai",
                "education",
                "curriculum",
                "machine-learning",
                "human-centered-learning"
            ],
            "author": "MS AI Curriculum Team",
            "license": "MIT"
        }
        return yaml.dump(package_json, default_flow_style=False)
    
    def create_env_template(self) -> str:
        """Create .env.template for environment variables"""
        env_template = """# MS AI Curriculum System - Environment Variables Template
# Copy this file to .env and fill in the actual values

# Database Configuration
DATABASE_URL=postgresql://msai_user:your_password@localhost:5432/msai_db
DB_PASSWORD=your_secure_password_here

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your_secret_key_here_minimum_32_characters
JWT_SECRET_KEY=your_jwt_secret_key_here
ENCRYPTION_KEY=your_encryption_key_here

# Application Settings
DEBUG=False
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000

# Domain Configuration
DOMAIN=msai.syzygyx.com
ALLOWED_HOSTS=msai.syzygyx.com,www.msai.syzygyx.com

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=noreply@msai.syzygyx.com

# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=msai-assets-production

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
LOG_LEVEL=INFO

# AI/ML Services
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key

# Social Learning Features
ENABLE_PEER_COLLABORATION=True
ENABLE_MENTOR_MATCHING=True
ENABLE_EMOTIONAL_SUPPORT=True

# Assessment Settings
ENABLE_PEER_ASSESSMENT=True
ENABLE_PORTFOLIO_ASSESSMENT=True
ENABLE_SELF_REFLECTION=True

# PWA Configuration
PWA_ENABLED=True
PWA_NAME=MS AI Curriculum
PWA_SHORT_NAME=MSAI
PWA_DESCRIPTION=Human-Centered AI Education Platform
"""
        return env_template
    
    def create_deployment_script(self) -> str:
        """Create deployment script"""
        deploy_script = """#!/bin/bash
# MS AI Curriculum System - Production Deployment Script

set -e

echo "🚀 Starting MS AI Curriculum System Deployment"
echo "=============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.template to .env and configure it."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p static media logs ssl

# Set proper permissions
echo "🔐 Setting proper permissions..."
chmod 755 static media logs
chmod 600 .env

# Build and start services
echo "🏗️ Building Docker images..."
docker-compose build --no-cache

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🏥 Checking service health..."
docker-compose ps

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose exec web python -c "from app.database import init_db; init_db()"

# Create superuser (optional)
echo "👤 Creating superuser..."
docker-compose exec web python -c "
from app.auth import create_superuser
create_superuser('admin@msai.syzygyx.com', 'admin123', 'Admin', 'User')
" || echo "Superuser may already exist"

# Collect static files
echo "📦 Collecting static files..."
docker-compose exec web python -c "from app.static import collect_static; collect_static()"

# Restart services to apply changes
echo "🔄 Restarting services..."
docker-compose restart

echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Application is available at: https://msai.syzygyx.com"
echo "📊 Monitor logs with: docker-compose logs -f"
echo "🛠️ Access shell with: docker-compose exec web bash"
echo ""
echo "📋 Next steps:"
echo "1. Configure SSL certificates"
echo "2. Set up monitoring and alerts"
echo "3. Configure backup strategies"
echo "4. Test all functionality"
"""
        return deploy_script
    
    def generate_all_configs(self, output_dir: str = "deployment"):
        """Generate all Docker configuration files"""
        print("🐳 Generating Docker configuration files...")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate files
        files_to_create = {
            'Dockerfile': self.create_dockerfile(),
            'docker-compose.yml': self.create_docker_compose(),
            'nginx.conf': self.create_nginx_config(),
            'requirements.txt': self.create_requirements_txt(),
            'package.json': self.create_package_json(),
            '.env.template': self.create_env_template(),
            'deploy.sh': self.create_deployment_script()
        }
        
        for filename, content in files_to_create.items():
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"✅ Created {filepath}")
        
        # Make deploy script executable
        deploy_script_path = os.path.join(output_dir, 'deploy.sh')
        os.chmod(deploy_script_path, 0o755)
        
        print(f"\n🎉 All Docker configuration files generated in {output_dir}/")
        print("\n📋 Next steps:")
        print("1. Copy .env.template to .env and configure environment variables")
        print("2. Run ./deploy.sh to deploy the application")
        print("3. Configure SSL certificates for HTTPS")
        print("4. Set up monitoring and logging")

def main():
    """Main function to generate Docker configurations"""
    generator = DockerConfigGenerator()
    generator.generate_all_configs()

if __name__ == "__main__":
    main()