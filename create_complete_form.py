#!/usr/bin/env python3
"""
Complete Google Form Creator for MS AI Application
This script will work once the Google Forms API 500 error is resolved
"""

import json
import os
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Use the new service account
SERVICE_ACCOUNT_FILE = 'msai-forms-creator-key.json'
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

def create_complete_form():
    """Create the complete MS AI application form"""
    try:
        # Authenticate
        credentials = authenticate_service_account()
        if not credentials:
            return None
        
        # Build the Forms API service
        service = build('forms', 'v1', credentials=credentials)
        
        print("🚀 Creating Complete MS AI Application Google Form...")
        
        # Step 1: Create the form with title only
        form_info = {
            "info": {
                "title": "MS AI Program Application - AURNOVA University"
            }
        }
        
        form = service.forms().create(body=form_info).execute()
        form_id = form['formId']
        
        print(f"✅ Form created with ID: {form_id}")
        print(f"🔗 Form URL: {form['responderUri']}")
        
        # Step 2: Update description
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
        
        # Step 3: Add all questions in batches
        print("📝 Adding form questions...")
        
        # Define all questions
        all_questions = [
            # Personal Information Section
            {
                "title": "Personal Information",
                "description": "Please provide your basic personal information.",
                "type": "page_break"
            },
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
            
            # Academic Information Section
            {
                "title": "Academic Information",
                "description": "Please provide details about your academic background and achievements.",
                "type": "page_break"
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
            },
            {
                "title": "Class Rank",
                "description": "Your class rank if available (e.g., Top 10%, 15th out of 200).",
                "type": "text",
                "required": False
            },
            {
                "title": "Relevant Coursework",
                "description": "List courses in mathematics, computer science, statistics, AI, machine learning, etc. Include course numbers and grades if available.",
                "type": "text",
                "required": True,
                "paragraph": True
            },
            {
                "title": "Research Experience and Publications",
                "description": "Describe any research projects, publications, conference presentations, or academic work. Include details about your role, methodology, and outcomes.",
                "type": "text",
                "required": True,
                "paragraph": True
            },
            {
                "title": "Academic Honors and Awards",
                "description": "List any academic honors, scholarships, dean's list, honor societies, or other academic recognitions.",
                "type": "text",
                "required": False,
                "paragraph": True
            },
            
            # Graduate School Preparation Section
            {
                "title": "Graduate School Preparation",
                "description": "Please indicate your preparation for graduate study in AI.",
                "type": "page_break"
            },
            {
                "title": "Prerequisite Coursework Completed",
                "description": "Please check all prerequisite courses you have completed. These courses are strongly recommended for success in the MS AI program.",
                "type": "checkbox",
                "required": True,
                "options": [
                    "Calculus (I, II, III)",
                    "Linear Algebra",
                    "Statistics and Probability",
                    "Programming (Python, Java, C++)",
                    "Data Structures and Algorithms",
                    "Machine Learning or AI",
                    "Database Systems",
                    "Computer Science Fundamentals"
                ]
            },
            {
                "title": "Programming Languages Proficiency",
                "description": "List programming languages you're proficient in and your level of expertise (beginner, intermediate, advanced).",
                "type": "text",
                "required": True,
                "paragraph": True
            },
            {
                "title": "Technical Skills and Tools",
                "description": "List frameworks, libraries, tools, and technologies you're familiar with (e.g., TensorFlow, PyTorch, AWS, Git, etc.).",
                "type": "text",
                "required": True,
                "paragraph": True
            },
            
            # Standardized Test Scores Section
            {
                "title": "Standardized Test Scores",
                "description": "Please provide your standardized test scores if available.",
                "type": "page_break"
            },
            {
                "title": "GRE Verbal Score",
                "description": "Enter your GRE Verbal Reasoning score (130-170).",
                "type": "text",
                "required": False
            },
            {
                "title": "GRE Quantitative Score",
                "description": "Enter your GRE Quantitative Reasoning score (130-170).",
                "type": "text",
                "required": False
            },
            {
                "title": "GRE Writing Score",
                "description": "Enter your GRE Analytical Writing score (0.0-6.0).",
                "type": "text",
                "required": False
            },
            {
                "title": "TOEFL Total Score",
                "description": "Enter your TOEFL total score (0-120).",
                "type": "text",
                "required": False
            },
            {
                "title": "IELTS Overall Score",
                "description": "Enter your IELTS overall band score (0.0-9.0).",
                "type": "text",
                "required": False
            },
            {
                "title": "English Proficiency",
                "description": "Please select your English proficiency level.",
                "type": "multiple_choice",
                "required": True,
                "options": ["Native Speaker", "TOEFL Score", "IELTS Score", "Duolingo English Test", "Other"]
            },
            {
                "title": "Test Date",
                "description": "Date of your most recent standardized test.",
                "type": "date",
                "required": False
            },
            
            # Essays Section
            {
                "title": "Essays and Statements",
                "description": "Please provide thoughtful responses to the following essay questions.",
                "type": "page_break"
            },
            {
                "title": "Statement of Purpose (750-1000 words)",
                "description": "Please address your academic background, research interests, career goals, and why you chose AURNOVA University. Be specific and provide concrete examples.",
                "type": "text",
                "required": True,
                "paragraph": True
            },
            {
                "title": "Personal Statement (500-750 words)",
                "description": "Tell us about yourself beyond your academic achievements, including personal experiences, challenges overcome, and unique perspectives.",
                "type": "text",
                "required": True,
                "paragraph": True
            },
            {
                "title": "Research Interests and Potential Thesis Topics (300-500 words)",
                "description": "Describe your research interests in AI and potential thesis topics. Be specific about current research and cite relevant papers if possible.",
                "type": "text",
                "required": True,
                "paragraph": True
            },
            {
                "title": "Career Goals and Professional Development (300-500 words)",
                "description": "Describe your short-term and long-term career aspirations, specific roles/companies of interest, and how this program will help.",
                "type": "text",
                "required": True,
                "paragraph": True
            },
            {
                "title": "Diversity and Inclusion Statement (Optional, 200-400 words)",
                "description": "How will you contribute to diversity and inclusion in our program and the broader AI community? This statement is optional but encouraged.",
                "type": "text",
                "required": False,
                "paragraph": True
            },
            
            # Professional Experience Section
            {
                "title": "Professional Experience",
                "description": "Please provide information about your professional background.",
                "type": "page_break"
            },
            {
                "title": "Current Employment Status",
                "description": "Please select your current employment status.",
                "type": "multiple_choice",
                "required": True,
                "options": ["Full-time employed", "Part-time employed", "Student", "Unemployed", "Other"]
            },
            {
                "title": "Work Experience",
                "description": "Describe your relevant work experience, including internships, research positions, and professional roles.",
                "type": "text",
                "required": True,
                "paragraph": True
            },
            {
                "title": "Notable Projects",
                "description": "Describe significant projects, GitHub repositories, or portfolio work.",
                "type": "text",
                "required": False,
                "paragraph": True
            },
            
            # References Section
            {
                "title": "References",
                "description": "Please provide contact information for 2-3 individuals who can speak to your academic abilities, research potential, and character. At least one should be from an academic setting.",
                "type": "page_break"
            },
            # Reference 1
            {
                "title": "Reference 1 - Name",
                "description": "Full name of your first reference.",
                "type": "text",
                "required": True
            },
            {
                "title": "Reference 1 - Title/Position",
                "description": "Job title or position of your first reference.",
                "type": "text",
                "required": True
            },
            {
                "title": "Reference 1 - Institution/Organization",
                "description": "Institution or organization where your first reference works.",
                "type": "text",
                "required": True
            },
            {
                "title": "Reference 1 - Email",
                "description": "Email address of your first reference.",
                "type": "text",
                "required": True
            },
            {
                "title": "Reference 1 - Phone",
                "description": "Phone number of your first reference (optional).",
                "type": "text",
                "required": False
            },
            {
                "title": "Reference 1 - Relationship",
                "description": "Your relationship to this reference (e.g., Professor, Supervisor, Mentor).",
                "type": "text",
                "required": True
            },
            # Reference 2
            {
                "title": "Reference 2 - Name",
                "description": "Full name of your second reference.",
                "type": "text",
                "required": True
            },
            {
                "title": "Reference 2 - Title/Position",
                "description": "Job title or position of your second reference.",
                "type": "text",
                "required": True
            },
            {
                "title": "Reference 2 - Institution/Organization",
                "description": "Institution or organization where your second reference works.",
                "type": "text",
                "required": True
            },
            {
                "title": "Reference 2 - Email",
                "description": "Email address of your second reference.",
                "type": "text",
                "required": True
            },
            {
                "title": "Reference 2 - Phone",
                "description": "Phone number of your second reference (optional).",
                "type": "text",
                "required": False
            },
            {
                "title": "Reference 2 - Relationship",
                "description": "Your relationship to this reference (e.g., Professor, Supervisor, Mentor).",
                "type": "text",
                "required": True
            },
            # Reference 3 (Optional)
            {
                "title": "Reference 3 - Name",
                "description": "Full name of your third reference (optional).",
                "type": "text",
                "required": False
            },
            {
                "title": "Reference 3 - Title/Position",
                "description": "Job title or position of your third reference (optional).",
                "type": "text",
                "required": False
            },
            {
                "title": "Reference 3 - Institution/Organization",
                "description": "Institution or organization where your third reference works (optional).",
                "type": "text",
                "required": False
            },
            {
                "title": "Reference 3 - Email",
                "description": "Email address of your third reference (optional).",
                "type": "text",
                "required": False
            },
            {
                "title": "Reference 3 - Phone",
                "description": "Phone number of your third reference (optional).",
                "type": "text",
                "required": False
            },
            {
                "title": "Reference 3 - Relationship",
                "description": "Your relationship to this reference (optional).",
                "type": "text",
                "required": False
            },
            
            # Additional Information Section
            {
                "title": "Additional Information",
                "description": "Please provide any additional information you'd like the admissions committee to know.",
                "type": "page_break"
            },
            {
                "title": "Honors, Awards, and Recognition",
                "description": "List academic honors, scholarships, competitions, professional awards, or other achievements.",
                "type": "text",
                "required": False,
                "paragraph": True
            },
            {
                "title": "Extracurricular Activities and Leadership",
                "description": "Describe your involvement in clubs, organizations, volunteer work, or leadership roles.",
                "type": "text",
                "required": False,
                "paragraph": True
            },
            {
                "title": "Additional Information",
                "description": "Any other information you'd like the admissions committee to know about your background, experiences, or circumstances.",
                "type": "text",
                "required": False,
                "paragraph": True
            }
        ]
        
        # Add questions in batches
        batch_size = 10
        for i in range(0, len(all_questions), batch_size):
            batch_questions = all_questions[i:i + batch_size]
            batch_requests = []
            
            for j, question in enumerate(batch_questions):
                request = create_question_request(question, i + j)
                if request:
                    batch_requests.append(request)
            
            if batch_requests:
                try:
                    service.forms().batchUpdate(formId=form_id, body={"requests": batch_requests}).execute()
                    print(f"✅ Added questions {i+1}-{min(i+batch_size, len(all_questions))}")
                except Exception as e:
                    print(f"❌ Error adding questions {i+1}-{min(i+batch_size, len(all_questions))}: {e}")
                    # Continue with next batch
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
        return None
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return None

def create_question_request(question, index):
    """Create a question request for the Forms API"""
    try:
        if question['type'] == 'page_break':
            return {
                "createItem": {
                    "item": {
                        "title": question['title'],
                        "description": question['description'],
                        "pageBreakItem": {}
                    },
                    "location": {"index": index}
                }
            }
        elif question['type'] == 'text':
            return {
                "createItem": {
                    "item": {
                        "title": question['title'],
                        "description": question['description'],
                        "questionItem": {
                            "question": {
                                "required": question.get('required', False),
                                "textQuestion": {
                                    "paragraph": question.get('paragraph', False)
                                }
                            }
                        }
                    },
                    "location": {"index": index}
                }
            }
        elif question['type'] == 'date':
            return {
                "createItem": {
                    "item": {
                        "title": question['title'],
                        "description": question['description'],
                        "questionItem": {
                            "question": {
                                "required": question.get('required', False),
                                "dateQuestion": {}
                            }
                        }
                    },
                    "location": {"index": index}
                }
            }
        elif question['type'] == 'multiple_choice':
            return {
                "createItem": {
                    "item": {
                        "title": question['title'],
                        "description": question['description'],
                        "questionItem": {
                            "question": {
                                "required": question.get('required', False),
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [{"value": opt} for opt in question.get('options', [])]
                                }
                            }
                        }
                    },
                    "location": {"index": index}
                }
            }
        elif question['type'] == 'checkbox':
            return {
                "createItem": {
                    "item": {
                        "title": question['title'],
                        "description": question['description'],
                        "questionItem": {
                            "question": {
                                "required": question.get('required', False),
                                "choiceQuestion": {
                                    "type": "CHECKBOX",
                                    "options": [{"value": opt} for opt in question.get('options', [])]
                                }
                            }
                        }
                    },
                    "location": {"index": index}
                }
            }
    except Exception as e:
        print(f"❌ Error creating question request for '{question['title']}': {e}")
        return None

def main():
    """Main function"""
    print("🚀 Complete MS AI Application Google Form Creator")
    print("=" * 60)
    
    # Check if service account key exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Service account key file not found: {SERVICE_ACCOUNT_FILE}")
        return
    
    # Create the form
    result = create_complete_form()
    
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
                'status': 'Complete Google Form created successfully'
            }, f, indent=2)
        print(f"\n💾 Form details saved to form_details.json")
        
        print(f"\n📋 Next steps:")
        print(f"1. Visit the form URL to test: {result['responderUri']}")
        print(f"2. Customize the form appearance and settings")
        print(f"3. Set up the linked Google Sheet for responses")
        print(f"4. Update your website to link to this form")
        print(f"5. Test the complete application flow")
        
    else:
        print("\n❌ Form creation failed. This is likely due to the Google Forms API 500 error.")
        print("\n🔧 Troubleshooting:")
        print("1. Wait a few hours and try again (API issues often resolve themselves)")
        print("2. Check Google Cloud Status page for any ongoing issues")
        print("3. Try creating a form manually in Google Forms to test if the API works")
        print("4. Contact Google support if the issue persists")

if __name__ == "__main__":
    main()