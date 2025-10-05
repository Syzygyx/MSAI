#!/bin/bash
set -e

echo "🚀 Starting deployment on server..."

# Stop the service
echo "⏹️  Stopping MS AI service..."
sudo systemctl stop msai || true

# Backup current version
if [ -f "/opt/msai/app.py" ]; then
    echo "💾 Creating backup..."
    cp /opt/msai/app.py /opt/msai/app.py.backup.$(date +%Y%m%d_%H%M%S)
fi

# Update application files
echo "📁 Updating application files..."
cp app.py /opt/msai/
cp msai_application_form.html /opt/msai/ || echo "⚠️  Application form HTML not found"
cp google_sheets_integration.py /opt/msai/ || echo "⚠️  Google Sheets integration not found"

# Create necessary directories
echo "📂 Creating directories..."
mkdir -p /opt/msai/uploads
mkdir -p /opt/msai/static
mkdir -p /opt/msai/templates

# Install/update Python dependencies
echo "📦 Installing dependencies..."
source /opt/msai/venv/bin/activate
pip install -r requirements.txt

# Update systemd service
echo "🔧 Updating systemd service..."
sudo cp msai.service /etc/systemd/system/
sudo systemctl daemon-reload

# Update nginx configuration
echo "🌐 Updating nginx configuration..."
sudo cp nginx_msai.conf /etc/nginx/sites-available/msai.syzygyx.com
sudo ln -sf /etc/nginx/sites-available/msai.syzygyx.com /etc/nginx/sites-enabled/
sudo nginx -t

# Start services
echo "🚀 Starting services..."
sudo systemctl start msai
sudo systemctl enable msai
sudo systemctl reload nginx

# Wait for service to start
echo "⏳ Waiting for service to start..."
sleep 15

# Test the deployment
echo "🧪 Testing deployment..."
if curl -f http://localhost:8000/health; then
    echo "✅ Deployment successful!"
    echo "🌐 Application is running at http://msai.syzygyx.com"
    echo "📝 Application form: http://msai.syzygyx.com/application"
    echo "📚 API docs: http://msai.syzygyx.com/docs"
else
    echo "❌ Deployment failed - service not responding"
    echo "🔍 Check logs with: sudo journalctl -u msai -f"
    exit 1
fi
