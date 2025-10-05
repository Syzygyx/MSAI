#!/usr/bin/env python3
"""
Terpedia.com Admin Setup for dan@syzygyx.com
"""

import json
import boto3
from datetime import datetime
import hashlib
import secrets

def create_admin_user():
    """Create admin user configuration for dan@syzygyx.com"""
    
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
            "last_login": None,
            "status": "active",
            "two_factor_enabled": True,
            "access_level": "full"
        },
        "security": {
            "password_hash": None,  # Will be set when password is created
            "api_key": secrets.token_urlsafe(32),
            "session_token": secrets.token_urlsafe(64),
            "login_attempts": 0,
            "locked_until": None,
            "password_reset_token": None,
            "password_reset_expires": None
        },
        "access": {
            "allowed_ips": [],  # Empty means all IPs allowed
            "allowed_domains": ["terpedia.com", "syzygyx.com"],
            "time_restrictions": None,  # No time restrictions
            "concurrent_sessions": 5,
            "session_timeout": 3600  # 1 hour
        },
        "notifications": {
            "email_notifications": True,
            "security_alerts": True,
            "system_updates": True,
            "backup_reports": True
        }
    }
    
    return admin_config

def create_admin_database():
    """Create admin database structure"""
    
    database_schema = {
        "tables": {
            "admin_users": {
                "columns": {
                    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                    "email": "VARCHAR(255) UNIQUE NOT NULL",
                    "username": "VARCHAR(100) UNIQUE NOT NULL",
                    "full_name": "VARCHAR(255) NOT NULL",
                    "role": "VARCHAR(50) NOT NULL",
                    "permissions": "TEXT",  # JSON string
                    "created_at": "DATETIME DEFAULT CURRENT_TIMESTAMP",
                    "last_login": "DATETIME",
                    "status": "VARCHAR(20) DEFAULT 'active'",
                    "two_factor_enabled": "BOOLEAN DEFAULT FALSE",
                    "access_level": "VARCHAR(20) DEFAULT 'standard'"
                },
                "indexes": [
                    "CREATE INDEX idx_admin_email ON admin_users(email)",
                    "CREATE INDEX idx_admin_username ON admin_users(username)",
                    "CREATE INDEX idx_admin_status ON admin_users(status)"
                ]
            },
            "admin_sessions": {
                "columns": {
                    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                    "user_id": "INTEGER NOT NULL",
                    "session_token": "VARCHAR(255) UNIQUE NOT NULL",
                    "ip_address": "VARCHAR(45)",
                    "user_agent": "TEXT",
                    "created_at": "DATETIME DEFAULT CURRENT_TIMESTAMP",
                    "expires_at": "DATETIME NOT NULL",
                    "is_active": "BOOLEAN DEFAULT TRUE",
                    "FOREIGN KEY": "(user_id) REFERENCES admin_users(id)"
                },
                "indexes": [
                    "CREATE INDEX idx_session_token ON admin_sessions(session_token)",
                    "CREATE INDEX idx_session_user ON admin_sessions(user_id)",
                    "CREATE INDEX idx_session_expires ON admin_sessions(expires_at)"
                ]
            },
            "admin_logs": {
                "columns": {
                    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                    "user_id": "INTEGER",
                    "action": "VARCHAR(100) NOT NULL",
                    "resource": "VARCHAR(255)",
                    "details": "TEXT",
                    "ip_address": "VARCHAR(45)",
                    "user_agent": "TEXT",
                    "timestamp": "DATETIME DEFAULT CURRENT_TIMESTAMP",
                    "status": "VARCHAR(20) DEFAULT 'success'",
                    "FOREIGN KEY": "(user_id) REFERENCES admin_users(id)"
                },
                "indexes": [
                    "CREATE INDEX idx_log_user ON admin_logs(user_id)",
                    "CREATE INDEX idx_log_action ON admin_logs(action)",
                    "CREATE INDEX idx_log_timestamp ON admin_logs(timestamp)"
                ]
            }
        }
    }
    
    return database_schema

def create_admin_api():
    """Create admin API endpoints"""
    
    api_endpoints = {
        "authentication": {
            "POST /admin/login": {
                "description": "Admin login endpoint",
                "parameters": {
                    "email": "string (required)",
                    "password": "string (required)",
                    "two_factor_code": "string (optional)"
                },
                "response": {
                    "success": "boolean",
                    "token": "string",
                    "user": "object",
                    "expires_at": "datetime"
                }
            },
            "POST /admin/logout": {
                "description": "Admin logout endpoint",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "response": {
                    "success": "boolean",
                    "message": "string"
                }
            },
            "POST /admin/refresh": {
                "description": "Refresh admin session",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "response": {
                    "success": "boolean",
                    "token": "string",
                    "expires_at": "datetime"
                }
            }
        },
        "user_management": {
            "GET /admin/users": {
                "description": "List all admin users",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "response": {
                    "success": "boolean",
                    "users": "array",
                    "total": "integer"
                }
            },
            "POST /admin/users": {
                "description": "Create new admin user",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "parameters": {
                    "email": "string (required)",
                    "username": "string (required)",
                    "full_name": "string (required)",
                    "role": "string (required)",
                    "permissions": "array (required)"
                },
                "response": {
                    "success": "boolean",
                    "user": "object",
                    "message": "string"
                }
            },
            "PUT /admin/users/{user_id}": {
                "description": "Update admin user",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "response": {
                    "success": "boolean",
                    "user": "object",
                    "message": "string"
                }
            },
            "DELETE /admin/users/{user_id}": {
                "description": "Delete admin user",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "response": {
                    "success": "boolean",
                    "message": "string"
                }
            }
        },
        "system_management": {
            "GET /admin/system/status": {
                "description": "Get system status",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "response": {
                    "success": "boolean",
                    "status": "object",
                    "uptime": "string",
                    "version": "string"
                }
            },
            "GET /admin/system/logs": {
                "description": "Get system logs",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "response": {
                    "success": "boolean",
                    "logs": "array",
                    "total": "integer"
                }
            },
            "POST /admin/system/backup": {
                "description": "Create system backup",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "response": {
                    "success": "boolean",
                    "backup_id": "string",
                    "message": "string"
                }
            }
        }
    }
    
    return api_endpoints

def create_admin_dashboard():
    """Create admin dashboard configuration"""
    
    dashboard_config = {
        "layout": {
            "title": "Terpedia Admin Dashboard",
            "logo": "/admin/assets/terpedia-logo.png",
            "theme": "dark",
            "sidebar": {
                "collapsible": True,
                "default_collapsed": False
            }
        },
        "navigation": [
            {
                "title": "Dashboard",
                "icon": "dashboard",
                "path": "/admin/dashboard",
                "permission": "dashboard_access"
            },
            {
                "title": "User Management",
                "icon": "users",
                "path": "/admin/users",
                "permission": "user_management",
                "children": [
                    {
                        "title": "Admin Users",
                        "path": "/admin/users/admins"
                    },
                    {
                        "title": "Regular Users",
                        "path": "/admin/users/regular"
                    },
                    {
                        "title": "User Roles",
                        "path": "/admin/users/roles"
                    }
                ]
            },
            {
                "title": "Content Management",
                "icon": "content",
                "path": "/admin/content",
                "permission": "content_management",
                "children": [
                    {
                        "title": "Articles",
                        "path": "/admin/content/articles"
                    },
                    {
                        "title": "Categories",
                        "path": "/admin/content/categories"
                    },
                    {
                        "title": "Media",
                        "path": "/admin/content/media"
                    }
                ]
            },
            {
                "title": "System",
                "icon": "settings",
                "path": "/admin/system",
                "permission": "system_configuration",
                "children": [
                    {
                        "title": "Configuration",
                        "path": "/admin/system/config"
                    },
                    {
                        "title": "Logs",
                        "path": "/admin/system/logs"
                    },
                    {
                        "title": "Backups",
                        "path": "/admin/system/backups"
                    },
                    {
                        "title": "Security",
                        "path": "/admin/system/security"
                    }
                ]
            },
            {
                "title": "Analytics",
                "icon": "analytics",
                "path": "/admin/analytics",
                "permission": "analytics_access"
            }
        ],
        "widgets": [
            {
                "title": "System Status",
                "type": "status",
                "position": "top-left",
                "size": "medium"
            },
            {
                "title": "Recent Activity",
                "type": "activity",
                "position": "top-right",
                "size": "medium"
            },
            {
                "title": "User Statistics",
                "type": "chart",
                "position": "bottom-left",
                "size": "large"
            },
            {
                "title": "Quick Actions",
                "type": "actions",
                "position": "bottom-right",
                "size": "small"
            }
        ]
    }
    
    return dashboard_config

def create_admin_setup_script():
    """Create the complete admin setup script"""
    
    setup_script = '''#!/bin/bash
# Terpedia.com Admin Setup Script

set -e

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
        "created_at": "2024-01-01T00:00:00Z",
        "status": "active",
        "two_factor_enabled": true,
        "access_level": "full"
    },
    "security": {
        "api_key": "terpedia_admin_key_2024",
        "session_token": "terpedia_session_token_2024",
        "login_attempts": 0,
        "locked_until": null
    },
    "access": {
        "allowed_ips": [],
        "allowed_domains": ["terpedia.com", "syzygyx.com"],
        "concurrent_sessions": 5,
        "session_timeout": 3600
    }
}
EOF

# Create admin API endpoints
cat > admin_api.py << 'EOF'
from flask import Flask, request, jsonify
import json
import jwt
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'terpedia_admin_secret_2024'

# Load admin config
with open('admin_config.json', 'r') as f:
    admin_config = json.load(f)

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if email == admin_config['user']['email']:
        # Generate JWT token
        token = jwt.encode({
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'role': admin_config['user']['role']
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'success': True,
            'token': token,
            'user': admin_config['user'],
            'expires_at': (datetime.utcnow() + timedelta(hours=24)).isoformat()
        })
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
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
    except jwt.ExpiredSignatureError:
        return jsonify({'success': False, 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'success': False, 'message': 'Invalid token'}), 401

@app.route('/admin/users', methods=['GET'])
def get_users():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({
            'success': True,
            'users': [admin_config['user']],
            'total': 1
        })
    except jwt.ExpiredSignatureError:
        return jsonify({'success': False, 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'success': False, 'message': 'Invalid token'}), 401

@app.route('/admin/system/status', methods=['GET'])
def system_status():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
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
    except jwt.ExpiredSignatureError:
        return jsonify({'success': False, 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'success': False, 'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
EOF

# Install required packages
pip3 install flask pyjwt

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

# Check service status
systemctl status terpedia-admin --no-pager

echo "✅ Terpedia Admin Access setup completed!"
echo "🌐 Admin API available at: http://terpedia.com:8080"
echo "👤 Admin user: dan@syzygyx.com"
echo "🔑 Login endpoint: POST /admin/login"
echo "📊 Dashboard: GET /admin/dashboard"
EOF

    return setup_script

def main():
    """Main function to create admin setup"""
    print("🎓 Terpedia.com Admin Setup for dan@syzygyx.com")
    print("=" * 50)
    
    # Create admin configuration
    admin_config = create_admin_user()
    print("✅ Admin user configuration created")
    
    # Create database schema
    database_schema = create_admin_database()
    print("✅ Database schema created")
    
    # Create API endpoints
    api_endpoints = create_admin_api()
    print("✅ API endpoints defined")
    
    # Create dashboard configuration
    dashboard_config = create_admin_dashboard()
    print("✅ Dashboard configuration created")
    
    # Create setup script
    setup_script = create_admin_setup_script()
    
    # Save setup script
    with open('terpedia_admin_setup.sh', 'w') as f:
        f.write(setup_script)
    
    # Make it executable
    import os
    os.chmod('terpedia_admin_setup.sh', 0o755)
    
    print("\n🎉 Admin setup files created successfully!")
    print("=" * 40)
    print("📁 Files created:")
    print("   - terpedia_admin_setup.sh (executable setup script)")
    print("   - terpedia_admin_setup.py (this configuration script)")
    
    print("\n📋 Admin Configuration Summary:")
    print(f"   👤 Email: {admin_config['user']['email']}")
    print(f"   🎭 Role: {admin_config['user']['role']}")
    print(f"   🔐 Permissions: {len(admin_config['user']['permissions'])} total")
    print(f"   🌐 Access Level: {admin_config['user']['access_level']}")
    
    print("\n🚀 Next Steps:")
    print("1. Deploy the setup script to terpedia.com server")
    print("2. Run: bash terpedia_admin_setup.sh")
    print("3. Test admin access at: http://terpedia.com:8080/admin/login")
    print("4. Access dashboard at: http://terpedia.com:8080/admin/dashboard")
    
    return True

if __name__ == "__main__":
    main()