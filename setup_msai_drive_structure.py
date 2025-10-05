#!/usr/bin/env python3
"""
Setup MSAI Google Drive with organizational structure
Creates Students, Faculty, Staff, and Courses folders
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
        response = requests.post(url, headers=headers, json=data, params={"requestId": "msai-drive-org"})
        
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

def create_organizational_folders(access_token, drive_id):
    """Create organizational folder structure"""
    folders = [
        {
            'name': 'Applicants',
            'description': 'Prospective student applications, admissions materials, and recruitment',
            'subfolders': [
                'Application Materials',
                'Admission Essays',
                'Recommendation Letters',
                'Transcripts',
                'Test Scores',
                'Interview Records',
                'Admission Decisions',
                'Waitlist',
                'Rejected Applications',
                'Recruitment Materials',
                'Scholarship Applications',
                'International Applicants'
            ]
        },
        {
            'name': 'Students',
            'description': 'Student records, assignments, projects, and portfolios',
            'subfolders': [
                'Current Students',
                'Graduated Students',
                'Student Projects',
                'Student Portfolios',
                'Student Records',
                'Assignments',
                'Grades'
            ]
        },
        {
            'name': 'Faculty',
            'description': 'Faculty information, research, and teaching materials',
            'subfolders': [
                'Faculty Profiles',
                'Research Papers',
                'Teaching Materials',
                'Course Development',
                'Faculty Meetings',
                'Professional Development',
                'Publications'
            ]
        },
        {
            'name': 'Staff',
            'description': 'Administrative staff documents and resources',
            'subfolders': [
                'Administrative Documents',
                'HR Records',
                'Budget and Finance',
                'IT Resources',
                'Facilities',
                'Policies and Procedures',
                'Staff Training'
            ]
        },
        {
            'name': 'Courses',
            'description': 'Course materials, syllabi, and curriculum content',
            'subfolders': [
                'Course Syllabi',
                'Lecture Materials',
                'Assignments',
                'Exams and Quizzes',
                'Course Resources',
                'AI Generated Content',
                'Course Evaluations'
            ]
        }
    ]
    
    created_folders = {}
    
    for folder in folders:
        print(f"\n📁 Creating {folder['name']} folder...")
        
        # Create main folder
        main_folder_id = create_folder(access_token, drive_id, folder['name'], folder['description'])
        if main_folder_id:
            created_folders[folder['name']] = {
                'id': main_folder_id,
                'subfolders': {}
            }
            
            # Create subfolders
            for subfolder in folder['subfolders']:
                subfolder_id = create_folder(access_token, main_folder_id, subfolder, f"Subfolder for {folder['name']} - {subfolder}")
                if subfolder_id:
                    created_folders[folder['name']]['subfolders'][subfolder] = subfolder_id
                    print(f"   ✅ Created subfolder: {subfolder}")
                else:
                    print(f"   ❌ Failed to create subfolder: {subfolder}")
        else:
            print(f"❌ Failed to create main folder: {folder['name']}")
    
    return created_folders

def create_folder(access_token, parent_id, name, description):
    """Create a single folder"""
    url = "https://www.googleapis.com/drive/v3/files"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "name": name,
        "description": description,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, params={"supportsAllDrives": "true"})
        
        if response.status_code == 200:
            folder_info = response.json()
            return folder_info['id']
        else:
            print(f"❌ Error creating folder {name}: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception creating folder {name}: {e}")
        return None

def create_additional_folders(access_token, drive_id):
    """Create additional organizational folders"""
    additional_folders = [
        {
            'name': 'Administrative',
            'description': 'General administrative documents and system configurations'
        },
        {
            'name': 'Research and Development',
            'description': 'Research papers, experiments, and development materials'
        },
        {
            'name': 'AI Generated Content',
            'description': 'AI-generated curriculum, assessments, and learning materials'
        },
        {
            'name': 'Templates',
            'description': 'Document templates and forms'
        },
        {
            'name': 'Archives',
            'description': 'Archived documents and historical records'
        }
    ]
    
    created_additional = {}
    
    for folder in additional_folders:
        folder_id = create_folder(access_token, drive_id, folder['name'], folder['description'])
        if folder_id:
            created_additional[folder['name']] = folder_id
            print(f"✅ Created additional folder: {folder['name']}")
        else:
            print(f"❌ Failed to create additional folder: {folder['name']}")
    
    return created_additional

def main():
    """Main function to setup MSAI Google Drive structure"""
    print("🚀 Setting up MSAI Google Drive with Organizational Structure")
    print("=" * 70)
    
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
    
    # Create organizational folder structure
    print(f"\n📂 Creating organizational folder structure in '{drive_name}'...")
    org_folders = create_organizational_folders(access_token, drive_id)
    
    # Create additional folders
    print(f"\n📂 Creating additional folders...")
    additional_folders = create_additional_folders(access_token, drive_id)
    
    # Save comprehensive configuration
    config = {
        'shared_drive_id': drive_id,
        'shared_drive_name': drive_name,
        'service_account_email': 'msai-service-account@syzygyx-161202.iam.gserviceaccount.com',
        'service_account_file': 'msai-service-account-key.json',
        'organizational_folders': org_folders,
        'additional_folders': additional_folders,
        'drive_url': f'https://drive.google.com/drive/folders/{drive_id}',
        'folder_structure': {
            'Applicants': {
                'description': 'Prospective student applications, admissions materials, and recruitment',
                'subfolders': ['Application Materials', 'Admission Essays', 'Recommendation Letters', 'Transcripts', 'Test Scores', 'Interview Records', 'Admission Decisions', 'Waitlist', 'Rejected Applications', 'Recruitment Materials', 'Scholarship Applications', 'International Applicants']
            },
            'Students': {
                'description': 'Student records, assignments, projects, and portfolios',
                'subfolders': ['Current Students', 'Graduated Students', 'Student Projects', 'Student Portfolios', 'Student Records', 'Assignments', 'Grades']
            },
            'Faculty': {
                'description': 'Faculty information, research, and teaching materials',
                'subfolders': ['Faculty Profiles', 'Research Papers', 'Teaching Materials', 'Course Development', 'Faculty Meetings', 'Professional Development', 'Publications']
            },
            'Staff': {
                'description': 'Administrative staff documents and resources',
                'subfolders': ['Administrative Documents', 'HR Records', 'Budget and Finance', 'IT Resources', 'Facilities', 'Policies and Procedures', 'Staff Training']
            },
            'Courses': {
                'description': 'Course materials, syllabi, and curriculum content',
                'subfolders': ['Course Syllabi', 'Lecture Materials', 'Assignments', 'Exams and Quizzes', 'Course Resources', 'AI Generated Content', 'Course Evaluations']
            }
        }
    }
    
    with open('msai_drive_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ MSAI Google Drive setup complete!")
    print(f"📁 Shared Drive: {config['shared_drive_name']}")
    print(f"🔗 Drive URL: {config['drive_url']}")
    print(f"📄 Configuration saved to: msai_drive_config.json")
    
    # Print folder summary
    print(f"\n📊 Folder Structure Created:")
    for folder_name, folder_data in org_folders.items():
        if isinstance(folder_data, dict) and 'subfolders' in folder_data:
            print(f"   📁 {folder_name} ({len(folder_data['subfolders'])} subfolders)")
            for subfolder_name in folder_data['subfolders'].keys():
                print(f"      📂 {subfolder_name}")
        else:
            print(f"   📁 {folder_name}")
    
    print(f"\n📁 Additional Folders:")
    for folder_name in additional_folders.keys():
        print(f"   📁 {folder_name}")
    
    return True

if __name__ == "__main__":
    main()