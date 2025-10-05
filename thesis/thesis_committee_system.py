"""
MS AI Curriculum System - Thesis Committee System
AI instructor committee formation and management for thesis evaluation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import random

class CommitteeRole(Enum):
    CHAIR = "chair"
    MEMBER = "member"
    EXTERNAL_EXAMINER = "external_examiner"
    GRADUATE_COORDINATOR = "graduate_coordinator"

class CommitteeStatus(Enum):
    FORMING = "forming"
    FORMED = "formed"
    ACTIVE = "active"
    REVIEWING = "reviewing"
    COMPLETED = "completed"
    DISBANDED = "disbanded"

class EvaluationPhase(Enum):
    PROPOSAL_REVIEW = "proposal_review"
    PROGRESS_REVIEW = "progress_review"
    FINAL_REVIEW = "final_review"
    DEFENSE_PREPARATION = "defense_preparation"
    DEFENSE_EVALUATION = "defense_evaluation"

@dataclass
class CommitteeMember:
    """Committee member structure"""
    member_id: str
    professor_id: str
    role: CommitteeRole
    expertise_areas: List[str]
    availability_status: str
    assigned_at: datetime
    responsibilities: List[str] = field(default_factory=list)
    evaluation_history: List[Dict[str, Any]] = field(default_factory=list)
    performance_rating: float = 0.0

@dataclass
class ThesisCommittee:
    """Thesis committee structure"""
    committee_id: str
    thesis_id: str
    student_id: str
    committee_members: List[CommitteeMember]
    status: CommitteeStatus
    formed_at: datetime
    current_phase: EvaluationPhase
    evaluation_schedule: Dict[str, datetime] = field(default_factory=dict)
    meeting_history: List[Dict[str, Any]] = field(default_factory=list)
    evaluation_criteria: Dict[str, Any] = field(default_factory=dict)
    final_recommendation: Optional[str] = None
    completion_date: Optional[datetime] = None

@dataclass
class CommitteeMeeting:
    """Committee meeting structure"""
    meeting_id: str
    committee_id: str
    meeting_type: str
    scheduled_date: datetime
    duration_minutes: int
    agenda: List[str]
    attendees: List[str]
    meeting_notes: str = ""
    decisions_made: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    next_meeting_date: Optional[datetime] = None

class ThesisCommitteeSystem:
    """AI instructor committee formation and management system"""
    
    def __init__(self, professor_system=None, thesis_system=None):
        self.professor_system = professor_system
        self.thesis_system = thesis_system
        
        # Committee data
        self.thesis_committees: Dict[str, ThesisCommittee] = {}
        self.committee_meetings: Dict[str, List[CommitteeMeeting]] = {}
        
        # Committee formation rules
        self.committee_rules = self._initialize_committee_rules()
        
    def _initialize_committee_rules(self) -> Dict[str, Any]:
        """Initialize committee formation rules"""
        return {
            "minimum_members": 3,
            "maximum_members": 5,
            "required_roles": [CommitteeRole.CHAIR, CommitteeRole.MEMBER],
            "optional_roles": [CommitteeRole.EXTERNAL_EXAMINER, CommitteeRole.GRADUATE_COORDINATOR],
            "expertise_requirements": {
                "primary_expertise": 1,  # At least 1 member with primary expertise
                "related_expertise": 1,  # At least 1 member with related expertise
                "methodology_expertise": 1  # At least 1 member with methodology expertise
            },
            "availability_requirements": {
                "minimum_availability": 0.8,  # 80% availability required
                "conflict_resolution": "automatic"  # Automatic conflict resolution
            }
        }
    
    def form_thesis_committee(self, thesis_id: str, student_id: str, 
                            research_area: str, thesis_proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Form AI instructor committee for thesis"""
        
        # Check if committee already exists
        existing_committees = [c for c in self.thesis_committees.values() if c.thesis_id == thesis_id]
        if existing_committees:
            return {
                "success": False,
                "error": "Committee already exists for this thesis",
                "committee_id": existing_committees[0].committee_id
            }
        
        # Create committee
        committee_id = f"COMMITTEE_{uuid.uuid4().hex[:8]}"
        
        # Select committee members
        committee_members = self._select_committee_members(research_area, thesis_proposal)
        
        if len(committee_members) < self.committee_rules["minimum_members"]:
            return {
                "success": False,
                "error": "Unable to form committee - insufficient qualified members",
                "available_members": len(committee_members)
            }
        
        # Create committee
        committee = ThesisCommittee(
            committee_id=committee_id,
            thesis_id=thesis_id,
            student_id=student_id,
            committee_members=committee_members,
            status=CommitteeStatus.FORMED,
            formed_at=datetime.now(),
            current_phase=EvaluationPhase.PROPOSAL_REVIEW,
            evaluation_criteria=self._generate_evaluation_criteria(research_area, thesis_proposal)
        )
        
        self.thesis_committees[committee_id] = committee
        
        # Schedule initial meeting
        initial_meeting = self._schedule_initial_meeting(committee_id)
        
        return {
            "success": True,
            "committee_id": committee_id,
            "thesis_id": thesis_id,
            "student_id": student_id,
            "committee_members": [
                {
                    "member_id": member.member_id,
                    "professor_id": member.professor_id,
                    "role": member.role.value,
                    "expertise_areas": member.expertise_areas,
                    "responsibilities": member.responsibilities
                }
                for member in committee_members
            ],
            "status": CommitteeStatus.FORMED.value,
            "current_phase": EvaluationPhase.PROPOSAL_REVIEW.value,
            "initial_meeting": initial_meeting,
            "evaluation_criteria": committee.evaluation_criteria
        }
    
    def _select_committee_members(self, research_area: str, thesis_proposal: Dict[str, Any]) -> List[CommitteeMember]:
        """Select appropriate AI professors for committee"""
        
        if not self.professor_system:
            return []
        
        professors = self.professor_system.professors
        selected_members = []
        
        # Select chair (primary advisor)
        chair = self._select_committee_chair(professors, research_area)
        if chair:
            selected_members.append(chair)
        
        # Select committee members
        members = self._select_committee_members_by_expertise(professors, research_area, thesis_proposal)
        selected_members.extend(members)
        
        # Select external examiner if needed
        external_examiner = self._select_external_examiner(professors, research_area)
        if external_examiner and len(selected_members) < self.committee_rules["maximum_members"]:
            selected_members.append(external_examiner)
        
        return selected_members
    
    def _select_committee_chair(self, professors: List, research_area: str) -> Optional[CommitteeMember]:
        """Select committee chair"""
        
        # Find professor with matching specialization
        for professor in professors:
            if research_area.lower() in professor.specialization.value.lower():
                return CommitteeMember(
                    member_id=f"MEMBER_{uuid.uuid4().hex[:8]}",
                    professor_id=professor.professor_id,
                    role=CommitteeRole.CHAIR,
                    expertise_areas=[research_area],
                    availability_status="available",
                    assigned_at=datetime.now(),
                    responsibilities=[
                        "Primary thesis advisor",
                        "Overall thesis guidance",
                        "Committee coordination",
                        "Final evaluation oversight"
                    ]
                )
        
        # Default to first professor if no match
        if professors:
            professor = professors[0]
            return CommitteeMember(
                member_id=f"MEMBER_{uuid.uuid4().hex[:8]}",
                professor_id=professor.professor_id,
                role=CommitteeRole.CHAIR,
                expertise_areas=[research_area],
                availability_status="available",
                assigned_at=datetime.now(),
                responsibilities=[
                    "Primary thesis advisor",
                    "Overall thesis guidance",
                    "Committee coordination",
                    "Final evaluation oversight"
                ]
            )
        
        return None
    
    def _select_committee_members_by_expertise(self, professors: List, research_area: str, 
                                            thesis_proposal: Dict[str, Any]) -> List[CommitteeMember]:
        """Select committee members based on expertise requirements"""
        
        members = []
        used_professors = set()
        
        # Extract expertise areas from thesis proposal
        methodology = thesis_proposal.get("methodology", "").lower()
        research_question = thesis_proposal.get("research_question", "").lower()
        
        # Select methodology expert
        methodology_expert = self._find_expertise_match(professors, ["methodology", "research methods", "experimental design"], used_professors)
        if methodology_expert:
            members.append(CommitteeMember(
                member_id=f"MEMBER_{uuid.uuid4().hex[:8]}",
                professor_id=methodology_expert.professor_id,
                role=CommitteeRole.MEMBER,
                expertise_areas=["methodology", "research methods"],
                availability_status="available",
                assigned_at=datetime.now(),
                responsibilities=[
                    "Methodology evaluation",
                    "Research design review",
                    "Statistical analysis guidance"
                ]
            ))
            used_professors.add(methodology_expert.professor_id)
        
        # Select domain expert
        domain_expert = self._find_expertise_match(professors, [research_area], used_professors)
        if domain_expert:
            members.append(CommitteeMember(
                member_id=f"MEMBER_{uuid.uuid4().hex[:8]}",
                professor_id=domain_expert.professor_id,
                role=CommitteeRole.MEMBER,
                expertise_areas=[research_area],
                availability_status="available",
                assigned_at=datetime.now(),
                responsibilities=[
                    "Domain expertise evaluation",
                    "Literature review guidance",
                    "Technical content review"
                ]
            ))
            used_professors.add(domain_expert.professor_id)
        
        # Select additional member if needed
        if len(members) < 2:
            additional_member = self._find_expertise_match(professors, ["artificial intelligence", "machine learning"], used_professors)
            if additional_member:
                members.append(CommitteeMember(
                    member_id=f"MEMBER_{uuid.uuid4().hex[:8]}",
                    professor_id=additional_member.professor_id,
                    role=CommitteeRole.MEMBER,
                    expertise_areas=["artificial intelligence", "machine learning"],
                    availability_status="available",
                    assigned_at=datetime.now(),
                    responsibilities=[
                        "General AI expertise",
                        "Technical evaluation",
                        "Innovation assessment"
                    ]
                ))
        
        return members
    
    def _find_expertise_match(self, professors: List, expertise_keywords: List[str], 
                            used_professors: set) -> Optional[Any]:
        """Find professor matching expertise keywords"""
        
        for professor in professors:
            if professor.professor_id in used_professors:
                continue
            
            # Check specialization
            for keyword in expertise_keywords:
                if keyword.lower() in professor.specialization.value.lower():
                    return professor
            
            # Check research interests
            for keyword in expertise_keywords:
                if any(keyword.lower() in interest.lower() for interest in professor.research_interests):
                    return professor
        
        return None
    
    def _select_external_examiner(self, professors: List, research_area: str) -> Optional[CommitteeMember]:
        """Select external examiner"""
        
        # For simulation, select a professor with different specialization
        for professor in professors:
            if research_area.lower() not in professor.specialization.value.lower():
                return CommitteeMember(
                    member_id=f"MEMBER_{uuid.uuid4().hex[:8]}",
                    professor_id=professor.professor_id,
                    role=CommitteeRole.EXTERNAL_EXAMINER,
                    expertise_areas=[professor.specialization.value],
                    availability_status="available",
                    assigned_at=datetime.now(),
                    responsibilities=[
                        "External perspective evaluation",
                        "Independent assessment",
                        "Quality assurance review"
                    ]
                )
        
        return None
    
    def _generate_evaluation_criteria(self, research_area: str, thesis_proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Generate evaluation criteria for thesis"""
        
        base_criteria = {
            "research_contribution": {
                "weight": 0.3,
                "description": "Originality and contribution to the field",
                "evaluation_points": [
                    "Novel research question",
                    "Significant contribution to knowledge",
                    "Practical applications",
                    "Theoretical advancement"
                ]
            },
            "methodology": {
                "weight": 0.25,
                "description": "Research methodology and approach",
                "evaluation_points": [
                    "Appropriate methodology selection",
                    "Rigorous experimental design",
                    "Data collection and analysis",
                    "Reproducibility"
                ]
            },
            "technical_quality": {
                "weight": 0.2,
                "description": "Technical implementation and quality",
                "evaluation_points": [
                    "Technical implementation quality",
                    "Code/documentation quality",
                    "System performance",
                    "Innovation in approach"
                ]
            },
            "presentation": {
                "weight": 0.15,
                "description": "Thesis presentation and communication",
                "evaluation_points": [
                    "Clear writing and organization",
                    "Effective presentation of results",
                    "Proper citations and references",
                    "Professional presentation"
                ]
            },
            "defense_performance": {
                "weight": 0.1,
                "description": "Thesis defense performance",
                "evaluation_points": [
                    "Understanding of research",
                    "Ability to answer questions",
                    "Defense of methodology",
                    "Future work discussion"
                ]
            }
        }
        
        # Customize criteria based on research area
        if research_area.lower() == "ai_ethics":
            base_criteria["ethical_considerations"] = {
                "weight": 0.2,
                "description": "Ethical considerations and implications",
                "evaluation_points": [
                    "Ethical framework application",
                    "Bias and fairness analysis",
                    "Privacy considerations",
                    "Social impact assessment"
                ]
            }
        
        return base_criteria
    
    def _schedule_initial_meeting(self, committee_id: str) -> Dict[str, Any]:
        """Schedule initial committee meeting"""
        
        committee = self.thesis_committees.get(committee_id)
        if not committee:
            return {"error": "Committee not found"}
        
        # Create meeting
        meeting_id = f"MEETING_{uuid.uuid4().hex[:8]}"
        meeting_date = datetime.now() + timedelta(days=7)  # Schedule for next week
        
        meeting = CommitteeMeeting(
            meeting_id=meeting_id,
            committee_id=committee_id,
            meeting_type="initial_meeting",
            scheduled_date=meeting_date,
            duration_minutes=90,
            agenda=[
                "Committee introduction and roles",
                "Thesis proposal review",
                "Research timeline discussion",
                "Evaluation criteria review",
                "Next steps planning"
            ],
            attendees=[member.professor_id for member in committee.committee_members]
        )
        
        # Store meeting
        if committee_id not in self.committee_meetings:
            self.committee_meetings[committee_id] = []
        self.committee_meetings[committee_id].append(meeting)
        
        return {
            "meeting_id": meeting_id,
            "scheduled_date": meeting_date.isoformat(),
            "duration_minutes": meeting.duration_minutes,
            "agenda": meeting.agenda,
            "attendees": meeting.attendees
        }
    
    def conduct_committee_meeting(self, meeting_id: str, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct committee meeting"""
        
        # Find meeting
        meeting = None
        committee_id = None
        for cid, meetings in self.committee_meetings.items():
            for m in meetings:
                if m.meeting_id == meeting_id:
                    meeting = m
                    committee_id = cid
                    break
            if meeting:
                break
        
        if not meeting:
            return {"success": False, "error": "Meeting not found"}
        
        committee = self.thesis_committees.get(committee_id)
        if not committee:
            return {"success": False, "error": "Committee not found"}
        
        # Update meeting with results
        meeting.meeting_notes = meeting_data.get("meeting_notes", "")
        meeting.decisions_made = meeting_data.get("decisions_made", [])
        meeting.action_items = meeting_data.get("action_items", [])
        meeting.next_meeting_date = datetime.fromisoformat(meeting_data["next_meeting_date"]) if meeting_data.get("next_meeting_date") else None
        
        # Update committee based on meeting results
        if meeting.meeting_type == "initial_meeting":
            committee.status = CommitteeStatus.ACTIVE
            committee.current_phase = EvaluationPhase.PROGRESS_REVIEW
        
        # Store meeting in committee history
        committee.meeting_history.append({
            "meeting_id": meeting_id,
            "meeting_type": meeting.meeting_type,
            "date": meeting.scheduled_date.isoformat(),
            "decisions": meeting.decisions_made,
            "action_items": meeting.action_items
        })
        
        return {
            "success": True,
            "meeting_id": meeting_id,
            "committee_id": committee_id,
            "meeting_results": {
                "meeting_notes": meeting.meeting_notes,
                "decisions_made": meeting.decisions_made,
                "action_items": meeting.action_items,
                "next_meeting_date": meeting.next_meeting_date.isoformat() if meeting.next_meeting_date else None
            },
            "committee_status": committee.status.value,
            "current_phase": committee.current_phase.value
        }
    
    def evaluate_thesis_progress(self, committee_id: str, evaluation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate thesis progress"""
        
        committee = self.thesis_committees.get(committee_id)
        if not committee:
            return {"success": False, "error": "Committee not found"}
        
        # Generate evaluation results
        evaluation_results = {
            "evaluation_id": f"EVAL_{uuid.uuid4().hex[:8]}",
            "committee_id": committee_id,
            "thesis_id": committee.thesis_id,
            "evaluation_date": datetime.now().isoformat(),
            "evaluation_phase": committee.current_phase.value,
            "criteria_scores": {},
            "overall_score": 0.0,
            "recommendation": "",
            "feedback": {},
            "next_steps": []
        }
        
        # Evaluate each criteria
        total_score = 0.0
        total_weight = 0.0
        
        for criteria_name, criteria_info in committee.evaluation_criteria.items():
            score = evaluation_data.get(f"{criteria_name}_score", random.uniform(3.0, 5.0))
            weight = criteria_info["weight"]
            
            evaluation_results["criteria_scores"][criteria_name] = {
                "score": score,
                "weight": weight,
                "weighted_score": score * weight,
                "feedback": evaluation_data.get(f"{criteria_name}_feedback", f"Good progress in {criteria_name}")
            }
            
            total_score += score * weight
            total_weight += weight
        
        evaluation_results["overall_score"] = total_score / total_weight if total_weight > 0 else 0.0
        
        # Determine recommendation
        if evaluation_results["overall_score"] >= 4.5:
            evaluation_results["recommendation"] = "excellent_progress"
            evaluation_results["next_steps"] = ["Continue current approach", "Prepare for final review"]
        elif evaluation_results["overall_score"] >= 3.5:
            evaluation_results["recommendation"] = "good_progress"
            evaluation_results["next_steps"] = ["Address minor issues", "Continue with current timeline"]
        elif evaluation_results["overall_score"] >= 2.5:
            evaluation_results["recommendation"] = "needs_improvement"
            evaluation_results["next_steps"] = ["Address identified issues", "Schedule additional review"]
        else:
            evaluation_results["recommendation"] = "significant_concerns"
            evaluation_results["next_steps"] = ["Major revisions required", "Extended timeline needed"]
        
        # Update committee phase
        if committee.current_phase == EvaluationPhase.PROGRESS_REVIEW:
            if evaluation_results["recommendation"] in ["excellent_progress", "good_progress"]:
                committee.current_phase = EvaluationPhase.FINAL_REVIEW
            else:
                committee.current_phase = EvaluationPhase.PROGRESS_REVIEW  # Stay in progress review
        
        return {
            "success": True,
            "evaluation_results": evaluation_results,
            "committee_status": committee.status.value,
            "current_phase": committee.current_phase.value
        }
    
    def schedule_thesis_defense(self, committee_id: str, defense_data: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule thesis defense"""
        
        committee = self.thesis_committees.get(committee_id)
        if not committee:
            return {"success": False, "error": "Committee not found"}
        
        # Update committee phase
        committee.current_phase = EvaluationPhase.DEFENSE_PREPARATION
        
        # Schedule defense meeting
        defense_meeting_id = f"DEFENSE_{uuid.uuid4().hex[:8]}"
        defense_date = datetime.fromisoformat(defense_data["defense_date"])
        
        defense_meeting = CommitteeMeeting(
            meeting_id=defense_meeting_id,
            committee_id=committee_id,
            meeting_type="thesis_defense",
            scheduled_date=defense_date,
            duration_minutes=120,  # 2 hours for defense
            agenda=[
                "Student presentation (30 minutes)",
                "Committee questions (60 minutes)",
                "Committee deliberation (30 minutes)"
            ],
            attendees=[member.professor_id for member in committee.committee_members]
        )
        
        # Store defense meeting
        if committee_id not in self.committee_meetings:
            self.committee_meetings[committee_id] = []
        self.committee_meetings[committee_id].append(defense_meeting)
        
        return {
            "success": True,
            "defense_meeting_id": defense_meeting_id,
            "defense_date": defense_date.isoformat(),
            "duration_minutes": defense_meeting.duration_minutes,
            "agenda": defense_meeting.agenda,
            "attendees": defense_meeting.attendees,
            "committee_phase": committee.current_phase.value
        }
    
    def conduct_thesis_defense(self, defense_meeting_id: str, defense_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct thesis defense"""
        
        # Find defense meeting
        defense_meeting = None
        committee_id = None
        for cid, meetings in self.committee_meetings.items():
            for m in meetings:
                if m.meeting_id == defense_meeting_id and m.meeting_type == "thesis_defense":
                    defense_meeting = m
                    committee_id = cid
                    break
            if defense_meeting:
                break
        
        if not defense_meeting:
            return {"success": False, "error": "Defense meeting not found"}
        
        committee = self.thesis_committees.get(committee_id)
        if not committee:
            return {"success": False, "error": "Committee not found"}
        
        # Update committee phase
        committee.current_phase = EvaluationPhase.DEFENSE_EVALUATION
        
        # Generate defense evaluation
        defense_evaluation = {
            "defense_id": f"DEFENSE_EVAL_{uuid.uuid4().hex[:8]}",
            "meeting_id": defense_meeting_id,
            "committee_id": committee_id,
            "defense_date": defense_meeting.scheduled_date.isoformat(),
            "presentation_score": defense_data.get("presentation_score", random.uniform(3.0, 5.0)),
            "question_answering_score": defense_data.get("question_answering_score", random.uniform(3.0, 5.0)),
            "knowledge_demonstration_score": defense_data.get("knowledge_demonstration_score", random.uniform(3.0, 5.0)),
            "overall_defense_score": 0.0,
            "committee_recommendation": "",
            "individual_evaluations": [],
            "final_decision": ""
        }
        
        # Calculate overall defense score
        scores = [
            defense_evaluation["presentation_score"],
            defense_evaluation["question_answering_score"],
            defense_evaluation["knowledge_demonstration_score"]
        ]
        defense_evaluation["overall_defense_score"] = sum(scores) / len(scores)
        
        # Generate individual committee member evaluations
        for member in committee.committee_members:
            member_evaluation = {
                "member_id": member.member_id,
                "professor_id": member.professor_id,
                "role": member.role.value,
                "evaluation_score": random.uniform(3.0, 5.0),
                "feedback": f"Strong defense performance from {member.role.value} perspective",
                "recommendation": "pass" if defense_evaluation["overall_defense_score"] >= 3.5 else "conditional_pass"
            }
            defense_evaluation["individual_evaluations"].append(member_evaluation)
        
        # Determine committee recommendation
        if defense_evaluation["overall_defense_score"] >= 4.5:
            defense_evaluation["committee_recommendation"] = "pass_with_distinction"
            defense_evaluation["final_decision"] = "approved"
        elif defense_evaluation["overall_defense_score"] >= 3.5:
            defense_evaluation["committee_recommendation"] = "pass"
            defense_evaluation["final_decision"] = "approved"
        elif defense_evaluation["overall_defense_score"] >= 2.5:
            defense_evaluation["committee_recommendation"] = "conditional_pass"
            defense_evaluation["final_decision"] = "conditional_approval"
        else:
            defense_evaluation["committee_recommendation"] = "fail"
            defense_evaluation["final_decision"] = "rejected"
        
        # Update committee
        committee.final_recommendation = defense_evaluation["final_decision"]
        committee.completion_date = datetime.now()
        committee.status = CommitteeStatus.COMPLETED
        
        # Update defense meeting
        defense_meeting.meeting_notes = f"Thesis defense completed. Final decision: {defense_evaluation['final_decision']}"
        defense_meeting.decisions_made = [f"Final decision: {defense_evaluation['final_decision']}"]
        
        return {
            "success": True,
            "defense_evaluation": defense_evaluation,
            "committee_status": committee.status.value,
            "final_decision": defense_evaluation["final_decision"],
            "completion_date": committee.completion_date.isoformat()
        }
    
    def get_committee_status(self, committee_id: str) -> Dict[str, Any]:
        """Get committee status and information"""
        
        committee = self.thesis_committees.get(committee_id)
        if not committee:
            return {"error": "Committee not found"}
        
        meetings = self.committee_meetings.get(committee_id, [])
        
        return {
            "committee_id": committee_id,
            "thesis_id": committee.thesis_id,
            "student_id": committee.student_id,
            "status": committee.status.value,
            "current_phase": committee.current_phase.value,
            "formed_at": committee.formed_at.isoformat(),
            "completion_date": committee.completion_date.isoformat() if committee.completion_date else None,
            "final_recommendation": committee.final_recommendation,
            "committee_members": [
                {
                    "member_id": member.member_id,
                    "professor_id": member.professor_id,
                    "role": member.role.value,
                    "expertise_areas": member.expertise_areas,
                    "responsibilities": member.responsibilities,
                    "performance_rating": member.performance_rating
                }
                for member in committee.committee_members
            ],
            "meetings_scheduled": len(meetings),
            "meetings_completed": len([m for m in meetings if m.meeting_notes]),
            "evaluation_criteria": committee.evaluation_criteria,
            "meeting_history": committee.meeting_history
        }
    
    def get_committee_analytics(self) -> Dict[str, Any]:
        """Get committee system analytics"""
        
        total_committees = len(self.thesis_committees)
        
        if total_committees == 0:
            return {"message": "No committees formed yet"}
        
        # Status distribution
        status_counts = {}
        for status in CommitteeStatus:
            status_counts[status.value] = len([c for c in self.thesis_committees.values() if c.status == status])
        
        # Phase distribution
        phase_counts = {}
        for phase in EvaluationPhase:
            phase_counts[phase.value] = len([c for c in self.thesis_committees.values() if c.current_phase == phase])
        
        # Role distribution
        role_counts = {}
        for role in CommitteeRole:
            role_counts[role.value] = sum(
                len([m for m in c.committee_members if m.role == role])
                for c in self.thesis_committees.values()
            )
        
        # Completion statistics
        completed_committees = [c for c in self.thesis_committees.values() if c.status == CommitteeStatus.COMPLETED]
        completion_times = []
        for committee in completed_committees:
            if committee.completion_date:
                completion_time = (committee.completion_date - committee.formed_at).total_seconds() / 3600  # hours
                completion_times.append(completion_time)
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        # Meeting statistics
        total_meetings = sum(len(meetings) for meetings in self.committee_meetings.values())
        
        return {
            "total_committees": total_committees,
            "status_distribution": status_counts,
            "phase_distribution": phase_counts,
            "role_distribution": role_counts,
            "completion_statistics": {
                "completed_committees": len(completed_committees),
                "average_completion_time_hours": avg_completion_time,
                "completion_rate": (len(completed_committees) / total_committees * 100) if total_committees > 0 else 0
            },
            "meeting_statistics": {
                "total_meetings": total_meetings,
                "average_meetings_per_committee": total_meetings / total_committees if total_committees > 0 else 0
            },
            "committee_size_statistics": {
                "average_committee_size": sum(len(c.committee_members) for c in self.thesis_committees.values()) / total_committees if total_committees > 0 else 0,
                "minimum_size": self.committee_rules["minimum_members"],
                "maximum_size": self.committee_rules["maximum_members"]
            }
        }