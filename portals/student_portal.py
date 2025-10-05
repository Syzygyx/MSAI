"""
MS AI Curriculum System - Student Portal
Comprehensive learning dashboard with AI Tutor integration
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid

class LearningStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    NEEDS_REVIEW = "needs_review"
    OVERDUE = "overdue"

class AssignmentType(Enum):
    LECTURE = "lecture"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    PROJECT = "project"
    EXAM = "exam"
    TUTORIAL = "tutorial"
    READING = "reading"

class NotificationType(Enum):
    ASSIGNMENT_DUE = "assignment_due"
    GRADE_POSTED = "grade_posted"
    TUTOR_SESSION = "tutor_session"
    COURSE_UPDATE = "course_update"
    SYSTEM_ALERT = "system_alert"
    ACHIEVEMENT = "achievement"

@dataclass
class CourseEnrollment:
    """Student's enrollment in a course"""
    enrollment_id: str
    student_id: str
    course_id: str
    course_title: str
    professor_id: str
    enrollment_date: datetime
    status: str  # active, completed, dropped
    current_grade: Optional[float] = None
    progress_percentage: float = 0.0
    last_accessed: Optional[datetime] = None

@dataclass
class Assignment:
    """Assignment or learning activity"""
    assignment_id: str
    course_id: str
    title: str
    assignment_type: AssignmentType
    due_date: datetime
    points_possible: int
    status: LearningStatus
    grade: Optional[float] = None
    submission_date: Optional[datetime] = None
    feedback: Optional[str] = None
    attempts: int = 0
    max_attempts: int = 1

@dataclass
class LearningGoal:
    """Student's learning goal"""
    goal_id: str
    student_id: str
    title: str
    description: str
    target_date: datetime
    progress_percentage: float = 0.0
    status: str = "active"  # active, completed, paused
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Notification:
    """System notification for student"""
    notification_id: str
    student_id: str
    type: NotificationType
    title: str
    message: str
    created_at: datetime
    read: bool = False
    action_required: bool = False
    action_url: Optional[str] = None

@dataclass
class Achievement:
    """Student achievement or badge"""
    achievement_id: str
    student_id: str
    title: str
    description: str
    icon_url: str
    earned_date: datetime
    category: str
    points: int = 0

class StudentPortal:
    """Comprehensive student portal with learning dashboard"""
    
    def __init__(self, user_manager=None, tutor_system=None, assistant_system=None, 
                 content_system=None, professor_system=None):
        self.user_manager = user_manager
        self.tutor_system = tutor_system
        self.assistant_system = assistant_system
        self.content_system = content_system
        self.professor_system = professor_system
        
        # Student data
        self.enrollments: Dict[str, List[CourseEnrollment]] = {}
        self.assignments: Dict[str, List[Assignment]] = {}
        self.learning_goals: Dict[str, List[LearningGoal]] = {}
        self.notifications: Dict[str, List[Notification]] = {}
        self.achievements: Dict[str, List[Achievement]] = {}
        
    def get_student_dashboard(self, student_id: str) -> Dict[str, Any]:
        """Get comprehensive student dashboard data"""
        # Get student's courses
        courses = self.enrollments.get(student_id, [])
        
        # Get upcoming assignments
        upcoming_assignments = self._get_upcoming_assignments(student_id)
        
        # Get recent grades
        recent_grades = self._get_recent_grades(student_id)
        
        # Get learning progress
        learning_progress = self._get_learning_progress(student_id)
        
        # Get notifications
        notifications = self.notifications.get(student_id, [])
        unread_notifications = [n for n in notifications if not n.read]
        
        # Get achievements
        achievements = self.achievements.get(student_id, [])
        recent_achievements = sorted(achievements, key=lambda x: x.earned_date, reverse=True)[:5]
        
        # Get AI tutor recommendations
        tutor_recommendations = self._get_tutor_recommendations(student_id)
        
        # Get AI assistant support
        assistant_support = self._get_assistant_support(student_id)
        
        return {
            "student_id": student_id,
            "dashboard_data": {
                "courses": [
                    {
                        "course_id": course.course_id,
                        "title": course.course_title,
                        "professor_id": course.professor_id,
                        "current_grade": course.current_grade,
                        "progress_percentage": course.progress_percentage,
                        "status": course.status,
                        "last_accessed": course.last_accessed.isoformat() if course.last_accessed else None
                    }
                    for course in courses
                ],
                "upcoming_assignments": [
                    {
                        "assignment_id": assignment.assignment_id,
                        "course_id": assignment.course_id,
                        "title": assignment.title,
                        "type": assignment.assignment_type.value,
                        "due_date": assignment.due_date.isoformat(),
                        "points_possible": assignment.points_possible,
                        "status": assignment.status.value
                    }
                    for assignment in upcoming_assignments
                ],
                "recent_grades": [
                    {
                        "assignment_id": grade.assignment_id,
                        "title": grade.title,
                        "grade": grade.grade,
                        "points_possible": grade.points_possible,
                        "submission_date": grade.submission_date.isoformat() if grade.submission_date else None,
                        "feedback": grade.feedback
                    }
                    for grade in recent_grades
                ],
                "learning_progress": learning_progress,
                "notifications": [
                    {
                        "notification_id": notif.notification_id,
                        "type": notif.type.value,
                        "title": notif.title,
                        "message": notif.message,
                        "created_at": notif.created_at.isoformat(),
                        "read": notif.read,
                        "action_required": notif.action_required,
                        "action_url": notif.action_url
                    }
                    for notif in unread_notifications[:10]
                ],
                "achievements": [
                    {
                        "achievement_id": achievement.achievement_id,
                        "title": achievement.title,
                        "description": achievement.description,
                        "icon_url": achievement.icon_url,
                        "earned_date": achievement.earned_date.isoformat(),
                        "category": achievement.category,
                        "points": achievement.points
                    }
                    for achievement in recent_achievements
                ],
                "tutor_recommendations": tutor_recommendations,
                "assistant_support": assistant_support
            },
            "summary_stats": {
                "total_courses": len(courses),
                "active_courses": len([c for c in courses if c.status == "active"]),
                "upcoming_deadlines": len(upcoming_assignments),
                "unread_notifications": len(unread_notifications),
                "total_achievements": len(achievements),
                "overall_gpa": self._calculate_overall_gpa(student_id),
                "completion_rate": self._calculate_completion_rate(student_id)
            }
        }
    
    def enroll_in_course(self, student_id: str, course_id: str, course_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enroll student in a course"""
        enrollment_id = f"ENROLL_{uuid.uuid4().hex[:8]}"
        
        enrollment = CourseEnrollment(
            enrollment_id=enrollment_id,
            student_id=student_id,
            course_id=course_id,
            course_title=course_data["title"],
            professor_id=course_data["professor_id"],
            enrollment_date=datetime.now(),
            status="active",
            progress_percentage=0.0
        )
        
        if student_id not in self.enrollments:
            self.enrollments[student_id] = []
        self.enrollments[student_id].append(enrollment)
        
        # Initialize assignments for the course
        self._initialize_course_assignments(student_id, course_id, course_data)
        
        # Create welcome notification
        self._create_notification(student_id, NotificationType.COURSE_UPDATE,
                                f"Welcome to {course_data['title']}!",
                                f"You've been enrolled in {course_data['title']}. Check out the course materials and assignments.")
        
        return {
            "success": True,
            "enrollment_id": enrollment_id,
            "course_id": course_id,
            "message": f"Successfully enrolled in {course_data['title']}"
        }
    
    def _initialize_course_assignments(self, student_id: str, course_id: str, course_data: Dict[str, Any]):
        """Initialize assignments for enrolled course"""
        if student_id not in self.assignments:
            self.assignments[student_id] = []
        
        # Generate sample assignments (in real system, this would come from course content)
        assignments = [
            Assignment(
                assignment_id=f"ASSIGN_{uuid.uuid4().hex[:8]}",
                course_id=course_id,
                title="Week 1: Introduction to AI",
                assignment_type=AssignmentType.LECTURE,
                due_date=datetime.now() + timedelta(days=7),
                points_possible=100,
                status=LearningStatus.NOT_STARTED
            ),
            Assignment(
                assignment_id=f"ASSIGN_{uuid.uuid4().hex[:8]}",
                course_id=course_id,
                title="Week 1 Quiz",
                assignment_type=AssignmentType.QUIZ,
                due_date=datetime.now() + timedelta(days=10),
                points_possible=50,
                status=LearningStatus.NOT_STARTED
            ),
            Assignment(
                assignment_id=f"ASSIGN_{uuid.uuid4().hex[:8]}",
                course_id=course_id,
                title="AI Ethics Assignment",
                assignment_type=AssignmentType.ASSIGNMENT,
                due_date=datetime.now() + timedelta(days=14),
                points_possible=150,
                status=LearningStatus.NOT_STARTED
            )
        ]
        
        self.assignments[student_id].extend(assignments)
    
    def submit_assignment(self, student_id: str, assignment_id: str, submission_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit assignment"""
        student_assignments = self.assignments.get(student_id, [])
        assignment = next((a for a in student_assignments if a.assignment_id == assignment_id), None)
        
        if not assignment:
            return {"success": False, "error": "Assignment not found"}
        
        if assignment.status == LearningStatus.COMPLETED:
            return {"success": False, "error": "Assignment already submitted"}
        
        if assignment.attempts >= assignment.max_attempts:
            return {"success": False, "error": "Maximum attempts exceeded"}
        
        # Update assignment
        assignment.status = LearningStatus.COMPLETED
        assignment.submission_date = datetime.now()
        assignment.attempts += 1
        
        # Simulate grading (in real system, this would be done by professor or AI)
        assignment.grade = self._simulate_grading(assignment, submission_data)
        assignment.feedback = self._generate_feedback(assignment, submission_data)
        
        # Update course progress
        self._update_course_progress(student_id, assignment.course_id)
        
        # Create notification
        self._create_notification(student_id, NotificationType.GRADE_POSTED,
                                f"Grade posted for {assignment.title}",
                                f"Your grade: {assignment.grade}/{assignment.points_possible}")
        
        # Check for achievements
        self._check_achievements(student_id, assignment)
        
        return {
            "success": True,
            "assignment_id": assignment_id,
            "grade": assignment.grade,
            "feedback": assignment.feedback,
            "submission_date": assignment.submission_date.isoformat()
        }
    
    def _simulate_grading(self, assignment: Assignment, submission_data: Dict[str, Any]) -> float:
        """Simulate assignment grading"""
        # Simple grading simulation
        base_score = random.uniform(0.7, 1.0)  # 70-100%
        
        # Adjust based on submission quality
        submission_text = submission_data.get("content", "").lower()
        if len(submission_text) > 100:
            base_score += 0.05
        if any(word in submission_text for word in ["analysis", "example", "because", "therefore"]):
            base_score += 0.1
        
        return min(assignment.points_possible, assignment.points_possible * base_score)
    
    def _generate_feedback(self, assignment: Assignment, submission_data: Dict[str, Any]) -> str:
        """Generate feedback for assignment"""
        if assignment.grade >= assignment.points_possible * 0.9:
            return "Excellent work! Your understanding of the concepts is clear and well-articulated."
        elif assignment.grade >= assignment.points_possible * 0.8:
            return "Good work! You demonstrate solid understanding with room for improvement in some areas."
        elif assignment.grade >= assignment.points_possible * 0.7:
            return "Satisfactory work. Consider reviewing the material and providing more detailed explanations."
        else:
            return "Please review the course materials and consider scheduling a tutoring session for additional support."
    
    def _update_course_progress(self, student_id: str, course_id: str):
        """Update course progress percentage"""
        student_assignments = self.assignments.get(student_id, [])
        course_assignments = [a for a in student_assignments if a.course_id == course_id]
        
        if not course_assignments:
            return
        
        completed_assignments = [a for a in course_assignments if a.status == LearningStatus.COMPLETED]
        progress_percentage = len(completed_assignments) / len(course_assignments) * 100
        
        # Update enrollment
        enrollment = next((e for e in self.enrollments[student_id] if e.course_id == course_id), None)
        if enrollment:
            enrollment.progress_percentage = progress_percentage
            enrollment.last_accessed = datetime.now()
    
    def _check_achievements(self, student_id: str, assignment: Assignment):
        """Check for new achievements"""
        if assignment.grade >= assignment.points_possible * 0.9:
            # High grade achievement
            achievement = Achievement(
                achievement_id=f"ACH_{uuid.uuid4().hex[:8]}",
                student_id=student_id,
                title="High Achiever",
                description=f"Scored 90% or higher on {assignment.title}",
                icon_url="/icons/high-achiever.png",
                earned_date=datetime.now(),
                category="academic",
                points=10
            )
            
            if student_id not in self.achievements:
                self.achievements[student_id] = []
            self.achievements[student_id].append(achievement)
            
            # Create notification
            self._create_notification(student_id, NotificationType.ACHIEVEMENT,
                                    "Achievement Unlocked!",
                                    f"You earned the 'High Achiever' badge for {assignment.title}")
    
    def start_tutoring_session(self, student_id: str, course_id: str, topic: str) -> Dict[str, Any]:
        """Start AI tutoring session"""
        if not self.tutor_system:
            return {"success": False, "error": "Tutor system not available"}
        
        # Get student profile
        profile_result = self.tutor_system.get_student_progress(student_id)
        if "error" in profile_result:
            # Create new profile
            profile_data = {
                "learning_style_quiz": {},
                "background": {"programming_experience": "intermediate"},
                "preferences": {},
                "strengths": [],
                "challenges": [],
                "goals": [],
                "interests": []
            }
            self.tutor_system.create_student_profile(student_id, "Student", "student@msai.edu", profile_data)
        
        # Start session
        session_result = self.tutor_system.start_tutoring_session(student_id, course_id, topic)
        
        if session_result["success"]:
            # Create notification
            self._create_notification(student_id, NotificationType.TUTOR_SESSION,
                                    "Tutoring Session Started",
                                    f"Your AI tutor {session_result['tutor_name']} is ready to help with {topic}")
        
        return session_result
    
    def request_assistant_support(self, student_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Request AI assistant support"""
        if not self.assistant_system:
            return {"success": False, "error": "Assistant system not available"}
        
        result = self.assistant_system.submit_student_request(student_id, request_data)
        
        if result["success"]:
            # Create notification
            self._create_notification(student_id, NotificationType.SYSTEM_ALERT,
                                    "Support Request Submitted",
                                    f"Your request has been assigned to {result['assigned_assistant']}")
        
        return result
    
    def _get_upcoming_assignments(self, student_id: str) -> List[Assignment]:
        """Get upcoming assignments for student"""
        student_assignments = self.assignments.get(student_id, [])
        now = datetime.now()
        
        upcoming = [
            a for a in student_assignments
            if a.due_date > now and a.status != LearningStatus.COMPLETED
        ]
        
        return sorted(upcoming, key=lambda x: x.due_date)[:10]
    
    def _get_recent_grades(self, student_id: str) -> List[Assignment]:
        """Get recent grades for student"""
        student_assignments = self.assignments.get(student_id, [])
        
        graded = [
            a for a in student_assignments
            if a.grade is not None and a.submission_date is not None
        ]
        
        return sorted(graded, key=lambda x: x.submission_date, reverse=True)[:10]
    
    def _get_learning_progress(self, student_id: str) -> Dict[str, Any]:
        """Get learning progress summary"""
        courses = self.enrollments.get(student_id, [])
        student_assignments = self.assignments.get(student_id, [])
        
        total_assignments = len(student_assignments)
        completed_assignments = len([a for a in student_assignments if a.status == LearningStatus.COMPLETED])
        
        return {
            "total_courses": len(courses),
            "active_courses": len([c for c in courses if c.status == "active"]),
            "total_assignments": total_assignments,
            "completed_assignments": completed_assignments,
            "completion_rate": (completed_assignments / total_assignments * 100) if total_assignments > 0 else 0,
            "average_grade": self._calculate_average_grade(student_id)
        }
    
    def _calculate_average_grade(self, student_id: str) -> float:
        """Calculate average grade for student"""
        student_assignments = self.assignments.get(student_id, [])
        graded_assignments = [a for a in student_assignments if a.grade is not None]
        
        if not graded_assignments:
            return 0.0
        
        total_points = sum(a.grade for a in graded_assignments)
        total_possible = sum(a.points_possible for a in graded_assignments)
        
        return (total_points / total_possible * 100) if total_possible > 0 else 0.0
    
    def _calculate_overall_gpa(self, student_id: str) -> float:
        """Calculate overall GPA"""
        courses = self.enrollments.get(student_id, [])
        courses_with_grades = [c for c in courses if c.current_grade is not None]
        
        if not courses_with_grades:
            return 0.0
        
        # Convert percentage grades to GPA (simplified)
        total_gpa = 0
        for course in courses_with_grades:
            if course.current_grade >= 90:
                total_gpa += 4.0
            elif course.current_grade >= 80:
                total_gpa += 3.0
            elif course.current_grade >= 70:
                total_gpa += 2.0
            elif course.current_grade >= 60:
                total_gpa += 1.0
        
        return total_gpa / len(courses_with_grades)
    
    def _calculate_completion_rate(self, student_id: str) -> float:
        """Calculate overall completion rate"""
        courses = self.enrollments.get(student_id, [])
        if not courses:
            return 0.0
        
        total_progress = sum(c.progress_percentage for c in courses)
        return total_progress / len(courses)
    
    def _get_tutor_recommendations(self, student_id: str) -> List[Dict[str, Any]]:
        """Get AI tutor recommendations"""
        if not self.tutor_system:
            return []
        
        progress = self.tutor_system.get_student_progress(student_id)
        if "error" in progress:
            return []
        
        recommendations = progress.get("recommendations", [])
        
        return [
            {
                "type": "tutoring_session",
                "title": "Schedule Tutoring Session",
                "description": "Get personalized help with challenging topics",
                "action_url": "/tutoring/schedule"
            },
            {
                "type": "study_group",
                "title": "Join Study Group",
                "description": "Connect with peers for collaborative learning",
                "action_url": "/study-groups"
            }
        ]
    
    def _get_assistant_support(self, student_id: str) -> Dict[str, Any]:
        """Get AI assistant support options"""
        return {
            "available_assistants": [
                {
                    "type": "academic_advisor",
                    "name": "Dr. Maya Academic",
                    "specialization": "Academic Planning",
                    "available": True
                },
                {
                    "type": "technical_support",
                    "name": "Tech Support Taylor",
                    "specialization": "Technical Issues",
                    "available": True
                },
                {
                    "type": "career_counselor",
                    "name": "Career Coach Carlos",
                    "specialization": "Career Development",
                    "available": True
                }
            ],
            "quick_support": [
                {
                    "title": "Academic Questions",
                    "description": "Get help with course selection and planning",
                    "action_url": "/support/academic"
                },
                {
                    "title": "Technical Issues",
                    "description": "Resolve platform and software problems",
                    "action_url": "/support/technical"
                },
                {
                    "title": "Career Guidance",
                    "description": "Explore career opportunities and development",
                    "action_url": "/support/career"
                }
            ]
        }
    
    def _create_notification(self, student_id: str, notification_type: NotificationType,
                          title: str, message: str, action_required: bool = False,
                          action_url: Optional[str] = None):
        """Create notification for student"""
        notification = Notification(
            notification_id=f"NOTIF_{uuid.uuid4().hex[:8]}",
            student_id=student_id,
            type=notification_type,
            title=title,
            message=message,
            created_at=datetime.now(),
            action_required=action_required,
            action_url=action_url
        )
        
        if student_id not in self.notifications:
            self.notifications[student_id] = []
        self.notifications[student_id].append(notification)
    
    def mark_notification_read(self, student_id: str, notification_id: str) -> Dict[str, Any]:
        """Mark notification as read"""
        student_notifications = self.notifications.get(student_id, [])
        notification = next((n for n in student_notifications if n.notification_id == notification_id), None)
        
        if not notification:
            return {"success": False, "error": "Notification not found"}
        
        notification.read = True
        
        return {
            "success": True,
            "notification_id": notification_id,
            "message": "Notification marked as read"
        }
    
    def create_learning_goal(self, student_id: str, goal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create learning goal for student"""
        goal_id = f"GOAL_{uuid.uuid4().hex[:8]}"
        
        goal = LearningGoal(
            goal_id=goal_id,
            student_id=student_id,
            title=goal_data["title"],
            description=goal_data["description"],
            target_date=datetime.fromisoformat(goal_data["target_date"]),
            status="active"
        )
        
        if student_id not in self.learning_goals:
            self.learning_goals[student_id] = []
        self.learning_goals[student_id].append(goal)
        
        return {
            "success": True,
            "goal_id": goal_id,
            "message": "Learning goal created successfully"
        }
    
    def get_learning_goals(self, student_id: str) -> List[Dict[str, Any]]:
        """Get student's learning goals"""
        goals = self.learning_goals.get(student_id, [])
        
        return [
            {
                "goal_id": goal.goal_id,
                "title": goal.title,
                "description": goal.description,
                "target_date": goal.target_date.isoformat(),
                "progress_percentage": goal.progress_percentage,
                "status": goal.status,
                "created_at": goal.created_at.isoformat()
            }
            for goal in goals
        ]