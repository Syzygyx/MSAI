"""
MS AI Curriculum System - Admissions Process
Comprehensive application, evaluation, and decision workflow
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid

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

class EvaluationCriteria(Enum):
    ACADEMIC_RECORD = "academic_record"
    WORK_EXPERIENCE = "work_experience"
    PERSONAL_STATEMENT = "personal_statement"
    LETTERS_OF_RECOMMENDATION = "letters_of_recommendation"
    TECHNICAL_SKILLS = "technical_skills"
    RESEARCH_EXPERIENCE = "research_experience"
    LEADERSHIP_EXPERIENCE = "leadership_experience"
    DIVERSITY_FACTORS = "diversity_factors"

class DecisionType(Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    WAITLIST = "waitlist"
    CONDITIONAL_ACCEPT = "conditional_accept"

@dataclass
class Application:
    """Student application for MS AI program"""
    application_id: str
    applicant_email: str
    personal_info: Dict[str, Any]
    academic_background: Dict[str, Any]
    work_experience: List[Dict[str, Any]]
    technical_skills: Dict[str, Any]
    personal_statement: str
    research_interests: List[str]
    career_goals: str
    letters_of_recommendation: List[Dict[str, Any]]
    test_scores: Dict[str, Any]
    status: ApplicationStatus
    created_at: datetime
    submitted_at: Optional[datetime] = None
    evaluation_notes: List[Dict[str, Any]] = field(default_factory=list)
    decision: Optional[Dict[str, Any]] = None
    interview_scheduled: Optional[datetime] = None
    interview_completed: Optional[datetime] = None

@dataclass
class Evaluation:
    """Application evaluation by admissions committee"""
    evaluation_id: str
    application_id: str
    evaluator_id: str
    criteria_scores: Dict[EvaluationCriteria, float]
    overall_score: float
    recommendation: DecisionType
    comments: str
    evaluated_at: datetime
    is_final: bool = False

@dataclass
class AdmissionsAgent:
    """AI Agent specialized for admissions tasks"""
    agent_id: str
    name: str
    specialization: str
    capabilities: List[str]
    status: str = "active"
    last_activity: Optional[datetime] = None
    evaluations_completed: int = 0

class AdmissionsSystem:
    """Comprehensive admissions management system"""
    
    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.applications: Dict[str, Application] = {}
        self.evaluations: Dict[str, Evaluation] = {}
        self.admissions_agents = self._initialize_admissions_agents()
        self.admission_criteria = self._initialize_admission_criteria()
        
    def _initialize_admissions_agents(self) -> List[AdmissionsAgent]:
        """Initialize AI agents for admissions tasks"""
        agents = [
            AdmissionsAgent(
                agent_id="ADMISSIONS_AGENT_001",
                name="Application Reviewer Agent",
                specialization="application_screening",
                capabilities=[
                    "application_completeness_check",
                    "academic_record_analysis",
                    "technical_skills_assessment",
                    "personal_statement_evaluation"
                ]
            ),
            AdmissionsAgent(
                agent_id="ADMISSIONS_AGENT_002",
                name="Academic Evaluator Agent",
                specialization="academic_assessment",
                capabilities=[
                    "gpa_analysis",
                    "course_relevance_evaluation",
                    "prerequisite_verification",
                    "academic_trend_analysis"
                ]
            ),
            AdmissionsAgent(
                agent_id="ADMISSIONS_AGENT_003",
                name="Experience Analyzer Agent",
                specialization="experience_evaluation",
                capabilities=[
                    "work_experience_assessment",
                    "research_experience_evaluation",
                    "leadership_experience_analysis",
                    "project_portfolio_review"
                ]
            ),
            AdmissionsAgent(
                agent_id="ADMISSIONS_AGENT_004",
                name="Diversity and Inclusion Agent",
                specialization="diversity_assessment",
                capabilities=[
                    "diversity_factor_analysis",
                    "inclusion_contribution_assessment",
                    "equity_consideration_evaluation",
                    "holistic_review_support"
                ]
            )
        ]
        return agents
    
    def _initialize_admission_criteria(self) -> Dict[str, Any]:
        """Initialize admission criteria and weights"""
        return {
            "minimum_requirements": {
                "gpa": 3.0,
                "prerequisites_completed": True,
                "personal_statement_word_count": 500,
                "letters_of_recommendation": 3
            },
            "evaluation_weights": {
                EvaluationCriteria.ACADEMIC_RECORD: 0.30,
                EvaluationCriteria.TECHNICAL_SKILLS: 0.25,
                EvaluationCriteria.PERSONAL_STATEMENT: 0.20,
                EvaluationCriteria.WORK_EXPERIENCE: 0.15,
                EvaluationCriteria.LETTERS_OF_RECOMMENDATION: 0.10
            },
            "bonus_factors": {
                EvaluationCriteria.RESEARCH_EXPERIENCE: 0.05,
                EvaluationCriteria.LEADERSHIP_EXPERIENCE: 0.05,
                EvaluationCriteria.DIVERSITY_FACTORS: 0.05
            }
        }
    
    def create_application(self, applicant_email: str, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new application"""
        application_id = f"APP_{uuid.uuid4().hex[:8].upper()}"
        
        application = Application(
            application_id=application_id,
            applicant_email=applicant_email,
            personal_info=application_data.get("personal_info", {}),
            academic_background=application_data.get("academic_background", {}),
            work_experience=application_data.get("work_experience", []),
            technical_skills=application_data.get("technical_skills", {}),
            personal_statement=application_data.get("personal_statement", ""),
            research_interests=application_data.get("research_interests", []),
            career_goals=application_data.get("career_goals", ""),
            letters_of_recommendation=application_data.get("letters_of_recommendation", []),
            test_scores=application_data.get("test_scores", {}),
            status=ApplicationStatus.DRAFT,
            created_at=datetime.now()
        )
        
        self.applications[application_id] = application
        
        return {
            "success": True,
            "application_id": application_id,
            "message": "Application created successfully"
        }
    
    def submit_application(self, application_id: str) -> Dict[str, Any]:
        """Submit application for review"""
        application = self.applications.get(application_id)
        if not application:
            return {"success": False, "error": "Application not found"}
        
        # Validate application completeness
        validation_result = self._validate_application(application)
        if not validation_result["is_valid"]:
            return {
                "success": False,
                "error": "Application incomplete",
                "missing_fields": validation_result["missing_fields"]
            }
        
        # Update application status
        application.status = ApplicationStatus.SUBMITTED
        application.submitted_at = datetime.now()
        
        # Start automated evaluation
        self._initiate_automated_evaluation(application_id)
        
        return {
            "success": True,
            "message": "Application submitted successfully",
            "next_steps": "Your application is now under review. You will be notified of the decision within 2-3 weeks."
        }
    
    def _validate_application(self, application: Application) -> Dict[str, Any]:
        """Validate application completeness"""
        missing_fields = []
        
        # Check required fields
        if not application.personal_info.get("first_name"):
            missing_fields.append("First name")
        if not application.personal_info.get("last_name"):
            missing_fields.append("Last name")
        if not application.personal_info.get("phone"):
            missing_fields.append("Phone number")
        if not application.personal_info.get("address"):
            missing_fields.append("Address")
        
        if not application.academic_background.get("degree"):
            missing_fields.append("Academic degree")
        if not application.academic_background.get("gpa"):
            missing_fields.append("GPA")
        if not application.academic_background.get("institution"):
            missing_fields.append("Institution name")
        
        if len(application.personal_statement) < 500:
            missing_fields.append("Personal statement (minimum 500 words)")
        
        if len(application.letters_of_recommendation) < 3:
            missing_fields.append("Letters of recommendation (minimum 3)")
        
        if not application.technical_skills.get("programming_languages"):
            missing_fields.append("Programming languages")
        
        return {
            "is_valid": len(missing_fields) == 0,
            "missing_fields": missing_fields
        }
    
    def _initiate_automated_evaluation(self, application_id: str):
        """Initiate automated evaluation using AI agents"""
        application = self.applications[application_id]
        
        # Update status
        application.status = ApplicationStatus.UNDER_REVIEW
        
        # Create evaluations for each agent
        for agent in self.admissions_agents:
            evaluation_id = f"EVAL_{uuid.uuid4().hex[:8].upper()}"
            
            # Generate evaluation based on agent specialization
            if agent.specialization == "application_screening":
                scores, recommendation, comments = self._evaluate_application_screening(application)
            elif agent.specialization == "academic_assessment":
                scores, recommendation, comments = self._evaluate_academic_record(application)
            elif agent.specialization == "experience_evaluation":
                scores, recommendation, comments = self._evaluate_experience(application)
            elif agent.specialization == "diversity_assessment":
                scores, recommendation, comments = self._evaluate_diversity_factors(application)
            else:
                scores, recommendation, comments = self._evaluate_general(application)
            
            evaluation = Evaluation(
                evaluation_id=evaluation_id,
                application_id=application_id,
                evaluator_id=agent.agent_id,
                criteria_scores=scores,
                overall_score=sum(scores.values()) / len(scores),
                recommendation=recommendation,
                comments=comments,
                evaluated_at=datetime.now()
            )
            
            self.evaluations[evaluation_id] = evaluation
            agent.evaluations_completed += 1
            agent.last_activity = datetime.now()
    
    def _evaluate_application_screening(self, application: Application) -> tuple:
        """Evaluate application completeness and quality"""
        scores = {}
        
        # Personal statement quality
        statement_score = min(10, len(application.personal_statement) / 50)  # Based on length
        scores[EvaluationCriteria.PERSONAL_STATEMENT] = statement_score
        
        # Technical skills assessment
        tech_score = 0
        if application.technical_skills.get("programming_languages"):
            languages = application.technical_skills["programming_languages"]
            tech_score += min(5, len(languages) * 1.5)
        if application.technical_skills.get("ai_ml_experience"):
            tech_score += 3
        if application.technical_skills.get("projects"):
            tech_score += 2
        scores[EvaluationCriteria.TECHNICAL_SKILLS] = min(10, tech_score)
        
        # Overall recommendation
        avg_score = sum(scores.values()) / len(scores)
        if avg_score >= 7:
            recommendation = DecisionType.ACCEPT
        elif avg_score >= 5:
            recommendation = DecisionType.WAITLIST
        else:
            recommendation = DecisionType.REJECT
        
        comments = f"Application screening completed. Technical skills: {tech_score}/10, Personal statement: {statement_score}/10"
        
        return scores, recommendation, comments
    
    def _evaluate_academic_record(self, application: Application) -> tuple:
        """Evaluate academic background"""
        scores = {}
        
        # GPA evaluation
        gpa = application.academic_background.get("gpa", 0)
        if gpa >= 3.7:
            gpa_score = 10
        elif gpa >= 3.5:
            gpa_score = 8
        elif gpa >= 3.3:
            gpa_score = 6
        elif gpa >= 3.0:
            gpa_score = 4
        else:
            gpa_score = 2
        scores[EvaluationCriteria.ACADEMIC_RECORD] = gpa_score
        
        # Prerequisites check
        prereq_score = 0
        if application.academic_background.get("prerequisites_completed"):
            prereq_score = 10
        scores[EvaluationCriteria.TECHNICAL_SKILLS] = prereq_score
        
        # Overall recommendation
        avg_score = sum(scores.values()) / len(scores)
        if avg_score >= 8:
            recommendation = DecisionType.ACCEPT
        elif avg_score >= 6:
            recommendation = DecisionType.WAITLIST
        else:
            recommendation = DecisionType.REJECT
        
        comments = f"Academic evaluation: GPA {gpa} ({gpa_score}/10), Prerequisites {'completed' if prereq_score == 10 else 'incomplete'}"
        
        return scores, recommendation, comments
    
    def _evaluate_experience(self, application: Application) -> tuple:
        """Evaluate work and research experience"""
        scores = {}
        
        # Work experience
        work_score = 0
        for exp in application.work_experience:
            years = exp.get("years", 0)
            if exp.get("ai_ml_relevant", False):
                work_score += years * 2
            else:
                work_score += years * 1
        scores[EvaluationCriteria.WORK_EXPERIENCE] = min(10, work_score)
        
        # Research experience
        research_score = 0
        if application.research_interests:
            research_score += len(application.research_interests) * 2
        if any(exp.get("research", False) for exp in application.work_experience):
            research_score += 5
        scores[EvaluationCriteria.RESEARCH_EXPERIENCE] = min(10, research_score)
        
        # Overall recommendation
        avg_score = sum(scores.values()) / len(scores)
        if avg_score >= 7:
            recommendation = DecisionType.ACCEPT
        elif avg_score >= 5:
            recommendation = DecisionType.WAITLIST
        else:
            recommendation = DecisionType.REJECT
        
        comments = f"Experience evaluation: Work experience {work_score}/10, Research experience {research_score}/10"
        
        return scores, recommendation, comments
    
    def _evaluate_diversity_factors(self, application: Application) -> tuple:
        """Evaluate diversity and inclusion factors"""
        scores = {}
        
        # Diversity factors
        diversity_score = 5  # Base score
        personal_info = application.personal_info
        
        # Underrepresented groups
        if personal_info.get("underrepresented_group"):
            diversity_score += 3
        
        # First generation college student
        if personal_info.get("first_generation"):
            diversity_score += 2
        
        # International student
        if personal_info.get("international_student"):
            diversity_score += 2
        
        # Leadership experience
        if any(exp.get("leadership", False) for exp in application.work_experience):
            diversity_score += 2
        
        scores[EvaluationCriteria.DIVERSITY_FACTORS] = min(10, diversity_score)
        
        # Overall recommendation
        if diversity_score >= 8:
            recommendation = DecisionType.ACCEPT
        elif diversity_score >= 6:
            recommendation = DecisionType.WAITLIST
        else:
            recommendation = DecisionType.REJECT
        
        comments = f"Diversity evaluation: Score {diversity_score}/10 based on background and experiences"
        
        return scores, recommendation, comments
    
    def _evaluate_general(self, application: Application) -> tuple:
        """General evaluation fallback"""
        scores = {
            EvaluationCriteria.ACADEMIC_RECORD: 5,
            EvaluationCriteria.TECHNICAL_SKILLS: 5,
            EvaluationCriteria.PERSONAL_STATEMENT: 5
        }
        
        recommendation = DecisionType.WAITLIST
        comments = "General evaluation completed"
        
        return scores, recommendation, comments
    
    def get_application_status(self, application_id: str) -> Dict[str, Any]:
        """Get application status and progress"""
        application = self.applications.get(application_id)
        if not application:
            return {"error": "Application not found"}
        
        # Get evaluations for this application
        app_evaluations = [
            eval for eval in self.evaluations.values() 
            if eval.application_id == application_id
        ]
        
        return {
            "application_id": application_id,
            "status": application.status.value,
            "created_at": application.created_at.isoformat(),
            "submitted_at": application.submitted_at.isoformat() if application.submitted_at else None,
            "evaluations_completed": len(app_evaluations),
            "total_evaluators": len(self.admissions_agents),
            "decision": application.decision,
            "next_steps": self._get_next_steps(application.status)
        }
    
    def _get_next_steps(self, status: ApplicationStatus) -> str:
        """Get next steps based on application status"""
        next_steps_map = {
            ApplicationStatus.DRAFT: "Complete all required fields and submit your application",
            ApplicationStatus.SUBMITTED: "Your application is being reviewed by our admissions committee",
            ApplicationStatus.UNDER_REVIEW: "AI agents are evaluating your application",
            ApplicationStatus.INTERVIEW_SCHEDULED: "Prepare for your interview",
            ApplicationStatus.INTERVIEW_COMPLETED: "Interview completed, final decision pending",
            ApplicationStatus.EVALUATION_COMPLETE: "Evaluation complete, decision will be communicated soon",
            ApplicationStatus.ACCEPTED: "Congratulations! Complete enrollment process",
            ApplicationStatus.REJECTED: "Application not accepted for this term",
            ApplicationStatus.WAITLISTED: "You are on the waitlist, we will notify you if a spot opens"
        }
        return next_steps_map.get(status, "Status update pending")
    
    def make_admission_decision(self, application_id: str, decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make final admission decision"""
        application = self.applications.get(application_id)
        if not application:
            return {"success": False, "error": "Application not found"}
        
        # Get all evaluations for this application
        app_evaluations = [
            eval for eval in self.evaluations.values() 
            if eval.application_id == application_id
        ]
        
        if len(app_evaluations) < len(self.admissions_agents):
            return {"success": False, "error": "Not all evaluations completed"}
        
        # Calculate overall recommendation
        recommendations = [eval.recommendation for eval in app_evaluations]
        accept_count = recommendations.count(DecisionType.ACCEPT)
        reject_count = recommendations.count(DecisionType.REJECT)
        
        # Make decision based on majority
        if accept_count > reject_count:
            final_decision = DecisionType.ACCEPT
            application.status = ApplicationStatus.ACCEPTED
        elif reject_count > accept_count:
            final_decision = DecisionType.REJECT
            application.status = ApplicationStatus.REJECTED
        else:
            final_decision = DecisionType.WAITLIST
            application.status = ApplicationStatus.WAITLISTED
        
        # Store decision
        application.decision = {
            "decision": final_decision.value,
            "decision_date": datetime.now().isoformat(),
            "decision_maker": decision_data.get("decision_maker", "Admissions Committee"),
            "comments": decision_data.get("comments", ""),
            "evaluation_summary": {
                "total_evaluations": len(app_evaluations),
                "accept_recommendations": accept_count,
                "reject_recommendations": reject_count,
                "average_score": sum(eval.overall_score for eval in app_evaluations) / len(app_evaluations)
            }
        }
        
        return {
            "success": True,
            "decision": final_decision.value,
            "message": f"Application {final_decision.value}",
            "decision_details": application.decision
        }
    
    def get_admissions_dashboard(self) -> Dict[str, Any]:
        """Get admissions dashboard data"""
        total_applications = len(self.applications)
        submitted_applications = len([app for app in self.applications.values() if app.status != ApplicationStatus.DRAFT])
        
        status_counts = {}
        for status in ApplicationStatus:
            status_counts[status.value] = len([app for app in self.applications.values() if app.status == status])
        
        recent_applications = sorted(
            [app for app in self.applications.values() if app.submitted_at],
            key=lambda x: x.submitted_at,
            reverse=True
        )[:10]
        
        return {
            "total_applications": total_applications,
            "submitted_applications": submitted_applications,
            "status_distribution": status_counts,
            "recent_applications": [
                {
                    "application_id": app.application_id,
                    "applicant_email": app.applicant_email,
                    "status": app.status.value,
                    "submitted_at": app.submitted_at.isoformat() if app.submitted_at else None
                }
                for app in recent_applications
            ],
            "ai_agent_status": {
                "total_agents": len(self.admissions_agents),
                "active_agents": len([a for a in self.admissions_agents if a.status == "active"]),
                "total_evaluations": sum(a.evaluations_completed for a in self.admissions_agents)
            },
            "admission_statistics": {
                "acceptance_rate": self._calculate_acceptance_rate(),
                "average_evaluation_time": self._calculate_average_evaluation_time(),
                "pending_decisions": len([app for app in self.applications.values() if app.status == ApplicationStatus.EVALUATION_COMPLETE])
            }
        }
    
    def _calculate_acceptance_rate(self) -> float:
        """Calculate acceptance rate"""
        decided_applications = [app for app in self.applications.values() if app.decision]
        if not decided_applications:
            return 0.0
        
        accepted_count = len([app for app in decided_applications if app.decision["decision"] == "accept"])
        return (accepted_count / len(decided_applications)) * 100
    
    def _calculate_average_evaluation_time(self) -> float:
        """Calculate average evaluation time"""
        evaluations_with_time = [
            eval for eval in self.evaluations.values() 
            if eval.evaluated_at
        ]
        
        if not evaluations_with_time:
            return 0.0
        
        # This would need application submission time to calculate properly
        # For now, return a simulated value
        return 2.5  # days