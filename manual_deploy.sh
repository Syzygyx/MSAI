#!/bin/bash
# Manual Deployment Script for MS AI Application
# Use this if GitHub Actions is not available or needs manual intervention

set -e

echo "🚀 Manual Deployment Script for MS AI Application"
echo "=" * 60

# Configuration
SERVER_IP="44.220.164.13"
SERVER_USER="ubuntu"
KEY_FILE="msai-production-key.pem"
APP_DIR="/opt/msai"

# Check if key file exists
if [ ! -f "$KEY_FILE" ]; then
    echo "❌ Key file $KEY_FILE not found."
    echo "Please ensure the SSH key is available in the current directory."
    exit 1
fi

echo "📋 Preparing deployment files..."

# Create deployment package
mkdir -p deployment_package

# Copy main application files
cp app_enhanced.py deployment_package/app.py
cp msai_application_form.html deployment_package/ || echo "⚠️  Application form HTML not found"
cp google_sheets_integration.py deployment_package/ || echo "⚠️  Google Sheets integration not found"

# Create requirements.txt
cat > deployment_package/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
pydantic==2.5.0
jinja2==3.1.2
gspread==5.12.0
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
google-api-python-client==2.108.0
python-multipart==0.0.6
email-validator==2.1.0
EOF

# Create systemd service file
cat > deployment_package/msai.service << 'EOF'
[Unit]
Description=MS AI Curriculum System with Application Form
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/msai
Environment=PATH=/opt/msai/venv/bin
ExecStart=/opt/msai/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create nginx configuration
cat > deployment_package/nginx_msai.conf << 'EOF'
server {
    listen 80;
    server_name msai.syzygyx.com www.msai.syzygyx.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /opt/msai/static/;
    }
    
    location /uploads/ {
        alias /opt/msai/uploads/;
    }
}
EOF

# Create deployment script
cat > deployment_package/deploy.sh << 'EOF'
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
EOF

chmod +x deployment_package/deploy.sh

# Create deployment archive
echo "📦 Creating deployment archive..."
tar -czf msai_manual_deployment.tar.gz -C deployment_package .

echo "🚀 Uploading to server..."

# Upload to server
scp -i "$KEY_FILE" msai_manual_deployment.tar.gz "$SERVER_USER@$SERVER_IP:/tmp/"

echo "🔧 Deploying on server..."

# Deploy on server
ssh -i "$KEY_FILE" "$SERVER_USER@$SERVER_IP" << 'EOF'
set -e

echo "📥 Extracting deployment package..."
cd /opt/msai
tar -xzf /tmp/msai_manual_deployment.tar.gz

echo "🔧 Running deployment script..."
./deploy.sh

echo "🧹 Cleaning up..."
rm -f /tmp/msai_manual_deployment.tar.gz

echo "✅ Manual deployment complete!"
EOF

echo "🧹 Cleaning up local files..."
rm -rf deployment_package
rm -f msai_manual_deployment.tar.gz

echo ""
echo "🎉 MANUAL DEPLOYMENT COMPLETE!"
echo "=" * 60
echo "🌐 Live URLs:"
echo "   Main Site: http://msai.syzygyx.com"
echo "   Application Form: http://msai.syzygyx.com/application"
echo "   Apply: http://msai.syzygyx.com/apply"
echo "   API Documentation: http://msai.syzygyx.com/docs"
echo "   Health Check: http://msai.syzygyx.com/health"
echo ""
echo "📊 New API Endpoints:"
echo "   POST /api/application - Submit application"
echo "   GET /api/applications - Get all applications"
echo "   GET /api/applications/stats - Get statistics"
echo "   GET /api/specializations - Get specializations"
echo "   GET /api/start-terms - Get start terms"
echo "   GET /api/program-formats - Get program formats"
echo ""
echo "✅ The application form is now live!"