#!/usr/bin/env python3
"""
Simple Google Form Creator - Creates MS AI Application Form
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

def create_basic_form():
    """Create a basic form with essential questions"""
    try:
        # Authenticate
        credentials = authenticate_service_account()
        if not credentials:
            return None
        
        # Build the Forms API service
        service = build('forms', 'v1', credentials=credentials)
        
        print("🚀 Creating basic Google Form...")
        
        # Step 1: Create the form with just the title
        form_info = {
            "info": {
                "title": "MS AI Program Application - AURNOVA University",
                "description": "Thank you for your interest in the Master of Science in Artificial Intelligence program at AURNOVA University. This application form will help us evaluate your qualifications and fit for our program.\n\nFor technical support, please contact: admissions@aurnova.edu"
            }
        }
        
        form = service.forms().create(body=form_info).execute()
        form_id = form['formId']
        
        print(f"✅ Basic form created with ID: {form_id}")
        print(f"🔗 Form URL: {form['responderUri']}")
        
        # Step 2: Add questions in small batches
        print("📝 Adding form questions...")
        
        # Batch 1: Personal Information
        batch1_requests = [
            {
                "createItem": {
                    "item": {
                        "title": "Personal Information",
                        "description": "Please provide your basic personal information.",
                        "pageBreakItem": {}
                    },
                    "location": {"index": 0}
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Full Name",
                        "description": "Enter your full legal name as it appears on official documents.",
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
            },
            {
                "createItem": {
                    "item": {
                        "title": "Email Address",
                        "description": "We will use this email to communicate with you about your application.",
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
            },
            {
                "createItem": {
                    "item": {
                        "title": "Phone Number",
                        "description": "Include country code if outside the United States.",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False
                                }
                            }
                        }
                    },
                    "location": {"index": 3}
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Date of Birth",
                        "description": "Enter your date of birth.",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "dateQuestion": {}
                            }
                        }
                    },
                    "location": {"index": 4}
                }
            }
        ]
        
        # Add first batch
        try:
            service.forms().batchUpdate(formId=form_id, body={"requests": batch1_requests}).execute()
            print("✅ Added personal information questions")
        except Exception as e:
            print(f"⚠️  Error adding batch 1: {e}")
        
        # Batch 2: Academic Information
        batch2_requests = [
            {
                "createItem": {
                    "item": {
                        "title": "Academic Information",
                        "description": "Please provide details about your academic background.",
                        "pageBreakItem": {}
                    },
                    "location": {"index": 5}
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Undergraduate Degree",
                        "description": "Enter your undergraduate degree (e.g., Bachelor of Science in Computer Science).",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False
                                }
                            }
                        }
                    },
                    "location": {"index": 6}
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Institution",
                        "description": "Name of the institution where you earned your undergraduate degree.",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False
                                }
                            }
                        }
                    },
                    "location": {"index": 7}
                }
            },
            {
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
                    "location": {"index": 8}
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Graduation Year",
                        "description": "Year you graduated or expect to graduate from your undergraduate program.",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False
                                }
                            }
                        }
                    },
                    "location": {"index": 9}
                }
            }
        ]
        
        # Add second batch
        try:
            service.forms().batchUpdate(formId=form_id, body={"requests": batch2_requests}).execute()
            print("✅ Added academic information questions")
        except Exception as e:
            print(f"⚠️  Error adding batch 2: {e}")
        
        # Batch 3: Essays
        batch3_requests = [
            {
                "createItem": {
                    "item": {
                        "title": "Essays and Statements",
                        "description": "Please provide thoughtful responses to the following essay questions.",
                        "pageBreakItem": {}
                    },
                    "location": {"index": 10}
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Statement of Purpose (750-1000 words)",
                        "description": "Please address your academic background, research interests, career goals, and why you chose AURNOVA University. Be specific and provide concrete examples.",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": True
                                }
                            }
                        }
                    },
                    "location": {"index": 11}
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Personal Statement (500-750 words)",
                        "description": "Tell us about yourself beyond your academic achievements, including personal experiences, challenges overcome, and unique perspectives.",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": True
                                }
                            }
                        }
                    },
                    "location": {"index": 12}
                }
            }
        ]
        
        # Add third batch
        try:
            service.forms().batchUpdate(formId=form_id, body={"requests": batch3_requests}).execute()
            print("✅ Added essay questions")
        except Exception as e:
            print(f"⚠️  Error adding batch 3: {e}")
        
        # Get the final form details
        final_form = service.forms().get(formId=form_id).execute()
        
        return {
            'formId': form_id,
            'responderUri': form['responderUri'],
            'form': final_form
        }
        
    except HttpError as error:
        print(f"❌ Error creating form: {error}")
        return None
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return None

def main():
    """Main function"""
    print("🚀 Creating MS AI Application Google Form (Simple Version)...")
    print("=" * 70)
    
    # Check if service account key exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Service account key file not found: {SERVICE_ACCOUNT_FILE}")
        return
    
    # Create the form
    result = create_basic_form()
    
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
                'createdAt': 'Just now'
            }, f, indent=2)
        print(f"\n💾 Form details saved to form_details.json")
        
        print(f"\n📋 Next steps:")
        print(f"1. Visit the form URL to test: {result['responderUri']}")
        print(f"2. Add more questions manually in Google Forms")
        print(f"3. Customize the form appearance and settings")
        print(f"4. Set up the linked Google Sheet for responses")
        print(f"5. Update your website to link to this form")
    else:
        print("\n❌ Form creation failed. Please check the error messages above.")

if __name__ == "__main__":
    import os
    main()