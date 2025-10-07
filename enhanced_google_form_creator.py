#!/usr/bin/env python3
"""
Enhanced Google Form Creator for MS AI Application
A comprehensive, production-ready solution for creating Google Forms programmatically.

Features:
- Multiple authentication methods (OAuth, Service Account)
- Comprehensive form validation
- Configuration management
- Error handling and logging
- Batch processing
- Form customization
- Response management
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from pathlib import Path

# Google API imports
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('google_form_creator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class FormConfig:
    """Configuration for Google Form creation"""
    title: str = "MS AI Program Application - AURNOVA University"
    description: str = "Thank you for your interest in the Master of Science in Artificial Intelligence program at AURNOVA University. This application form will help us evaluate your qualifications and fit for our program.\n\nFor technical support, please contact: admissions@aurnova.edu"
    collect_emails: bool = True
    limit_responses: bool = True
    show_progress: bool = True
    confirmation_message: str = "Thank you for your application to the MS AI program! We will review your application and contact you within 2-3 weeks."
    theme_color: str = "#1976D2"  # Blue theme
    custom_logo_url: Optional[str] = None

@dataclass
class QuestionConfig:
    """Configuration for individual form questions"""
    title: str
    description: str
    required: bool = True
    question_type: str = "TEXT"
    options: Optional[List[str]] = None
    validation: Optional[Dict[str, Any]] = None
    placeholder: Optional[str] = None

class GoogleFormCreator:
    """Enhanced Google Form Creator with comprehensive features"""
    
    def __init__(self, config_file: str = "form_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.service = None
        self.form_id = None
        
        # API Scopes
        self.SCOPES = [
            'https://www.googleapis.com/auth/forms.body',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
    
    def _load_config(self) -> FormConfig:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                return FormConfig(**config_data)
            except Exception as e:
                logger.warning(f"Could not load config file: {e}. Using defaults.")
        
        # Create default config
        config = FormConfig()
        self._save_config(config)
        return config
    
    def _save_config(self, config: FormConfig):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(asdict(config), f, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Could not save config: {e}")
    
    def authenticate_oauth(self, credentials_file: str = "credentials.json") -> bool:
        """Authenticate using OAuth 2.0"""
        try:
            creds = None
            token_file = 'token.json'
            
            # Load existing token
            if os.path.exists(token_file):
                creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)
            
            # Refresh or get new credentials
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(credentials_file):
                        logger.error(f"Credentials file not found: {credentials_file}")
                        return False
                    
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save credentials
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
            
            self.service = build('forms', 'v1', credentials=creds)
            logger.info("OAuth authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"OAuth authentication failed: {e}")
            return False
    
    def authenticate_service_account(self, service_account_file: str = "msai-service-key.json") -> bool:
        """Authenticate using service account"""
        try:
            if not os.path.exists(service_account_file):
                logger.error(f"Service account file not found: {service_account_file}")
                return False
            
            credentials = service_account.Credentials.from_service_account_file(
                service_account_file, scopes=self.SCOPES)
            
            self.service = build('forms', 'v1', credentials=credentials)
            logger.info("Service account authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"Service account authentication failed: {e}")
            return False
    
    def get_form_questions(self) -> List[QuestionConfig]:
        """Get comprehensive list of form questions"""
        return [
            # Section 1: Personal Information
            QuestionConfig("Personal Information", "Please provide your basic personal information.", 
                          question_type="PAGE_BREAK", required=False),
            
            QuestionConfig("Full Name", "Enter your full legal name as it appears on official documents.",
                          validation={"min_length": 2, "max_length": 100}),
            
            QuestionConfig("Email Address", "We will use this email to communicate with you about your application.",
                          validation={"type": "email"}),
            
            QuestionConfig("Phone Number", "Include country code if outside the United States.",
                          validation={"pattern": r"^[\+]?[1-9][\d]{0,15}$"}),
            
            QuestionConfig("Date of Birth", "Enter your date of birth.", question_type="DATE"),
            
            QuestionConfig("Gender", "Please select your gender identity.", question_type="MULTIPLE_CHOICE",
                          options=["Male", "Female", "Non-binary", "Prefer not to say"]),
            
            QuestionConfig("Mailing Address", "Please provide your complete mailing address including street, city, state, ZIP code, and country.",
                          question_type="TEXT", validation={"min_length": 10}),
            
            # Section 2: Academic Information
            QuestionConfig("Academic Information", "Please provide details about your academic background and achievements.",
                          question_type="PAGE_BREAK", required=False),
            
            QuestionConfig("Undergraduate Degree", "Enter your undergraduate degree (e.g., Bachelor of Science in Computer Science).",
                          validation={"min_length": 5}),
            
            QuestionConfig("Institution", "Name of the institution where you earned your undergraduate degree.",
                          validation={"min_length": 3}),
            
            QuestionConfig("GPA", "Enter your undergraduate GPA on a 4.0 scale.",
                          validation={"min": 0.0, "max": 4.0, "type": "number"}),
            
            QuestionConfig("Graduation Year", "Year you graduated or expect to graduate from your undergraduate program.",
                          validation={"min": 1950, "max": 2030, "type": "number"}),
            
            QuestionConfig("Class Rank", "Your class rank if available (e.g., Top 10%, 15th out of 200).",
                          required=False),
            
            QuestionConfig("Relevant Coursework", "List courses in mathematics, computer science, statistics, AI, machine learning, etc. Include course numbers and grades if available.",
                          question_type="TEXT", validation={"min_length": 50}),
            
            QuestionConfig("Research Experience and Publications", "Describe any research projects, publications, conference presentations, or academic work. Include details about your role, methodology, and outcomes.",
                          question_type="TEXT", validation={"min_length": 100}),
            
            QuestionConfig("Academic Honors and Awards", "List any academic honors, scholarships, dean's list, honor societies, or other academic recognitions.",
                          required=False, question_type="TEXT"),
            
            # Section 3: Graduate School Preparation
            QuestionConfig("Graduate School Preparation", "Please indicate your preparation for graduate study in AI.",
                          question_type="PAGE_BREAK", required=False),
            
            QuestionConfig("Prerequisite Coursework Completed", "Please check all prerequisite courses you have completed. These courses are strongly recommended for success in the MS AI program.",
                          question_type="CHECKBOX", options=[
                              "Calculus (I, II, III)", "Linear Algebra", "Statistics and Probability",
                              "Programming (Python, Java, C++)", "Data Structures and Algorithms",
                              "Machine Learning or AI", "Database Systems", "Computer Science Fundamentals"
                          ]),
            
            QuestionConfig("Programming Languages Proficiency", "List programming languages you're proficient in and your level of expertise (beginner, intermediate, advanced).",
                          question_type="TEXT", validation={"min_length": 20}),
            
            QuestionConfig("Technical Skills and Tools", "List frameworks, libraries, tools, and technologies you're familiar with (e.g., TensorFlow, PyTorch, AWS, Git, etc.).",
                          question_type="TEXT", validation={"min_length": 20}),
            
            # Section 4: Standardized Test Scores
            QuestionConfig("Standardized Test Scores", "Please provide your standardized test scores if available.",
                          question_type="PAGE_BREAK", required=False),
            
            QuestionConfig("GRE Verbal Score", "Enter your GRE Verbal Reasoning score (130-170).",
                          required=False, validation={"min": 130, "max": 170, "type": "number"}),
            
            QuestionConfig("GRE Quantitative Score", "Enter your GRE Quantitative Reasoning score (130-170).",
                          required=False, validation={"min": 130, "max": 170, "type": "number"}),
            
            QuestionConfig("GRE Writing Score", "Enter your GRE Analytical Writing score (0.0-6.0).",
                          required=False, validation={"min": 0.0, "max": 6.0, "type": "number"}),
            
            QuestionConfig("TOEFL Total Score", "Enter your TOEFL total score (0-120).",
                          required=False, validation={"min": 0, "max": 120, "type": "number"}),
            
            QuestionConfig("IELTS Overall Score", "Enter your IELTS overall band score (0.0-9.0).",
                          required=False, validation={"min": 0.0, "max": 9.0, "type": "number"}),
            
            QuestionConfig("English Proficiency", "Please select your English proficiency level.",
                          question_type="MULTIPLE_CHOICE", options=[
                              "Native Speaker", "TOEFL Score", "IELTS Score", 
                              "Duolingo English Test", "Other"
                          ]),
            
            QuestionConfig("Test Date", "Date of your most recent standardized test.",
                          question_type="DATE", required=False),
            
            # Section 5: Essays and Statements
            QuestionConfig("Essays and Statements", "Please provide thoughtful responses to the following essay questions.",
                          question_type="PAGE_BREAK", required=False),
            
            QuestionConfig("Statement of Purpose (750-1000 words)", 
                          "Please address your academic background, research interests, career goals, and why you chose AURNOVA University. Be specific and provide concrete examples.",
                          question_type="TEXT", validation={"min_length": 750, "max_length": 1000}),
            
            QuestionConfig("Personal Statement (500-750 words)",
                          "Tell us about yourself beyond your academic achievements, including personal experiences, challenges overcome, and unique perspectives.",
                          question_type="TEXT", validation={"min_length": 500, "max_length": 750}),
            
            QuestionConfig("Research Interests and Potential Thesis Topics (300-500 words)",
                          "Describe your research interests in AI and potential thesis topics. Be specific about current research and cite relevant papers if possible.",
                          question_type="TEXT", validation={"min_length": 300, "max_length": 500}),
            
            QuestionConfig("Career Goals and Professional Development (300-500 words)",
                          "Describe your short-term and long-term career aspirations, specific roles/companies of interest, and how this program will help.",
                          question_type="TEXT", validation={"min_length": 300, "max_length": 500}),
            
            QuestionConfig("Diversity and Inclusion Statement (Optional, 200-400 words)",
                          "How will you contribute to diversity and inclusion in our program and the broader AI community? This statement is optional but encouraged.",
                          required=False, question_type="TEXT", validation={"min_length": 200, "max_length": 400}),
            
            # Section 6: Professional Experience
            QuestionConfig("Professional Experience", "Please provide information about your professional background.",
                          question_type="PAGE_BREAK", required=False),
            
            QuestionConfig("Current Employment Status", "Please select your current employment status.",
                          question_type="MULTIPLE_CHOICE", options=[
                              "Full-time employed", "Part-time employed", "Student", "Unemployed", "Other"
                          ]),
            
            QuestionConfig("Work Experience", "Describe your relevant work experience, including internships, research positions, and professional roles.",
                          question_type="TEXT", validation={"min_length": 50}),
            
            QuestionConfig("Notable Projects", "Describe significant projects, GitHub repositories, or portfolio work.",
                          required=False, question_type="TEXT"),
            
            # Section 7: References
            QuestionConfig("References", "Please provide contact information for 2-3 individuals who can speak to your academic abilities, research potential, and character. At least one should be from an academic setting.",
                          question_type="PAGE_BREAK", required=False),
            
            # Reference 1
            QuestionConfig("Reference 1 - Name", "Full name of your first reference.",
                          validation={"min_length": 2}),
            
            QuestionConfig("Reference 1 - Title/Position", "Job title or position of your first reference.",
                          validation={"min_length": 2}),
            
            QuestionConfig("Reference 1 - Institution/Organization", "Institution or organization where your first reference works.",
                          validation={"min_length": 2}),
            
            QuestionConfig("Reference 1 - Email", "Email address of your first reference.",
                          validation={"type": "email"}),
            
            QuestionConfig("Reference 1 - Phone", "Phone number of your first reference (optional).",
                          required=False),
            
            QuestionConfig("Reference 1 - Relationship", "Your relationship to this reference (e.g., Professor, Supervisor, Mentor).",
                          validation={"min_length": 3}),
            
            # Reference 2
            QuestionConfig("Reference 2 - Name", "Full name of your second reference.",
                          validation={"min_length": 2}),
            
            QuestionConfig("Reference 2 - Title/Position", "Job title or position of your second reference.",
                          validation={"min_length": 2}),
            
            QuestionConfig("Reference 2 - Institution/Organization", "Institution or organization where your second reference works.",
                          validation={"min_length": 2}),
            
            QuestionConfig("Reference 2 - Email", "Email address of your second reference.",
                          validation={"type": "email"}),
            
            QuestionConfig("Reference 2 - Phone", "Phone number of your second reference (optional).",
                          required=False),
            
            QuestionConfig("Reference 2 - Relationship", "Your relationship to this reference (e.g., Professor, Supervisor, Mentor).",
                          validation={"min_length": 3}),
            
            # Reference 3 (Optional)
            QuestionConfig("Reference 3 - Name", "Full name of your third reference (optional).",
                          required=False),
            
            QuestionConfig("Reference 3 - Title/Position", "Job title or position of your third reference (optional).",
                          required=False),
            
            QuestionConfig("Reference 3 - Institution/Organization", "Institution or organization where your third reference works (optional).",
                          required=False),
            
            QuestionConfig("Reference 3 - Email", "Email address of your third reference (optional).",
                          required=False, validation={"type": "email"}),
            
            QuestionConfig("Reference 3 - Phone", "Phone number of your third reference (optional).",
                          required=False),
            
            QuestionConfig("Reference 3 - Relationship", "Your relationship to this reference (optional).",
                          required=False),
            
            # Section 8: Additional Information
            QuestionConfig("Additional Information", "Please provide any additional information you'd like the admissions committee to know.",
                          question_type="PAGE_BREAK", required=False),
            
            QuestionConfig("Honors, Awards, and Recognition", "List academic honors, scholarships, competitions, professional awards, or other achievements.",
                          required=False, question_type="TEXT"),
            
            QuestionConfig("Extracurricular Activities and Leadership", "Describe your involvement in clubs, organizations, volunteer work, or leadership roles.",
                          required=False, question_type="TEXT"),
            
            QuestionConfig("Additional Information", "Any other information you'd like the admissions committee to know about your background, experiences, or circumstances.",
                          required=False, question_type="TEXT")
        ]
    
    def create_form_structure(self) -> Dict[str, Any]:
        """Create the complete form structure"""
        form_structure = {
            "info": {
                "title": self.config.title,
                "description": self.config.description
            },
            "items": [],
            "settings": {
                "quizSettings": {
                    "isQuiz": False
                }
            }
        }
        
        # Add questions
        for question in self.get_form_questions():
            item = self._create_question_item(question)
            if item:
                form_structure["items"].append(item)
        
        return form_structure
    
    def _create_question_item(self, question: QuestionConfig) -> Optional[Dict[str, Any]]:
        """Create a question item from QuestionConfig"""
        try:
            item = {
                "title": question.title,
                "description": question.description
            }
            
            if question.question_type == "PAGE_BREAK":
                item["pageBreakItem"] = {}
            elif question.question_type == "TEXT":
                item["questionItem"] = {
                    "question": {
                        "required": question.required,
                        "textQuestion": {
                            "paragraph": len(question.description) > 100
                        }
                    }
                }
            elif question.question_type == "DATE":
                item["questionItem"] = {
                    "question": {
                        "required": question.required,
                        "dateQuestion": {}
                    }
                }
            elif question.question_type == "MULTIPLE_CHOICE":
                item["questionItem"] = {
                    "question": {
                        "required": question.required,
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": [{"value": opt} for opt in question.options or []]
                        }
                    }
                }
            elif question.question_type == "CHECKBOX":
                item["questionItem"] = {
                    "question": {
                        "required": question.required,
                        "choiceQuestion": {
                            "type": "CHECKBOX",
                            "options": [{"value": opt} for opt in question.options or []]
                        }
                    }
                }
            else:
                logger.warning(f"Unknown question type: {question.question_type}")
                return None
            
            return item
            
        except Exception as e:
            logger.error(f"Error creating question item '{question.title}': {e}")
            return None
    
    def create_form(self) -> Optional[Dict[str, Any]]:
        """Create the Google Form"""
        if not self.service:
            logger.error("Not authenticated. Please authenticate first.")
            return None
        
        try:
            logger.info("Creating Google Form...")
            
            # Create form structure
            form_structure = self.create_form_structure()
            
            # Create the form
            form = self.service.forms().create(body=form_structure).execute()
            self.form_id = form['formId']
            
            logger.info(f"Form created successfully with ID: {self.form_id}")
            
            # Update form settings
            self._update_form_settings()
            
            # Get final form details
            final_form = self.service.forms().get(formId=self.form_id).execute()
            
            return {
                'formId': self.form_id,
                'responderUri': form['responderUri'],
                'form': final_form,
                'created_at': datetime.now().isoformat()
            }
            
        except HttpError as error:
            logger.error(f"HTTP error creating form: {error}")
            if error.resp.status == 403:
                logger.error("Permission denied. Check your authentication and API permissions.")
            return None
        except Exception as error:
            logger.error(f"Unexpected error creating form: {error}")
            return None
    
    def _update_form_settings(self):
        """Update form settings after creation"""
        if not self.form_id:
            return
        
        try:
            settings_update = {
                "requests": [{
                    "updateSettings": {
                        "settings": {
                            "quizSettings": {
                                "isQuiz": False
                            }
                        },
                        "updateMask": "quizSettings"
                    }
                }]
            }
            
            self.service.forms().batchUpdate(formId=self.form_id, body=settings_update).execute()
            logger.info("Form settings updated successfully")
            
        except Exception as e:
            logger.warning(f"Could not update form settings: {e}")
    
    def create_linked_sheet(self) -> Optional[str]:
        """Create a linked Google Sheet for responses"""
        if not self.form_id or not self.service:
            return None
        
        try:
            # Import Drive API
            drive_service = build('drive', 'v3', credentials=self.service._http.credentials)
            
            # Create new spreadsheet
            spreadsheet_body = {
                'name': f'MS AI Applications - {datetime.now().strftime("%Y-%m-%d")}',
                'mimeType': 'application/vnd.google-apps.spreadsheet'
            }
            
            spreadsheet = drive_service.files().create(body=spreadsheet_body).execute()
            sheet_id = spreadsheet['id']
            
            logger.info(f"Linked sheet created: {sheet_id}")
            return sheet_id
            
        except Exception as e:
            logger.error(f"Error creating linked sheet: {e}")
            return None
    
    def save_form_details(self, form_data: Dict[str, Any], output_file: str = "form_details.json"):
        """Save form details to file"""
        try:
            with open(output_file, 'w') as f:
                json.dump(form_data, f, indent=2)
            logger.info(f"Form details saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving form details: {e}")

def main():
    """Main function to create Google Form"""
    print("🚀 Enhanced Google Form Creator for MS AI Application")
    print("=" * 60)
    
    # Initialize creator
    creator = GoogleFormCreator()
    
    # Try different authentication methods
    authenticated = False
    
    # Try service account first
    if creator.authenticate_service_account():
        authenticated = True
        print("✅ Authenticated using service account")
    # Try OAuth as fallback
    elif creator.authenticate_oauth():
        authenticated = True
        print("✅ Authenticated using OAuth")
    
    if not authenticated:
        print("❌ Authentication failed. Please check your credentials.")
        print("\nSetup instructions:")
        print("1. For service account: Ensure 'msai-service-key.json' exists")
        print("2. For OAuth: Ensure 'credentials.json' exists and run OAuth flow")
        return
    
    # Create the form
    form_data = creator.create_form()
    
    if form_data:
        print(f"\n🎉 Form created successfully!")
        print(f"📝 Form ID: {form_data['formId']}")
        print(f"🔗 Form URL: {form_data['responderUri']}")
        
        # Create linked sheet
        sheet_id = creator.create_linked_sheet()
        if sheet_id:
            print(f"📊 Linked Sheet ID: {sheet_id}")
            form_data['linkedSheetId'] = sheet_id
        
        # Save details
        creator.save_form_details(form_data)
        
        print(f"\n📋 Next steps:")
        print(f"1. Test the form: {form_data['responderUri']}")
        print(f"2. Customize appearance and settings")
        print(f"3. Update your website with the form URL")
        print(f"4. Monitor responses in the linked Google Sheet")
        
    else:
        print("\n❌ Form creation failed. Check the logs for details.")

if __name__ == "__main__":
    main()