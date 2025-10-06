#!/usr/bin/env python3
"""
Create Google Form using gcloud authentication - Simplified approach
"""

import subprocess
import json
import os

def run_gcloud_command(command):
    """Run a gcloud command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception running command: {e}")
        return None

def get_access_token():
    """Get access token using gcloud"""
    return run_gcloud_command("gcloud auth application-default print-access-token")

def create_form_with_curl():
    """Create Google Form using curl with gcloud token"""
    
    # Get access token
    print("🔑 Getting access token...")
    token = get_access_token()
    if not token:
        print("❌ Failed to get access token")
        return None
    
    print("✅ Access token obtained")
    
    # Form data
    form_data = {
        "info": {
            "title": "MS AI Program Application - AURNOVA University",
            "description": "Thank you for your interest in the Master of Science in Artificial Intelligence program at AURNOVA University. This application form will help us evaluate your qualifications and fit for our program."
        },
        "items": [
            # Personal Information Section
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
            
            # Academic Information Section
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
                "title": "Relevant Coursework",
                "description": "List courses in mathematics, computer science, statistics, AI, machine learning, etc.",
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
                "description": "Describe any research projects, publications, conference presentations, or academic work.",
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
            
            # Prerequisites Section
            {
                "title": "Prerequisite Coursework",
                "description": "Please check all prerequisite courses you have completed.",
                "itemType": "PAGE_BREAK"
            },
            {
                "title": "Prerequisite Coursework Completed",
                "description": "These courses are strongly recommended for success in the MS AI program.",
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
                "description": "List programming languages you're proficient in and your level of expertise.",
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
                "description": "List frameworks, libraries, tools, and technologies you're familiar with.",
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
            
            # Test Scores Section
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
            
            # Essays Section
            {
                "title": "Essays and Statements",
                "description": "Please provide thoughtful responses to the following essay questions.",
                "itemType": "PAGE_BREAK"
            },
            {
                "title": "Statement of Purpose (750-1000 words)",
                "description": "Please address your academic background, research interests, career goals, and why you chose AURNOVA University.",
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
                "description": "Tell us about yourself beyond your academic achievements, including personal experiences and unique perspectives.",
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
                "description": "Describe your research interests in AI and potential thesis topics.",
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
                "description": "Describe your short-term and long-term career aspirations.",
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
            
            # References Section
            {
                "title": "References",
                "description": "Please provide contact information for 2-3 individuals who can speak to your abilities.",
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
                "title": "Reference 1 - Institution",
                "description": "Institution where your first reference works.",
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
                "title": "Reference 2 - Institution",
                "description": "Institution where your second reference works.",
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
            
            # Additional Information
            {
                "title": "Additional Information",
                "description": "Please provide any additional information you'd like the admissions committee to know.",
                "itemType": "PAGE_BREAK"
            },
            {
                "title": "Work Experience",
                "description": "Describe your relevant work experience, including internships and professional roles.",
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
                "title": "Honors and Awards",
                "description": "List any academic honors, scholarships, or other achievements.",
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
                "description": "Any other information you'd like the admissions committee to know.",
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
    
    # Save form data to a file
    with open('form_data.json', 'w') as f:
        json.dump(form_data, f, indent=2)
    
    print("✅ Form data prepared and saved to form_data.json")
    
    # Create curl command
    curl_command = f'''curl -X POST \\
    -H "Authorization: Bearer {token}" \\
    -H "Content-Type: application/json" \\
    -d @form_data.json \\
    "https://forms.googleapis.com/v1/forms"'''
    
    print("🚀 Creating Google Form...")
    print("Running curl command...")
    
    # Execute curl command
    result = run_gcloud_command(curl_command)
    
    if result:
        try:
            form_response = json.loads(result)
            if 'formId' in form_response:
                print(f"✅ Google Form created successfully!")
                print(f"📝 Form ID: {form_response['formId']}")
                print(f"🔗 Form URL: {form_response.get('responderUri', 'N/A')}")
                return form_response
            else:
                print(f"❌ Unexpected response: {result}")
                return None
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response: {result}")
            return None
    else:
        print("❌ Failed to create form")
        return None

def main():
    """Main function"""
    print("🚀 Creating MS AI Application Google Form using gcloud...")
    print("=" * 60)
    
    # Check if we're authenticated
    auth_result = run_gcloud_command("gcloud auth list --filter=status:ACTIVE --format='value(account)'")
    if not auth_result:
        print("❌ No active gcloud authentication found!")
        print("Please run: gcloud auth login")
        return
    
    print(f"✅ Authenticated as: {auth_result}")
    
    # Create the form
    form = create_form_with_curl()
    
    if form:
        print("\n🎉 Form creation completed!")
        print(f"\n📋 Next steps:")
        print(f"1. Visit the form URL to test the form")
        print(f"2. Customize the form appearance and settings")
        print(f"3. Set up the linked Google Sheet for responses")
        print(f"4. Update your website to link to this form")
        print(f"5. Test the complete application flow")
    else:
        print("\n❌ Form creation failed. Please check the error messages above.")

if __name__ == "__main__":
    main()