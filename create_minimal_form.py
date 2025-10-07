#!/usr/bin/env python3
"""
Minimal Google Form Creator - Creates MS AI Application Form
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

def create_minimal_form():
    """Create a minimal form to test API access"""
    try:
        # Authenticate
        credentials = authenticate_service_account()
        if not credentials:
            return None
        
        # Build the Forms API service
        service = build('forms', 'v1', credentials=credentials)
        
        print("🚀 Creating minimal Google Form...")
        
        # Create the form with just the title
        form_info = {
            "info": {
                "title": "MS AI Program Application - AURNOVA University"
            }
        }
        
        print("📝 Creating form with title only...")
        form = service.forms().create(body=form_info).execute()
        form_id = form['formId']
        
        print(f"✅ Form created with ID: {form_id}")
        print(f"🔗 Form URL: {form['responderUri']}")
        
        # Now try to add a simple question
        print("📝 Adding a simple question...")
        
        question_request = {
            "requests": [{
                "createItem": {
                    "item": {
                        "title": "Full Name",
                        "description": "Enter your full legal name.",
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
            service.forms().batchUpdate(formId=form_id, body=question_request).execute()
            print("✅ Added first question")
        except Exception as e:
            print(f"⚠️  Error adding question: {e}")
        
        # Add email question
        email_request = {
            "requests": [{
                "createItem": {
                    "item": {
                        "title": "Email Address",
                        "description": "Enter your email address.",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False
                                }
                            }
                        }
                    },
                    "location": {"index": 1}
                }
            }]
        }
        
        try:
            service.forms().batchUpdate(formId=form_id, body=email_request).execute()
            print("✅ Added email question")
        except Exception as e:
            print(f"⚠️  Error adding email question: {e}")
        
        # Add GPA question
        gpa_request = {
            "requests": [{
                "createItem": {
                    "item": {
                        "title": "GPA",
                        "description": "Enter your undergraduate GPA on a 4.0 scale.",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False
                                }
                            }
                        }
                    },
                    "location": {"index": 2}
                }
            }]
        }
        
        try:
            service.forms().batchUpdate(formId=form_id, body=gpa_request).execute()
            print("✅ Added GPA question")
        except Exception as e:
            print(f"⚠️  Error adding GPA question: {e}")
        
        # Add essay question
        essay_request = {
            "requests": [{
                "createItem": {
                    "item": {
                        "title": "Statement of Purpose",
                        "description": "Please describe your academic background, research interests, and career goals (500-1000 words).",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": True
                                }
                            }
                        }
                    },
                    "location": {"index": 3}
                }
            }]
        }
        
        try:
            service.forms().batchUpdate(formId=form_id, body=essay_request).execute()
            print("✅ Added essay question")
        except Exception as e:
            print(f"⚠️  Error adding essay question: {e}")
        
        # Get the final form details
        final_form = service.forms().get(formId=form_id).execute()
        
        return {
            'formId': form_id,
            'responderUri': form['responderUri'],
            'form': final_form
        }
        
    except HttpError as error:
        print(f"❌ Error creating form: {error}")
        if error.resp.status == 403:
            print("💡 This might be a permissions issue. Check that the service account has the correct permissions.")
        elif error.resp.status == 400:
            print("💡 This might be a request format issue. Check the API documentation.")
        return None
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return None

def main():
    """Main function"""
    print("🚀 Creating Minimal MS AI Application Google Form...")
    print("=" * 60)
    
    # Check if service account key exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Service account key file not found: {SERVICE_ACCOUNT_FILE}")
        return
    
    # Create the form
    result = create_minimal_form()
    
    if result:
        print("\n🎉 Form creation completed!")
        print(f"\n📋 Form Details:")
        print(f"📝 Form ID: {result['formId']}")
        print(f"🔗 Form URL: {result['responderUri']}")
        
        # Save form details to file
        with open('form_details.json', 'w') as f:
            json.dump({
                'formId': result['formId'],
                'formUrl': result['responderUri'],
                'createdAt': 'Just now',
                'status': 'Minimal form created successfully'
            }, f, indent=2)
        print(f"\n💾 Form details saved to form_details.json")
        
        print(f"\n📋 Next steps:")
        print(f"1. Visit the form URL to test: {result['responderUri']}")
        print(f"2. Add more questions manually in Google Forms")
        print(f"3. Customize the form appearance and settings")
        print(f"4. Set up the linked Google Sheet for responses")
        print(f"5. Update your website to link to this form")
        print(f"6. Test the complete application flow")
        
        print(f"\n💡 This is a minimal form with basic questions.")
        print(f"   You can add more questions manually in Google Forms or")
        print(f"   run additional scripts to add more questions programmatically.")
    else:
        print("\n❌ Form creation failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("1. Check that the Google Forms API is enabled in your Google Cloud project")
        print("2. Verify that the service account has the correct permissions")
        print("3. Check the service account key file is valid")
        print("4. Try creating a form manually in Google Forms to test API access")

if __name__ == "__main__":
    main()