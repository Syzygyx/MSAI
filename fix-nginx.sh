#!/bin/bash

# Fix nginx configuration on the running instance
INSTANCE_ID="i-0da2a0063c5d527b4"

# Create a script to fix nginx
cat > fix_nginx_remote.sh << 'EOF'
#!/bin/bash

# Remove default nginx config
rm -f /etc/nginx/conf.d/default.conf

# Create proper nginx config
cat > /etc/nginx/conf.d/msai.conf << 'NGINX_EOF'
server {
    listen 80 default_server;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX_EOF

# Test nginx config
nginx -t

# Restart nginx
systemctl restart nginx

# Check status
systemctl status nginx --no-pager
systemctl status msai --no-pager

# Test the application
curl -f http://localhost/health || echo "Nginx not working"
curl -f http://localhost:8000/health || echo "App not working"

echo "Nginx fix completed at $(date)"
EOF

# Send the script to the instance and execute it
aws --profile msai ssm send-command \
  --instance-ids $INSTANCE_ID \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["bash /tmp/fix_nginx_remote.sh"]' \
  --comment "Fix nginx configuration"

echo "Sent nginx fix command to instance $INSTANCE_ID"