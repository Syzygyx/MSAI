#!/bin/bash

# Fix nginx configuration on the running instance
INSTANCE_ID="i-089e18b5d44190a19"

# Create a comprehensive nginx fix script
cat > nginx_fix.sh << 'EOF'
#!/bin/bash

echo "Starting nginx fix at $(date)"

# Stop nginx
systemctl stop nginx

# Remove all existing nginx configs
rm -f /etc/nginx/conf.d/*
rm -f /etc/nginx/sites-enabled/*
rm -f /etc/nginx/sites-available/*

# Create a clean nginx.conf
cat > /etc/nginx/nginx.conf << 'NGINX_EOF'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Main server block for port 80
    server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name msai.syzygyx.com _;

        # Root location
        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $host;
            proxy_set_header X-Forwarded-Port $server_port;
            
            # CORS headers
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range";
            
            # Handle preflight requests
            if ($request_method = 'OPTIONS') {
                add_header Access-Control-Allow-Origin *;
                add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
                add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range";
                add_header Access-Control-Max-Age 1728000;
                add_header Content-Type 'text/plain; charset=utf-8';
                add_header Content-Length 0;
                return 204;
            }
        }

        # Health check endpoint
        location /health {
            proxy_pass http://127.0.0.1:8000/health;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # API endpoints
        location /api/ {
            proxy_pass http://127.0.0.1:8000/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
NGINX_EOF

# Test nginx configuration
echo "Testing nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo "Nginx configuration is valid"
    
    # Start nginx
    systemctl start nginx
    systemctl enable nginx
    
    # Check nginx status
    systemctl status nginx --no-pager
    
    # Wait a moment for nginx to start
    sleep 5
    
    # Test the application
    echo "Testing application endpoints..."
    curl -f http://localhost/health || echo "Health check failed"
    curl -f http://localhost/ || echo "Root endpoint failed"
    curl -f http://localhost/api/professors || echo "Professors API failed"
    
    echo "Nginx fix completed at $(date)"
else
    echo "Nginx configuration is invalid!"
    exit 1
fi
EOF

# Send the script to the instance and execute it
aws --profile msai ssm send-command \
  --instance-ids $INSTANCE_ID \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["bash /tmp/nginx_fix.sh"]' \
  --comment "Fix nginx configuration for port 80"

echo "Sent nginx fix command to instance $INSTANCE_ID"