#!/usr/bin/env python3
"""
Setup Google Drive for MSAI Curriculum System
Creates a Shared Drive and configures service account access
"""

import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Service account credentials
SERVICE_ACCOUNT_FILE = 'msai-service-account-key.json'
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata'
]

def setup_google_drive():
    """Setup Google Drive access and create Shared Drive"""
    print("🚀 Setting up Google Drive for MSAI Curriculum System")
    print("=" * 60)
    
    # Load service account credentials
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        print("✅ Service account credentials loaded")
    except Exception as e:
        print(f"❌ Error loading service account credentials: {e}")
        return False
    
    # Build Drive API service
    try:
        service = build('drive', 'v3', credentials=credentials)
        print("✅ Google Drive API service initialized")
    except Exception as e:
        print(f"❌ Error initializing Drive API: {e}")
        return False
    
    # Create Shared Drive
    try:
        shared_drive_metadata = {
            'name': 'MSAI Curriculum System',
            'description': 'Shared Drive for MSAI Curriculum System - AI-powered education platform',
            'restrictions': {
                'adminManagedRestrictions': False,
                'copyRequiresWriterPermission': True,
                'domainUsersOnly': False,
                'driveMembersOnly': True
            }
        }
        
        shared_drive = service.drives().create(
            body=shared_drive_metadata,
            requestId='msai-shared-drive-' + str(int(os.urandom(4).hex(), 16))
        ).execute()
        
        shared_drive_id = shared_drive['id']
        print(f"✅ Shared Drive created: {shared_drive['name']} (ID: {shared_drive_id})")
        
    except HttpError as e:
        if e.resp.status == 409:
            print("⚠️  Shared Drive already exists, finding existing drive...")
            # List existing drives to find MSAI drive
            drives = service.drives().list().execute()
            shared_drive_id = None
            for drive in drives.get('drives', []):
                if 'MSAI' in drive['name']:
                    shared_drive_id = drive['id']
                    print(f"✅ Found existing MSAI Shared Drive: {drive['name']} (ID: {shared_drive_id})")
                    break
            
            if not shared_drive_id:
                print("❌ Could not find existing MSAI Shared Drive")
                return False
        else:
            print(f"❌ Error creating Shared Drive: {e}")
            return False
    
    # Add service account as manager of the Shared Drive
    try:
        permission_metadata = {
            'role': 'manager',
            'type': 'user',
            'emailAddress': 'msai-service-account@syzygyx-161202.iam.gserviceaccount.com'
        }
        
        service.permissions().create(
            fileId=shared_drive_id,
            body=permission_metadata,
            supportsAllDrives=True
        ).execute()
        
        print("✅ Service account added as manager of Shared Drive")
        
    except HttpError as e:
        if e.resp.status == 409:
            print("✅ Service account already has access to Shared Drive")
        else:
            print(f"❌ Error adding service account to Shared Drive: {e}")
            return False
    
    # Create folder structure
    try:
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
            folder_metadata = {
                'name': folder['name'],
                'description': folder['description'],
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [shared_drive_id]
            }
            
            created_folder = service.files().create(
                body=folder_metadata,
                supportsAllDrives=True,
                fields='id,name'
            ).execute()
            
            created_folders[folder['name']] = created_folder['id']
            print(f"✅ Created folder: {folder['name']}")
        
    except HttpError as e:
        print(f"❌ Error creating folders: {e}")
        return False
    
    # Save configuration
    config = {
        'shared_drive_id': shared_drive_id,
        'shared_drive_name': 'MSAI Curriculum System',
        'service_account_email': 'msai-service-account@syzygyx-161202.iam.gserviceaccount.com',
        'service_account_file': SERVICE_ACCOUNT_FILE,
        'scopes': SCOPES,
        'folders': created_folders,
        'drive_url': f'https://drive.google.com/drive/folders/{shared_drive_id}'
    }
    
    with open('msai_drive_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Google Drive setup complete!")
    print(f"📁 Shared Drive: {config['shared_drive_name']}")
    print(f"🔗 Drive URL: {config['drive_url']}")
    print(f"📄 Configuration saved to: msai_drive_config.json")
    print(f"📁 Created {len(created_folders)} folders")
    
    return True

def test_drive_access():
    """Test Google Drive access"""
    print("\n🧪 Testing Google Drive access...")
    
    try:
        with open('msai_drive_config.json', 'r') as f:
            config = json.load(f)
        
        credentials = service_account.Credentials.from_service_account_file(
            config['service_account_file'], scopes=config['scopes']
        )
        
        service = build('drive', 'v3', credentials=credentials)
        
        # Test listing files in the shared drive
        results = service.files().list(
            q=f"'{config['shared_drive_id']}' in parents",
            supportsAllDrives=True,
            fields="files(id,name,mimeType)"
        ).execute()
        
        files = results.get('files', [])
        print(f"✅ Successfully accessed Shared Drive")
        print(f"📁 Found {len(files)} items in the drive")
        
        for file in files:
            file_type = "📁" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
            print(f"   {file_type} {file['name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing drive access: {e}")
        return False

if __name__ == "__main__":
    if setup_google_drive():
        test_drive_access()
    else:
        print("❌ Google Drive setup failed")