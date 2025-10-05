"""
MS AI Curriculum System - Admission Workflow
Complete admission workflow from application to enrollment
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import random

class WorkflowStage(Enum):
    APPLICATION_SUBMITTED = "application_submitted"
    INITIAL_REVIEW = "initial_review"
    DOCUMENT_VERIFICATION = "document_verification"
    AI_EVALUATION = "ai_evaluation"
    HUMAN_REVIEW = "human_review"
    INTERVIEW_SCHEDULING = "interview_scheduling"
    INTERVIEW_CONDUCTED = "interview_conducted"
    COMMITTEE_REVIEW = "committee_review"
    DECISION_MADE = "decision_made"
    DECISION_COMMUNICATED = "decision_communicated"
    ENROLLMENT_PROCESSING = "enrollment_processing"
    ENROLLMENT_COMPLETED = "enrollment_completed"

class DecisionType(Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    WAITLIST = "waitlist"
    CONDITIONAL_ACCEPT = "conditional_accept"

class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"
    PORTAL_NOTIFICATION = "portal_notification"
    PHONE_CALL = "phone_call"

@dataclass
class WorkflowStep:
    """Individual step in admission workflow"""
    step_id: str
    stage: WorkflowStage
    description: str
    assigned_to: str  # AI agent or human reviewer
    due_date: datetime
    completed_at: Optional[datetime] = None
    status: str = "pending"  # pending, in_progress, completed, failed
    notes: str = ""
    required_documents: List[str] = field(default_factory=list)
    auto_triggered: bool = False

@dataclass
class AdmissionWorkflow:
    """Complete admission workflow for an application"""
    workflow_id: str
    application_id: str
    applicant_email: str
    current_stage: WorkflowStage
    workflow_steps: List[WorkflowStep]
    decision: Optional[DecisionType] = None
    decision_reason: str = ""
    decision_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    estimated_completion_date: Optional[datetime] = None
    priority: str = "normal"  # low, normal, high, urgent
    notifications_sent: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class EnrollmentData:
    """Student enrollment data"""
    enrollment_id: str
    application_id: str
    student_id: str
    program: str
    start_term: str
    enrollment_date: datetime
    status: str  # enrolled, deferred, withdrawn
    tuition_deposit_paid: bool = False
    orientation_completed: bool = False
    advisor_assigned: str = ""

class AdmissionWorkflowManager:
    """Manages complete admission workflow from application to enrollment"""
    
    def __init__(self, admissions_system=None, evaluation_system=None, 
                 application_portal=None, user_manager=None):
        self.admissions_system = admissions_system
        self.evaluation_system = evaluation_system
        self.application_portal = application_portal
        self.user_manager = user_manager
        
        # Workflow data
        self.admission_workflows: Dict[str, AdmissionWorkflow] = {}
        self.enrollment_data: Dict[str, EnrollmentData] = {}
        
        # Workflow templates
        self.workflow_templates = self._initialize_workflow_templates()
        
    def _initialize_workflow_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize workflow templates for different application types"""
        return {
            "standard": [
                {
                    "stage": WorkflowStage.APPLICATION_SUBMITTED,
                    "description": "Application submitted and received",
                    "assigned_to": "SYSTEM",
                    "due_hours": 0,
                    "auto_triggered": True
                },
                {
                    "stage": WorkflowStage.INITIAL_REVIEW,
                    "description": "Initial application review and completeness check",
                    "assigned_to": "AI_ADMIN_AGENT",
                    "due_hours": 24,
                    "auto_triggered": True
                },
                {
                    "stage": WorkflowStage.DOCUMENT_VERIFICATION,
                    "description": "Verify submitted documents and transcripts",
                    "assigned_to": "AI_ADMIN_AGENT",
                    "due_hours": 48,
                    "auto_triggered": True
                },
                {
                    "stage": WorkflowStage.AI_EVALUATION,
                    "description": "Automated AI evaluation of application",
                    "assigned_to": "AI_EVALUATION_SYSTEM",
                    "due_hours": 72,
                    "auto_triggered": True
                },
                {
                    "stage": WorkflowStage.HUMAN_REVIEW,
                    "description": "Human review of AI evaluation results",
                    "assigned_to": "ADMISSIONS_COMMITTEE",
                    "due_hours": 120,
                    "auto_triggered": False
                },
                {
                    "stage": WorkflowStage.INTERVIEW_SCHEDULING,
                    "description": "Schedule interview if required",
                    "assigned_to": "AI_ADMIN_AGENT",
                    "due_hours": 144,
                    "auto_triggered": False
                },
                {
                    "stage": WorkflowStage.INTERVIEW_CONDUCTED,
                    "description": "Conduct admission interview",
                    "assigned_to": "ADMISSIONS_COMMITTEE",
                    "due_hours": 168,
                    "auto_triggered": False
                },
                {
                    "stage": WorkflowStage.COMMITTEE_REVIEW,
                    "description": "Final committee review and decision",
                    "assigned_to": "ADMISSIONS_COMMITTEE",
                    "due_hours": 192,
                    "auto_triggered": False
                },
                {
                    "stage": WorkflowStage.DECISION_MADE,
                    "description": "Final admission decision made",
                    "assigned_to": "ADMISSIONS_DIRECTOR",
                    "due_hours": 216,
                    "auto_triggered": False
                },
                {
                    "stage": WorkflowStage.DECISION_COMMUNICATED,
                    "description": "Decision communicated to applicant",
                    "assigned_to": "AI_ADMIN_AGENT",
                    "due_hours": 240,
                    "auto_triggered": True
                },
                {
                    "stage": WorkflowStage.ENROLLMENT_PROCESSING,
                    "description": "Process enrollment for accepted students",
                    "assigned_to": "AI_ADMIN_AGENT",
                    "due_hours": 264,
                    "auto_triggered": True
                },
                {
                    "stage": WorkflowStage.ENROLLMENT_COMPLETED,
                    "description": "Enrollment completed and student activated",
                    "assigned_to": "SYSTEM",
                    "due_hours": 288,
                    "auto_triggered": True
                }
            ],
            "fast_track": [
                {
                    "stage": WorkflowStage.APPLICATION_SUBMITTED,
                    "description": "Application submitted and received",
                    "assigned_to": "SYSTEM",
                    "due_hours": 0,
                    "auto_triggered": True
                },
                {
                    "stage": WorkflowStage.INITIAL_REVIEW,
                    "description": "Initial application review and completeness check",
                    "assigned_to": "AI_ADMIN_AGENT",
                    "due_hours": 12,
                    "auto_triggered": True
                },
                {
                    "stage": WorkflowStage.DOCUMENT_VERIFICATION,
                    "description": "Verify submitted documents and transcripts",
                    "assigned_to": "AI_ADMIN_AGENT",
                    "due_hours": 24,
                    "auto_triggered": True
                },
                {
                    "stage": WorkflowStage.AI_EVALUATION,
                    "description": "Automated AI evaluation of application",
                    "assigned_to": "AI_EVALUATION_SYSTEM",
                    "due_hours": 36,
                    "auto_triggered": True
                },
                {
                    "stage": WorkflowStage.HUMAN_REVIEW,
                    "description": "Human review of AI evaluation results",
                    "assigned_to": "ADMISSIONS_COMMITTEE",
                    "due_hours": 48,
                    "auto_triggered": False
                },
                {
                    "stage": WorkflowStage.DECISION_MADE,
                    "description": "Final admission decision made",
                    "assigned_to": "ADMISSIONS_DIRECTOR",
                    "due_hours": 60,
                    "auto_triggered": False
                },
                {
                    "stage": WorkflowStage.DECISION_COMMUNICATED,
                    "description": "Decision communicated to applicant",
                    "assigned_to": "AI_ADMIN_AGENT",
                    "due_hours": 72,
                    "auto_triggered": True
                },
                {
                    "stage": WorkflowStage.ENROLLMENT_PROCESSING,
                    "description": "Process enrollment for accepted students",
                    "assigned_to": "AI_ADMIN_AGENT",
                    "due_hours": 84,
                    "auto_triggered": True
                },
                {
                    "stage": WorkflowStage.ENROLLMENT_COMPLETED,
                    "description": "Enrollment completed and student activated",
                    "assigned_to": "SYSTEM",
                    "due_hours": 96,
                    "auto_triggered": True
                }
            ]
        }
    
    def initiate_admission_workflow(self, application_id: str, applicant_email: str, 
                                   workflow_type: str = "standard") -> Dict[str, Any]:
        """Initiate admission workflow for submitted application"""
        
        # Check if workflow already exists
        existing_workflows = [wf for wf in self.admission_workflows.values() if wf.application_id == application_id]
        if existing_workflows:
            return {
                "success": False,
                "error": "Workflow already exists for this application",
                "workflow_id": existing_workflows[0].workflow_id
            }
        
        # Create workflow
        workflow_id = f"WF_{uuid.uuid4().hex[:8]}"
        
        # Get workflow template
        template = self.workflow_templates.get(workflow_type, self.workflow_templates["standard"])
        
        # Create workflow steps
        workflow_steps = []
        for step_template in template:
            step_id = f"STEP_{uuid.uuid4().hex[:8]}"
            due_date = datetime.now() + timedelta(hours=step_template["due_hours"])
            
            step = WorkflowStep(
                step_id=step_id,
                stage=step_template["stage"],
                description=step_template["description"],
                assigned_to=step_template["assigned_to"],
                due_date=due_date,
                auto_triggered=step_template["auto_triggered"]
            )
            workflow_steps.append(step)
        
        # Create workflow
        workflow = AdmissionWorkflow(
            workflow_id=workflow_id,
            application_id=application_id,
            applicant_email=applicant_email,
            current_stage=WorkflowStage.APPLICATION_SUBMITTED,
            workflow_steps=workflow_steps,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            estimated_completion_date=datetime.now() + timedelta(days=12)  # 12 days for standard workflow
        )
        
        self.admission_workflows[workflow_id] = workflow
        
        # Start first step
        self._execute_workflow_step(workflow_id, WorkflowStage.APPLICATION_SUBMITTED)
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "application_id": application_id,
            "current_stage": WorkflowStage.APPLICATION_SUBMITTED.value,
            "estimated_completion_date": workflow.estimated_completion_date.isoformat(),
            "total_steps": len(workflow_steps),
            "message": "Admission workflow initiated successfully"
        }
    
    def _execute_workflow_step(self, workflow_id: str, stage: WorkflowStage) -> Dict[str, Any]:
        """Execute specific workflow step"""
        
        workflow = self.admission_workflows.get(workflow_id)
        if not workflow:
            return {"success": False, "error": "Workflow not found"}
        
        # Find step
        step = next((s for s in workflow.workflow_steps if s.stage == stage), None)
        if not step:
            return {"success": False, "error": "Step not found"}
        
        # Update step status
        step.status = "in_progress"
        workflow.updated_at = datetime.now()
        
        # Execute step based on stage
        if stage == WorkflowStage.APPLICATION_SUBMITTED:
            result = self._execute_application_submitted(workflow)
        elif stage == WorkflowStage.INITIAL_REVIEW:
            result = self._execute_initial_review(workflow)
        elif stage == WorkflowStage.DOCUMENT_VERIFICATION:
            result = self._execute_document_verification(workflow)
        elif stage == WorkflowStage.AI_EVALUATION:
            result = self._execute_ai_evaluation(workflow)
        elif stage == WorkflowStage.HUMAN_REVIEW:
            result = self._execute_human_review(workflow)
        elif stage == WorkflowStage.DECISION_MADE:
            result = self._execute_decision_made(workflow)
        elif stage == WorkflowStage.DECISION_COMMUNICATED:
            result = self._execute_decision_communicated(workflow)
        elif stage == WorkflowStage.ENROLLMENT_PROCESSING:
            result = self._execute_enrollment_processing(workflow)
        elif stage == WorkflowStage.ENROLLMENT_COMPLETED:
            result = self._execute_enrollment_completed(workflow)
        else:
            result = {"success": True, "message": f"Step {stage.value} executed"}
        
        # Update step completion
        if result["success"]:
            step.status = "completed"
            step.completed_at = datetime.now()
            workflow.current_stage = stage
            
            # Trigger next step if auto-triggered
            self._trigger_next_step(workflow_id, stage)
        else:
            step.status = "failed"
            step.notes = result.get("error", "Step execution failed")
        
        return result
    
    def _execute_application_submitted(self, workflow: AdmissionWorkflow) -> Dict[str, Any]:
        """Execute application submitted step"""
        
        # Send confirmation notification
        notification = {
            "type": NotificationType.EMAIL.value,
            "recipient": workflow.applicant_email,
            "subject": "Application Received - MS AI Program",
            "message": "Your application has been received and is being processed.",
            "sent_at": datetime.now().isoformat()
        }
        
        workflow.notifications_sent.append(notification)
        
        return {
            "success": True,
            "message": "Application submission confirmed",
            "notification_sent": True
        }
    
    def _execute_initial_review(self, workflow: AdmissionWorkflow) -> Dict[str, Any]:
        """Execute initial review step"""
        
        # Simulate initial review
        application_data = self._get_application_data(workflow.application_id)
        
        # Check completeness
        required_sections = ["personal_info", "academic_background", "work_experience", "technical_skills", "personal_statement"]
        missing_sections = [section for section in required_sections if section not in application_data]
        
        if missing_sections:
            return {
                "success": False,
                "error": f"Application incomplete. Missing sections: {', '.join(missing_sections)}"
            }
        
        # Check document requirements
        required_documents = ["transcript", "personal_statement"]
        # This would check actual document uploads
        
        return {
            "success": True,
            "message": "Initial review completed - application is complete",
            "review_notes": "Application meets initial requirements"
        }
    
    def _execute_document_verification(self, workflow: AdmissionWorkflow) -> Dict[str, Any]:
        """Execute document verification step"""
        
        # Simulate document verification
        verification_results = {
            "transcript": {"verified": True, "notes": "Official transcript received"},
            "personal_statement": {"verified": True, "notes": "Personal statement submitted"},
            "recommendation_letters": {"verified": False, "notes": "Pending submission"}
        }
        
        return {
            "success": True,
            "message": "Document verification completed",
            "verification_results": verification_results
        }
    
    def _execute_ai_evaluation(self, workflow: AdmissionWorkflow) -> Dict[str, Any]:
        """Execute AI evaluation step"""
        
        if not self.evaluation_system:
            return {
                "success": False,
                "error": "Evaluation system not available"
            }
        
        # Get application data
        application_data = self._get_application_data(workflow.application_id)
        
        # Perform evaluation
        evaluation_result = self.evaluation_system.evaluate_application(
            workflow.application_id, application_data
        )
        
        if evaluation_result["success"]:
            # Store evaluation result
            workflow.workflow_steps[3].notes = f"AI Evaluation Score: {evaluation_result['overall_score']:.1f}, Recommendation: {evaluation_result['recommendation']}"
            
            return {
                "success": True,
                "message": "AI evaluation completed",
                "evaluation_id": evaluation_result["evaluation_id"],
                "overall_score": evaluation_result["overall_score"],
                "recommendation": evaluation_result["recommendation"]
            }
        else:
            return {
                "success": False,
                "error": "AI evaluation failed"
            }
    
    def _execute_human_review(self, workflow: AdmissionWorkflow) -> Dict[str, Any]:
        """Execute human review step"""
        
        # This would typically involve human reviewers
        # For simulation, we'll use AI evaluation results
        
        evaluation_step = next((s for s in workflow.workflow_steps if s.stage == WorkflowStage.AI_EVALUATION), None)
        if not evaluation_step or not evaluation_step.notes:
            return {
                "success": False,
                "error": "AI evaluation not completed"
            }
        
        # Simulate human review
        review_notes = "Human review completed. AI evaluation results validated. Application shows strong potential."
        
        return {
            "success": True,
            "message": "Human review completed",
            "review_notes": review_notes
        }
    
    def _execute_decision_made(self, workflow: AdmissionWorkflow) -> Dict[str, Any]:
        """Execute decision made step"""
        
        # Get evaluation results
        evaluation_step = next((s for s in workflow.workflow_steps if s.stage == WorkflowStage.AI_EVALUATION), None)
        
        if evaluation_step and evaluation_step.notes:
            # Extract recommendation from notes
            if "Recommendation: accept" in evaluation_step.notes:
                decision = DecisionType.ACCEPT
                decision_reason = "Strong academic background and technical competency"
            elif "Recommendation: waitlist" in evaluation_step.notes:
                decision = DecisionType.WAITLIST
                decision_reason = "Good qualifications but limited spots available"
            else:
                decision = DecisionType.REJECT
                decision_reason = "Does not meet minimum requirements"
        else:
            decision = DecisionType.REJECT
            decision_reason = "Incomplete evaluation"
        
        # Update workflow
        workflow.decision = decision
        workflow.decision_reason = decision_reason
        workflow.decision_date = datetime.now()
        
        return {
            "success": True,
            "message": "Decision made",
            "decision": decision.value,
            "decision_reason": decision_reason
        }
    
    def _execute_decision_communicated(self, workflow: AdmissionWorkflow) -> Dict[str, Any]:
        """Execute decision communication step"""
        
        if not workflow.decision:
            return {
                "success": False,
                "error": "No decision made yet"
            }
        
        # Send decision notification
        if workflow.decision == DecisionType.ACCEPT:
            subject = "Congratulations! You've been accepted to the MS AI Program"
            message = f"Congratulations! We are pleased to inform you that you have been accepted to the MS AI Program. {workflow.decision_reason}"
        elif workflow.decision == DecisionType.WAITLIST:
            subject = "Application Status Update - Waitlist"
            message = f"Thank you for your application. You have been placed on our waitlist. {workflow.decision_reason}"
        else:
            subject = "Application Decision - MS AI Program"
            message = f"Thank you for your application. Unfortunately, we are unable to offer you admission at this time. {workflow.decision_reason}"
        
        notification = {
            "type": NotificationType.EMAIL.value,
            "recipient": workflow.applicant_email,
            "subject": subject,
            "message": message,
            "sent_at": datetime.now().isoformat()
        }
        
        workflow.notifications_sent.append(notification)
        
        return {
            "success": True,
            "message": "Decision communicated",
            "notification_sent": True,
            "decision": workflow.decision.value
        }
    
    def _execute_enrollment_processing(self, workflow: AdmissionWorkflow) -> Dict[str, Any]:
        """Execute enrollment processing step"""
        
        if workflow.decision != DecisionType.ACCEPT:
            return {
                "success": False,
                "error": "Only accepted students can be enrolled"
            }
        
        # Create enrollment data
        enrollment_id = f"ENROLL_{uuid.uuid4().hex[:8]}"
        student_id = f"STUDENT_{uuid.uuid4().hex[:8]}"
        
        enrollment = EnrollmentData(
            enrollment_id=enrollment_id,
            application_id=workflow.application_id,
            student_id=student_id,
            program="MS AI",
            start_term="Fall 2024",
            enrollment_date=datetime.now(),
            status="enrolled"
        )
        
        self.enrollment_data[enrollment_id] = enrollment
        
        # Create user account
        if self.user_manager:
            user_result = self.user_manager.create_user(
                email=workflow.applicant_email,
                password="temp_password_123",  # Would be generated securely
                first_name="Student",  # Would be extracted from application
                last_name="Name",
                role="student"
            )
        
        return {
            "success": True,
            "message": "Enrollment processing completed",
            "enrollment_id": enrollment_id,
            "student_id": student_id,
            "program": enrollment.program,
            "start_term": enrollment.start_term
        }
    
    def _execute_enrollment_completed(self, workflow: AdmissionWorkflow) -> Dict[str, Any]:
        """Execute enrollment completion step"""
        
        # Find enrollment data
        enrollment = next((e for e in self.enrollment_data.values() if e.application_id == workflow.application_id), None)
        
        if not enrollment:
            return {
                "success": False,
                "error": "Enrollment data not found"
            }
        
        # Send welcome notification
        notification = {
            "type": NotificationType.EMAIL.value,
            "recipient": workflow.applicant_email,
            "subject": "Welcome to the MS AI Program!",
            "message": f"Welcome to the MS AI Program! Your enrollment is complete. Student ID: {enrollment.student_id}",
            "sent_at": datetime.now().isoformat()
        }
        
        workflow.notifications_sent.append(notification)
        
        return {
            "success": True,
            "message": "Enrollment completed",
            "student_id": enrollment.student_id,
            "welcome_notification_sent": True
        }
    
    def _trigger_next_step(self, workflow_id: str, current_stage: WorkflowStage):
        """Trigger next step in workflow"""
        
        workflow = self.admission_workflows.get(workflow_id)
        if not workflow:
            return
        
        # Find next step
        current_index = None
        for i, step in enumerate(workflow.workflow_steps):
            if step.stage == current_stage:
                current_index = i
                break
        
        if current_index is not None and current_index < len(workflow.workflow_steps) - 1:
            next_step = workflow.workflow_steps[current_index + 1]
            if next_step.auto_triggered:
                # Schedule next step execution
                self._execute_workflow_step(workflow_id, next_step.stage)
    
    def _get_application_data(self, application_id: str) -> Dict[str, Any]:
        """Get application data for processing"""
        
        # This would typically fetch from application portal
        # For simulation, return sample data
        return {
            "personal_info": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com"
            },
            "academic_background": {
                "gpa": 3.7,
                "major": "Computer Science",
                "institution": "University of Florida"
            },
            "work_experience": {
                "years_experience": 2,
                "programming_languages": "Python, Java, JavaScript",
                "ai_ml_experience": "Machine learning projects"
            },
            "technical_skills": {
                "programming_proficiency": "Advanced",
                "ai_ml_knowledge": "Intermediate"
            },
            "personal_statement": {
                "motivation": "I am passionate about artificial intelligence and want to advance my career in this field.",
                "career_goals": "I want to become a machine learning engineer and contribute to AI research."
            }
        }
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow status and progress"""
        
        workflow = self.admission_workflows.get(workflow_id)
        if not workflow:
            return {"error": "Workflow not found"}
        
        # Calculate progress
        completed_steps = len([s for s in workflow.workflow_steps if s.status == "completed"])
        total_steps = len(workflow.workflow_steps)
        progress_percentage = (completed_steps / total_steps) * 100
        
        # Get current step
        current_step = next((s for s in workflow.workflow_steps if s.stage == workflow.current_stage), None)
        
        return {
            "workflow_id": workflow_id,
            "application_id": workflow.application_id,
            "applicant_email": workflow.applicant_email,
            "current_stage": workflow.current_stage.value,
            "progress_percentage": progress_percentage,
            "completed_steps": completed_steps,
            "total_steps": total_steps,
            "current_step": {
                "stage": current_step.stage.value if current_step else None,
                "description": current_step.description if current_step else None,
                "assigned_to": current_step.assigned_to if current_step else None,
                "due_date": current_step.due_date.isoformat() if current_step else None,
                "status": current_step.status if current_step else None
            },
            "decision": workflow.decision.value if workflow.decision else None,
            "decision_reason": workflow.decision_reason,
            "decision_date": workflow.decision_date.isoformat() if workflow.decision_date else None,
            "estimated_completion_date": workflow.estimated_completion_date.isoformat() if workflow.estimated_completion_date else None,
            "created_at": workflow.created_at.isoformat(),
            "updated_at": workflow.updated_at.isoformat(),
            "notifications_sent": len(workflow.notifications_sent)
        }
    
    def get_workflow_analytics(self) -> Dict[str, Any]:
        """Get workflow analytics and statistics"""
        
        total_workflows = len(self.admission_workflows)
        
        if total_workflows == 0:
            return {"message": "No workflows completed yet"}
        
        # Stage distribution
        stage_counts = {}
        for stage in WorkflowStage:
            stage_counts[stage.value] = len([wf for wf in self.admission_workflows.values() if wf.current_stage == stage])
        
        # Decision distribution
        decision_counts = {}
        for decision in DecisionType:
            decision_counts[decision.value] = len([wf for wf in self.admission_workflows.values() if wf.decision == decision])
        
        # Completion times
        completed_workflows = [wf for wf in self.admission_workflows.values() if wf.decision is not None]
        completion_times = []
        for wf in completed_workflows:
            if wf.decision_date:
                completion_time = (wf.decision_date - wf.created_at).total_seconds() / 3600  # hours
                completion_times.append(completion_time)
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        # Enrollment statistics
        total_enrollments = len(self.enrollment_data)
        successful_enrollments = len([e for e in self.enrollment_data.values() if e.status == "enrolled"])
        
        return {
            "total_workflows": total_workflows,
            "stage_distribution": stage_counts,
            "decision_distribution": decision_counts,
            "completion_statistics": {
                "completed_workflows": len(completed_workflows),
                "average_completion_time_hours": avg_completion_time,
                "fastest_completion_hours": min(completion_times) if completion_times else 0,
                "slowest_completion_hours": max(completion_times) if completion_times else 0
            },
            "enrollment_statistics": {
                "total_enrollments": total_enrollments,
                "successful_enrollments": successful_enrollments,
                "enrollment_rate": (successful_enrollments / total_workflows * 100) if total_workflows > 0 else 0
            },
            "workflow_efficiency": {
                "average_steps_completed": sum(len([s for s in wf.workflow_steps if s.status == "completed"]) for wf in self.admission_workflows.values()) / total_workflows,
                "auto_triggered_steps": sum(len([s for s in wf.workflow_steps if s.auto_triggered]) for wf in self.admission_workflows.values()),
                "manual_steps": sum(len([s for s in wf.workflow_steps if not s.auto_triggered]) for wf in self.admission_workflows.values())
            }
        }
    
    def get_enrollment_data(self, enrollment_id: str) -> Dict[str, Any]:
        """Get enrollment data"""
        
        enrollment = self.enrollment_data.get(enrollment_id)
        if not enrollment:
            return {"error": "Enrollment not found"}
        
        return {
            "enrollment_id": enrollment_id,
            "application_id": enrollment.application_id,
            "student_id": enrollment.student_id,
            "program": enrollment.program,
            "start_term": enrollment.start_term,
            "enrollment_date": enrollment.enrollment_date.isoformat(),
            "status": enrollment.status,
            "tuition_deposit_paid": enrollment.tuition_deposit_paid,
            "orientation_completed": enrollment.orientation_completed,
            "advisor_assigned": enrollment.advisor_assigned
        }