#!/usr/bin/env python3
"""
Test Google Drive access for MSAI Curriculum System
"""

import json
import subprocess
import requests

def run_gcloud_command(command):
    """Run a gcloud command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_drive_access():
    """Test Google Drive access"""
    print("🧪 Testing Google Drive Access for MSAI")
    print("=" * 50)
    
    # Check if config file exists
    try:
        with open('msai_drive_config.json', 'r') as f:
            config = json.load(f)
        print("✅ Configuration file found")
    except FileNotFoundError:
        print("❌ Configuration file not found. Please complete the manual setup first.")
        return False
    
    # Get access token
    print("\n🔑 Getting access token...")
    success, stdout, stderr = run_gcloud_command("gcloud auth print-access-token")
    if not success:
        print(f"❌ Error getting access token: {stderr}")
        return False
    
    access_token = stdout.strip()
    print("✅ Access token obtained")
    
    # Test access to Shared Drive
    print(f"\n📁 Testing access to Shared Drive: {config['shared_drive_name']}")
    
    url = f"https://www.googleapis.com/drive/v3/files?q='{config['shared_drive_id']}' in parents"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, params={"supportsAllDrives": "true"})
        
        if response.status_code == 200:
            files = response.json()
            print(f"✅ Successfully accessed Shared Drive")
            print(f"📁 Found {len(files.get('files', []))} items")
            
            for file in files.get('files', []):
                file_type = "📁" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
                print(f"   {file_type} {file['name']}")
            
            return True
        else:
            print(f"❌ Error accessing Shared Drive: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception accessing Shared Drive: {e}")
        return False

def main():
    """Main function"""
    if test_drive_access():
        print("\n✅ Google Drive access test successful!")
        print("🚀 MSAI Curriculum System is ready to use Google Drive")
    else:
        print("\n❌ Google Drive access test failed!")
        print("📋 Please check the setup instructions in GOOGLE_DRIVE_SETUP.md")

if __name__ == "__main__":
    main()