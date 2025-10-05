#!/usr/bin/env python3
"""
Setup Google Drive using gcloud CLI and REST API
"""

import subprocess
import json
import requests
import os

def run_gcloud_command(command):
    """Run a gcloud command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def get_access_token():
    """Get access token using gcloud"""
    success, stdout, stderr = run_gcloud_command("gcloud auth print-access-token")
    if success:
        return stdout.strip()
    else:
        print(f"❌ Error getting access token: {stderr}")
        return None

def create_shared_drive(access_token):
    """Create a Shared Drive using Google Drive API"""
    url = "https://www.googleapis.com/drive/v3/drives"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "name": "MSAI Curriculum System",
        "description": "Shared Drive for MSAI Curriculum System - AI-powered education platform"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, params={"requestId": "msai-drive-001"})
        
        if response.status_code == 200:
            drive_info = response.json()
            print(f"✅ Shared Drive created: {drive_info['name']} (ID: {drive_info['id']})")
            return drive_info
        elif response.status_code == 409:
            print("⚠️  Shared Drive already exists, listing existing drives...")
            return list_existing_drives(access_token)
        else:
            print(f"❌ Error creating Shared Drive: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception creating Shared Drive: {e}")
        return None

def list_existing_drives(access_token):
    """List existing Shared Drives"""
    url = "https://www.googleapis.com/drive/v3/drives"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            drives = response.json()
            for drive in drives.get('drives', []):
                if 'MSAI' in drive['name']:
                    print(f"✅ Found existing MSAI Shared Drive: {drive['name']} (ID: {drive['id']})")
                    return drive
            print("❌ No existing MSAI Shared Drive found")
            return None
        else:
            print(f"❌ Error listing drives: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception listing drives: {e}")
        return None

def create_folders(access_token, drive_id):
    """Create folder structure in the Shared Drive"""
    folders = [
        {
            'name': 'Curriculum Materials',
            'description': 'Course materials, syllabi, and educational content'
        },
        {
            'name': 'Student Projects',
            'description': 'Student assignments, projects, and portfolios'
        },
        {
            'name': 'AI Generated Content',
            'description': 'AI-generated curriculum, assessments, and learning materials'
        },
        {
            'name': 'Research and Development',
            'description': 'Research papers, experiments, and development materials'
        },
        {
            'name': 'Administrative',
            'description': 'Administrative documents, reports, and system configurations'
        }
    ]
    
    created_folders = {}
    
    for folder in folders:
        url = "https://www.googleapis.com/drive/v3/files"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "name": folder['name'],
            "description": folder['description'],
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [drive_id]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, params={"supportsAllDrives": "true"})
            
            if response.status_code == 200:
                folder_info = response.json()
                created_folders[folder['name']] = folder_info['id']
                print(f"✅ Created folder: {folder['name']}")
            else:
                print(f"❌ Error creating folder {folder['name']}: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Exception creating folder {folder['name']}: {e}")
    
    return created_folders

def main():
    """Main function to setup Google Drive"""
    print("🚀 Setting up Google Drive for MSAI Curriculum System")
    print("=" * 60)
    
    # Get access token
    print("🔑 Getting access token...")
    access_token = get_access_token()
    if not access_token:
        print("❌ Failed to get access token")
        return False
    
    print("✅ Access token obtained")
    
    # Create Shared Drive
    print("\n📁 Creating Shared Drive...")
    drive_info = create_shared_drive(access_token)
    if not drive_info:
        print("❌ Failed to create or find Shared Drive")
        return False
    
    drive_id = drive_info['id']
    drive_name = drive_info['name']
    
    # Create folder structure
    print(f"\n📂 Creating folder structure in '{drive_name}'...")
    folders = create_folders(access_token, drive_id)
    
    # Save configuration
    config = {
        'shared_drive_id': drive_id,
        'shared_drive_name': drive_name,
        'service_account_email': 'msai-service-account@syzygyx-161202.iam.gserviceaccount.com',
        'service_account_file': 'msai-service-account-key.json',
        'folders': folders,
        'drive_url': f'https://drive.google.com/drive/folders/{drive_id}'
    }
    
    with open('msai_drive_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Google Drive setup complete!")
    print(f"📁 Shared Drive: {config['shared_drive_name']}")
    print(f"🔗 Drive URL: {config['drive_url']}")
    print(f"📄 Configuration saved to: msai_drive_config.json")
    print(f"📁 Created {len(folders)} folders")
    
    return True

if __name__ == "__main__":
    main()