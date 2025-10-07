#!/usr/bin/env python3
"""
Working Google Form Creator - Step by step approach
"""

import json
import os
import time
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

def create_google_form_step_by_step():
    """Create Google Form step by step to avoid API issues"""
    try:
        # Authenticate
        credentials = authenticate_service_account()
        if not credentials:
            return None
        
        # Build the Forms API service
        service = build('forms', 'v1', credentials=credentials)
        
        print("🚀 Creating Google Form step by step...")
        
        # Step 1: Create the form with just the title
        print("📝 Step 1: Creating form with title...")
        form_info = {
            "info": {
                "title": "MS AI Program Application - AURNOVA University"
            }
        }
        
        form = service.forms().create(body=form_info).execute()
        form_id = form['formId']
        
        print(f"✅ Form created with ID: {form_id}")
        print(f"🔗 Form URL: {form['responderUri']}")
        
        # Wait a moment for the form to be fully created
        time.sleep(2)
        
        # Step 2: Update the description
        print("📝 Step 2: Updating form description...")
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
        
        # Step 3: Add questions one by one to avoid batch issues
        print("📝 Step 3: Adding questions one by one...")
        
        questions = [
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
            },
            {
                "title": "Mailing Address",
                "description": "Please provide your complete mailing address including street, city, state, ZIP code, and country.",
                "type": "text",
                "required": True,
                "paragraph": True
            },
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
        
        for i, question in enumerate(questions):
            try:
                print(f"  Adding question {i+1}: {question['title']}")
                
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
                                                "paragraph": question.get('paragraph', False)
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
                
                # Small delay between requests
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ❌ Error adding {question['title']}: {e}")
                continue
        
        # Step 4: Add essay questions
        print("📝 Step 4: Adding essay questions...")
        
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
                print(f"  Adding essay {i+1}: {essay['title']}")
                
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
                            "location": {"index": len(questions) + i}
                        }
                    }]
                }
                
                service.forms().batchUpdate(formId=form_id, body=request).execute()
                print(f"  ✅ Added: {essay['title']}")
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ❌ Error adding {essay['title']}: {e}")
                continue
        
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
        elif error.resp.status == 500:
            print("💡 This is a server error. The Google Forms API might be experiencing issues.")
        return None
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return None

def main():
    """Main function"""
    print("🚀 Creating MS AI Application Google Form (Step by Step)...")
    print("=" * 70)
    
    # Check if service account key exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Service account key file not found: {SERVICE_ACCOUNT_FILE}")
        return
    
    # Create the form
    result = create_google_form_step_by_step()
    
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
                'status': 'Google Form created successfully'
            }, f, indent=2)
        print(f"\n💾 Form details saved to form_details.json")
        
        print(f"\n📋 Next steps:")
        print(f"1. Visit the form URL to test: {result['responderUri']}")
        print(f"2. Add more questions manually in Google Forms if needed")
        print(f"3. Customize the form appearance and settings")
        print(f"4. Set up the linked Google Sheet for responses")
        print(f"5. Update your website to link to this form")
        print(f"6. Test the complete application flow")
        
    else:
        print("\n❌ Form creation failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("1. Check that the Google Forms API is enabled in your Google Cloud project")
        print("2. Verify that the service account has the correct permissions")
        print("3. Check the service account key file is valid")
        print("4. Try creating a form manually in Google Forms to test API access")

if __name__ == "__main__":
    main()