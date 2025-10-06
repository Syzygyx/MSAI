#!/usr/bin/env python3
"""
Test Google Form creation with minimal form
"""

import json
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

def create_simple_form():
    """Create a simple test form"""
    try:
        # Authenticate
        credentials = authenticate_service_account()
        if not credentials:
            return None
        
        # Build the Forms API service
        service = build('forms', 'v1', credentials=credentials)
        
        print("🚀 Creating simple test form...")
        
        # Create a very basic form
        form_info = {
            "info": {
                "title": "MS AI Test Form"
            }
        }
        
        form = service.forms().create(body=form_info).execute()
        form_id = form['formId']
        
        print(f"✅ Test form created with ID: {form_id}")
        print(f"🔗 Form URL: {form['responderUri']}")
        
        # Try to add one simple question
        print("📝 Adding a test question...")
        
        batch_request = {
            "requests": [{
                "createItem": {
                    "item": {
                        "title": "What is your name?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False
                                }
                            }
                        }
                    },
                    "location": {"index": 0}
                }
            }]
        }
        
        try:
            service.forms().batchUpdate(formId=form_id, body=batch_request).execute()
            print("✅ Test question added successfully!")
        except Exception as e:
            print(f"❌ Error adding question: {e}")
        
        return {
            'formId': form_id,
            'responderUri': form['responderUri']
        }
        
    except HttpError as error:
        print(f"❌ Error creating form: {error}")
        return None
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return None

def main():
    """Main function"""
    print("🧪 Testing Google Form creation...")
    print("=" * 50)
    
    # Check if service account key exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Service account key file not found: {SERVICE_ACCOUNT_FILE}")
        return
    
    # Create the test form
    result = create_simple_form()
    
    if result:
        print("\n🎉 Test form created successfully!")
        print(f"📝 Form ID: {result['formId']}")
        print(f"🔗 Form URL: {result['responderUri']}")
        print("\n✅ Google Forms API is working! You can now create the full form manually.")
    else:
        print("\n❌ Test form creation failed.")
        print("💡 This might be a temporary issue with Google's servers.")
        print("💡 Try the manual setup approach instead.")

if __name__ == "__main__":
    import os
    main()