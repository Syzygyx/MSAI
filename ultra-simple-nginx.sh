#!/bin/bash
yum install -y nginx
echo "server { listen 80; location / { return 200 'MS AI Working on Port 80!'; } }" > /etc/nginx/nginx.conf
systemctl start nginx
echo "Done"