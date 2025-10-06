#!/usr/bin/env python3
"""
Create Google Form using service account authentication
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

def create_form_structure():
    """Define the complete form structure"""
    return {
        "info": {
            "title": "MS AI Program Application - AURNOVA University",
            "description": "Thank you for your interest in the Master of Science in Artificial Intelligence program at AURNOVA University. This application form will help us evaluate your qualifications and fit for our program.\n\nFor technical support, please contact: admissions@aurnova.edu"
        },
        "items": [
            # Section 1: Personal Information
            {
                "title": "Personal Information",
                "description": "Please provide your basic personal information.",
                "itemType": "PAGE_BREAK"
            },
            {
                "title": "Full Name",
                "description": "Enter your full legal name as it appears on official documents.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Email Address",
                "description": "We will use this email to communicate with you about your application.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Phone Number",
                "description": "Include country code if outside the United States.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Date of Birth",
                "description": "Enter your date of birth.",
                "itemType": "DATE",
                "questionItem": {
                    "question": {
                        "required": True
                    }
                }
            },
            {
                "title": "Gender",
                "description": "Please select your gender identity.",
                "itemType": "MULTIPLE_CHOICE",
                "questionItem": {
                    "question": {
                        "required": True,
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": [
                                {"value": "Male"},
                                {"value": "Female"},
                                {"value": "Non-binary"},
                                {"value": "Prefer not to say"}
                            ]
                        }
                    }
                }
            },
            {
                "title": "Mailing Address",
                "description": "Please provide your complete mailing address including street, city, state, ZIP code, and country.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            
            # Section 2: Academic Information
            {
                "title": "Academic Information",
                "description": "Please provide details about your academic background and achievements.",
                "itemType": "PAGE_BREAK"
            },
            {
                "title": "Undergraduate Degree",
                "description": "Enter your undergraduate degree (e.g., Bachelor of Science in Computer Science).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Institution",
                "description": "Name of the institution where you earned your undergraduate degree.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "GPA",
                "description": "Enter your undergraduate GPA on a 4.0 scale.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Graduation Year",
                "description": "Year you graduated or expect to graduate from your undergraduate program.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Class Rank",
                "description": "Your class rank if available (e.g., Top 10%, 15th out of 200).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Relevant Coursework",
                "description": "List courses in mathematics, computer science, statistics, AI, machine learning, etc. Include course numbers and grades if available.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            {
                "title": "Research Experience and Publications",
                "description": "Describe any research projects, publications, conference presentations, or academic work. Include details about your role, methodology, and outcomes.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            {
                "title": "Academic Honors and Awards",
                "description": "List any academic honors, scholarships, dean's list, honor societies, or other academic recognitions.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            
            # Section 3: Graduate School Preparation
            {
                "title": "Graduate School Preparation",
                "description": "Please indicate your preparation for graduate study in AI.",
                "itemType": "PAGE_BREAK"
            },
            {
                "title": "Prerequisite Coursework Completed",
                "description": "Please check all prerequisite courses you have completed. These courses are strongly recommended for success in the MS AI program.",
                "itemType": "CHECKBOX",
                "questionItem": {
                    "question": {
                        "required": True,
                        "choiceQuestion": {
                            "type": "CHECKBOX",
                            "options": [
                                {"value": "Calculus (I, II, III)"},
                                {"value": "Linear Algebra"},
                                {"value": "Statistics and Probability"},
                                {"value": "Programming (Python, Java, C++)"},
                                {"value": "Data Structures and Algorithms"},
                                {"value": "Machine Learning or AI"},
                                {"value": "Database Systems"},
                                {"value": "Computer Science Fundamentals"}
                            ]
                        }
                    }
                }
            },
            {
                "title": "Programming Languages Proficiency",
                "description": "List programming languages you're proficient in and your level of expertise (beginner, intermediate, advanced).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            {
                "title": "Technical Skills and Tools",
                "description": "List frameworks, libraries, tools, and technologies you're familiar with (e.g., TensorFlow, PyTorch, AWS, Git, etc.).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            
            # Section 4: Standardized Test Scores
            {
                "title": "Standardized Test Scores",
                "description": "Please provide your standardized test scores if available.",
                "itemType": "PAGE_BREAK"
            },
            {
                "title": "GRE Verbal Score",
                "description": "Enter your GRE Verbal Reasoning score (130-170).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "GRE Quantitative Score",
                "description": "Enter your GRE Quantitative Reasoning score (130-170).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "GRE Writing Score",
                "description": "Enter your GRE Analytical Writing score (0.0-6.0).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "TOEFL Total Score",
                "description": "Enter your TOEFL total score (0-120).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "IELTS Overall Score",
                "description": "Enter your IELTS overall band score (0.0-9.0).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "English Proficiency",
                "description": "Please select your English proficiency level.",
                "itemType": "MULTIPLE_CHOICE",
                "questionItem": {
                    "question": {
                        "required": True,
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": [
                                {"value": "Native Speaker"},
                                {"value": "TOEFL Score"},
                                {"value": "IELTS Score"},
                                {"value": "Duolingo English Test"},
                                {"value": "Other"}
                            ]
                        }
                    }
                }
            },
            {
                "title": "Test Date",
                "description": "Date of your most recent standardized test.",
                "itemType": "DATE",
                "questionItem": {
                    "question": {
                        "required": False
                    }
                }
            },
            
            # Section 5: Essays and Statements
            {
                "title": "Essays and Statements",
                "description": "Please provide thoughtful responses to the following essay questions.",
                "itemType": "PAGE_BREAK"
            },
            {
                "title": "Statement of Purpose (750-1000 words)",
                "description": "Please address your academic background, research interests, career goals, and why you chose AURNOVA University. Be specific and provide concrete examples.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            {
                "title": "Personal Statement (500-750 words)",
                "description": "Tell us about yourself beyond your academic achievements, including personal experiences, challenges overcome, and unique perspectives.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            {
                "title": "Research Interests (300-500 words)",
                "description": "Describe your research interests in AI and potential thesis topics. Be specific about current research and cite relevant papers if possible.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            {
                "title": "Career Goals (300-500 words)",
                "description": "Describe your short-term and long-term career aspirations, specific roles/companies of interest, and how this program will help.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            {
                "title": "Diversity Statement (Optional, 200-400 words)",
                "description": "How will you contribute to diversity and inclusion in our program and the broader AI community? This statement is optional but encouraged.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            
            # Section 6: Professional Experience
            {
                "title": "Professional Experience",
                "description": "Please provide information about your professional background.",
                "itemType": "PAGE_BREAK"
            },
            {
                "title": "Current Employment Status",
                "description": "Please select your current employment status.",
                "itemType": "MULTIPLE_CHOICE",
                "questionItem": {
                    "question": {
                        "required": True,
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": [
                                {"value": "Full-time employed"},
                                {"value": "Part-time employed"},
                                {"value": "Student"},
                                {"value": "Unemployed"},
                                {"value": "Other"}
                            ]
                        }
                    }
                }
            },
            {
                "title": "Work Experience",
                "description": "Describe your relevant work experience, including internships, research positions, and professional roles.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            {
                "title": "Notable Projects",
                "description": "Describe significant projects, GitHub repositories, or portfolio work.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            
            # Section 7: References
            {
                "title": "References",
                "description": "Please provide contact information for 2-3 individuals who can speak to your academic abilities, research potential, and character. At least one should be from an academic setting.",
                "itemType": "PAGE_BREAK"
            },
            {
                "title": "Reference 1 - Name",
                "description": "Full name of your first reference.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 1 - Title/Position",
                "description": "Job title or position of your first reference.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 1 - Institution/Organization",
                "description": "Institution or organization where your first reference works.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 1 - Email",
                "description": "Email address of your first reference.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 1 - Phone",
                "description": "Phone number of your first reference (optional).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 1 - Relationship",
                "description": "Your relationship to this reference (e.g., Professor, Supervisor, Mentor).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 2 - Name",
                "description": "Full name of your second reference.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 2 - Title/Position",
                "description": "Job title or position of your second reference.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 2 - Institution/Organization",
                "description": "Institution or organization where your second reference works.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 2 - Email",
                "description": "Email address of your second reference.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 2 - Phone",
                "description": "Phone number of your second reference (optional).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 2 - Relationship",
                "description": "Your relationship to this reference (e.g., Professor, Supervisor, Mentor).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 3 - Name",
                "description": "Full name of your third reference (optional).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 3 - Title/Position",
                "description": "Job title or position of your third reference (optional).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 3 - Institution/Organization",
                "description": "Institution or organization where your third reference works (optional).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 3 - Email",
                "description": "Email address of your third reference (optional).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 3 - Phone",
                "description": "Phone number of your third reference (optional).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Reference 3 - Relationship",
                "description": "Your relationship to this reference (optional).",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            
            # Section 8: Additional Information
            {
                "title": "Additional Information",
                "description": "Please provide any additional information you'd like the admissions committee to know.",
                "itemType": "PAGE_BREAK"
            },
            {
                "title": "Honors, Awards, and Recognition",
                "description": "List academic honors, scholarships, competitions, professional awards, or other achievements.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            {
                "title": "Extracurricular Activities and Leadership",
                "description": "Describe your involvement in clubs, organizations, volunteer work, or leadership roles.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            },
            {
                "title": "Additional Information",
                "description": "Any other information you'd like the admissions committee to know about your background, experiences, or circumstances.",
                "itemType": "TEXT",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {
                            "paragraph": True
                        }
                    }
                }
            }
        ],
        "settings": {
            "quizSettings": {
                "isQuiz": False
            }
        }
    }

def create_google_form():
    """Create the Google Form using service account"""
    try:
        # Authenticate
        credentials = authenticate_service_account()
        if not credentials:
            return None
        
        # Build the Forms API service
        service = build('forms', 'v1', credentials=credentials)
        
        # Get form structure
        form_structure = create_form_structure()
        
        print("🚀 Creating Google Form...")
        
        # Create the form
        form = service.forms().create(body=form_structure).execute()
        
        print(f"✅ Google Form created successfully!")
        print(f"📝 Form ID: {form['formId']}")
        print(f"🔗 Form URL: {form['responderUri']}")
        
        # Try to get the linked sheet ID
        try:
            # Get form details to find linked sheet
            form_details = service.forms().get(formId=form['formId']).execute()
            if 'linkedSheetId' in form_details:
                print(f"📊 Responses Sheet ID: {form_details['linkedSheetId']}")
                print(f"📊 Responses URL: https://docs.google.com/spreadsheets/d/{form_details['linkedSheetId']}")
        except Exception as e:
            print(f"ℹ️  Note: Could not retrieve linked sheet details: {e}")
        
        return form
        
    except HttpError as error:
        print(f"❌ Error creating form: {error}")
        if error.resp.status == 403:
            print("💡 This might be a permissions issue. The service account may need additional permissions.")
        return None
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return None

def main():
    """Main function"""
    print("🚀 Creating MS AI Application Google Form using Service Account...")
    print("=" * 70)
    
    # Check if service account key exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Service account key file not found: {SERVICE_ACCOUNT_FILE}")
        print("Please ensure the service account key file exists.")
        return
    
    print(f"✅ Using service account: msai-service-account@syzygyx-161202.iam.gserviceaccount.com")
    
    # Create the form
    form = create_google_form()
    
    if form:
        print("\n🎉 Form creation completed!")
        print(f"\n📋 Next steps:")
        print(f"1. Visit the form URL to test: {form['responderUri']}")
        print(f"2. Update your website with the form URL")
        print(f"3. Test the complete application flow")
        print(f"4. Monitor responses in the linked Google Sheet")
        
        # Save form details to file
        with open('form_details.json', 'w') as f:
            json.dump({
                'formId': form['formId'],
                'formUrl': form['responderUri'],
                'createdAt': form.get('createTime', 'Unknown')
            }, f, indent=2)
        print(f"\n💾 Form details saved to form_details.json")
    else:
        print("\n❌ Form creation failed. Please check the error messages above.")

if __name__ == "__main__":
    import os
    main()