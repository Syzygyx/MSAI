"""
User Management System for MS AI Curriculum
Role-based access control and user authentication
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import hashlib
import secrets
import jwt
from passlib.context import CryptContext

class UserRole(Enum):
    ADMINISTRATOR = "administrator"
    INSTRUCTOR = "instructor"
    STUDENT = "student"
    GUEST = "guest"

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"

@dataclass
class User:
    """User entity with role-based permissions"""
    user_id: str
    email: str
    password_hash: str
    first_name: str
    last_name: str
    role: UserRole
    status: UserStatus
    created_at: datetime
    last_login: Optional[datetime] = None
    profile_data: Dict[str, Any] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UserSession:
    """User session management"""
    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True

class UserManager:
    """Manages user accounts and authentication"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, UserSession] = {}
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.jwt_secret = "MSAI_JWT_SECRET_2024_PRODUCTION"
        self.jwt_algorithm = "HS256"
        
    def create_user(self, email: str, password: str, first_name: str, 
                   last_name: str, role: UserRole) -> User:
        """Create a new user account"""
        user_id = f"USER_{len(self.users) + 1:06d}"
        password_hash = self.pwd_context.hash(password)
        
        user = User(
            user_id=user_id,
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=role,
            status=UserStatus.PENDING,
            created_at=datetime.now(),
            permissions=self._get_default_permissions(role),
            preferences=self._get_default_preferences(role)
        )
        
        self.users[user_id] = user
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self._find_user_by_email(email)
        if not user:
            return None
        
        if not self.pwd_context.verify(password, user.password_hash):
            return None
        
        if user.status != UserStatus.ACTIVE:
            return None
        
        # Update last login
        user.last_login = datetime.now()
        return user
    
    def create_session(self, user: User, ip_address: str, user_agent: str) -> UserSession:
        """Create a new user session"""
        session_id = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)
        
        session = UserSession(
            session_id=session_id,
            user_id=user.user_id,
            created_at=datetime.now(),
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.sessions[session_id] = session
        return session
    
    def validate_session(self, session_id: str) -> Optional[User]:
        """Validate user session and return user"""
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        if not session.is_active:
            return None
        
        if datetime.now() > session.expires_at:
            session.is_active = False
            return None
        
        user = self.users.get(session.user_id)
        if not user or user.status != UserStatus.ACTIVE:
            return None
        
        return user
    
    def generate_jwt_token(self, user: User) -> str:
        """Generate JWT token for user"""
        payload = {
            'user_id': user.user_id,
            'email': user.email,
            'role': user.role.value,
            'exp': datetime.now() + timedelta(hours=24),
            'iat': datetime.now()
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    def validate_jwt_token(self, token: str) -> Optional[User]:
        """Validate JWT token and return user"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            user_id = payload['user_id']
            return self.users.get(user_id)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def _find_user_by_email(self, email: str) -> Optional[User]:
        """Find user by email address"""
        for user in self.users.values():
            if user.email.lower() == email.lower():
                return user
        return None
    
    def _get_default_permissions(self, role: UserRole) -> List[str]:
        """Get default permissions for user role"""
        permissions_map = {
            UserRole.ADMINISTRATOR: [
                'system_admin', 'user_management', 'course_management',
                'curriculum_management', 'accreditation_management',
                'analytics_access', 'reporting_access', 'ai_agent_management'
            ],
            UserRole.INSTRUCTOR: [
                'course_management', 'student_management', 'grading_access',
                'ai_professor_access', 'curriculum_access', 'analytics_access'
            ],
            UserRole.STUDENT: [
                'course_access', 'assignment_submission', 'ai_tutor_access',
                'progress_tracking', 'peer_interaction'
            ],
            UserRole.GUEST: [
                'public_content_access'
            ]
        }
        return permissions_map.get(role, [])
    
    def _get_default_preferences(self, role: UserRole) -> Dict[str, Any]:
        """Get default preferences for user role"""
        preferences_map = {
            UserRole.ADMINISTRATOR: {
                'dashboard_layout': 'admin_dashboard',
                'notifications': ['system_alerts', 'user_activity', 'accreditation_updates'],
                'theme': 'professional',
                'ai_agent_interaction': 'full_access'
            },
            UserRole.INSTRUCTOR: {
                'dashboard_layout': 'instructor_dashboard',
                'notifications': ['student_submissions', 'course_updates', 'ai_professor_insights'],
                'theme': 'academic',
                'ai_agent_interaction': 'teaching_focused'
            },
            UserRole.STUDENT: {
                'dashboard_layout': 'student_dashboard',
                'notifications': ['assignment_deadlines', 'ai_tutor_sessions', 'peer_interactions'],
                'theme': 'learning_focused',
                'ai_agent_interaction': 'learning_support'
            },
            UserRole.GUEST: {
                'dashboard_layout': 'public_dashboard',
                'notifications': [],
                'theme': 'default',
                'ai_agent_interaction': 'limited'
            }
        }
        return preferences_map.get(role, {})

class RoleBasedAccessControl:
    """Role-based access control system"""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
        
    def check_permission(self, user: User, permission: str) -> bool:
        """Check if user has specific permission"""
        return permission in user.permissions
    
    def check_role_access(self, user: User, required_role: UserRole) -> bool:
        """Check if user has required role or higher"""
        role_hierarchy = {
            UserRole.GUEST: 0,
            UserRole.STUDENT: 1,
            UserRole.INSTRUCTOR: 2,
            UserRole.ADMINISTRATOR: 3
        }
        
        user_level = role_hierarchy.get(user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level
    
    def get_accessible_features(self, user: User) -> List[str]:
        """Get list of features accessible to user"""
        features_map = {
            UserRole.ADMINISTRATOR: [
                'system_dashboard', 'user_management', 'course_management',
                'curriculum_design', 'accreditation_tracking', 'analytics_dashboard',
                'ai_agent_management', 'reporting_tools', 'system_settings'
            ],
            UserRole.INSTRUCTOR: [
                'instructor_dashboard', 'course_management', 'student_management',
                'grading_tools', 'ai_professor_interaction', 'curriculum_access',
                'analytics_access', 'assignment_creation'
            ],
            UserRole.STUDENT: [
                'student_dashboard', 'course_access', 'assignment_submission',
                'ai_tutor_interaction', 'progress_tracking', 'peer_collaboration',
                'neural_network_training', 'portfolio_management'
            ],
            UserRole.GUEST: [
                'public_dashboard', 'course_catalog', 'program_information'
            ]
        }
        return features_map.get(user.role, [])

# Initialize default users for testing
def initialize_default_users() -> UserManager:
    """Initialize system with default users"""
    user_manager = UserManager()
    
    # Create default administrator
    admin = user_manager.create_user(
        email="admin@msai.syzygyx.com",
        password="Admin123!",
        first_name="System",
        last_name="Administrator",
        role=UserRole.ADMINISTRATOR
    )
    admin.status = UserStatus.ACTIVE
    
    # Create default instructor
    instructor = user_manager.create_user(
        email="instructor@msai.syzygyx.com",
        password="Instructor123!",
        first_name="Dr. Jane",
        last_name="Smith",
        role=UserRole.INSTRUCTOR
    )
    instructor.status = UserStatus.ACTIVE
    
    # Create default student
    student = user_manager.create_user(
        email="student@msai.syzygyx.com",
        password="Student123!",
        first_name="John",
        last_name="Doe",
        role=UserRole.STUDENT
    )
    student.status = UserStatus.ACTIVE
    
    return user_manager