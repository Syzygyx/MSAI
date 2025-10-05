#!/bin/bash

# MS AI Deployment Script
# This script deploys the application to msai.syzygyx.com

set -e  # Exit on any error

# Configuration
SERVER_HOST="3.84.224.16"
SERVER_USER="ubuntu"  # Adjust based on your server setup
DEPLOY_PATH="/var/www/msai"
BACKUP_PATH="/var/backups/msai"

echo "🚀 Starting MS AI deployment..."

# Check if required files exist
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found. Please ensure the application form is ready."
    exit 1
fi

# Create backup of current deployment
echo "📦 Creating backup..."
ssh $SERVER_USER@$SERVER_HOST "sudo mkdir -p $BACKUP_PATH && sudo cp -r $DEPLOY_PATH $BACKUP_PATH/backup-$(date +%Y%m%d-%H%M%S) 2>/dev/null || true"

# Create deployment directory
echo "📁 Setting up deployment directory..."
ssh $SERVER_USER@$SERVER_HOST "sudo mkdir -p $DEPLOY_PATH"

# Sync files to server
echo "📤 Syncing files to server..."
rsync -avz --delete \
  --exclude='.git' \
  --exclude='.github' \
  --exclude='node_modules' \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  --exclude='.env' \
  --exclude='test_*.py' \
  --exclude='playwright_env' \
  --exclude='test_results.json' \
  --exclude='deploy.sh' \
  ./ $SERVER_USER@$SERVER_HOST:$DEPLOY_PATH/

# Set proper permissions
echo "🔐 Setting permissions..."
ssh $SERVER_USER@$SERVER_HOST "sudo chmod -R 755 $DEPLOY_PATH && sudo chown -R www-data:www-data $DEPLOY_PATH"

# Restart web server
echo "🔄 Restarting web server..."
ssh $SERVER_USER@$SERVER_HOST "sudo systemctl reload nginx"

# Verify deployment
echo "✅ Verifying deployment..."
sleep 5

if curl -f -s http://msai.syzygyx.com > /dev/null; then
    echo "🎉 Deployment successful!"
    echo "🌐 Site is live at: http://msai.syzygyx.com"
    echo "📋 Application form: http://msai.syzygyx.com/apply"
else
    echo "❌ Deployment verification failed!"
    echo "🔍 Checking server status..."
    ssh $SERVER_USER@$SERVER_HOST "sudo systemctl status nginx"
    exit 1
fi

echo "✨ Deployment completed successfully!"