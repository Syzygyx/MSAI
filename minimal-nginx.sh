#!/bin/bash
yum update -y
yum install -y python3 python3-pip nginx

mkdir -p /opt/msai
cd /opt/msai

cat > app.py << 'EOF'
from fastapi import FastAPI
import uvicorn
app = FastAPI()
@app.get("/")
def root():
    return {"message": "MS AI Working!", "status": "success"}
@app.get("/health")
def health():
    return {"status": "healthy"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

pip3 install fastapi uvicorn

cat > /etc/systemd/system/msai.service << 'EOF'
[Unit]
Description=MS AI
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

cat > /etc/nginx/nginx.conf << 'EOF'
events { worker_connections 1024; }
http {
    server {
        listen 80;
        location / {
            proxy_pass http://127.0.0.1:8000;
        }
    }
}
EOF

systemctl daemon-reload
systemctl enable msai
systemctl start msai
systemctl enable nginx
systemctl start nginx

sleep 10
curl http://localhost:8000/health
curl http://localhost/health

echo "Done at $(date)"