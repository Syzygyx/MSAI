#!/usr/bin/env python3
"""
Google Forms Creator for MS AI Application
This script creates a comprehensive Google Form for the MS AI program application.
"""

import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

# Scopes required for Google Forms API
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/drive.file'
]

# Form configuration
FORM_TITLE = "MS AI Program Application - AURNOVA University"
FORM_DESCRIPTION = """
Thank you for your interest in the Master of Science in Artificial Intelligence program at AURNOVA University.

This application form will help us evaluate your qualifications and fit for our program. Please complete all required sections carefully.

For technical support, please contact: admissions@aurnova.edu
"""

def authenticate():
    """Authenticate with Google APIs"""
    creds = None
    
    # Check if token file exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials, get them
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def create_form_structure():
    """Define the complete form structure"""
    return {
        "info": {
            "title": FORM_TITLE,
            "description": FORM_DESCRIPTION
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
                "description": """Please address the following in your statement of purpose:

1. Your academic background and how it has prepared you for graduate study in AI
2. Specific research interests within AI and why they interest you
3. Career goals and how this MS AI program will help you achieve them
4. Why you chose AURNOVA University and this particular program
5. Any relevant research experience, projects, or publications
6. How you plan to contribute to the AI community

Please be specific and provide concrete examples. Avoid generic statements.""",
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
                "description": """Tell us about yourself beyond your academic achievements:

1. Personal experiences that have shaped your interest in AI
2. Challenges you've overcome and how they've prepared you for graduate study
3. Leadership experiences and how you've made a positive impact
4. Unique perspectives or experiences you bring to the program
5. How you handle failure and learn from setbacks
6. Your approach to collaboration and teamwork

Be authentic and specific. This is your opportunity to show who you are as a person.""",
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
                "title": "Research Interests and Potential Thesis Topics (300-500 words)",
                "description": """Describe your research interests in detail:

1. Specific AI subfields that interest you (e.g., computer vision, NLP, robotics, etc.)
2. Current research trends or problems you find compelling
3. Potential thesis topics you might explore
4. How your background has prepared you for research in these areas
5. Any specific faculty members whose research aligns with your interests
6. How your research interests connect to your career goals

Be specific about current research and cite relevant papers if possible.""",
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
                "title": "Career Goals and Professional Development (300-500 words)",
                "description": """Describe your career aspirations:

1. Short-term goals (1-3 years after graduation)
2. Long-term career vision (5-10 years)
3. Specific roles or companies you're interested in
4. How this MS AI program will help you achieve these goals
5. Skills you hope to develop during the program
6. How you plan to stay current with AI developments
7. Your vision for contributing to the AI field

Be specific about industries, roles, and the impact you want to make.""",
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
                "title": "Diversity and Inclusion Statement (Optional, 200-400 words)",
                "description": """How will you contribute to diversity and inclusion in our program and the broader AI community?

Consider addressing:
- Your unique background and perspectives
- Experiences with diverse communities
- How you plan to promote inclusivity in AI
- Your commitment to ethical AI development
- Any initiatives you've led or participated in related to diversity

This statement is optional but encouraged.""",
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
    """Create the Google Form"""
    try:
        # Authenticate
        creds = authenticate()
        
        # Build the Forms API service
        service = build('forms', 'v1', credentials=creds)
        
        # Get form structure
        form_structure = create_form_structure()
        
        # Create the form
        form = service.forms().create(body=form_structure).execute()
        
        print(f"✅ Google Form created successfully!")
        print(f"📝 Form ID: {form['formId']}")
        print(f"🔗 Form URL: {form['responderUri']}")
        print(f"📊 Responses URL: {form['linkedSheetId']}")
        
        return form
        
    except HttpError as error:
        print(f"❌ Error creating form: {error}")
        return None
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return None

def main():
    """Main function"""
    print("🚀 Creating MS AI Application Google Form...")
    print("=" * 50)
    
    # Check if credentials file exists
    if not os.path.exists('credentials.json'):
        print("❌ Error: credentials.json file not found!")
        print("\n📋 To set up Google API credentials:")
        print("1. Go to https://console.developers.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable Google Forms API and Google Drive API")
        print("4. Create credentials (OAuth 2.0 Client ID)")
        print("5. Download the JSON file and save as 'credentials.json'")
        print("6. Run this script again")
        return
    
    # Create the form
    form = create_google_form()
    
    if form:
        print("\n🎉 Form creation completed!")
        print(f"\n📋 Next steps:")
        print(f"1. Visit the form URL to test: {form['responderUri']}")
        print(f"2. Customize the form appearance and settings")
        print(f"3. Set up the linked Google Sheet for responses")
        print(f"4. Update your website to link to this form")
        print(f"5. Test the complete application flow")

if __name__ == "__main__":
    main()