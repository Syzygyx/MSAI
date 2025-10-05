#!/bin/bash
# Terpedia Admin Setup Script

echo "🎓 Setting up Terpedia Admin Access for dan@syzygyx.com..."

# Create admin directory
mkdir -p /opt/terpedia-admin
cd /opt/terpedia-admin

# Create admin configuration
cat > admin_config.json << 'EOF'
{
    "user": {
        "email": "dan@syzygyx.com",
        "username": "dan_admin",
        "full_name": "Dan Admin",
        "role": "super_admin",
        "permissions": [
            "user_management",
            "content_management", 
            "system_configuration",
            "database_access",
            "api_management",
            "security_settings",
            "backup_restore",
            "analytics_access",
            "domain_management",
            "ssl_certificates"
        ],
        "status": "active",
        "access_level": "full"
    },
    "security": {
        "api_key": "terpedia_admin_key_2024",
        "session_token": "terpedia_session_token_2024"
    },
    "access": {
        "allowed_domains": ["terpedia.com", "syzygyx.com"],
        "concurrent_sessions": 5,
        "session_timeout": 3600
    }
}
EOF

# Create simple admin API
cat > admin_api.py << 'EOF'
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load admin config
with open('admin_config.json', 'r') as f:
    admin_config = json.load(f)

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data.get('email')
    
    if email == admin_config['user']['email']:
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': admin_config['user'],
            'token': admin_config['security']['session_token']
        })
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    return jsonify({
        'success': True,
        'dashboard': {
            'title': 'Terpedia Admin Dashboard',
            'user': admin_config['user'],
            'system_status': 'online',
            'uptime': '100%',
            'version': '1.0.0'
        }
    })

@app.route('/admin/users', methods=['GET'])
def get_users():
    return jsonify({
        'success': True,
        'users': [admin_config['user']],
        'total': 1
    })

@app.route('/admin/system/status', methods=['GET'])
def system_status():
    return jsonify({
        'success': True,
        'status': {
            'database': 'online',
            'api': 'online',
            'storage': 'online',
            'cache': 'online'
        },
        'uptime': '99.9%',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
EOF

# Install Flask
pip3 install flask

# Create systemd service
cat > /etc/systemd/system/terpedia-admin.service << 'EOF'
[Unit]
Description=Terpedia Admin API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/terpedia-admin
ExecStart=/usr/bin/python3 admin_api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Start the service
systemctl daemon-reload
systemctl enable terpedia-admin
systemctl start terpedia-admin

echo "✅ Terpedia Admin Access setup completed!"
echo "🌐 Admin API available at: http://terpedia.com:8080"
echo "👤 Admin user: dan@syzygyx.com"
echo "🔑 Login endpoint: POST /admin/login"
echo "📊 Dashboard: GET /admin/dashboard"
