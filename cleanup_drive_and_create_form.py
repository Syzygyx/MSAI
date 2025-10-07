#!/usr/bin/env python3
"""
Clean up Drive storage and create Google Form
"""

import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Service account credentials
SERVICE_ACCOUNT_FILE = 'msai-service-key.json'
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/drive.file'
]

def authenticate_service_account():
    """Authenticate using service account"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return credentials
    except Exception as e:
        print(f"❌ Error authenticating service account: {e}")
        return None

def cleanup_drive_storage():
    """Clean up Drive storage to free space"""
    try:
        credentials = authenticate_service_account()
        if not credentials:
            return False
        
        drive_service = build('drive', 'v3', credentials=credentials)
        
        print("🧹 Cleaning up Drive storage...")
        
        # List all files
        results = drive_service.files().list(pageSize=100, fields='files(id,name,mimeType,size,createdTime)').execute()
        files = results.get('files', [])
        
        print(f"📁 Found {len(files)} files in Drive")
        
        if not files:
            print("✅ Drive is already empty")
            return True
        
        # Show files
        print("\n📋 Files in Drive:")
        for file in files:
            size = file.get('size', 'Unknown')
            created = file.get('createdTime', 'Unknown')
            print(f"- {file['name']} ({file['mimeType']}) - Size: {size} - Created: {created}")
        
        # Ask user what to delete
        print("\n🗑️  Files that can be safely deleted:")
        deletable_files = []
        
        for file in files:
            name = file['name'].lower()
            if any(keyword in name for keyword in ['test', 'temp', 'old', 'backup', 'copy']):
                deletable_files.append(file)
                print(f"  - {file['name']} (matches cleanup criteria)")
        
        if not deletable_files:
            print("  No files match cleanup criteria")
            print("\n💡 You may need to manually delete files or increase quota")
            return False
        
        # Delete files
        deleted_count = 0
        for file in deletable_files:
            try:
                drive_service.files().delete(fileId=file['id']).execute()
                print(f"  ✅ Deleted: {file['name']}")
                deleted_count += 1
            except Exception as e:
                print(f"  ❌ Error deleting {file['name']}: {e}")
        
        print(f"\n✅ Deleted {deleted_count} files")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning up Drive: {e}")
        return False

def try_create_form():
    """Try to create Google Form after cleanup"""
    try:
        credentials = authenticate_service_account()
        if not credentials:
            return None
        
        service = build('forms', 'v1', credentials=credentials)
        
        print("🚀 Attempting to create Google Form...")
        
        # Create the form
        form_info = {
            "info": {
                "title": "MS AI Program Application - AURNOVA University"
            }
        }
        
        form = service.forms().create(body=form_info).execute()
        form_id = form['formId']
        
        print(f"✅ Form created successfully!")
        print(f"📝 Form ID: {form_id}")
        print(f"🔗 Form URL: {form['responderUri']}")
        
        # Update description
        print("📝 Updating form description...")
        description_update = {
            "requests": [{
                "updateFormInfo": {
                    "info": {
                        "description": "Thank you for your interest in the Master of Science in Artificial Intelligence program at AURNOVA University. This application form will help us evaluate your qualifications and fit for our program.\n\nFor technical support, please contact: admissions@aurnova.edu"
                    },
                    "updateMask": "description"
                }
            }]
        }
        
        try:
            service.forms().batchUpdate(formId=form_id, body=description_update).execute()
            print("✅ Description updated")
        except Exception as e:
            print(f"⚠️  Could not update description: {e}")
        
        # Add basic questions
        print("📝 Adding basic questions...")
        
        basic_questions = [
            {
                "title": "Full Name",
                "description": "Enter your full legal name as it appears on official documents.",
                "type": "text",
                "required": True
            },
            {
                "title": "Email Address",
                "description": "We will use this email to communicate with you about your application.",
                "type": "text",
                "required": True
            },
            {
                "title": "Phone Number",
                "description": "Include country code if outside the United States.",
                "type": "text",
                "required": True
            },
            {
                "title": "Date of Birth",
                "description": "Enter your date of birth.",
                "type": "date",
                "required": True
            },
            {
                "title": "Gender",
                "description": "Please select your gender identity.",
                "type": "multiple_choice",
                "required": True,
                "options": ["Male", "Female", "Non-binary", "Prefer not to say"]
            }
        ]
        
        # Add questions one by one
        for i, question in enumerate(basic_questions):
            try:
                print(f"  Adding: {question['title']}")
                
                if question['type'] == 'text':
                    request = {
                        "requests": [{
                            "createItem": {
                                "item": {
                                    "title": question['title'],
                                    "description": question['description'],
                                    "questionItem": {
                                        "question": {
                                            "required": question['required'],
                                            "textQuestion": {
                                                "paragraph": False
                                            }
                                        }
                                    }
                                },
                                "location": {"index": i}
                            }
                        }]
                    }
                elif question['type'] == 'date':
                    request = {
                        "requests": [{
                            "createItem": {
                                "item": {
                                    "title": question['title'],
                                    "description": question['description'],
                                    "questionItem": {
                                        "question": {
                                            "required": question['required'],
                                            "dateQuestion": {}
                                        }
                                    }
                                },
                                "location": {"index": i}
                            }
                        }]
                    }
                elif question['type'] == 'multiple_choice':
                    request = {
                        "requests": [{
                            "createItem": {
                                "item": {
                                    "title": question['title'],
                                    "description": question['description'],
                                    "questionItem": {
                                        "question": {
                                            "required": question['required'],
                                            "choiceQuestion": {
                                                "type": "RADIO",
                                                "options": [{"value": opt} for opt in question['options']]
                                            }
                                        }
                                    }
                                },
                                "location": {"index": i}
                            }
                        }]
                    }
                
                service.forms().batchUpdate(formId=form_id, body=request).execute()
                print(f"  ✅ Added: {question['title']}")
                
            except Exception as e:
                print(f"  ❌ Error adding {question['title']}: {e}")
        
        return {
            'formId': form_id,
            'responderUri': form['responderUri'],
            'form': service.forms().get(formId=form_id).execute()
        }
        
    except HttpError as error:
        print(f"❌ Error creating form: {error}")
        if error.resp.status == 403:
            print("💡 This might be a permissions issue.")
        elif error.resp.status == 500:
            print("💡 This is a server error. The Google Forms API might be experiencing issues.")
        return None
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return None

def main():
    """Main function"""
    print("🚀 Drive Cleanup and Google Form Creation")
    print("=" * 50)
    
    # Check if service account key exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Service account key file not found: {SERVICE_ACCOUNT_FILE}")
        return
    
    # Step 1: Clean up Drive storage
    print("Step 1: Cleaning up Drive storage...")
    cleanup_success = cleanup_drive_storage()
    
    if not cleanup_success:
        print("\n⚠️  Drive cleanup had issues. You may need to manually clean up or increase quota.")
        print("Proceeding with form creation attempt anyway...")
    
    # Step 2: Try to create form
    print("\nStep 2: Attempting to create Google Form...")
    result = try_create_form()
    
    if result:
        print("\n🎉 SUCCESS! Google Form created!")
        print(f"\n📋 Form Details:")
        print(f"📝 Form ID: {result['formId']}")
        print(f"🔗 Form URL: {result['responderUri']}")
        
        # Save form details
        with open('form_details.json', 'w') as f:
            json.dump({
                'formId': result['formId'],
                'formUrl': result['responderUri'],
                'createdAt': 'Just now',
                'status': 'Google Form created successfully after cleanup'
            }, f, indent=2)
        print(f"\n💾 Form details saved to form_details.json")
        
        print(f"\n📋 Next steps:")
        print(f"1. Visit the form URL to test: {result['responderUri']}")
        print(f"2. Add more questions manually in Google Forms")
        print(f"3. Customize the form appearance and settings")
        print(f"4. Set up the linked Google Sheet for responses")
        
    else:
        print("\n❌ Form creation still failed after cleanup.")
        print("\n🔧 Alternative solutions:")
        print("1. Create the form manually in Google Forms")
        print("2. Use OAuth authentication instead of service account")
        print("3. Contact Google support about quota issues")
        print("4. Use a different Google account with fresh quota")

if __name__ == "__main__":
    main()