#!/bin/bash
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
