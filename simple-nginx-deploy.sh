#!/bin/bash

# Simple nginx deployment
yum update -y
yum install -y python3 python3-pip nginx

# Create app
mkdir -p /opt/msai
cd /opt/msai

cat > app.py << 'EOF'
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "MS AI System Working!", "status": "success"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

# Install FastAPI
pip3 install fastapi uvicorn

# Create systemd service
cat > /etc/systemd/system/msai.service << 'EOF'
[Unit]
Description=MS AI App
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/msai
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Simple nginx config
cat > /etc/nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        location / {
            proxy_pass http://127.0.0.1:8000;
        }
    }
}
EOF

# Start services
systemctl daemon-reload
systemctl enable msai
systemctl start msai
systemctl enable nginx
systemctl start nginx

# Test
sleep 10
curl http://localhost:8000/health
curl http://localhost/health

echo "Deployment done at $(date)"