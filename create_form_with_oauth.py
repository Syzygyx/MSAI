#!/usr/bin/env python3
"""
Create Google Form using OAuth authentication
This should work even if service account has issues
"""

import json
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# OAuth scopes
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/drive.file'
]

def authenticate_oauth():
    """Authenticate using OAuth 2.0"""
    try:
        creds = None
        token_file = 'token.json'
        
        # Load existing token
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                from google.auth.transport.requests import Request
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    print("❌ OAuth credentials file not found: credentials.json")
                    print("Run: python create_oauth_credentials.py")
                    return None
                
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        return creds
        
    except Exception as e:
        print(f"❌ OAuth authentication failed: {e}")
        return None

def create_form_with_oauth():
    """Create Google Form using OAuth"""
    try:
        # Authenticate
        creds = authenticate_oauth()
        if not creds:
            return None
        
        # Build the Forms API service
        service = build('forms', 'v1', credentials=creds)
        
        print("🚀 Creating Google Form with OAuth...")
        
        # Create the form
        form_info = {
            "info": {
                "title": "MS AI Program Application - AURNOVA University"
            }
        }
        
        form = service.forms().create(body=form_info).execute()
        form_id = form['formId']
        
        print(f"✅ Form created with ID: {form_id}")
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
        
        # Add questions in batches
        print("📝 Adding questions...")
        
        # Batch 1: Personal Information
        personal_questions = [
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
        
        # Add personal questions
        for i, question in enumerate(personal_questions):
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
        
        # Add academic questions
        print("📝 Adding academic questions...")
        
        academic_questions = [
            {
                "title": "Undergraduate Degree",
                "description": "Enter your undergraduate degree (e.g., Bachelor of Science in Computer Science).",
                "type": "text",
                "required": True
            },
            {
                "title": "Institution",
                "description": "Name of the institution where you earned your undergraduate degree.",
                "type": "text",
                "required": True
            },
            {
                "title": "GPA",
                "description": "Enter your undergraduate GPA on a 4.0 scale.",
                "type": "text",
                "required": True
            },
            {
                "title": "Graduation Year",
                "description": "Year you graduated or expect to graduate from your undergraduate program.",
                "type": "text",
                "required": True
            }
        ]
        
        for i, question in enumerate(academic_questions):
            try:
                print(f"  Adding: {question['title']}")
                
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
                            "location": {"index": len(personal_questions) + i}
                        }
                    }]
                }
                
                service.forms().batchUpdate(formId=form_id, body=request).execute()
                print(f"  ✅ Added: {question['title']}")
                
            except Exception as e:
                print(f"  ❌ Error adding {question['title']}: {e}")
        
        # Add essay questions
        print("📝 Adding essay questions...")
        
        essay_questions = [
            {
                "title": "Statement of Purpose (750-1000 words)",
                "description": "Please address your academic background, research interests, career goals, and why you chose AURNOVA University. Be specific and provide concrete examples.",
                "required": True
            },
            {
                "title": "Personal Statement (500-750 words)",
                "description": "Tell us about yourself beyond your academic achievements, including personal experiences, challenges overcome, and unique perspectives.",
                "required": True
            },
            {
                "title": "Research Interests and Potential Thesis Topics (300-500 words)",
                "description": "Describe your research interests in AI and potential thesis topics. Be specific about current research and cite relevant papers if possible.",
                "required": True
            },
            {
                "title": "Career Goals and Professional Development (300-500 words)",
                "description": "Describe your short-term and long-term career aspirations, specific roles/companies of interest, and how this program will help.",
                "required": True
            }
        ]
        
        for i, essay in enumerate(essay_questions):
            try:
                print(f"  Adding: {essay['title']}")
                
                request = {
                    "requests": [{
                        "createItem": {
                            "item": {
                                "title": essay['title'],
                                "description": essay['description'],
                                "questionItem": {
                                    "question": {
                                        "required": essay['required'],
                                        "textQuestion": {
                                            "paragraph": True
                                        }
                                    }
                                }
                            },
                            "location": {"index": len(personal_questions) + len(academic_questions) + i}
                        }
                    }]
                }
                
                service.forms().batchUpdate(formId=form_id, body=request).execute()
                print(f"  ✅ Added: {essay['title']}")
                
            except Exception as e:
                print(f"  ❌ Error adding {essay['title']}: {e}")
        
        return {
            'formId': form_id,
            'responderUri': form['responderUri'],
            'form': service.forms().get(formId=form_id).execute()
        }
        
    except HttpError as error:
        print(f"❌ Error creating form: {error}")
        return None
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return None

def main():
    """Main function"""
    print("🚀 Creating MS AI Application Google Form with OAuth...")
    print("=" * 60)
    
    # Check if OAuth credentials exist
    if not os.path.exists('credentials.json'):
        print("❌ OAuth credentials file not found: credentials.json")
        print("\n📋 To set up OAuth credentials:")
        print("1. Run: python create_oauth_credentials.py")
        print("2. Follow the instructions to create OAuth credentials")
        print("3. Run this script again")
        return
    
    # Create the form
    result = create_form_with_oauth()
    
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
                'status': 'Google Form created successfully with OAuth'
            }, f, indent=2)
        print(f"\n💾 Form details saved to form_details.json")
        
        print(f"\n📋 Next steps:")
        print(f"1. Visit the form URL to test: {result['responderUri']}")
        print(f"2. Add more questions manually in Google Forms if needed")
        print(f"3. Customize the form appearance and settings")
        print(f"4. Set up the linked Google Sheet for responses")
        print(f"5. Update your website to link to this form")
        
    else:
        print("\n❌ Form creation failed. Please check the error messages above.")

if __name__ == "__main__":
    main()