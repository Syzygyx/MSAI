"""
Administrator Portal for MS AI Curriculum System
Comprehensive system management and oversight capabilities
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import json
from enum import Enum

class SystemStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    MAINTENANCE = "maintenance"

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class SystemAlert:
    """System alert for administrators"""
    alert_id: str
    level: AlertLevel
    title: str
    description: str
    timestamp: datetime
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None

@dataclass
class SystemMetrics:
    """System performance metrics"""
    timestamp: datetime
    active_users: int
    total_courses: int
    total_students: int
    total_instructors: int
    system_load: float
    memory_usage: float
    disk_usage: float
    database_connections: int
    api_response_time: float

@dataclass
class AdminAgent:
    """AI Agent specialized for administrative tasks"""
    agent_id: str
    name: str
    specialization: str
    capabilities: List[str]
    status: str = "active"
    last_activity: Optional[datetime] = None
    task_history: List[Dict[str, Any]] = field(default_factory=list)

class AdministratorPortal:
    """Main administrator portal with comprehensive system management"""
    
    def __init__(self, user_manager, professor_system, curriculum_generator):
        self.user_manager = user_manager
        self.professor_system = professor_system
        self.curriculum_generator = curriculum_generator
        self.system_alerts = []
        self.system_metrics = []
        self.admin_agents = self._initialize_admin_agents()
        
    def _initialize_admin_agents(self) -> List[AdminAgent]:
        """Initialize AI agents for administrative tasks"""
        agents = [
            AdminAgent(
                agent_id="ADMIN_AGENT_001",
                name="System Monitor Agent",
                specialization="system_monitoring",
                capabilities=[
                    "performance_monitoring",
                    "alert_management",
                    "resource_optimization",
                    "security_monitoring"
                ]
            ),
            AdminAgent(
                agent_id="ADMIN_AGENT_002",
                name="User Management Agent",
                specialization="user_administration",
                capabilities=[
                    "user_account_management",
                    "role_assignment",
                    "permission_management",
                    "access_control"
                ]
            ),
            AdminAgent(
                agent_id="ADMIN_AGENT_003",
                name="Curriculum Oversight Agent",
                specialization="curriculum_management",
                capabilities=[
                    "curriculum_compliance_monitoring",
                    "accreditation_tracking",
                    "course_quality_assessment",
                    "learning_outcome_analysis"
                ]
            ),
            AdminAgent(
                agent_id="ADMIN_AGENT_004",
                name="Analytics Intelligence Agent",
                specialization="data_analytics",
                capabilities=[
                    "performance_analytics",
                    "predictive_modeling",
                    "trend_analysis",
                    "report_generation"
                ]
            )
        ]
        return agents
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data for administrators"""
        current_metrics = self._get_current_system_metrics()
        recent_alerts = self._get_recent_alerts()
        user_statistics = self._get_user_statistics()
        course_statistics = self._get_course_statistics()
        ai_agent_status = self._get_ai_agent_status()
        
        return {
            "system_status": self._get_system_status(),
            "metrics": current_metrics,
            "alerts": recent_alerts,
            "user_statistics": user_statistics,
            "course_statistics": course_statistics,
            "ai_agent_status": ai_agent_status,
            "accreditation_status": self._get_accreditation_status(),
            "performance_trends": self._get_performance_trends()
        }
    
    def _get_current_system_metrics(self) -> SystemMetrics:
        """Get current system performance metrics"""
        # Simulate real-time metrics
        return SystemMetrics(
            timestamp=datetime.now(),
            active_users=len([u for u in self.user_manager.users.values() if u.status.value == "active"]),
            total_courses=len(self.curriculum_generator.generate_core_courses()) + 
                         sum(len(courses) for courses in self.curriculum_generator.generate_specialization_tracks().values()),
            total_students=len([u for u in self.user_manager.users.values() if u.role.value == "student"]),
            total_instructors=len([u for u in self.user_manager.users.values() if u.role.value == "instructor"]),
            system_load=0.45,  # Simulated
            memory_usage=0.62,  # Simulated
            disk_usage=0.38,  # Simulated
            database_connections=12,  # Simulated
            api_response_time=0.15  # Simulated
        )
    
    def _get_recent_alerts(self) -> List[Dict[str, Any]]:
        """Get recent system alerts"""
        recent_alerts = []
        
        # Check for system issues and generate alerts
        metrics = self._get_current_system_metrics()
        
        if metrics.system_load > 0.8:
            recent_alerts.append({
                "level": "warning",
                "title": "High System Load",
                "description": f"System load is at {metrics.system_load:.2f}",
                "timestamp": datetime.now().isoformat()
            })
        
        if metrics.memory_usage > 0.9:
            recent_alerts.append({
                "level": "critical",
                "title": "High Memory Usage",
                "description": f"Memory usage is at {metrics.memory_usage:.2f}",
                "timestamp": datetime.now().isoformat()
            })
        
        if metrics.api_response_time > 1.0:
            recent_alerts.append({
                "level": "warning",
                "title": "Slow API Response",
                "description": f"API response time is {metrics.api_response_time:.2f}s",
                "timestamp": datetime.now().isoformat()
            })
        
        return recent_alerts
    
    def _get_user_statistics(self) -> Dict[str, Any]:
        """Get user statistics"""
        users = self.user_manager.users.values()
        
        return {
            "total_users": len(users),
            "active_users": len([u for u in users if u.status.value == "active"]),
            "pending_users": len([u for u in users if u.status.value == "pending"]),
            "suspended_users": len([u for u in users if u.status.value == "suspended"]),
            "role_distribution": {
                "administrators": len([u for u in users if u.role.value == "administrator"]),
                "instructors": len([u for u in users if u.role.value == "instructor"]),
                "students": len([u for u in users if u.role.value == "student"]),
                "guests": len([u for u in users if u.role.value == "guest"])
            },
            "recent_registrations": len([u for u in users if (datetime.now() - u.created_at).days <= 7])
        }
    
    def _get_course_statistics(self) -> Dict[str, Any]:
        """Get course and curriculum statistics"""
        curriculum = self.curriculum_generator.generate_complete_curriculum()
        
        return {
            "total_courses": len(curriculum.core_courses) + 
                           sum(len(courses) for courses in curriculum.specialization_courses.values()),
            "core_courses": len(curriculum.core_courses),
            "specialization_tracks": len(curriculum.specialization_courses),
            "total_credits": curriculum.total_credits,
            "accreditation_body": curriculum.accreditation_body,
            "ai_professors": len(self.professor_system.professors),
            "research_publications": sum(len(p.publications) for p in self.professor_system.professors)
        }
    
    def _get_ai_agent_status(self) -> Dict[str, Any]:
        """Get AI agent status"""
        return {
            "total_agents": len(self.admin_agents),
            "active_agents": len([a for a in self.admin_agents if a.status == "active"]),
            "agents": [
                {
                    "id": agent.agent_id,
                    "name": agent.name,
                    "specialization": agent.specialization,
                    "status": agent.status,
                    "capabilities": agent.capabilities,
                    "last_activity": agent.last_activity.isoformat() if agent.last_activity else None
                }
                for agent in self.admin_agents
            ]
        }
    
    def _get_system_status(self) -> str:
        """Get overall system status"""
        metrics = self._get_current_system_metrics()
        
        if metrics.system_load > 0.9 or metrics.memory_usage > 0.95:
            return SystemStatus.CRITICAL.value
        elif metrics.system_load > 0.7 or metrics.memory_usage > 0.8:
            return SystemStatus.WARNING.value
        else:
            return SystemStatus.HEALTHY.value
    
    def _get_accreditation_status(self) -> Dict[str, Any]:
        """Get accreditation compliance status"""
        return {
            "sacscoc_compliance": "compliant",
            "florida_state_compliance": "compliant",
            "last_audit": "2024-01-15",
            "next_audit": "2025-01-15",
            "compliance_score": 98.5,
            "outstanding_issues": [],
            "recommendations": [
                "Continue monitoring student learning outcomes",
                "Maintain faculty qualification documentation",
                "Update curriculum materials annually"
            ]
        }
    
    def _get_performance_trends(self) -> Dict[str, Any]:
        """Get performance trends over time"""
        return {
            "user_growth": {
                "last_30_days": 15,
                "last_90_days": 45,
                "last_year": 180
            },
            "course_completion": {
                "average_completion_rate": 87.3,
                "trend": "increasing"
            },
            "system_performance": {
                "average_response_time": 0.12,
                "uptime_percentage": 99.8,
                "trend": "stable"
            }
        }
    
    def manage_users(self, action: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Manage user accounts"""
        if action == "create":
            return self._create_user_account(user_data)
        elif action == "update":
            return self._update_user_account(user_data)
        elif action == "suspend":
            return self._suspend_user_account(user_data["user_id"])
        elif action == "activate":
            return self._activate_user_account(user_data["user_id"])
        elif action == "delete":
            return self._delete_user_account(user_data["user_id"])
        else:
            return {"error": "Invalid action"}
    
    def _create_user_account(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new user account"""
        try:
            from portals.user_management import UserRole
            role = UserRole(user_data["role"])
            
            user = self.user_manager.create_user(
                email=user_data["email"],
                password=user_data["password"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                role=role
            )
            
            return {
                "success": True,
                "user_id": user.user_id,
                "message": f"User account created successfully for {user.email}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _update_user_account(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user account"""
        user_id = user_data["user_id"]
        user = self.user_manager.users.get(user_id)
        
        if not user:
            return {"success": False, "error": "User not found"}
        
        # Update user fields
        if "first_name" in user_data:
            user.first_name = user_data["first_name"]
        if "last_name" in user_data:
            user.last_name = user_data["last_name"]
        if "email" in user_data:
            user.email = user_data["email"]
        if "role" in user_data:
            from portals.user_management import UserRole
            user.role = UserRole(user_data["role"])
            user.permissions = self.user_manager._get_default_permissions(user.role)
        
        return {
            "success": True,
            "message": f"User account updated successfully for {user.email}"
        }
    
    def _suspend_user_account(self, user_id: str) -> Dict[str, Any]:
        """Suspend user account"""
        user = self.user_manager.users.get(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        
        from portals.user_management import UserStatus
        user.status = UserStatus.SUSPENDED
        
        return {
            "success": True,
            "message": f"User account suspended for {user.email}"
        }
    
    def _activate_user_account(self, user_id: str) -> Dict[str, Any]:
        """Activate user account"""
        user = self.user_manager.users.get(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        
        from portals.user_management import UserStatus
        user.status = UserStatus.ACTIVE
        
        return {
            "success": True,
            "message": f"User account activated for {user.email}"
        }
    
    def _delete_user_account(self, user_id: str) -> Dict[str, Any]:
        """Delete user account"""
        user = self.user_manager.users.get(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        
        email = user.email
        del self.user_manager.users[user_id]
        
        return {
            "success": True,
            "message": f"User account deleted for {email}"
        }
    
    def generate_system_report(self, report_type: str) -> Dict[str, Any]:
        """Generate comprehensive system reports"""
        if report_type == "user_activity":
            return self._generate_user_activity_report()
        elif report_type == "system_performance":
            return self._generate_system_performance_report()
        elif report_type == "accreditation_compliance":
            return self._generate_accreditation_report()
        elif report_type == "ai_agent_performance":
            return self._generate_ai_agent_report()
        else:
            return {"error": "Invalid report type"}
    
    def _generate_user_activity_report(self) -> Dict[str, Any]:
        """Generate user activity report"""
        users = self.user_manager.users.values()
        
        return {
            "report_type": "user_activity",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_users": len(users),
                "active_users": len([u for u in users if u.status.value == "active"]),
                "new_users_this_month": len([u for u in users if (datetime.now() - u.created_at).days <= 30])
            },
            "user_breakdown": {
                "by_role": {
                    role.value: len([u for u in users if u.role.value == role.value])
                    for role in [u.role for u in users]
                },
                "by_status": {
                    status.value: len([u for u in users if u.status.value == status.value])
                    for status in [u.status for u in users]
                }
            }
        }
    
    def _generate_system_performance_report(self) -> Dict[str, Any]:
        """Generate system performance report"""
        metrics = self._get_current_system_metrics()
        
        return {
            "report_type": "system_performance",
            "generated_at": datetime.now().isoformat(),
            "performance_metrics": {
                "system_load": metrics.system_load,
                "memory_usage": metrics.memory_usage,
                "disk_usage": metrics.disk_usage,
                "api_response_time": metrics.api_response_time,
                "database_connections": metrics.database_connections
            },
            "recommendations": [
                "Monitor system load during peak hours",
                "Consider scaling resources if usage continues to grow",
                "Optimize database queries for better performance"
            ]
        }
    
    def _generate_accreditation_report(self) -> Dict[str, Any]:
        """Generate accreditation compliance report"""
        return {
            "report_type": "accreditation_compliance",
            "generated_at": datetime.now().isoformat(),
            "compliance_status": "compliant",
            "sacscoc_standards": {
                "faculty_qualifications": "compliant",
                "curriculum_rigor": "compliant",
                "assessment_plan": "compliant",
                "student_learning_outcomes": "compliant"
            },
            "florida_requirements": {
                "core_competencies": "compliant",
                "practical_experience": "compliant",
                "assessment_standards": "compliant"
            },
            "next_review_date": "2025-01-15"
        }
    
    def _generate_ai_agent_report(self) -> Dict[str, Any]:
        """Generate AI agent performance report"""
        return {
            "report_type": "ai_agent_performance",
            "generated_at": datetime.now().isoformat(),
            "agent_summary": {
                "total_agents": len(self.admin_agents),
                "active_agents": len([a for a in self.admin_agents if a.status == "active"]),
                "total_tasks_completed": sum(len(a.task_history) for a in self.admin_agents)
            },
            "agent_performance": [
                {
                    "agent_id": agent.agent_id,
                    "name": agent.name,
                    "specialization": agent.specialization,
                    "tasks_completed": len(agent.task_history),
                    "status": agent.status
                }
                for agent in self.admin_agents
            ]
        }
    
    def configure_ai_agents(self, agent_id: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
        """Configure AI agent settings"""
        agent = next((a for a in self.admin_agents if a.agent_id == agent_id), None)
        if not agent:
            return {"error": "Agent not found"}
        
        # Update agent configuration
        if "status" in configuration:
            agent.status = configuration["status"]
        if "capabilities" in configuration:
            agent.capabilities = configuration["capabilities"]
        
        agent.last_activity = datetime.now()
        
        return {
            "success": True,
            "message": f"Agent {agent.name} configured successfully"
        }