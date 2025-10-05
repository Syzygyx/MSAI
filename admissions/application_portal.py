"""
MS AI Curriculum System - Application Portal
Comprehensive student application portal with form submission and tracking
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import random

class ApplicationStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_COMPLETED = "interview_completed"
    EVALUATION_COMPLETE = "evaluation_complete"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WAITLISTED = "waitlisted"
    WITHDRAWN = "withdrawn"

class DocumentType(Enum):
    TRANSCRIPT = "transcript"
    RECOMMENDATION_LETTER = "recommendation_letter"
    PERSONAL_STATEMENT = "personal_statement"
    RESUME = "resume"
    PORTFOLIO = "portfolio"
    TEST_SCORES = "test_scores"
    IDENTIFICATION = "identification"
    FINANCIAL_DOCUMENTS = "financial_documents"

class ApplicationStep(Enum):
    PERSONAL_INFO = "personal_info"
    ACADEMIC_BACKGROUND = "academic_background"
    WORK_EXPERIENCE = "work_experience"
    TECHNICAL_SKILLS = "technical_skills"
    PERSONAL_STATEMENT = "personal_statement"
    RECOMMENDATIONS = "recommendations"
    DOCUMENTS = "documents"
    REVIEW_SUBMIT = "review_submit"

@dataclass
class ApplicationForm:
    """Application form structure"""
    form_id: str
    applicant_email: str
    current_step: ApplicationStep
    completed_steps: List[ApplicationStep]
    form_data: Dict[str, Any]
    created_at: datetime
    last_updated: datetime
    status: ApplicationStatus
    progress_percentage: float = 0.0
    validation_errors: List[str] = field(default_factory=list)
    auto_save_enabled: bool = True

@dataclass
class ApplicationDocument:
    """Application document structure"""
    document_id: str
    application_id: str
    document_type: DocumentType
    file_name: str
    file_size: int
    upload_date: datetime
    status: str  # uploaded, verified, rejected
    verification_notes: str = ""
    file_path: str = ""

@dataclass
class ApplicationProgress:
    """Application progress tracking"""
    application_id: str
    applicant_email: str
    current_step: ApplicationStep
    completed_steps: List[ApplicationStep]
    progress_percentage: float
    estimated_completion_time: int  # minutes
    last_activity: datetime
    time_spent_minutes: int = 0
    help_requests: int = 0
    auto_saves: int = 0

class ApplicationPortal:
    """Comprehensive application portal for MS AI program"""
    
    def __init__(self, admissions_system=None, assistant_system=None):
        self.admissions_system = admissions_system
        self.assistant_system = assistant_system
        
        # Application data
        self.application_forms: Dict[str, ApplicationForm] = {}
        self.application_documents: Dict[str, List[ApplicationDocument]] = {}
        self.application_progress: Dict[str, ApplicationProgress] = {}
        
        # Form templates and validation rules
        self.form_templates = self._initialize_form_templates()
        self.validation_rules = self._initialize_validation_rules()
        
    def _initialize_form_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize application form templates"""
        return {
            "personal_info": {
                "title": "Personal Information",
                "fields": [
                    {"name": "first_name", "type": "text", "required": True, "label": "First Name"},
                    {"name": "last_name", "type": "text", "required": True, "label": "Last Name"},
                    {"name": "email", "type": "email", "required": True, "label": "Email Address"},
                    {"name": "phone", "type": "tel", "required": True, "label": "Phone Number"},
                    {"name": "date_of_birth", "type": "date", "required": True, "label": "Date of Birth"},
                    {"name": "address", "type": "textarea", "required": True, "label": "Address"},
                    {"name": "citizenship", "type": "select", "required": True, "label": "Citizenship Status"},
                    {"name": "emergency_contact", "type": "text", "required": True, "label": "Emergency Contact"}
                ]
            },
            "academic_background": {
                "title": "Academic Background",
                "fields": [
                    {"name": "undergraduate_degree", "type": "text", "required": True, "label": "Undergraduate Degree"},
                    {"name": "undergraduate_institution", "type": "text", "required": True, "label": "Institution"},
                    {"name": "graduation_year", "type": "number", "required": True, "label": "Graduation Year"},
                    {"name": "gpa", "type": "number", "required": True, "label": "GPA", "min": 0, "max": 4.0},
                    {"name": "major", "type": "text", "required": True, "label": "Major Field of Study"},
                    {"name": "relevant_courses", "type": "textarea", "required": False, "label": "Relevant Coursework"},
                    {"name": "academic_honors", "type": "textarea", "required": False, "label": "Academic Honors/Awards"},
                    {"name": "research_experience", "type": "textarea", "required": False, "label": "Research Experience"}
                ]
            },
            "work_experience": {
                "title": "Work Experience",
                "fields": [
                    {"name": "current_position", "type": "text", "required": False, "label": "Current Position"},
                    {"name": "current_company", "type": "text", "required": False, "label": "Current Company"},
                    {"name": "years_experience", "type": "number", "required": True, "label": "Years of Experience"},
                    {"name": "ai_ml_experience", "type": "textarea", "required": False, "label": "AI/ML Experience"},
                    {"name": "programming_languages", "type": "text", "required": True, "label": "Programming Languages"},
                    {"name": "technical_skills", "type": "textarea", "required": True, "label": "Technical Skills"},
                    {"name": "projects", "type": "textarea", "required": False, "label": "Notable Projects"},
                    {"name": "certifications", "type": "textarea", "required": False, "label": "Certifications"}
                ]
            },
            "technical_skills": {
                "title": "Technical Skills Assessment",
                "fields": [
                    {"name": "programming_proficiency", "type": "select", "required": True, "label": "Programming Proficiency", "options": ["Beginner", "Intermediate", "Advanced", "Expert"]},
                    {"name": "ai_ml_knowledge", "type": "select", "required": True, "label": "AI/ML Knowledge Level", "options": ["Beginner", "Intermediate", "Advanced", "Expert"]},
                    {"name": "mathematics_background", "type": "select", "required": True, "label": "Mathematics Background", "options": ["Basic", "Intermediate", "Strong", "Advanced"]},
                    {"name": "statistics_knowledge", "type": "select", "required": True, "label": "Statistics Knowledge", "options": ["Basic", "Intermediate", "Strong", "Advanced"]},
                    {"name": "tools_frameworks", "type": "textarea", "required": True, "label": "Tools and Frameworks"},
                    {"name": "github_profile", "type": "url", "required": False, "label": "GitHub Profile"},
                    {"name": "portfolio_url", "type": "url", "required": False, "label": "Portfolio/Website"},
                    {"name": "online_courses", "type": "textarea", "required": False, "label": "Online Courses Completed"}
                ]
            },
            "personal_statement": {
                "title": "Personal Statement",
                "fields": [
                    {"name": "motivation", "type": "textarea", "required": True, "label": "Why do you want to pursue MS in AI?", "min_length": 200},
                    {"name": "career_goals", "type": "textarea", "required": True, "label": "Career Goals", "min_length": 150},
                    {"name": "research_interests", "type": "textarea", "required": True, "label": "Research Interests", "min_length": 100},
                    {"name": "contribution", "type": "textarea", "required": True, "label": "How will you contribute to the program?", "min_length": 150},
                    {"name": "challenges", "type": "textarea", "required": False, "label": "Challenges you've overcome"},
                    {"name": "additional_info", "type": "textarea", "required": False, "label": "Additional Information"}
                ]
            },
            "recommendations": {
                "title": "Recommendations",
                "fields": [
                    {"name": "recommender_1_name", "type": "text", "required": True, "label": "Recommender 1 Name"},
                    {"name": "recommender_1_title", "type": "text", "required": True, "label": "Recommender 1 Title"},
                    {"name": "recommender_1_email", "type": "email", "required": True, "label": "Recommender 1 Email"},
                    {"name": "recommender_1_relationship", "type": "text", "required": True, "label": "Relationship to Recommender 1"},
                    {"name": "recommender_2_name", "type": "text", "required": True, "label": "Recommender 2 Name"},
                    {"name": "recommender_2_title", "type": "text", "required": True, "label": "Recommender 2 Title"},
                    {"name": "recommender_2_email", "type": "email", "required": True, "label": "Recommender 2 Email"},
                    {"name": "recommender_2_relationship", "type": "text", "required": True, "label": "Relationship to Recommender 2"},
                    {"name": "recommender_3_name", "type": "text", "required": True, "label": "Recommender 3 Name"},
                    {"name": "recommender_3_title", "type": "text", "required": True, "label": "Recommender 3 Title"},
                    {"name": "recommender_3_email", "type": "email", "required": True, "label": "Recommender 3 Email"},
                    {"name": "recommender_3_relationship", "type": "text", "required": True, "label": "Relationship to Recommender 3"}
                ]
            }
        }
    
    def _initialize_validation_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize form validation rules"""
        return {
            "email": {
                "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                "message": "Please enter a valid email address"
            },
            "phone": {
                "pattern": r"^\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$",
                "message": "Please enter a valid phone number"
            },
            "gpa": {
                "min": 0.0,
                "max": 4.0,
                "message": "GPA must be between 0.0 and 4.0"
            },
            "years_experience": {
                "min": 0,
                "max": 50,
                "message": "Years of experience must be between 0 and 50"
            },
            "personal_statement_min_length": {
                "motivation": 200,
                "career_goals": 150,
                "research_interests": 100,
                "contribution": 150
            }
        }
    
    def start_application(self, applicant_email: str) -> Dict[str, Any]:
        """Start new application process"""
        
        # Check if application already exists
        existing_applications = [app for app in self.application_forms.values() if app.applicant_email == applicant_email]
        if existing_applications:
            return {
                "success": False,
                "error": "Application already exists for this email address",
                "existing_application_id": existing_applications[0].form_id
            }
        
        # Create new application form
        form_id = f"APP_{uuid.uuid4().hex[:8]}"
        
        application_form = ApplicationForm(
            form_id=form_id,
            applicant_email=applicant_email,
            current_step=ApplicationStep.PERSONAL_INFO,
            completed_steps=[],
            form_data={},
            created_at=datetime.now(),
            last_updated=datetime.now(),
            status=ApplicationStatus.DRAFT,
            progress_percentage=0.0
        )
        
        self.application_forms[form_id] = application_form
        
        # Create progress tracking
        progress = ApplicationProgress(
            application_id=form_id,
            applicant_email=applicant_email,
            current_step=ApplicationStep.PERSONAL_INFO,
            completed_steps=[],
            progress_percentage=0.0,
            estimated_completion_time=45,  # minutes
            last_activity=datetime.now()
        )
        
        self.application_progress[form_id] = progress
        
        return {
            "success": True,
            "application_id": form_id,
            "current_step": ApplicationStep.PERSONAL_INFO.value,
            "form_template": self.form_templates["personal_info"],
            "estimated_completion_time": progress.estimated_completion_time,
            "message": "Application started successfully"
        }
    
    def get_application_form(self, application_id: str, step: ApplicationStep) -> Dict[str, Any]:
        """Get application form for specific step"""
        
        application_form = self.application_forms.get(application_id)
        if not application_form:
            return {"success": False, "error": "Application not found"}
        
        # Get form template for step
        step_key = step.value
        if step_key not in self.form_templates:
            return {"success": False, "error": f"Form template not found for step: {step_key}"}
        
        form_template = self.form_templates[step_key]
        
        # Get existing data for this step
        step_data = application_form.form_data.get(step_key, {})
        
        return {
            "success": True,
            "application_id": application_id,
            "step": step.value,
            "form_template": form_template,
            "existing_data": step_data,
            "validation_errors": application_form.validation_errors,
            "progress_percentage": application_form.progress_percentage
        }
    
    def save_application_step(self, application_id: str, step: ApplicationStep, 
                            form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save application step data"""
        
        application_form = self.application_forms.get(application_id)
        if not application_form:
            return {"success": False, "error": "Application not found"}
        
        # Validate form data
        validation_result = self._validate_form_data(step, form_data)
        if not validation_result["is_valid"]:
            application_form.validation_errors = validation_result["errors"]
            return {
                "success": False,
                "error": "Validation failed",
                "validation_errors": validation_result["errors"]
            }
        
        # Save form data
        step_key = step.value
        application_form.form_data[step_key] = form_data
        application_form.last_updated = datetime.now()
        application_form.validation_errors = []
        
        # Update progress
        self._update_application_progress(application_id, step)
        
        return {
            "success": True,
            "application_id": application_id,
            "step": step.value,
            "progress_percentage": application_form.progress_percentage,
            "next_step": self._get_next_step(step),
            "message": "Form data saved successfully"
        }
    
    def _validate_form_data(self, step: ApplicationStep, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate form data based on step and rules"""
        
        errors = []
        step_key = step.value
        
        if step_key not in self.form_templates:
            return {"is_valid": False, "errors": ["Invalid step"]}
        
        form_template = self.form_templates[step_key]
        
        # Validate each field
        for field in form_template["fields"]:
            field_name = field["name"]
            field_value = form_data.get(field_name, "")
            
            # Check required fields
            if field.get("required", False) and not field_value:
                errors.append(f"{field['label']} is required")
                continue
            
            # Skip validation if field is empty and not required
            if not field_value and not field.get("required", False):
                continue
            
            # Type-specific validation
            if field["type"] == "email":
                if not self._validate_email(field_value):
                    errors.append(f"{field['label']} must be a valid email address")
            
            elif field["type"] == "number":
                try:
                    num_value = float(field_value)
                    if "min" in field and num_value < field["min"]:
                        errors.append(f"{field['label']} must be at least {field['min']}")
                    if "max" in field and num_value > field["max"]:
                        errors.append(f"{field['label']} must be at most {field['max']}")
                except ValueError:
                    errors.append(f"{field['label']} must be a valid number")
            
            elif field["type"] == "textarea":
                min_length = field.get("min_length", 0)
                if len(field_value) < min_length:
                    errors.append(f"{field['label']} must be at least {min_length} characters")
            
            elif field["type"] == "url":
                if not self._validate_url(field_value):
                    errors.append(f"{field['label']} must be a valid URL")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None
    
    def _validate_url(self, url: str) -> bool:
        """Validate URL format"""
        import re
        pattern = r"^https?://[^\s/$.?#].[^\s]*$"
        return re.match(pattern, url) is not None
    
    def _update_application_progress(self, application_id: str, completed_step: ApplicationStep):
        """Update application progress"""
        
        application_form = self.application_forms[application_id]
        progress = self.application_progress[application_id]
        
        # Add step to completed steps if not already there
        if completed_step not in application_form.completed_steps:
            application_form.completed_steps.append(completed_step)
        
        # Calculate progress percentage
        total_steps = len(ApplicationStep)
        completed_count = len(application_form.completed_steps)
        application_form.progress_percentage = (completed_count / total_steps) * 100
        
        # Update progress tracking
        progress.completed_steps = application_form.completed_steps.copy()
        progress.progress_percentage = application_form.progress_percentage
        progress.last_activity = datetime.now()
        
        # Update current step
        next_step = self._get_next_step(completed_step)
        if next_step:
            application_form.current_step = next_step
            progress.current_step = next_step
    
    def _get_next_step(self, current_step: ApplicationStep) -> Optional[ApplicationStep]:
        """Get next step in application process"""
        
        step_order = [
            ApplicationStep.PERSONAL_INFO,
            ApplicationStep.ACADEMIC_BACKGROUND,
            ApplicationStep.WORK_EXPERIENCE,
            ApplicationStep.TECHNICAL_SKILLS,
            ApplicationStep.PERSONAL_STATEMENT,
            ApplicationStep.RECOMMENDATIONS,
            ApplicationStep.DOCUMENTS,
            ApplicationStep.REVIEW_SUBMIT
        ]
        
        try:
            current_index = step_order.index(current_step)
            if current_index < len(step_order) - 1:
                return step_order[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def upload_document(self, application_id: str, document_type: DocumentType, 
                      file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Upload document to application"""
        
        application_form = self.application_forms.get(application_id)
        if not application_form:
            return {"success": False, "error": "Application not found"}
        
        # Create document record
        document_id = f"DOC_{uuid.uuid4().hex[:8]}"
        document = ApplicationDocument(
            document_id=document_id,
            application_id=application_id,
            document_type=document_type,
            file_name=file_info["file_name"],
            file_size=file_info["file_size"],
            upload_date=datetime.now(),
            status="uploaded",
            file_path=file_info.get("file_path", "")
        )
        
        # Add to application documents
        if application_id not in self.application_documents:
            self.application_documents[application_id] = []
        self.application_documents[application_id].append(document)
        
        # Update application form
        application_form.last_updated = datetime.now()
        
        return {
            "success": True,
            "document_id": document_id,
            "document_type": document_type.value,
            "file_name": document.file_name,
            "upload_date": document.upload_date.isoformat(),
            "message": "Document uploaded successfully"
        }
    
    def get_application_status(self, application_id: str) -> Dict[str, Any]:
        """Get application status and progress"""
        
        application_form = self.application_forms.get(application_id)
        if not application_form:
            return {"error": "Application not found"}
        
        progress = self.application_progress.get(application_id)
        documents = self.application_documents.get(application_id, [])
        
        return {
            "application_id": application_id,
            "applicant_email": application_form.applicant_email,
            "status": application_form.status.value,
            "current_step": application_form.current_step.value,
            "completed_steps": [step.value for step in application_form.completed_steps],
            "progress_percentage": application_form.progress_percentage,
            "created_at": application_form.created_at.isoformat(),
            "last_updated": application_form.last_updated.isoformat(),
            "documents_uploaded": len(documents),
            "documents": [
                {
                    "document_id": doc.document_id,
                    "document_type": doc.document_type.value,
                    "file_name": doc.file_name,
                    "upload_date": doc.upload_date.isoformat(),
                    "status": doc.status
                }
                for doc in documents
            ],
            "next_steps": self._get_next_steps_guidance(application_form),
            "estimated_completion_time": progress.estimated_completion_time if progress else 0
        }
    
    def _get_next_steps_guidance(self, application_form: ApplicationForm) -> List[str]:
        """Get guidance for next steps"""
        
        current_step = application_form.current_step
        completed_steps = application_form.completed_steps
        
        guidance = []
        
        if current_step == ApplicationStep.PERSONAL_INFO:
            guidance.append("Complete your personal information")
            guidance.append("Ensure all required fields are filled")
        elif current_step == ApplicationStep.ACADEMIC_BACKGROUND:
            guidance.append("Provide your academic background")
            guidance.append("Include relevant coursework and achievements")
        elif current_step == ApplicationStep.WORK_EXPERIENCE:
            guidance.append("Detail your work experience")
            guidance.append("Highlight AI/ML related experience")
        elif current_step == ApplicationStep.TECHNICAL_SKILLS:
            guidance.append("Assess your technical skills")
            guidance.append("Include programming languages and tools")
        elif current_step == ApplicationStep.PERSONAL_STATEMENT:
            guidance.append("Write compelling personal statement")
            guidance.append("Explain your motivation and career goals")
        elif current_step == ApplicationStep.RECOMMENDATIONS:
            guidance.append("Provide recommender information")
            guidance.append("Ensure recommenders can speak to your abilities")
        elif current_step == ApplicationStep.DOCUMENTS:
            guidance.append("Upload required documents")
            guidance.append("Ensure all documents are clear and readable")
        elif current_step == ApplicationStep.REVIEW_SUBMIT:
            guidance.append("Review your application thoroughly")
            guidance.append("Submit when ready")
        
        return guidance
    
    def submit_application(self, application_id: str) -> Dict[str, Any]:
        """Submit completed application"""
        
        application_form = self.application_forms.get(application_id)
        if not application_form:
            return {"success": False, "error": "Application not found"}
        
        # Check if all required steps are completed
        required_steps = [
            ApplicationStep.PERSONAL_INFO,
            ApplicationStep.ACADEMIC_BACKGROUND,
            ApplicationStep.WORK_EXPERIENCE,
            ApplicationStep.TECHNICAL_SKILLS,
            ApplicationStep.PERSONAL_STATEMENT,
            ApplicationStep.RECOMMENDATIONS
        ]
        
        missing_steps = [step for step in required_steps if step not in application_form.completed_steps]
        if missing_steps:
            return {
                "success": False,
                "error": "Application incomplete",
                "missing_steps": [step.value for step in missing_steps]
            }
        
        # Validate final submission
        final_validation = self._validate_final_submission(application_form)
        if not final_validation["is_valid"]:
            return {
                "success": False,
                "error": "Final validation failed",
                "validation_errors": final_validation["errors"]
            }
        
        # Update application status
        application_form.status = ApplicationStatus.SUBMITTED
        application_form.last_updated = datetime.now()
        
        # Submit to admissions system
        if self.admissions_system:
            submission_result = self.admissions_system.submit_application(application_id)
            if not submission_result["success"]:
                return submission_result
        
        return {
            "success": True,
            "application_id": application_id,
            "status": ApplicationStatus.SUBMITTED.value,
            "submission_date": application_form.last_updated.isoformat(),
            "message": "Application submitted successfully",
            "next_steps": [
                "Application is now under review",
                "You will receive email updates on your application status",
                "Check your email for any additional requirements"
            ]
        }
    
    def _validate_final_submission(self, application_form: ApplicationForm) -> Dict[str, Any]:
        """Validate application for final submission"""
        
        errors = []
        
        # Check required documents
        required_documents = [DocumentType.TRANSCRIPT, DocumentType.PERSONAL_STATEMENT]
        uploaded_documents = self.application_documents.get(application_form.form_id, [])
        uploaded_types = [doc.document_type for doc in uploaded_documents]
        
        for doc_type in required_documents:
            if doc_type not in uploaded_types:
                errors.append(f"Required document missing: {doc_type.value}")
        
        # Check form completeness
        for step_key, template in self.form_templates.items():
            if step_key not in application_form.form_data:
                errors.append(f"Form section incomplete: {template['title']}")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    def get_application_dashboard(self, applicant_email: str) -> Dict[str, Any]:
        """Get application dashboard for applicant"""
        
        # Find applications for this email
        applications = [app for app in self.application_forms.values() if app.applicant_email == applicant_email]
        
        if not applications:
            return {
                "applicant_email": applicant_email,
                "applications": [],
                "message": "No applications found"
            }
        
        application_summaries = []
        for app in applications:
            progress = self.application_progress.get(app.form_id)
            documents = self.application_documents.get(app.form_id, [])
            
            summary = {
                "application_id": app.form_id,
                "status": app.status.value,
                "current_step": app.current_step.value,
                "progress_percentage": app.progress_percentage,
                "created_at": app.created_at.isoformat(),
                "last_updated": app.last_updated.isoformat(),
                "documents_count": len(documents),
                "estimated_completion_time": progress.estimated_completion_time if progress else 0
            }
            application_summaries.append(summary)
        
        return {
            "applicant_email": applicant_email,
            "applications": application_summaries,
            "total_applications": len(applications),
            "active_applications": len([app for app in applications if app.status == ApplicationStatus.DRAFT])
        }
    
    def request_help(self, application_id: str, help_type: str, description: str) -> Dict[str, Any]:
        """Request help during application process"""
        
        application_form = self.application_forms.get(application_id)
        if not application_form:
            return {"success": False, "error": "Application not found"}
        
        # Update progress tracking
        progress = self.application_progress.get(application_id)
        if progress:
            progress.help_requests += 1
            progress.last_activity = datetime.now()
        
        # Create help request
        help_request_id = f"HELP_{uuid.uuid4().hex[:8]}"
        
        # Submit to assistant system if available
        if self.assistant_system:
            assistant_result = self.assistant_system.submit_student_request(
                application_form.applicant_email,
                {
                    "title": f"Application Help Request: {help_type}",
                    "description": description,
                    "urgency": "medium",
                    "tags": ["application", "help", help_type]
                }
            )
            
            if assistant_result["success"]:
                return {
                    "success": True,
                    "help_request_id": help_request_id,
                    "assistant_request_id": assistant_result["request_id"],
                    "assigned_assistant": assistant_result["assigned_assistant"],
                    "estimated_response_time": assistant_result["estimated_response_time"],
                    "message": "Help request submitted successfully"
                }
        
        return {
            "success": True,
            "help_request_id": help_request_id,
            "message": "Help request recorded, you will be contacted soon"
        }
    
    def get_application_statistics(self) -> Dict[str, Any]:
        """Get application portal statistics"""
        
        total_applications = len(self.application_forms)
        
        # Status distribution
        status_counts = {}
        for status in ApplicationStatus:
            status_counts[status.value] = len([app for app in self.application_forms.values() if app.status == status])
        
        # Step completion statistics
        step_completion = {}
        for step in ApplicationStep:
            completed_count = len([app for app in self.application_forms.values() if step in app.completed_steps])
            step_completion[step.value] = {
                "completed": completed_count,
                "completion_rate": (completed_count / total_applications * 100) if total_applications > 0 else 0
            }
        
        # Document upload statistics
        total_documents = sum(len(docs) for docs in self.application_documents.values())
        document_types = {}
        for docs in self.application_documents.values():
            for doc in docs:
                doc_type = doc.document_type.value
                document_types[doc_type] = document_types.get(doc_type, 0) + 1
        
        return {
            "total_applications": total_applications,
            "status_distribution": status_counts,
            "step_completion": step_completion,
            "document_statistics": {
                "total_documents": total_documents,
                "document_types": document_types
            },
            "average_completion_time": sum(
                progress.estimated_completion_time for progress in self.application_progress.values()
            ) / len(self.application_progress) if self.application_progress else 0,
            "help_requests": sum(
                progress.help_requests for progress in self.application_progress.values()
            )
        }