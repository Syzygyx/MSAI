#!/bin/bash
# Deploy Application Form to Live MS AI Site
# This script updates the live server with the enhanced application that includes the application form

set -e

echo "🚀 Deploying Application Form to MS AI Live Site..."

# Server details
SERVER_IP="44.220.164.13"
SERVER_USER="ubuntu"
KEY_FILE="msai-production-key.pem"

# Check if key file exists
if [ ! -f "$KEY_FILE" ]; then
    echo "❌ Key file $KEY_FILE not found. Please ensure the SSH key is available."
    exit 1
fi

echo "📋 Preparing deployment files..."

# Create deployment package
mkdir -p deployment_package
cp app_enhanced.py deployment_package/app.py
cp msai_application_form.html deployment_package/
cp google_sheets_integration.py deployment_package/

# Create requirements.txt for the enhanced app
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

echo "📦 Creating deployment archive..."
tar -czf msai_application_deployment.tar.gz -C deployment_package .

echo "🚀 Uploading to server..."

# Upload to server
scp -i "$KEY_FILE" msai_application_deployment.tar.gz "$SERVER_USER@$SERVER_IP:/tmp/"

echo "🔧 Deploying on server..."

# Deploy on server
ssh -i "$KEY_FILE" "$SERVER_USER@$SERVER_IP" << 'EOF'
set -e

echo "📥 Extracting deployment package..."
cd /opt/msai
tar -xzf /tmp/msai_application_deployment.tar.gz

echo "🔧 Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "📁 Creating necessary directories..."
mkdir -p uploads
mkdir -p static
mkdir -p templates

echo "🔄 Stopping existing service..."
sudo systemctl stop msai || true

echo "📋 Updating systemd service..."
sudo cp msai.service /etc/systemd/system/
sudo systemctl daemon-reload

echo "🌐 Updating nginx configuration..."
sudo cp nginx_msai.conf /etc/nginx/sites-available/msai.syzygyx.com
sudo ln -sf /etc/nginx/sites-available/msai.syzygyx.com /etc/nginx/sites-enabled/
sudo nginx -t

echo "🚀 Starting services..."
sudo systemctl start msai
sudo systemctl enable msai
sudo systemctl reload nginx

echo "⏳ Waiting for service to start..."
sleep 10

echo "🔍 Checking service status..."
sudo systemctl status msai --no-pager

echo "🌐 Testing endpoints..."
curl -f http://localhost:8000/health || echo "Health check failed"
curl -f http://localhost:8000/application || echo "Application form check failed"

echo "✅ Deployment complete!"
EOF

echo "🧹 Cleaning up..."
rm -rf deployment_package
rm -f msai_application_deployment.tar.gz

echo "🎉 Application Form Deployment Complete!"
echo ""
echo "🌐 Live URLs:"
echo "   Main Site: http://msai.syzygyx.com"
echo "   Application Form: http://msai.syzygyx.com/application"
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
echo "✅ The application form is now live on the site!"