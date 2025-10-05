#!/bin/bash
yum update -y
yum install -y nginx

# Create simple HTML redirect page
cat > /usr/share/nginx/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>MS AI Curriculum System</title>
    <meta http-equiv="refresh" content="0; url=http://msai.syzygyx.com:8000">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f0f0; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 20px; }
        .loading { margin: 20px 0; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        a { color: #3498db; text-decoration: none; background: #ecf0f1; padding: 10px 20px; border-radius: 5px; display: inline-block; margin-top: 20px; }
        a:hover { background: #bdc3c7; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 MS AI Curriculum System</h1>
        <p>Redirecting to the application...</p>
        <div class="loading">
            <div class="spinner"></div>
        </div>
        <p>If you're not redirected automatically, <a href="http://msai.syzygyx.com:8000">click here</a></p>
    </div>
    <script>window.location.href = 'http://msai.syzygyx.com:8000';</script>
</body>
</html>
EOF

# Start nginx
systemctl enable nginx
systemctl start nginx

echo "Port 80 redirect page deployed at $(date)"