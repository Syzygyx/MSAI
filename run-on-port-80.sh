#!/bin/bash
# Run MS AI Curriculum System on port 80 locally

set -e

echo "🚀 Starting MS AI Curriculum System on port 80..."

# Check if running as root (needed for port 80)
if [ "$EUID" -ne 0 ]; then
    echo "❌ This script needs to run as root to use port 80"
    echo "Please run: sudo ./run-on-port-80.sh"
    exit 1
fi

# Install nginx if not present
if ! command -v nginx &> /dev/null; then
    echo "Installing nginx..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install nginx
    else
        # Linux
        apt-get update && apt-get install -y nginx
    fi
fi

# Create nginx configuration
cat > /usr/local/etc/nginx/msai.conf << 'EOF'
server {
    listen 80;
    server_name msai.syzygyx.com localhost;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Start the local MS AI application (if not running)
if ! curl -s http://localhost:8001/health > /dev/null; then
    echo "Starting MS AI application on port 8001..."
    cd /Users/danielmcshan/GitHub/MSAI
    docker-compose up -d
    sleep 10
fi

# Start nginx
echo "Starting nginx on port 80..."
nginx -s reload 2>/dev/null || nginx

echo "✅ MS AI Curriculum System is now running on port 80!"
echo "🌐 Access at: http://msai.syzygyx.com"
echo "🔍 Health check: http://msai.syzygyx.com/health"
echo "👨‍🏫 Professors: http://msai.syzygyx.com/api/professors"
echo "📚 Curriculum: http://msai.syzygyx.com/api/curriculum"
echo "👥 Students: http://msai.syzygyx.com/api/students"

# Test the endpoints
echo ""
echo "🧪 Testing endpoints..."
curl -s http://localhost/health | python3 -m json.tool || echo "Health check failed"