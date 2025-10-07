#!/bin/bash

# Google Docs MCP Server Setup Script
# This script automates the installation and configuration of the Google Docs MCP server

set -e  # Exit on any error

echo "🚀 Setting up Google Docs MCP Server for Cursor"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Node.js is installed
check_nodejs() {
    print_status "Checking Node.js installation..."
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js is installed: $NODE_VERSION"
        
        # Check if version is 18 or higher
        NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
        if [ "$NODE_MAJOR" -lt 18 ]; then
            print_warning "Node.js version $NODE_VERSION detected. Version 18+ is recommended."
        fi
    else
        print_error "Node.js is not installed. Please install Node.js 18+ first."
        echo "Visit: https://nodejs.org/"
        exit 1
    fi
}

# Check if npm is installed
check_npm() {
    print_status "Checking npm installation..."
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "npm is installed: $NPM_VERSION"
    else
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
}

# Create project directory
create_project_dir() {
    print_status "Creating project directory..."
    PROJECT_DIR="/Users/danielmcshan/GitHub/MSAI/google-docs-mcp"
    
    if [ -d "$PROJECT_DIR" ]; then
        print_warning "Directory $PROJECT_DIR already exists. Updating..."
        cd "$PROJECT_DIR"
        git pull origin main
    else
        print_status "Cloning Google Docs MCP repository..."
        git clone https://github.com/a-bonus/google-docs-mcp.git "$PROJECT_DIR"
        cd "$PROJECT_DIR"
    fi
    
    print_success "Project directory ready: $PROJECT_DIR"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    npm install
    print_success "Dependencies installed successfully"
}

# Build the project
build_project() {
    print_status "Building the project..."
    npm run build
    print_success "Project built successfully"
}

# Create configuration file
create_config() {
    print_status "Creating MCP configuration file..."
    
    CONFIG_FILE="mcp-config.json"
    SERVICE_ACCOUNT_FILE="/Users/danielmcshan/GitHub/MSAI/google-service-account.json"
    
    cat > "$CONFIG_FILE" << EOF
{
  "serviceAccountPath": "$SERVICE_ACCOUNT_FILE",
  "scopes": [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/forms.body"
  ],
  "port": 3001,
  "logLevel": "info"
}
EOF
    
    print_success "Configuration file created: $CONFIG_FILE"
}

# Create Cursor MCP configuration
create_cursor_config() {
    print_status "Creating Cursor MCP configuration..."
    
    CURSOR_CONFIG_DIR="$HOME/Library/Application Support/Cursor/User"
    CURSOR_MCP_CONFIG="$CURSOR_CONFIG_DIR/mcp-settings.json"
    
    # Create directory if it doesn't exist
    mkdir -p "$CURSOR_CONFIG_DIR"
    
    # Check if Cursor config already exists
    if [ -f "$CURSOR_MCP_CONFIG" ]; then
        print_warning "Cursor MCP configuration already exists. Creating backup..."
        cp "$CURSOR_MCP_CONFIG" "$CURSOR_MCP_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
    fi
    
    # Create Cursor MCP configuration
    cat > "$CURSOR_MCP_CONFIG" << EOF
{
  "mcpServers": {
    "google-docs": {
      "command": "node",
      "args": ["$PROJECT_DIR/dist/index.js"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "$SERVICE_ACCOUNT_FILE"
      }
    }
  }
}
EOF
    
    print_success "Cursor MCP configuration created: $CURSOR_MCP_CONFIG"
}

# Check for service account file
check_service_account() {
    print_status "Checking for Google service account file..."
    
    SERVICE_ACCOUNT_FILE="/Users/danielmcshan/GitHub/MSAI/google-service-account.json"
    
    if [ -f "$SERVICE_ACCOUNT_FILE" ]; then
        print_success "Service account file found: $SERVICE_ACCOUNT_FILE"
        
        # Validate JSON format
        if jq empty "$SERVICE_ACCOUNT_FILE" 2>/dev/null; then
            print_success "Service account file is valid JSON"
        else
            print_error "Service account file is not valid JSON"
            exit 1
        fi
    else
        print_warning "Service account file not found: $SERVICE_ACCOUNT_FILE"
        print_status "Please download your service account key from Google Cloud Console:"
        echo "1. Go to https://console.cloud.google.com/"
        echo "2. Navigate to IAM & Admin > Service Accounts"
        echo "3. Create or select a service account"
        echo "4. Generate a new JSON key"
        echo "5. Save it as: $SERVICE_ACCOUNT_FILE"
        echo ""
        read -p "Press Enter when you have downloaded the service account file..."
        
        if [ -f "$SERVICE_ACCOUNT_FILE" ]; then
            print_success "Service account file found after download"
        else
            print_error "Service account file still not found. Please check the path and try again."
            exit 1
        fi
    fi
}

# Test the MCP server
test_mcp_server() {
    print_status "Testing MCP server..."
    
    # Start server in background
    npm start &
    SERVER_PID=$!
    
    # Wait for server to start
    sleep 3
    
    # Test health endpoint
    if curl -s http://localhost:3001/health > /dev/null; then
        print_success "MCP server is running and responding"
    else
        print_warning "MCP server health check failed"
    fi
    
    # Stop the server
    kill $SERVER_PID 2>/dev/null || true
    
    print_success "MCP server test completed"
}

# Create startup script
create_startup_script() {
    print_status "Creating startup script..."
    
    STARTUP_SCRIPT="start-mcp-server.sh"
    
    cat > "$STARTUP_SCRIPT" << 'EOF'
#!/bin/bash
# Google Docs MCP Server Startup Script

echo "🚀 Starting Google Docs MCP Server..."

# Check if service account file exists
if [ ! -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "❌ Service account file not found: $GOOGLE_APPLICATION_CREDENTIALS"
    echo "Please set GOOGLE_APPLICATION_CREDENTIALS environment variable"
    exit 1
fi

# Start the server
npm start
EOF
    
    chmod +x "$STARTUP_SCRIPT"
    print_success "Startup script created: $STARTUP_SCRIPT"
}

# Create environment file
create_env_file() {
    print_status "Creating environment file..."
    
    ENV_FILE=".env"
    
    cat > "$ENV_FILE" << EOF
# Google Docs MCP Server Environment Variables
GOOGLE_APPLICATION_CREDENTIALS=/Users/danielmcshan/GitHub/MSAI/google-service-account.json
MCP_LOG_LEVEL=info
MCP_PORT=3001
EOF
    
    print_success "Environment file created: $ENV_FILE"
}

# Main installation function
main() {
    echo ""
    print_status "Starting Google Docs MCP Server installation..."
    echo ""
    
    # Run all checks and installations
    check_nodejs
    check_npm
    create_project_dir
    install_dependencies
    build_project
    check_service_account
    create_config
    create_cursor_config
    create_startup_script
    create_env_file
    test_mcp_server
    
    echo ""
    print_success "🎉 Google Docs MCP Server setup completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "1. Restart Cursor to load the MCP server"
    echo "2. Test the integration by asking Cursor to create a Google Doc"
    echo "3. Check the MCP server logs if you encounter issues"
    echo ""
    print_status "Files created:"
    echo "- MCP configuration: mcp-config.json"
    echo "- Cursor configuration: $HOME/Library/Application Support/Cursor/User/mcp-settings.json"
    echo "- Startup script: start-mcp-server.sh"
    echo "- Environment file: .env"
    echo ""
    print_status "To start the MCP server manually:"
    echo "cd $PROJECT_DIR && ./start-mcp-server.sh"
    echo ""
    print_status "To check server status:"
    echo "curl http://localhost:3001/health"
    echo ""
}

# Run main function
main "$@"