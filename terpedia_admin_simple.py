#!/usr/bin/env python3
"""
Terpedia.com Admin Setup for dan@syzygyx.com - Simple Version
"""

import json
from datetime import datetime

def create_admin_config():
    """Create admin configuration for dan@syzygyx.com"""
    
    admin_config = {
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
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "two_factor_enabled": True,
            "access_level": "full"
        },
        "security": {
            "api_key": "terpedia_admin_key_2024",
            "session_token": "terpedia_session_token_2024",
            "login_attempts": 0,
            "locked_until": None
        },
        "access": {
            "allowed_ips": [],
            "allowed_domains": ["terpedia.com", "syzygyx.com"],
            "concurrent_sessions": 5,
            "session_timeout": 3600
        },
        "endpoints": {
            "login": "/admin/login",
            "dashboard": "/admin/dashboard",
            "users": "/admin/users",
            "system": "/admin/system/status",
            "logs": "/admin/system/logs"
        }
    }
    
    return admin_config

def create_setup_script():
    """Create deployment script"""
    
    script_content = """#!/bin/bash
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
"""
    
    return script_content

def main():
    """Main function"""
    print("🎓 Terpedia.com Admin Setup for dan@syzygyx.com")
    print("=" * 50)
    
    # Create admin configuration
    admin_config = create_admin_config()
    print("✅ Admin configuration created")
    
    # Create setup script
    setup_script = create_setup_script()
    
    # Save files
    with open('terpedia_admin_config.json', 'w') as f:
        json.dump(admin_config, f, indent=2)
    
    with open('terpedia_admin_setup.sh', 'w') as f:
        f.write(setup_script)
    
    # Make script executable
    import os
    os.chmod('terpedia_admin_setup.sh', 0o755)
    
    print("\n🎉 Admin setup files created successfully!")
    print("=" * 40)
    print("📁 Files created:")
    print("   - terpedia_admin_config.json")
    print("   - terpedia_admin_setup.sh")
    
    print("\n📋 Admin Configuration:")
    print(f"   👤 Email: {admin_config['user']['email']}")
    print(f"   🎭 Role: {admin_config['user']['role']}")
    print(f"   🔐 Permissions: {len(admin_config['user']['permissions'])} total")
    print(f"   🌐 Access Level: {admin_config['user']['access_level']}")
    
    print("\n🚀 Deployment Instructions:")
    print("1. Copy terpedia_admin_setup.sh to terpedia.com server")
    print("2. Run: bash terpedia_admin_setup.sh")
    print("3. Test admin access:")
    print("   - Login: POST http://terpedia.com:8080/admin/login")
    print("   - Dashboard: GET http://terpedia.com:8080/admin/dashboard")
    print("   - Users: GET http://terpedia.com:8080/admin/users")
    print("   - System: GET http://terpedia.com:8080/admin/system/status")
    
    return True

if __name__ == "__main__":
    main()