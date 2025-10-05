"""
MS AI Curriculum System - Enhanced AI Assistant System
Comprehensive administrative and academic support with human-centered approach
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import random

class AssistantType(Enum):
    ACADEMIC_ADVISOR = "academic_advisor"
    TECHNICAL_SUPPORT = "technical_support"
    CAREER_COUNSELOR = "career_counselor"
    RESEARCH_ASSISTANT = "research_assistant"
    ADMINISTRATIVE_SUPPORT = "administrative_support"
    ACCESSIBILITY_COORDINATOR = "accessibility_coordinator"
    MENTAL_HEALTH_SUPPORT = "mental_health_support"
    FINANCIAL_AID_ADVISOR = "financial_aid_advisor"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ESCALATED = "escalated"

class RequestCategory(Enum):
    ACADEMIC = "academic"
    TECHNICAL = "technical"
    ADMINISTRATIVE = "administrative"
    PERSONAL = "personal"
    EMERGENCY = "emergency"
    INFORMATION = "information"

@dataclass
class StudentRequest:
    """Student request for assistance"""
    request_id: str
    student_id: str
    category: RequestCategory
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    assigned_assistant: Optional[str]
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    resolution_notes: str = ""
    student_satisfaction: Optional[float] = None
    tags: List[str] = field(default_factory=list)
    attachments: List[str] = field(default_factory=list)

@dataclass
class Task:
    """Task for AI Assistant"""
    task_id: str
    assistant_id: str
    request_id: str
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_duration_minutes: int = 0
    actual_duration_minutes: int = 0
    notes: str = ""
    resources_used: List[str] = field(default_factory=list)

@dataclass
class AIAssistant:
    """AI Assistant with specialized capabilities"""
    assistant_id: str
    name: str
    assistant_type: AssistantType
    specialization: str
    capabilities: List[str]
    personality_traits: List[str]
    communication_style: str
    expertise_level: str
    cultural_sensitivity: str
    language_support: List[str]
    availability_hours: Dict[str, List[int]]  # day: [start_hour, end_hour]
    status: str = "active"
    total_tasks_completed: int = 0
    average_response_time_minutes: float = 0.0
    student_satisfaction_rating: float = 0.0
    escalation_rate: float = 0.0

class EnhancedAIAssistantSystem:
    """Advanced AI Assistant system for comprehensive support"""
    
    def __init__(self, user_manager=None):
        self.user_manager = user_manager
        self.student_requests: Dict[str, StudentRequest] = {}
        self.tasks: Dict[str, Task] = {}
        self.ai_assistants = self._initialize_ai_assistants()
        self.knowledge_base = self._initialize_knowledge_base()
        
    def _initialize_ai_assistants(self) -> List[AIAssistant]:
        """Initialize AI assistants with specialized roles"""
        return [
            AIAssistant(
                assistant_id="ASSISTANT_001",
                name="Dr. Maya Academic",
                assistant_type=AssistantType.ACADEMIC_ADVISOR,
                specialization="Academic Planning and Course Selection",
                capabilities=[
                    "course_recommendation",
                    "degree_planning",
                    "prerequisite_checking",
                    "graduation_tracking",
                    "academic_policy_explanation",
                    "study_strategy_guidance"
                ],
                personality_traits=["supportive", "analytical", "patient", "encouraging"],
                communication_style="Warm and professional, with clear explanations and personalized guidance",
                expertise_level="expert",
                cultural_sensitivity="high",
                language_support=["English", "Spanish", "Mandarin"],
                availability_hours={
                    "monday": [9, 17], "tuesday": [9, 17], "wednesday": [9, 17],
                    "thursday": [9, 17], "friday": [9, 17], "saturday": [10, 14],
                    "sunday": []
                }
            ),
            AIAssistant(
                assistant_id="ASSISTANT_002",
                name="Tech Support Taylor",
                assistant_type=AssistantType.TECHNICAL_SUPPORT,
                specialization="Technical Issues and Platform Support",
                capabilities=[
                    "platform_troubleshooting",
                    "software_installation",
                    "hardware_support",
                    "network_issues",
                    "data_recovery",
                    "security_guidance"
                ],
                personality_traits=["patient", "methodical", "helpful", "tech-savvy"],
                communication_style="Clear and step-by-step, with technical accuracy and user-friendly explanations",
                expertise_level="expert",
                cultural_sensitivity="medium",
                language_support=["English"],
                availability_hours={
                    "monday": [8, 20], "tuesday": [8, 20], "wednesday": [8, 20],
                    "thursday": [8, 20], "friday": [8, 20], "saturday": [9, 17],
                    "sunday": [10, 16]
                }
            ),
            AIAssistant(
                assistant_id="ASSISTANT_003",
                name="Career Coach Carlos",
                assistant_type=AssistantType.CAREER_COUNSELOR,
                specialization="Career Development and Job Placement",
                capabilities=[
                    "career_assessment",
                    "resume_review",
                    "interview_preparation",
                    "job_search_strategy",
                    "industry_insights",
                    "networking_guidance"
                ],
                personality_traits=["motivational", "insightful", "connected", "optimistic"],
                communication_style="Inspiring and practical, with real-world insights and actionable advice",
                expertise_level="expert",
                cultural_sensitivity="high",
                language_support=["English", "Spanish"],
                availability_hours={
                    "monday": [10, 18], "tuesday": [10, 18], "wednesday": [10, 18],
                    "thursday": [10, 18], "friday": [10, 18], "saturday": [9, 15],
                    "sunday": []
                }
            ),
            AIAssistant(
                assistant_id="ASSISTANT_004",
                name="Research Assistant Riley",
                assistant_type=AssistantType.RESEARCH_ASSISTANT,
                specialization="Research Support and Academic Writing",
                capabilities=[
                    "literature_review",
                    "research_methodology",
                    "data_analysis_guidance",
                    "academic_writing",
                    "citation_management",
                    "research_ethics"
                ],
                personality_traits=["analytical", "thorough", "curious", "precise"],
                communication_style="Academic and precise, with attention to detail and scholarly standards",
                expertise_level="expert",
                cultural_sensitivity="medium",
                language_support=["English"],
                availability_hours={
                    "monday": [9, 17], "tuesday": [9, 17], "wednesday": [9, 17],
                    "thursday": [9, 17], "friday": [9, 17], "saturday": [10, 14],
                    "sunday": []
                }
            ),
            AIAssistant(
                assistant_id="ASSISTANT_005",
                name="Admin Assistant Alex",
                assistant_type=AssistantType.ADMINISTRATIVE_SUPPORT,
                specialization="Administrative Tasks and Documentation",
                capabilities=[
                    "enrollment_assistance",
                    "transcript_requests",
                    "financial_aid_guidance",
                    "policy_explanation",
                    "document_processing",
                    "deadline_tracking"
                ],
                personality_traits=["organized", "efficient", "helpful", "detail-oriented"],
                communication_style="Professional and efficient, with clear instructions and timely responses",
                expertise_level="expert",
                cultural_sensitivity="high",
                language_support=["English", "Spanish"],
                availability_hours={
                    "monday": [8, 17], "tuesday": [8, 17], "wednesday": [8, 17],
                    "thursday": [8, 17], "friday": [8, 17], "saturday": [9, 13],
                    "sunday": []
                }
            ),
            AIAssistant(
                assistant_id="ASSISTANT_006",
                name="Accessibility Advocate Avery",
                assistant_type=AssistantType.ACCESSIBILITY_COORDINATOR,
                specialization="Accessibility and Inclusive Learning",
                capabilities=[
                    "accessibility_assessment",
                    "accommodation_coordination",
                    "assistive_technology_guidance",
                    "inclusive_design_support",
                    "disability_advocacy",
                    "universal_design_principles"
                ],
                personality_traits=["inclusive", "advocate", "patient", "empathetic"],
                communication_style="Inclusive and supportive, with focus on accessibility and equal opportunities",
                expertise_level="expert",
                cultural_sensitivity="very_high",
                language_support=["English", "ASL"],
                availability_hours={
                    "monday": [9, 17], "tuesday": [9, 17], "wednesday": [9, 17],
                    "thursday": [9, 17], "friday": [9, 17], "saturday": [10, 14],
                    "sunday": []
                }
            ),
            AIAssistant(
                assistant_id="ASSISTANT_007",
                name="Wellness Counselor Willow",
                assistant_type=AssistantType.MENTAL_HEALTH_SUPPORT,
                specialization="Mental Health and Wellness Support",
                capabilities=[
                    "stress_management",
                    "anxiety_support",
                    "study_balance_guidance",
                    "wellness_resources",
                    "crisis_intervention",
                    "mental_health_referrals"
                ],
                personality_traits=["empathetic", "supportive", "non-judgmental", "compassionate"],
                communication_style="Compassionate and supportive, with focus on student wellbeing and mental health",
                expertise_level="expert",
                cultural_sensitivity="very_high",
                language_support=["English", "Spanish"],
                availability_hours={
                    "monday": [9, 18], "tuesday": [9, 18], "wednesday": [9, 18],
                    "thursday": [9, 18], "friday": [9, 18], "saturday": [10, 15],
                    "sunday": [12, 16]
                }
            ),
            AIAssistant(
                assistant_id="ASSISTANT_008",
                name="Financial Aid Felix",
                assistant_type=AssistantType.FINANCIAL_AID_ADVISOR,
                specialization="Financial Aid and Scholarship Guidance",
                capabilities=[
                    "financial_aid_application",
                    "scholarship_search",
                    "budget_planning",
                    "loan_guidance",
                    "financial_literacy",
                    "cost_optimization"
                ],
                personality_traits=["knowledgeable", "helpful", "practical", "supportive"],
                communication_style="Practical and informative, with clear financial guidance and support",
                expertise_level="expert",
                cultural_sensitivity="high",
                language_support=["English", "Spanish"],
                availability_hours={
                    "monday": [9, 17], "tuesday": [9, 17], "wednesday": [9, 17],
                    "thursday": [9, 17], "friday": [9, 17], "saturday": [9, 13],
                    "sunday": []
                }
            )
        ]
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize knowledge base for common queries"""
        return {
            "academic_policies": {
                "grading_scale": "A: 90-100%, B: 80-89%, C: 70-79%, D: 60-69%, F: Below 60%",
                "attendance_policy": "Students must attend at least 80% of classes",
                "late_submission": "Late assignments receive 10% penalty per day",
                "academic_integrity": "All work must be original and properly cited"
            },
            "technical_support": {
                "common_issues": [
                    "Login problems",
                    "Video playback issues",
                    "Assignment submission errors",
                    "Browser compatibility",
                    "Mobile app issues"
                ],
                "solutions": {
                    "login_problems": "Clear browser cache, check credentials, contact support",
                    "video_issues": "Check internet connection, try different browser, update Flash",
                    "submission_errors": "Check file format, size limits, internet connection"
                }
            },
            "career_resources": {
                "job_boards": ["LinkedIn", "Indeed", "Glassdoor", "AI-specific job sites"],
                "resume_tips": [
                    "Use action verbs",
                    "Quantify achievements",
                    "Tailor to job description",
                    "Include relevant skills"
                ],
                "interview_preparation": [
                    "Research the company",
                    "Practice common questions",
                    "Prepare examples of achievements",
                    "Dress professionally"
                ]
            },
            "financial_aid": {
                "types": ["Grants", "Scholarships", "Loans", "Work-study"],
                "application_process": "Complete FAFSA, submit required documents, meet deadlines",
                "requirements": "Maintain GPA, enroll full-time, meet income guidelines"
            }
        }
    
    def submit_student_request(self, student_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit new student request for assistance"""
        request_id = f"REQ_{uuid.uuid4().hex[:8]}"
        
        # Determine category and priority
        category = self._categorize_request(request_data["description"])
        priority = self._assess_priority(request_data["description"], request_data.get("urgency", "medium"))
        
        # Create request
        request = StudentRequest(
            request_id=request_id,
            student_id=student_id,
            category=category,
            title=request_data["title"],
            description=request_data["description"],
            priority=priority,
            status=TaskStatus.PENDING,
            assigned_assistant=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            due_date=self._calculate_due_date(priority),
            tags=request_data.get("tags", []),
            attachments=request_data.get("attachments", [])
        )
        
        self.student_requests[request_id] = request
        
        # Auto-assign assistant
        assigned_assistant = self._auto_assign_assistant(request)
        if assigned_assistant:
            request.assigned_assistant = assigned_assistant
            request.status = TaskStatus.IN_PROGRESS
            
            # Create task for assistant
            task = self._create_task_for_assistant(request, assigned_assistant)
            self.tasks[task.task_id] = task
        
        return {
            "success": True,
            "request_id": request_id,
            "category": category.value,
            "priority": priority.value,
            "assigned_assistant": assigned_assistant,
            "estimated_response_time": self._get_estimated_response_time(priority),
            "due_date": request.due_date.isoformat() if request.due_date else None
        }
    
    def _categorize_request(self, description: str) -> RequestCategory:
        """Categorize request based on description"""
        description_lower = description.lower()
        
        academic_keywords = ["course", "grade", "assignment", "exam", "study", "academic", "degree"]
        technical_keywords = ["login", "password", "error", "bug", "technical", "software", "hardware"]
        administrative_keywords = ["enrollment", "transcript", "financial", "aid", "policy", "deadline"]
        personal_keywords = ["stress", "anxiety", "mental", "health", "wellness", "personal"]
        emergency_keywords = ["urgent", "emergency", "crisis", "immediate", "asap"]
        
        if any(keyword in description_lower for keyword in emergency_keywords):
            return RequestCategory.EMERGENCY
        elif any(keyword in description_lower for keyword in academic_keywords):
            return RequestCategory.ACADEMIC
        elif any(keyword in description_lower for keyword in technical_keywords):
            return RequestCategory.TECHNICAL
        elif any(keyword in description_lower for keyword in administrative_keywords):
            return RequestCategory.ADMINISTRATIVE
        elif any(keyword in description_lower for keyword in personal_keywords):
            return RequestCategory.PERSONAL
        else:
            return RequestCategory.INFORMATION
    
    def _assess_priority(self, description: str, urgency: str) -> TaskPriority:
        """Assess request priority"""
        description_lower = description.lower()
        
        # High priority keywords
        high_priority_keywords = ["urgent", "deadline", "exam", "grade", "crisis", "emergency"]
        critical_keywords = ["crisis", "emergency", "immediate", "asap", "critical"]
        
        if any(keyword in description_lower for keyword in critical_keywords):
            return TaskPriority.CRITICAL
        elif any(keyword in description_lower for keyword in high_priority_keywords):
            return TaskPriority.HIGH
        elif urgency == "high":
            return TaskPriority.HIGH
        elif urgency == "medium":
            return TaskPriority.MEDIUM
        else:
            return TaskPriority.LOW
    
    def _calculate_due_date(self, priority: TaskPriority) -> datetime:
        """Calculate due date based on priority"""
        now = datetime.now()
        
        if priority == TaskPriority.CRITICAL:
            return now + timedelta(hours=2)
        elif priority == TaskPriority.URGENT:
            return now + timedelta(hours=4)
        elif priority == TaskPriority.HIGH:
            return now + timedelta(days=1)
        elif priority == TaskPriority.MEDIUM:
            return now + timedelta(days=3)
        else:
            return now + timedelta(days=7)
    
    def _auto_assign_assistant(self, request: StudentRequest) -> Optional[str]:
        """Auto-assign appropriate assistant based on request category"""
        category_mapping = {
            RequestCategory.ACADEMIC: AssistantType.ACADEMIC_ADVISOR,
            RequestCategory.TECHNICAL: AssistantType.TECHNICAL_SUPPORT,
            RequestCategory.ADMINISTRATIVE: AssistantType.ADMINISTRATIVE_SUPPORT,
            RequestCategory.PERSONAL: AssistantType.MENTAL_HEALTH_SUPPORT,
            RequestCategory.EMERGENCY: AssistantType.MENTAL_HEALTH_SUPPORT,
            RequestCategory.INFORMATION: AssistantType.ADMINISTRATIVE_SUPPORT
        }
        
        target_type = category_mapping.get(request.category)
        if not target_type:
            return None
        
        # Find available assistant of the right type
        available_assistants = [
            assistant for assistant in self.ai_assistants
            if assistant.assistant_type == target_type and assistant.status == "active"
        ]
        
        if not available_assistants:
            return None
        
        # Select assistant with lowest current workload
        return min(available_assistants, key=lambda a: a.total_tasks_completed).assistant_id
    
    def _create_task_for_assistant(self, request: StudentRequest, assistant_id: str) -> Task:
        """Create task for assigned assistant"""
        task_id = f"TASK_{uuid.uuid4().hex[:8]}"
        
        task = Task(
            task_id=task_id,
            assistant_id=assistant_id,
            request_id=request.request_id,
            title=request.title,
            description=request.description,
            priority=request.priority,
            status=TaskStatus.IN_PROGRESS,
            created_at=datetime.now(),
            due_date=request.due_date,
            estimated_duration_minutes=self._estimate_task_duration(request)
        )
        
        return task
    
    def _estimate_task_duration(self, request: StudentRequest) -> int:
        """Estimate task duration based on complexity"""
        duration_mapping = {
            TaskPriority.CRITICAL: 30,  # minutes
            TaskPriority.URGENT: 60,
            TaskPriority.HIGH: 120,
            TaskPriority.MEDIUM: 240,
            TaskPriority.LOW: 480
        }
        
        return duration_mapping.get(request.priority, 120)
    
    def _get_estimated_response_time(self, priority: TaskPriority) -> str:
        """Get estimated response time for student"""
        response_times = {
            TaskPriority.CRITICAL: "Within 2 hours",
            TaskPriority.URGENT: "Within 4 hours",
            TaskPriority.HIGH: "Within 24 hours",
            TaskPriority.MEDIUM: "Within 3 days",
            TaskPriority.LOW: "Within 1 week"
        }
        
        return response_times.get(priority, "Within 24 hours")
    
    def process_assistant_response(self, task_id: str, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process assistant's response to student request"""
        task = self.tasks.get(task_id)
        if not task:
            return {"success": False, "error": "Task not found"}
        
        request = self.student_requests.get(task.request_id)
        if not request:
            return {"success": False, "error": "Request not found"}
        
        # Update task
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        task.actual_duration_minutes = int((task.completed_at - task.created_at).total_seconds() / 60)
        task.notes = response_data.get("notes", "")
        task.resources_used = response_data.get("resources_used", [])
        
        # Update request
        request.status = TaskStatus.COMPLETED
        request.resolution_notes = response_data.get("resolution", "")
        request.updated_at = datetime.now()
        
        # Update assistant stats
        assistant = next(a for a in self.ai_assistants if a.assistant_id == task.assistant_id)
        assistant.total_tasks_completed += 1
        
        # Calculate new average response time
        total_time = assistant.average_response_time_minutes * (assistant.total_tasks_completed - 1)
        assistant.average_response_time_minutes = (total_time + task.actual_duration_minutes) / assistant.total_tasks_completed
        
        return {
            "success": True,
            "task_id": task_id,
            "request_id": request.request_id,
            "resolution": response_data.get("resolution", ""),
            "resources_provided": response_data.get("resources_used", []),
            "completion_time": task.actual_duration_minutes,
            "next_steps": response_data.get("next_steps", [])
        }
    
    def get_student_request_status(self, request_id: str) -> Dict[str, Any]:
        """Get status of student request"""
        request = self.student_requests.get(request_id)
        if not request:
            return {"error": "Request not found"}
        
        task = next((t for t in self.tasks.values() if t.request_id == request_id), None)
        
        return {
            "request_id": request_id,
            "title": request.title,
            "category": request.category.value,
            "priority": request.priority.value,
            "status": request.status.value,
            "assigned_assistant": request.assigned_assistant,
            "created_at": request.created_at.isoformat(),
            "updated_at": request.updated_at.isoformat(),
            "due_date": request.due_date.isoformat() if request.due_date else None,
            "resolution_notes": request.resolution_notes,
            "task_status": task.status.value if task else "Not assigned",
            "estimated_completion": task.estimated_duration_minutes if task else 0
        }
    
    def get_assistant_dashboard(self, assistant_id: str) -> Dict[str, Any]:
        """Get dashboard data for AI assistant"""
        assistant = next((a for a in self.ai_assistants if a.assistant_id == assistant_id), None)
        if not assistant:
            return {"error": "Assistant not found"}
        
        # Get assistant's tasks
        assistant_tasks = [t for t in self.tasks.values() if t.assistant_id == assistant_id]
        
        # Get recent requests
        recent_requests = [
            r for r in self.student_requests.values()
            if r.assigned_assistant == assistant_id
        ]
        
        # Calculate metrics
        completed_tasks = [t for t in assistant_tasks if t.status == TaskStatus.COMPLETED]
        pending_tasks = [t for t in assistant_tasks if t.status == TaskStatus.IN_PROGRESS]
        
        return {
            "assistant_id": assistant_id,
            "name": assistant.name,
            "specialization": assistant.specialization,
            "status": assistant.status,
            "metrics": {
                "total_tasks_completed": len(completed_tasks),
                "pending_tasks": len(pending_tasks),
                "average_response_time_minutes": assistant.average_response_time_minutes,
                "student_satisfaction_rating": assistant.student_satisfaction_rating,
                "escalation_rate": assistant.escalation_rate
            },
            "recent_requests": [
                {
                    "request_id": r.request_id,
                    "title": r.title,
                    "category": r.category.value,
                    "priority": r.priority.value,
                    "status": r.status.value,
                    "created_at": r.created_at.isoformat()
                }
                for r in sorted(recent_requests, key=lambda x: x.created_at, reverse=True)[:10]
            ],
            "current_workload": len(pending_tasks),
            "availability": assistant.availability_hours
        }
    
    def generate_knowledge_base_response(self, query: str, category: str) -> Dict[str, Any]:
        """Generate response from knowledge base"""
        query_lower = query.lower()
        
        # Search knowledge base
        relevant_info = []
        
        if category == "academic":
            for topic, info in self.knowledge_base["academic_policies"].items():
                if topic.replace("_", " ") in query_lower:
                    relevant_info.append(f"{topic.replace('_', ' ').title()}: {info}")
        
        elif category == "technical":
            for issue in self.knowledge_base["technical_support"]["common_issues"]:
                if issue.lower() in query_lower:
                    relevant_info.append(f"Common issue: {issue}")
                    if issue.lower() in self.knowledge_base["technical_support"]["solutions"]:
                        relevant_info.append(f"Solution: {self.knowledge_base['technical_support']['solutions'][issue.lower()]}")
        
        elif category == "career":
            if "resume" in query_lower:
                relevant_info.extend(self.knowledge_base["career_resources"]["resume_tips"])
            elif "interview" in query_lower:
                relevant_info.extend(self.knowledge_base["career_resources"]["interview_preparation"])
            elif "job" in query_lower:
                relevant_info.extend(self.knowledge_base["career_resources"]["job_boards"])
        
        elif category == "financial":
            if "aid" in query_lower or "financial" in query_lower:
                relevant_info.append(f"Types: {', '.join(self.knowledge_base['financial_aid']['types'])}")
                relevant_info.append(f"Process: {self.knowledge_base['financial_aid']['application_process']}")
                relevant_info.append(f"Requirements: {self.knowledge_base['financial_aid']['requirements']}")
        
        return {
            "success": True,
            "query": query,
            "category": category,
            "relevant_information": relevant_info,
            "sources": ["MS AI Knowledge Base"],
            "last_updated": datetime.now().isoformat()
        }
    
    def escalate_request(self, request_id: str, escalation_reason: str) -> Dict[str, Any]:
        """Escalate request to human support"""
        request = self.student_requests.get(request_id)
        if not request:
            return {"success": False, "error": "Request not found"}
        
        # Update request status
        request.status = TaskStatus.ESCALATED
        request.updated_at = datetime.now()
        request.resolution_notes += f"\nEscalated: {escalation_reason}"
        
        # Update assistant escalation rate
        if request.assigned_assistant:
            assistant = next(a for a in self.ai_assistants if a.assistant_id == request.assigned_assistant)
            assistant.escalation_rate = (assistant.escalation_rate * assistant.total_tasks_completed + 1) / (assistant.total_tasks_completed + 1)
        
        return {
            "success": True,
            "request_id": request_id,
            "status": "escalated",
            "escalation_reason": escalation_reason,
            "human_support_notified": True,
            "estimated_human_response": "Within 24 hours"
        }
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        total_requests = len(self.student_requests)
        completed_requests = len([r for r in self.student_requests.values() if r.status == TaskStatus.COMPLETED])
        pending_requests = len([r for r in self.student_requests.values() if r.status == TaskStatus.IN_PROGRESS])
        escalated_requests = len([r for r in self.student_requests.values() if r.status == TaskStatus.ESCALATED])
        
        # Category breakdown
        category_counts = {}
        for request in self.student_requests.values():
            category = request.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Priority breakdown
        priority_counts = {}
        for request in self.student_requests.values():
            priority = request.priority.value
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Assistant performance
        assistant_performance = []
        for assistant in self.ai_assistants:
            assistant_tasks = [t for t in self.tasks.values() if t.assistant_id == assistant.assistant_id]
            completed_tasks = [t for t in assistant_tasks if t.status == TaskStatus.COMPLETED]
            
            assistant_performance.append({
                "assistant_id": assistant.assistant_id,
                "name": assistant.name,
                "specialization": assistant.specialization,
                "tasks_completed": len(completed_tasks),
                "average_response_time": assistant.average_response_time_minutes,
                "satisfaction_rating": assistant.student_satisfaction_rating,
                "escalation_rate": assistant.escalation_rate
            })
        
        return {
            "total_requests": total_requests,
            "completed_requests": completed_requests,
            "pending_requests": pending_requests,
            "escalated_requests": escalated_requests,
            "completion_rate": (completed_requests / total_requests * 100) if total_requests > 0 else 0,
            "category_distribution": category_counts,
            "priority_distribution": priority_counts,
            "assistant_performance": assistant_performance,
            "system_uptime": "99.9%",
            "average_response_time": sum(a.average_response_time_minutes for a in self.ai_assistants) / len(self.ai_assistants),
            "student_satisfaction": sum(a.student_satisfaction_rating for a in self.ai_assistants) / len(self.ai_assistants)
        }