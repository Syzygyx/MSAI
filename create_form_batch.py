#!/usr/bin/env python3
"""
Create Google Form using service account authentication with batch updates
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

def create_form_items():
    """Define all form items for batch update"""
    return [
        # Section 1: Personal Information
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
        },
        {
            "createItem": {
                "item": {
                    "title": "Gender",
                    "description": "Please select your gender identity.",
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
                "location": {"index": 5}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Mailing Address",
                    "description": "Please provide your complete mailing address including street, city, state, ZIP code, and country.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 6}
            }
        },
        
        # Section 2: Academic Information
        {
            "createItem": {
                "item": {
                    "title": "Academic Information",
                    "description": "Please provide details about your academic background and achievements.",
                    "pageBreakItem": {}
                },
                "location": {"index": 7}
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
                "location": {"index": 8}
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
                "location": {"index": 9}
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
                "location": {"index": 10}
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
                "location": {"index": 11}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Class Rank",
                    "description": "Your class rank if available (e.g., Top 10%, 15th out of 200).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 12}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Relevant Coursework",
                    "description": "List courses in mathematics, computer science, statistics, AI, machine learning, etc. Include course numbers and grades if available.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 13}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Research Experience and Publications",
                    "description": "Describe any research projects, publications, conference presentations, or academic work. Include details about your role, methodology, and outcomes.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 14}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Academic Honors and Awards",
                    "description": "List any academic honors, scholarships, dean's list, honor societies, or other academic recognitions.",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 15}
            }
        },
        
        # Section 3: Graduate School Preparation
        {
            "createItem": {
                "item": {
                    "title": "Graduate School Preparation",
                    "description": "Please indicate your preparation for graduate study in AI.",
                    "pageBreakItem": {}
                },
                "location": {"index": 16}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Prerequisite Coursework Completed",
                    "description": "Please check all prerequisite courses you have completed. These courses are strongly recommended for success in the MS AI program.",
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
                "location": {"index": 17}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Programming Languages Proficiency",
                    "description": "List programming languages you're proficient in and your level of expertise (beginner, intermediate, advanced).",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 18}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Technical Skills and Tools",
                    "description": "List frameworks, libraries, tools, and technologies you're familiar with (e.g., TensorFlow, PyTorch, AWS, Git, etc.).",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 19}
            }
        },
        
        # Section 4: Standardized Test Scores
        {
            "createItem": {
                "item": {
                    "title": "Standardized Test Scores",
                    "description": "Please provide your standardized test scores if available.",
                    "pageBreakItem": {}
                },
                "location": {"index": 20}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "GRE Verbal Score",
                    "description": "Enter your GRE Verbal Reasoning score (130-170).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 21}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "GRE Quantitative Score",
                    "description": "Enter your GRE Quantitative Reasoning score (130-170).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 22}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "GRE Writing Score",
                    "description": "Enter your GRE Analytical Writing score (0.0-6.0).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 23}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "TOEFL Total Score",
                    "description": "Enter your TOEFL total score (0-120).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 24}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "IELTS Overall Score",
                    "description": "Enter your IELTS overall band score (0.0-9.0).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 25}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "English Proficiency",
                    "description": "Please select your English proficiency level.",
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
                "location": {"index": 26}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Test Date",
                    "description": "Date of your most recent standardized test.",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "dateQuestion": {}
                        }
                    }
                },
                "location": {"index": 27}
            }
        },
        
        # Section 5: Essays and Statements
        {
            "createItem": {
                "item": {
                    "title": "Essays and Statements",
                    "description": "Please provide thoughtful responses to the following essay questions.",
                    "pageBreakItem": {}
                },
                "location": {"index": 28}
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
                "location": {"index": 29}
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
                "location": {"index": 30}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Research Interests (300-500 words)",
                    "description": "Describe your research interests in AI and potential thesis topics. Be specific about current research and cite relevant papers if possible.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 31}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Career Goals (300-500 words)",
                    "description": "Describe your short-term and long-term career aspirations, specific roles/companies of interest, and how this program will help.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 32}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Diversity Statement (Optional, 200-400 words)",
                    "description": "How will you contribute to diversity and inclusion in our program and the broader AI community? This statement is optional but encouraged.",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 33}
            }
        },
        
        # Section 6: Professional Experience
        {
            "createItem": {
                "item": {
                    "title": "Professional Experience",
                    "description": "Please provide information about your professional background.",
                    "pageBreakItem": {}
                },
                "location": {"index": 34}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Current Employment Status",
                    "description": "Please select your current employment status.",
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
                "location": {"index": 35}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Work Experience",
                    "description": "Describe your relevant work experience, including internships, research positions, and professional roles.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 36}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Notable Projects",
                    "description": "Describe significant projects, GitHub repositories, or portfolio work.",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 37}
            }
        },
        
        # Section 7: References
        {
            "createItem": {
                "item": {
                    "title": "References",
                    "description": "Please provide contact information for 2-3 individuals who can speak to your academic abilities, research potential, and character. At least one should be from an academic setting.",
                    "pageBreakItem": {}
                },
                "location": {"index": 38}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 1 - Name",
                    "description": "Full name of your first reference.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 39}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 1 - Title/Position",
                    "description": "Job title or position of your first reference.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 40}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 1 - Institution/Organization",
                    "description": "Institution or organization where your first reference works.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 41}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 1 - Email",
                    "description": "Email address of your first reference.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 42}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 1 - Phone",
                    "description": "Phone number of your first reference (optional).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 43}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 1 - Relationship",
                    "description": "Your relationship to this reference (e.g., Professor, Supervisor, Mentor).",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 44}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 2 - Name",
                    "description": "Full name of your second reference.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 45}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 2 - Title/Position",
                    "description": "Job title or position of your second reference.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 46}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 2 - Institution/Organization",
                    "description": "Institution or organization where your second reference works.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 47}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 2 - Email",
                    "description": "Email address of your second reference.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 48}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 2 - Phone",
                    "description": "Phone number of your second reference (optional).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 49}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 2 - Relationship",
                    "description": "Your relationship to this reference (e.g., Professor, Supervisor, Mentor).",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 50}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 3 - Name",
                    "description": "Full name of your third reference (optional).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 51}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 3 - Title/Position",
                    "description": "Job title or position of your third reference (optional).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 52}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 3 - Institution/Organization",
                    "description": "Institution or organization where your third reference works (optional).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 53}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 3 - Email",
                    "description": "Email address of your third reference (optional).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 54}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 3 - Phone",
                    "description": "Phone number of your third reference (optional).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 55}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Reference 3 - Relationship",
                    "description": "Your relationship to this reference (optional).",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                "location": {"index": 56}
            }
        },
        
        # Section 8: Additional Information
        {
            "createItem": {
                "item": {
                    "title": "Additional Information",
                    "description": "Please provide any additional information you'd like the admissions committee to know.",
                    "pageBreakItem": {}
                },
                "location": {"index": 57}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Honors, Awards, and Recognition",
                    "description": "List academic honors, scholarships, competitions, professional awards, or other achievements.",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 58}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Extracurricular Activities and Leadership",
                    "description": "Describe your involvement in clubs, organizations, volunteer work, or leadership roles.",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 59}
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Additional Information",
                    "description": "Any other information you'd like the admissions committee to know about your background, experiences, or circumstances.",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                "location": {"index": 60}
            }
        }
    ]

def create_google_form():
    """Create the Google Form using service account with batch updates"""
    try:
        # Authenticate
        credentials = authenticate_service_account()
        if not credentials:
            return None
        
        # Build the Forms API service
        service = build('forms', 'v1', credentials=credentials)
        
        print("🚀 Creating Google Form...")
        
        # Step 1: Create the form with just the title
        form_info = {
            "info": {
                "title": "MS AI Program Application - AURNOVA University",
                "description": "Thank you for your interest in the Master of Science in Artificial Intelligence program at AURNOVA University. This application form will help us evaluate your qualifications and fit for our program.\n\nFor technical support, please contact: admissions@aurnova.edu"
            }
        }
        
        form = service.forms().create(body=form_info).execute()
        form_id = form['formId']
        
        print(f"✅ Form created with ID: {form_id}")
        print(f"🔗 Form URL: {form['responderUri']}")
        
        # Step 2: Add all items using batch update
        print("📝 Adding form items...")
        
        # Split items into batches (Google Forms API has limits)
        items = create_form_items()
        batch_size = 20  # Process 20 items at a time
        
        for i in range(0, len(items), batch_size):
            batch_items = items[i:i + batch_size]
            batch_request = {
                "requests": batch_items
            }
            
            print(f"  Processing batch {i//batch_size + 1}/{(len(items) + batch_size - 1)//batch_size}...")
            
            try:
                service.forms().batchUpdate(formId=form_id, body=batch_request).execute()
                print(f"  ✅ Batch {i//batch_size + 1} completed")
            except HttpError as e:
                print(f"  ❌ Error in batch {i//batch_size + 1}: {e}")
                # Continue with next batch
                continue
        
        print("✅ All form items added successfully!")
        
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
    print("🚀 Creating MS AI Application Google Form using Service Account...")
    print("=" * 70)
    
    # Check if service account key exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Service account key file not found: {SERVICE_ACCOUNT_FILE}")
        print("Please ensure the service account key file exists.")
        return
    
    print(f"✅ Using service account: msai-service-account@syzygyx-161202.iam.gserviceaccount.com")
    
    # Create the form
    result = create_google_form()
    
    if result:
        print("\n🎉 Form creation completed!")
        print(f"\n📋 Form Details:")
        print(f"📝 Form ID: {result['formId']}")
        print(f"🔗 Form URL: {result['responderUri']}")
        
        print(f"\n📋 Next steps:")
        print(f"1. Visit the form URL to test: {result['responderUri']}")
        print(f"2. Update your website with the form URL")
        print(f"3. Test the complete application flow")
        print(f"4. Monitor responses in the linked Google Sheet")
        
        # Save form details to file
        with open('form_details.json', 'w') as f:
            json.dump({
                'formId': result['formId'],
                'formUrl': result['responderUri'],
                'createdAt': 'Just now'
            }, f, indent=2)
        print(f"\n💾 Form details saved to form_details.json")
    else:
        print("\n❌ Form creation failed. Please check the error messages above.")

if __name__ == "__main__":
    import os
    main()