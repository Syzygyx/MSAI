# Google Docs MCP Server Setup Guide

This guide will help you install and configure the Google Docs MCP server in Cursor to enable Google Docs integration.

## Prerequisites

- Node.js (version 18 or higher)
- npm or yarn
- Cursor IDE
- Google Cloud Project with APIs enabled

## Step 1: Google Cloud Setup

### 1.1 Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Note your project ID

### 1.2 Enable Required APIs
Enable these APIs in your Google Cloud project:
- Google Docs API
- Google Drive API
- Google Sheets API
- Google Forms API

### 1.3 Create Service Account
1. Go to IAM & Admin > Service Accounts
2. Click "Create Service Account"
3. Name: `mcp-google-docs`
4. Description: `MCP server for Google Docs integration`
5. Click "Create and Continue"
6. Grant roles:
   - Editor (or more specific roles)
   - Google Docs API User
   - Google Drive API User
7. Click "Done"

### 1.4 Generate Service Account Key
1. Click on your service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose "JSON" format
5. Download the key file
6. Save as `google-service-account.json` in your project directory

## Step 2: Install Google Docs MCP Server

### 2.1 Clone the Repository
```bash
cd /Users/danielmcshan/GitHub/MSAI
git clone https://github.com/a-bonus/google-docs-mcp.git
cd google-docs-mcp
```

### 2.2 Install Dependencies
```bash
npm install
```

### 2.3 Build the Server
```bash
npm run build
```

### 2.4 Install Globally (Optional)
```bash
npm install -g .
```

## Step 3: Configure the MCP Server

### 3.1 Create Configuration File
Create `mcp-config.json` in the google-docs-mcp directory:

```json
{
  "serviceAccountPath": "/Users/danielmcshan/GitHub/MSAI/google-service-account.json",
  "scopes": [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/forms.body"
  ],
  "port": 3001,
  "logLevel": "info"
}
```

### 3.2 Test the Server
```bash
# Start the server
npm start

# In another terminal, test it
curl http://localhost:3001/health
```

## Step 4: Configure Cursor MCP

### 4.1 Open Cursor Settings
1. Open Cursor
2. Go to Settings (Cmd+,)
3. Search for "MCP" or "Model Context Protocol"

### 4.2 Add MCP Server Configuration
Add this to your Cursor MCP configuration:

```json
{
  "mcpServers": {
    "google-docs": {
      "command": "node",
      "args": ["/Users/danielmcshan/GitHub/MSAI/google-docs-mcp/dist/index.js"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/Users/danielmcshan/GitHub/MSAI/google-service-account.json"
      }
    }
  }
}
```

### 4.3 Alternative: Use Package Manager
If you installed globally:
```json
{
  "mcpServers": {
    "google-docs": {
      "command": "google-docs-mcp",
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/Users/danielmcshan/GitHub/MSAI/google-service-account.json"
      }
    }
  }
}
```

## Step 5: Verify Installation

### 5.1 Restart Cursor
Close and reopen Cursor to load the MCP server.

### 5.2 Test MCP Integration
1. Open a new chat in Cursor
2. Try asking: "Can you create a Google Doc for me?"
3. The MCP server should provide Google Docs tools

### 5.3 Check MCP Server Status
Look for MCP server status in Cursor's status bar or settings.

## Step 6: Troubleshooting

### Common Issues

#### 6.1 Authentication Errors
```bash
# Check service account file
ls -la /Users/danielmcshan/GitHub/MSAI/google-service-account.json

# Verify JSON format
cat /Users/danielmcshan/GitHub/MSAI/google-service-account.json | jq .
```

#### 6.2 Permission Errors
- Ensure service account has proper roles
- Check API quotas in Google Cloud Console
- Verify APIs are enabled

#### 6.3 MCP Server Not Starting
```bash
# Check server logs
cd /Users/danielmcshan/GitHub/MSAI/google-docs-mcp
npm start

# Check for errors
tail -f logs/mcp-server.log
```

#### 6.4 Cursor Not Detecting MCP
- Restart Cursor completely
- Check MCP configuration syntax
- Verify file paths are correct
- Check Cursor logs for MCP errors

## Step 7: Advanced Configuration

### 7.1 Custom Scopes
Add additional scopes to `mcp-config.json`:
```json
{
  "scopes": [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/calendar"
  ]
}
```

### 7.2 Multiple Service Accounts
```json
{
  "serviceAccounts": {
    "docs": "/path/to/docs-service-account.json",
    "sheets": "/path/to/sheets-service-account.json"
  }
}
```

### 7.3 Environment Variables
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/Users/danielmcshan/GitHub/MSAI/google-service-account.json"
export MCP_LOG_LEVEL="debug"
```

## Step 8: Usage Examples

Once configured, you can use the MCP server in Cursor:

### 8.1 Create Documents
"Create a new Google Doc titled 'Project Proposal'"

### 8.2 Read Documents
"Read the content of document ID: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"

### 8.3 Update Documents
"Add a new paragraph to the document about project timeline"

### 8.4 Create Forms
"Create a Google Form for collecting user feedback"

## Step 9: Security Best Practices

### 9.1 Service Account Security
- Store service account keys securely
- Use environment variables for paths
- Regularly rotate keys
- Limit permissions to minimum required

### 9.2 MCP Server Security
- Run MCP server locally only
- Use HTTPS in production
- Monitor server logs
- Implement rate limiting

## Step 10: Maintenance

### 10.1 Regular Updates
```bash
cd /Users/danielmcshan/GitHub/MSAI/google-docs-mcp
git pull origin main
npm update
npm run build
```

### 10.2 Monitor Performance
- Check Google Cloud Console for API usage
- Monitor MCP server logs
- Update Cursor regularly

### 10.3 Backup Configuration
```bash
# Backup MCP configuration
cp ~/.cursor/mcp-config.json ~/backup/mcp-config-$(date +%Y%m%d).json
```

## Support

If you encounter issues:
1. Check the [Google Docs MCP repository](https://github.com/a-bonus/google-docs-mcp) for updates
2. Review Google Cloud Console for API errors
3. Check Cursor's MCP documentation
4. Create an issue in the MCP repository

## Next Steps

Once the MCP server is working:
1. Test all Google Docs operations
2. Integrate with your existing Google Form creator
3. Set up automated document generation
4. Create templates for common documents