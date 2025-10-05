"""
MS AI Curriculum System - Enhanced Instructor Portal
Comprehensive course management with AI Professor integration
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import random

class CourseStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ACTIVE = "active"
    ARCHIVED = "archived"
    SUSPENDED = "suspended"

class AssignmentType(Enum):
    LECTURE = "lecture"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    PROJECT = "project"
    EXAM = "exam"
    TUTORIAL = "tutorial"
    READING = "reading"
    DISCUSSION = "discussion"

class GradingStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"

@dataclass
class Course:
    """Course structure for instructor portal"""
    course_id: str
    title: str
    description: str
    instructor_id: str
    status: CourseStatus
    created_at: datetime
    updated_at: datetime
    enrollment_count: int = 0
    completion_rate: float = 0.0
    average_grade: float = 0.0
    student_satisfaction: float = 0.0
    learning_objectives: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    credits: int = 3

@dataclass
class Assignment:
    """Assignment structure for instructor portal"""
    assignment_id: str
    course_id: str
    title: str
    description: str
    assignment_type: AssignmentType
    points_possible: int
    due_date: datetime
    created_at: datetime
    status: str = "draft"
    submissions_count: int = 0
    graded_count: int = 0
    average_grade: float = 0.0
    instructions: str = ""
    rubric: Optional[Dict[str, Any]] = None

@dataclass
class StudentSubmission:
    """Student submission for grading"""
    submission_id: str
    assignment_id: str
    student_id: str
    student_name: str
    submitted_at: datetime
    content: str
    attachments: List[str] = field(default_factory=list)
    grade: Optional[float] = None
    feedback: Optional[str] = None
    grading_status: GradingStatus = GradingStatus.PENDING
    graded_at: Optional[datetime] = None
    graded_by: Optional[str] = None

@dataclass
class InstructorAgent:
    """AI Agent specialized for instructor tasks"""
    agent_id: str
    name: str
    specialization: str
    capabilities: List[str]
    status: str = "active"
    last_activity: Optional[datetime] = None
    tasks_completed: int = 0
    collaboration_score: float = 0.0

class EnhancedInstructorPortal:
    """Advanced instructor portal with AI Professor integration"""
    
    def __init__(self, user_manager=None, professor_system=None, content_system=None, 
                 tutor_system=None, assistant_system=None):
        self.user_manager = user_manager
        self.professor_system = professor_system
        self.content_system = content_system
        self.tutor_system = tutor_system
        self.assistant_system = assistant_system
        
        # Instructor data
        self.courses: Dict[str, List[Course]] = {}
        self.assignments: Dict[str, List[Assignment]] = {}
        self.submissions: Dict[str, List[StudentSubmission]] = {}
        self.instructor_agents = self._initialize_instructor_agents()
        
    def _initialize_instructor_agents(self) -> List[InstructorAgent]:
        """Initialize AI agents for instructor tasks"""
        return [
            InstructorAgent(
                agent_id="INSTRUCTOR_AGENT_001",
                name="Course Design Assistant",
                specialization="Course Content Development",
                capabilities=[
                    "curriculum_design",
                    "learning_objective_creation",
                    "assessment_development",
                    "content_organization",
                    "accreditation_alignment"
                ]
            ),
            InstructorAgent(
                agent_id="INSTRUCTOR_AGENT_002",
                name="Assessment Coordinator",
                specialization="Assessment and Grading Support",
                capabilities=[
                    "rubric_creation",
                    "grading_assistance",
                    "feedback_generation",
                    "grade_analysis",
                    "assessment_optimization"
                ]
            ),
            InstructorAgent(
                agent_id="INSTRUCTOR_AGENT_003",
                name="Student Engagement Specialist",
                specialization="Student Interaction and Engagement",
                capabilities=[
                    "engagement_monitoring",
                    "intervention_recommendations",
                    "communication_optimization",
                    "motivation_strategies",
                    "learning_support"
                ]
            ),
            InstructorAgent(
                agent_id="INSTRUCTOR_AGENT_004",
                name="Research Collaboration Agent",
                specialization="Research and Academic Collaboration",
                capabilities=[
                    "research_support",
                    "collaboration_facilitation",
                    "publication_assistance",
                    "academic_networking",
                    "research_tracking"
                ]
            )
        ]
    
    def get_instructor_dashboard(self, instructor_id: str) -> Dict[str, Any]:
        """Get comprehensive instructor dashboard"""
        # Get instructor's courses
        courses = self.courses.get(instructor_id, [])
        
        # Get course statistics
        course_stats = self._get_course_statistics(instructor_id)
        
        # Get assignment statistics
        assignment_stats = self._get_assignment_statistics(instructor_id)
        
        # Get student performance data
        student_performance = self._get_student_performance(instructor_id)
        
        # Get AI Professor collaboration data
        ai_collaboration = self._get_ai_collaboration_data(instructor_id)
        
        # Get upcoming tasks
        upcoming_tasks = self._get_upcoming_tasks(instructor_id)
        
        return {
            "instructor_id": instructor_id,
            "dashboard_data": {
                "courses": [
                    {
                        "course_id": course.course_id,
                        "title": course.title,
                        "status": course.status.value,
                        "enrollment_count": course.enrollment_count,
                        "completion_rate": course.completion_rate,
                        "average_grade": course.average_grade,
                        "student_satisfaction": course.student_satisfaction,
                        "last_updated": course.updated_at.isoformat()
                    }
                    for course in courses
                ],
                "course_statistics": course_stats,
                "assignment_statistics": assignment_stats,
                "student_performance": student_performance,
                "ai_collaboration": ai_collaboration,
                "upcoming_tasks": upcoming_tasks
            },
            "summary_stats": {
                "total_courses": len(courses),
                "active_courses": len([c for c in courses if c.status == CourseStatus.ACTIVE]),
                "total_students": sum(c.enrollment_count for c in courses),
                "pending_grades": self._count_pending_grades(instructor_id),
                "average_course_rating": sum(c.student_satisfaction for c in courses) / len(courses) if courses else 0,
                "ai_collaboration_score": self._calculate_collaboration_score(instructor_id)
            }
        }
    
    def _get_course_statistics(self, instructor_id: str) -> Dict[str, Any]:
        """Get course statistics for instructor"""
        courses = self.courses.get(instructor_id, [])
        
        if not courses:
            return {"total_courses": 0, "average_enrollment": 0, "average_completion": 0}
        
        return {
            "total_courses": len(courses),
            "average_enrollment": sum(c.enrollment_count for c in courses) / len(courses),
            "average_completion": sum(c.completion_rate for c in courses) / len(courses),
            "average_grade": sum(c.average_grade for c in courses) / len(courses),
            "average_satisfaction": sum(c.student_satisfaction for c in courses) / len(courses),
            "course_status_distribution": {
                "active": len([c for c in courses if c.status == CourseStatus.ACTIVE]),
                "draft": len([c for c in courses if c.status == CourseStatus.DRAFT]),
                "archived": len([c for c in courses if c.status == CourseStatus.ARCHIVED])
            }
        }
    
    def _get_assignment_statistics(self, instructor_id: str) -> Dict[str, Any]:
        """Get assignment statistics for instructor"""
        courses = self.courses.get(instructor_id, [])
        course_ids = [c.course_id for c in courses]
        
        all_assignments = []
        for course_id in course_ids:
            assignments = self.assignments.get(course_id, [])
            all_assignments.extend(assignments)
        
        if not all_assignments:
            return {"total_assignments": 0, "pending_grades": 0, "average_submissions": 0}
        
        return {
            "total_assignments": len(all_assignments),
            "pending_grades": sum(1 for a in all_assignments if a.graded_count < a.submissions_count),
            "average_submissions": sum(a.submissions_count for a in all_assignments) / len(all_assignments),
            "average_grade": sum(a.average_grade for a in all_assignments) / len(all_assignments),
            "assignment_types": {
                "lecture": len([a for a in all_assignments if a.assignment_type == AssignmentType.LECTURE]),
                "quiz": len([a for a in all_assignments if a.assignment_type == AssignmentType.QUIZ]),
                "assignment": len([a for a in all_assignments if a.assignment_type == AssignmentType.ASSIGNMENT]),
                "exam": len([a for a in all_assignments if a.assignment_type == AssignmentType.EXAM])
            }
        }
    
    def _get_student_performance(self, instructor_id: str) -> Dict[str, Any]:
        """Get student performance data"""
        courses = self.courses.get(instructor_id, [])
        
        return {
            "total_students": sum(c.enrollment_count for c in courses),
            "average_performance": sum(c.average_grade for c in courses) / len(courses) if courses else 0,
            "completion_rate": sum(c.completion_rate for c in courses) / len(courses) if courses else 0,
            "satisfaction_score": sum(c.student_satisfaction for c in courses) / len(courses) if courses else 0,
            "at_risk_students": random.randint(2, 8),  # Simulated
            "top_performers": random.randint(5, 15)   # Simulated
        }
    
    def _get_ai_collaboration_data(self, instructor_id: str) -> Dict[str, Any]:
        """Get AI Professor collaboration data"""
        return {
            "collaboration_sessions": random.randint(10, 25),
            "ai_professor_interactions": random.randint(50, 100),
            "content_generated": random.randint(20, 40),
            "research_collaborations": random.randint(3, 8),
            "average_collaboration_score": random.uniform(4.0, 5.0),
            "ai_professors_available": [
                {"name": "Dr. Sarah Chen", "specialization": "Machine Learning", "availability": "high"},
                {"name": "Dr. Marcus Rodriguez", "specialization": "Computer Vision", "availability": "medium"},
                {"name": "Dr. Aisha Patel", "specialization": "AI Ethics", "availability": "high"},
                {"name": "Dr. James Kim", "specialization": "NLP", "availability": "medium"}
            ]
        }
    
    def _get_upcoming_tasks(self, instructor_id: str) -> List[Dict[str, Any]]:
        """Get upcoming tasks for instructor"""
        tasks = []
        
        # Get assignments due for grading
        courses = self.courses.get(instructor_id, [])
        for course in courses:
            assignments = self.assignments.get(course.course_id, [])
            for assignment in assignments:
                if assignment.graded_count < assignment.submissions_count:
                    tasks.append({
                        "task_id": f"TASK_{uuid.uuid4().hex[:8]}",
                        "type": "grading",
                        "title": f"Grade {assignment.title}",
                        "course": course.title,
                        "due_date": (assignment.due_date + timedelta(days=3)).isoformat(),
                        "priority": "high" if assignment.graded_count < assignment.submissions_count * 0.5 else "medium",
                        "submissions_pending": assignment.submissions_count - assignment.graded_count
                    })
        
        return sorted(tasks, key=lambda x: x["due_date"])[:10]
    
    def _count_pending_grades(self, instructor_id: str) -> int:
        """Count pending grades for instructor"""
        courses = self.courses.get(instructor_id, [])
        pending_count = 0
        
        for course in courses:
            assignments = self.assignments.get(course.course_id, [])
            for assignment in assignments:
                pending_count += assignment.submissions_count - assignment.graded_count
        
        return pending_count
    
    def _calculate_collaboration_score(self, instructor_id: str) -> float:
        """Calculate AI collaboration score"""
        # Simulate collaboration score based on various factors
        return random.uniform(3.5, 5.0)
    
    def create_course(self, instructor_id: str, course_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new course"""
        course_id = f"COURSE_{uuid.uuid4().hex[:8]}"
        
        course = Course(
            course_id=course_id,
            title=course_data["title"],
            description=course_data["description"],
            instructor_id=instructor_id,
            status=CourseStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            learning_objectives=course_data.get("learning_objectives", []),
            prerequisites=course_data.get("prerequisites", []),
            credits=course_data.get("credits", 3)
        )
        
        if instructor_id not in self.courses:
            self.courses[instructor_id] = []
        self.courses[instructor_id].append(course)
        
        # Initialize assignments for the course
        self._initialize_course_assignments(course_id, course_data)
        
        return {
            "success": True,
            "course_id": course_id,
            "message": f"Course '{course_data['title']}' created successfully"
        }
    
    def _initialize_course_assignments(self, course_id: str, course_data: Dict[str, Any]):
        """Initialize assignments for new course"""
        if course_id not in self.assignments:
            self.assignments[course_id] = []
        
        # Generate sample assignments
        assignments = [
            Assignment(
                assignment_id=f"ASSIGN_{uuid.uuid4().hex[:8]}",
                course_id=course_id,
                title="Course Introduction",
                description="Introduction to course concepts and objectives",
                assignment_type=AssignmentType.LECTURE,
                points_possible=100,
                due_date=datetime.now() + timedelta(days=7),
                created_at=datetime.now()
            ),
            Assignment(
                assignment_id=f"ASSIGN_{uuid.uuid4().hex[:8]}",
                course_id=course_id,
                title="Week 1 Quiz",
                description="Assessment of week 1 learning objectives",
                assignment_type=AssignmentType.QUIZ,
                points_possible=50,
                due_date=datetime.now() + timedelta(days=14),
                created_at=datetime.now()
            ),
            Assignment(
                assignment_id=f"ASSIGN_{uuid.uuid4().hex[:8]}",
                course_id=course_id,
                title="Midterm Exam",
                description="Comprehensive midterm examination",
                assignment_type=AssignmentType.EXAM,
                points_possible=200,
                due_date=datetime.now() + timedelta(days=45),
                created_at=datetime.now()
            )
        ]
        
        self.assignments[course_id].extend(assignments)
    
    def create_assignment(self, course_id: str, assignment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new assignment"""
        assignment_id = f"ASSIGN_{uuid.uuid4().hex[:8]}"
        
        assignment = Assignment(
            assignment_id=assignment_id,
            course_id=course_id,
            title=assignment_data["title"],
            description=assignment_data["description"],
            assignment_type=AssignmentType(assignment_data["type"]),
            points_possible=assignment_data["points_possible"],
            due_date=datetime.fromisoformat(assignment_data["due_date"]),
            created_at=datetime.now(),
            instructions=assignment_data.get("instructions", ""),
            rubric=assignment_data.get("rubric")
        )
        
        if course_id not in self.assignments:
            self.assignments[course_id] = []
        self.assignments[course_id].append(assignment)
        
        return {
            "success": True,
            "assignment_id": assignment_id,
            "message": f"Assignment '{assignment_data['title']}' created successfully"
        }
    
    def grade_assignment(self, assignment_id: str, submission_id: str, 
                        grade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Grade student assignment"""
        # Find submission
        submission = None
        for course_submissions in self.submissions.values():
            for sub in course_submissions:
                if sub.submission_id == submission_id:
                    submission = sub
                    break
        
        if not submission:
            return {"success": False, "error": "Submission not found"}
        
        # Update submission
        submission.grade = grade_data["grade"]
        submission.feedback = grade_data.get("feedback", "")
        submission.grading_status = GradingStatus.COMPLETED
        submission.graded_at = datetime.now()
        submission.graded_by = grade_data.get("graded_by", "Instructor")
        
        # Update assignment statistics
        assignment = None
        for course_assignments in self.assignments.values():
            for assign in course_assignments:
                if assign.assignment_id == assignment_id:
                    assignment = assign
                    break
        
        if assignment:
            assignment.graded_count += 1
            # Update average grade
            if assignment.average_grade == 0:
                assignment.average_grade = submission.grade
            else:
                assignment.average_grade = (assignment.average_grade + submission.grade) / 2
        
        return {
            "success": True,
            "submission_id": submission_id,
            "grade": submission.grade,
            "feedback": submission.feedback,
            "graded_at": submission.graded_at.isoformat()
        }
    
    def collaborate_with_ai_professor(self, course_id: str, collaboration_type: str, 
                                    data: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with AI Professor"""
        if not self.professor_system:
            return {"success": False, "error": "Professor system not available"}
        
        # Find appropriate AI Professor
        course = None
        for instructor_courses in self.courses.values():
            for c in instructor_courses:
                if c.course_id == course_id:
                    course = c
                    break
        
        if not course:
            return {"success": False, "error": "Course not found"}
        
        # Select AI Professor based on course content
        ai_professor = self._select_ai_professor_for_collaboration(course, collaboration_type)
        
        if collaboration_type == "content_generation":
            return self._generate_course_content_with_ai(ai_professor, course, data)
        elif collaboration_type == "assessment_creation":
            return self._create_assessment_with_ai(ai_professor, course, data)
        elif collaboration_type == "research_collaboration":
            return self._collaborate_on_research(ai_professor, course, data)
        else:
            return {"success": False, "error": f"Unknown collaboration type: {collaboration_type}"}
    
    def _select_ai_professor_for_collaboration(self, course: Course, collaboration_type: str):
        """Select appropriate AI Professor for collaboration"""
        # Map course topics to AI Professor specializations
        topic_mapping = {
            "machine learning": "PROF_001",  # Dr. Sarah Chen
            "computer vision": "PROF_002",   # Dr. Marcus Rodriguez
            "ai ethics": "PROF_003",         # Dr. Aisha Patel
            "nlp": "PROF_004"                # Dr. James Kim
        }
        
        # Simple mapping based on course title
        course_title_lower = course.title.lower()
        for topic, professor_id in topic_mapping.items():
            if topic in course_title_lower:
                return professor_id
        
        # Default to Dr. Sarah Chen
        return "PROF_001"
    
    def _generate_course_content_with_ai(self, ai_professor_id: str, course: Course, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate course content with AI Professor"""
        content_type = data.get("content_type", "lecture")
        
        # Simulate AI Professor content generation
        generated_content = {
            "lecture": {
                "title": f"AI-Generated Lecture: {course.title}",
                "outline": [
                    "Introduction to key concepts",
                    "Theoretical foundations",
                    "Practical applications",
                    "Case studies and examples",
                    "Summary and next steps"
                ],
                "key_points": [
                    "Fundamental concepts explained clearly",
                    "Real-world applications highlighted",
                    "Interactive elements included",
                    "Assessment opportunities identified"
                ],
                "estimated_duration": "90 minutes",
                "difficulty_level": "intermediate"
            },
            "assignment": {
                "title": f"AI-Designed Assignment: {course.title}",
                "description": "Comprehensive assignment covering key learning objectives",
                "objectives": [
                    "Apply theoretical knowledge to practical problems",
                    "Demonstrate understanding of core concepts",
                    "Develop critical thinking skills",
                    "Enhance problem-solving abilities"
                ],
                "rubric": {
                    "excellent": "Demonstrates mastery of concepts with innovative applications",
                    "good": "Shows solid understanding with clear explanations",
                    "satisfactory": "Meets basic requirements with some gaps",
                    "needs_improvement": "Shows effort but lacks depth or accuracy"
                }
            }
        }
        
        return {
            "success": True,
            "ai_professor_id": ai_professor_id,
            "collaboration_type": "content_generation",
            "generated_content": generated_content.get(content_type, {}),
            "collaboration_notes": "AI Professor provided expert insights and recommendations",
            "next_steps": [
                "Review generated content",
                "Customize for specific course needs",
                "Integrate with existing curriculum",
                "Schedule follow-up collaboration"
            ]
        }
    
    def _create_assessment_with_ai(self, ai_professor_id: str, course: Course, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create assessment with AI Professor"""
        assessment_type = data.get("assessment_type", "quiz")
        
        # Simulate AI Professor assessment creation
        assessment_content = {
            "quiz": {
                "questions": [
                    {
                        "question": "What is the primary goal of machine learning?",
                        "type": "multiple_choice",
                        "options": [
                            "To replace human intelligence",
                            "To enable computers to learn from data",
                            "To create artificial consciousness",
                            "To automate all human tasks"
                        ],
                        "correct_answer": 1,
                        "points": 10
                    },
                    {
                        "question": "Explain the difference between supervised and unsupervised learning.",
                        "type": "short_answer",
                        "points": 20
                    }
                ],
                "total_points": 100,
                "time_limit": 30
            },
            "exam": {
                "sections": [
                    {
                        "title": "Multiple Choice",
                        "questions": 20,
                        "points_per_question": 5
                    },
                    {
                        "title": "Short Answer",
                        "questions": 5,
                        "points_per_question": 20
                    },
                    {
                        "title": "Essay",
                        "questions": 2,
                        "points_per_question": 50
                    }
                ],
                "total_points": 300,
                "time_limit": 120
            }
        }
        
        return {
            "success": True,
            "ai_professor_id": ai_professor_id,
            "collaboration_type": "assessment_creation",
            "assessment_content": assessment_content.get(assessment_type, {}),
            "ai_recommendations": [
                "Questions align with learning objectives",
                "Difficulty level appropriate for course level",
                "Mix of question types for comprehensive assessment",
                "Clear rubrics provided for grading"
            ]
        }
    
    def _collaborate_on_research(self, ai_professor_id: str, course: Course, data: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate on research with AI Professor"""
        research_topic = data.get("research_topic", course.title)
        
        # Simulate research collaboration
        research_collaboration = {
            "research_topic": research_topic,
            "collaboration_areas": [
                "Literature review and analysis",
                "Methodology development",
                "Data collection strategies",
                "Results interpretation",
                "Publication planning"
            ],
            "ai_contributions": [
                "Provided comprehensive literature review",
                "Suggested innovative methodologies",
                "Identified potential research gaps",
                "Recommended publication venues"
            ],
            "collaboration_outcomes": [
                "Research proposal developed",
                "Methodology refined",
                "Timeline established",
                "Publication strategy planned"
            ]
        }
        
        return {
            "success": True,
            "ai_professor_id": ai_professor_id,
            "collaboration_type": "research_collaboration",
            "research_collaboration": research_collaboration,
            "next_steps": [
                "Schedule regular collaboration meetings",
                "Develop detailed research proposal",
                "Identify funding opportunities",
                "Plan publication timeline"
            ]
        }
    
    def get_course_analytics(self, course_id: str) -> Dict[str, Any]:
        """Get detailed course analytics"""
        course = None
        for instructor_courses in self.courses.values():
            for c in instructor_courses:
                if c.course_id == course_id:
                    course = c
                    break
        
        if not course:
            return {"error": "Course not found"}
        
        assignments = self.assignments.get(course_id, [])
        submissions = self.submissions.get(course_id, [])
        
        return {
            "course_id": course_id,
            "course_title": course.title,
            "analytics": {
                "enrollment_trends": {
                    "current_enrollment": course.enrollment_count,
                    "enrollment_growth": "+15%",
                    "retention_rate": course.completion_rate
                },
                "performance_metrics": {
                    "average_grade": course.average_grade,
                    "grade_distribution": {
                        "A": random.randint(20, 30),
                        "B": random.randint(30, 40),
                        "C": random.randint(20, 30),
                        "D": random.randint(5, 15),
                        "F": random.randint(1, 5)
                    },
                    "completion_rate": course.completion_rate
                },
                "engagement_metrics": {
                    "student_satisfaction": course.student_satisfaction,
                    "assignment_submission_rate": random.uniform(85, 95),
                    "discussion_participation": random.uniform(70, 85),
                    "resource_access_rate": random.uniform(90, 98)
                },
                "assignment_analysis": [
                    {
                        "assignment_id": a.assignment_id,
                        "title": a.title,
                        "type": a.assignment_type.value,
                        "submissions": a.submissions_count,
                        "average_grade": a.average_grade,
                        "completion_rate": (a.submissions_count / course.enrollment_count * 100) if course.enrollment_count > 0 else 0
                    }
                    for a in assignments
                ]
            },
            "recommendations": [
                "Consider adding more interactive elements",
                "Provide additional support for struggling students",
                "Enhance assignment feedback quality",
                "Increase discussion opportunities"
            ]
        }
    
    def get_student_submissions(self, assignment_id: str) -> List[Dict[str, Any]]:
        """Get student submissions for assignment"""
        submissions = []
        
        for course_submissions in self.submissions.values():
            for submission in course_submissions:
                if submission.assignment_id == assignment_id:
                    submissions.append({
                        "submission_id": submission.submission_id,
                        "student_id": submission.student_id,
                        "student_name": submission.student_name,
                        "submitted_at": submission.submitted_at.isoformat(),
                        "content": submission.content,
                        "attachments": submission.attachments,
                        "grade": submission.grade,
                        "feedback": submission.feedback,
                        "grading_status": submission.grading_status.value,
                        "graded_at": submission.graded_at.isoformat() if submission.graded_at else None,
                        "graded_by": submission.graded_by
                    })
        
        return sorted(submissions, key=lambda x: x["submitted_at"], reverse=True)
    
    def get_instructor_analytics(self, instructor_id: str) -> Dict[str, Any]:
        """Get comprehensive instructor analytics"""
        courses = self.courses.get(instructor_id, [])
        
        return {
            "instructor_id": instructor_id,
            "analytics": {
                "teaching_effectiveness": {
                    "overall_rating": random.uniform(4.0, 5.0),
                    "student_satisfaction": sum(c.student_satisfaction for c in courses) / len(courses) if courses else 0,
                    "course_completion_rate": sum(c.completion_rate for c in courses) / len(courses) if courses else 0,
                    "average_grade": sum(c.average_grade for c in courses) / len(courses) if courses else 0
                },
                "course_management": {
                    "total_courses": len(courses),
                    "active_courses": len([c for c in courses if c.status == CourseStatus.ACTIVE]),
                    "total_students": sum(c.enrollment_count for c in courses),
                    "average_class_size": sum(c.enrollment_count for c in courses) / len(courses) if courses else 0
                },
                "ai_collaboration": {
                    "collaboration_sessions": random.randint(15, 30),
                    "ai_professor_interactions": random.randint(60, 120),
                    "content_generated": random.randint(25, 50),
                    "research_collaborations": random.randint(5, 12),
                    "collaboration_score": random.uniform(4.0, 5.0)
                },
                "workload_analysis": {
                    "assignments_created": sum(len(self.assignments.get(c.course_id, [])) for c in courses),
                    "grades_pending": self._count_pending_grades(instructor_id),
                    "average_grading_time": random.uniform(5, 15),  # minutes per assignment
                    "workload_score": random.uniform(3.0, 5.0)
                }
            },
            "recommendations": [
                "Consider using AI Professor for content generation",
                "Implement automated grading for multiple choice questions",
                "Schedule regular AI collaboration sessions",
                "Focus on improving student engagement"
            ]
        }