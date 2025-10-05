"""
MS AI Curriculum System - Thesis Process
Comprehensive thesis management with AI instructor committee presentations
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid

class ThesisStatus(Enum):
    PROPOSAL_DRAFT = "proposal_draft"
    PROPOSAL_SUBMITTED = "proposal_submitted"
    PROPOSAL_APPROVED = "proposal_approved"
    PROPOSAL_REJECTED = "proposal_rejected"
    RESEARCH_IN_PROGRESS = "research_in_progress"
    THESIS_DRAFT = "thesis_draft"
    THESIS_SUBMITTED = "thesis_submitted"
    DEFENSE_SCHEDULED = "defense_scheduled"
    DEFENSE_COMPLETED = "defense_completed"
    THESIS_APPROVED = "thesis_approved"
    THESIS_REJECTED = "thesis_rejected"
    REVISION_REQUIRED = "revision_required"
    COMPLETED = "completed"

class ThesisType(Enum):
    RESEARCH_THESIS = "research_thesis"
    APPLIED_PROJECT = "applied_project"
    INDUSTRY_COLLABORATION = "industry_collaboration"
    OPEN_SOURCE_CONTRIBUTION = "open_source_contribution"

class CommitteeRole(Enum):
    CHAIR = "chair"
    MEMBER = "member"
    EXTERNAL_EXAMINER = "external_examiner"
    INDUSTRY_ADVISOR = "industry_advisor"

@dataclass
class ThesisProposal:
    """Thesis proposal document"""
    proposal_id: str
    student_id: str
    title: str
    abstract: str
    research_question: str
    objectives: List[str]
    methodology: str
    literature_review: str
    timeline: Dict[str, Any]
    resources_needed: List[str]
    expected_outcomes: List[str]
    thesis_type: ThesisType
    status: ThesisStatus
    created_at: datetime
    submitted_at: Optional[datetime] = None
    advisor_id: Optional[str] = None
    committee_feedback: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class ThesisCommittee:
    """Thesis committee with AI instructors"""
    committee_id: str
    student_id: str
    thesis_id: str
    members: List[Dict[str, Any]]
    chair_id: str
    formed_at: datetime
    status: str = "active"

@dataclass
class Thesis:
    """Main thesis document"""
    thesis_id: str
    student_id: str
    proposal_id: str
    title: str
    abstract: str
    introduction: str
    literature_review: str
    methodology: str
    results: str
    discussion: str
    conclusion: str
    references: List[str]
    appendices: List[str]
    status: ThesisStatus
    created_at: datetime
    submitted_at: Optional[datetime] = None
    defense_scheduled: Optional[datetime] = None
    defense_completed: Optional[datetime] = None
    final_grade: Optional[float] = None

@dataclass
class ThesisDefense:
    """Thesis defense presentation"""
    defense_id: str
    thesis_id: str
    student_id: str
    committee_id: str
    scheduled_date: datetime
    duration_minutes: int
    presentation_materials: List[str]
    questions_asked: List[Dict[str, Any]]
    committee_evaluations: List[Dict[str, Any]]
    final_decision: Optional[str] = None
    completed_at: Optional[datetime] = None

class ThesisSystem:
    """Comprehensive thesis management system"""
    
    def __init__(self, user_manager, professor_system):
        self.user_manager = user_manager
        self.professor_system = professor_system
        self.thesis_proposals: Dict[str, ThesisProposal] = {}
        self.theses: Dict[str, Thesis] = {}
        self.committees: Dict[str, ThesisCommittee] = {}
        self.defenses: Dict[str, ThesisDefense] = {}
        
    def create_thesis_proposal(self, student_id: str, proposal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new thesis proposal"""
        proposal_id = f"PROP_{uuid.uuid4().hex[:8].upper()}"
        
        proposal = ThesisProposal(
            proposal_id=proposal_id,
            student_id=student_id,
            title=proposal_data["title"],
            abstract=proposal_data["abstract"],
            research_question=proposal_data["research_question"],
            objectives=proposal_data["objectives"],
            methodology=proposal_data["methodology"],
            literature_review=proposal_data["literature_review"],
            timeline=proposal_data["timeline"],
            resources_needed=proposal_data["resources_needed"],
            expected_outcomes=proposal_data["expected_outcomes"],
            thesis_type=ThesisType(proposal_data["thesis_type"]),
            status=ThesisStatus.PROPOSAL_DRAFT,
            created_at=datetime.now(),
            advisor_id=proposal_data.get("advisor_id")
        )
        
        self.thesis_proposals[proposal_id] = proposal
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "message": "Thesis proposal created successfully"
        }
    
    def submit_thesis_proposal(self, proposal_id: str) -> Dict[str, Any]:
        """Submit thesis proposal for committee review"""
        proposal = self.thesis_proposals.get(proposal_id)
        if not proposal:
            return {"success": False, "error": "Proposal not found"}
        
        # Validate proposal completeness
        validation_result = self._validate_proposal(proposal)
        if not validation_result["is_valid"]:
            return {
                "success": False,
                "error": "Proposal incomplete",
                "missing_sections": validation_result["missing_sections"]
            }
        
        # Update proposal status
        proposal.status = ThesisStatus.PROPOSAL_SUBMITTED
        proposal.submitted_at = datetime.now()
        
        # Form committee and initiate review
        committee_id = self._form_thesis_committee(proposal_id)
        
        return {
            "success": True,
            "message": "Thesis proposal submitted successfully",
            "committee_id": committee_id,
            "next_steps": "Your proposal is now under review by the thesis committee"
        }
    
    def _validate_proposal(self, proposal: ThesisProposal) -> Dict[str, Any]:
        """Validate thesis proposal completeness"""
        missing_sections = []
        
        if len(proposal.title) < 10:
            missing_sections.append("Title (minimum 10 characters)")
        
        if len(proposal.abstract) < 200:
            missing_sections.append("Abstract (minimum 200 words)")
        
        if len(proposal.research_question) < 20:
            missing_sections.append("Research question (minimum 20 characters)")
        
        if len(proposal.objectives) < 3:
            missing_sections.append("Objectives (minimum 3 objectives)")
        
        if len(proposal.methodology) < 100:
            missing_sections.append("Methodology (minimum 100 words)")
        
        if len(proposal.literature_review) < 300:
            missing_sections.append("Literature review (minimum 300 words)")
        
        if not proposal.timeline:
            missing_sections.append("Timeline")
        
        if len(proposal.expected_outcomes) < 2:
            missing_sections.append("Expected outcomes (minimum 2 outcomes)")
        
        return {
            "is_valid": len(missing_sections) == 0,
            "missing_sections": missing_sections
        }
    
    def _form_thesis_committee(self, proposal_id: str) -> str:
        """Form thesis committee with AI instructors"""
        proposal = self.thesis_proposals[proposal_id]
        committee_id = f"COMM_{uuid.uuid4().hex[:8].upper()}"
        
        # Select AI instructors based on thesis topic and specialization
        committee_members = self._select_committee_members(proposal)
        
        committee = ThesisCommittee(
            committee_id=committee_id,
            student_id=proposal.student_id,
            thesis_id=proposal_id,
            members=committee_members,
            chair_id=committee_members[0]["professor_id"],  # First member as chair
            formed_at=datetime.now()
        )
        
        self.committees[committee_id] = committee
        
        # Initiate committee review
        self._initiate_committee_review(proposal_id, committee_id)
        
        return committee_id
    
    def _select_committee_members(self, proposal: ThesisProposal) -> List[Dict[str, Any]]:
        """Select AI instructors for thesis committee"""
        # Match professors based on thesis topic and specialization
        relevant_professors = []
        
        # Analyze thesis topic to find relevant specializations
        topic_keywords = proposal.title.lower() + " " + proposal.research_question.lower()
        
        for professor in self.professor_system.professors:
            relevance_score = 0
            
            # Check specialization match
            if professor.specialization.value in topic_keywords:
                relevance_score += 3
            
            # Check research interests match
            for interest in professor.research_interests:
                if interest.lower() in topic_keywords:
                    relevance_score += 2
            
            # Check recent publications relevance
            for publication in professor.publications:
                if any(keyword in publication.title.lower() for keyword in topic_keywords.split()):
                    relevance_score += 1
            
            if relevance_score > 0:
                relevant_professors.append((professor, relevance_score))
        
        # Sort by relevance and select top 3-4 professors
        relevant_professors.sort(key=lambda x: x[1], reverse=True)
        selected_professors = relevant_professors[:4]  # Maximum 4 committee members
        
        # If not enough relevant professors, add general AI professors
        if len(selected_professors) < 3:
            general_professors = [
                prof for prof in self.professor_system.professors 
                if prof not in [p[0] for p in selected_professors]
            ]
            selected_professors.extend([(prof, 1) for prof in general_professors[:3-len(selected_professors)]])
        
        # Format committee members
        committee_members = []
        for i, (professor, score) in enumerate(selected_professors):
            role = CommitteeRole.CHAIR if i == 0 else CommitteeRole.MEMBER
            committee_members.append({
                "professor_id": professor.professor_id,
                "name": professor.name,
                "specialization": professor.specialization.value,
                "role": role.value,
                "relevance_score": score,
                "expertise_level": professor.expertise_level
            })
        
        return committee_members
    
    def _initiate_committee_review(self, proposal_id: str, committee_id: str):
        """Initiate committee review of thesis proposal"""
        proposal = self.thesis_proposals[proposal_id]
        committee = self.committees[committee_id]
        
        # Generate feedback from each committee member
        for member in committee.members:
            professor = next(
                (p for p in self.professor_system.professors if p.professor_id == member["professor_id"]),
                None
            )
            
            if professor:
                feedback = self._generate_professor_feedback(professor, proposal)
                proposal.committee_feedback.append(feedback)
        
        # Make committee decision
        self._make_committee_decision(proposal_id, committee_id)
    
    def _generate_professor_feedback(self, professor, proposal: ThesisProposal) -> Dict[str, Any]:
        """Generate feedback from AI professor"""
        feedback = {
            "professor_id": professor.professor_id,
            "professor_name": professor.name,
            "specialization": professor.specialization.value,
            "evaluation_date": datetime.now().isoformat(),
            "scores": {},
            "comments": "",
            "recommendations": [],
            "decision": "pending"
        }
        
        # Evaluate different aspects based on professor's expertise
        if professor.specialization.value == "machine_learning":
            feedback["scores"]["methodology"] = self._evaluate_methodology(proposal)
            feedback["scores"]["technical_feasibility"] = self._evaluate_technical_feasibility(proposal)
            feedback["comments"] = f"From a machine learning perspective, the methodology shows {'strong' if feedback['scores']['methodology'] > 7 else 'moderate'} technical merit."
        
        elif professor.specialization.value == "ai_ethics":
            feedback["scores"]["ethical_considerations"] = self._evaluate_ethical_aspects(proposal)
            feedback["scores"]["social_impact"] = self._evaluate_social_impact(proposal)
            feedback["comments"] = f"Ethical considerations are {'well addressed' if feedback['scores']['ethical_considerations'] > 7 else 'need improvement'} in this proposal."
        
        elif professor.specialization.value == "computer_vision":
            feedback["scores"]["technical_approach"] = self._evaluate_technical_approach(proposal)
            feedback["scores"]["innovation"] = self._evaluate_innovation(proposal)
            feedback["comments"] = f"The technical approach demonstrates {'significant' if feedback['scores']['technical_approach'] > 7 else 'moderate'} innovation potential."
        
        else:  # NLP or general
            feedback["scores"]["research_quality"] = self._evaluate_research_quality(proposal)
            feedback["scores"]["feasibility"] = self._evaluate_feasibility(proposal)
            feedback["comments"] = f"Overall research quality is {'excellent' if feedback['scores']['research_quality'] > 7 else 'good'} with {'high' if feedback['scores']['feasibility'] > 7 else 'moderate'} feasibility."
        
        # Generate recommendations based on professor's teaching philosophy
        if "hands_on" in professor.persona.teaching_methods:
            feedback["recommendations"].append("Consider including more practical implementation details")
        
        if "research" in professor.persona.teaching_methods:
            feedback["recommendations"].append("Strengthen the literature review with recent publications")
        
        if "collaborative" in professor.persona.teaching_methods:
            feedback["recommendations"].append("Consider interdisciplinary collaboration opportunities")
        
        # Make recommendation
        avg_score = sum(feedback["scores"].values()) / len(feedback["scores"])
        if avg_score >= 7:
            feedback["decision"] = "approve"
        elif avg_score >= 5:
            feedback["decision"] = "conditional_approval"
        else:
            feedback["decision"] = "reject"
        
        return feedback
    
    def _evaluate_methodology(self, proposal: ThesisProposal) -> float:
        """Evaluate methodology quality"""
        score = 5.0  # Base score
        
        if "machine learning" in proposal.methodology.lower():
            score += 2
        if "neural network" in proposal.methodology.lower():
            score += 1
        if "experiment" in proposal.methodology.lower():
            score += 1
        if "dataset" in proposal.methodology.lower():
            score += 1
        
        return min(10, score)
    
    def _evaluate_technical_feasibility(self, proposal: ThesisProposal) -> float:
        """Evaluate technical feasibility"""
        score = 5.0  # Base score
        
        if len(proposal.timeline) >= 4:  # Has detailed timeline
            score += 2
        if len(proposal.resources_needed) > 0:
            score += 1
        if "python" in proposal.resources_needed or "tensorflow" in proposal.resources_needed:
            score += 2
        
        return min(10, score)
    
    def _evaluate_ethical_aspects(self, proposal: ThesisProposal) -> float:
        """Evaluate ethical considerations"""
        score = 5.0  # Base score
        
        ethical_keywords = ["ethics", "bias", "fairness", "privacy", "transparency", "accountability"]
        for keyword in ethical_keywords:
            if keyword in proposal.abstract.lower() or keyword in proposal.research_question.lower():
                score += 1
        
        return min(10, score)
    
    def _evaluate_social_impact(self, proposal: ThesisProposal) -> float:
        """Evaluate social impact potential"""
        score = 5.0  # Base score
        
        impact_keywords = ["social", "impact", "benefit", "society", "community", "application"]
        for keyword in impact_keywords:
            if keyword in proposal.expected_outcomes:
                score += 1
        
        return min(10, score)
    
    def _evaluate_technical_approach(self, proposal: ThesisProposal) -> float:
        """Evaluate technical approach"""
        score = 5.0  # Base score
        
        if "algorithm" in proposal.methodology.lower():
            score += 2
        if "model" in proposal.methodology.lower():
            score += 1
        if "optimization" in proposal.methodology.lower():
            score += 1
        if "evaluation" in proposal.methodology.lower():
            score += 1
        
        return min(10, score)
    
    def _evaluate_innovation(self, proposal: ThesisProposal) -> float:
        """Evaluate innovation level"""
        score = 5.0  # Base score
        
        innovation_keywords = ["novel", "innovative", "new", "original", "breakthrough", "advancement"]
        for keyword in innovation_keywords:
            if keyword in proposal.title.lower() or keyword in proposal.research_question.lower():
                score += 1
        
        return min(10, score)
    
    def _evaluate_research_quality(self, proposal: ThesisProposal) -> float:
        """Evaluate overall research quality"""
        score = 5.0  # Base score
        
        if len(proposal.literature_review) > 500:
            score += 2
        if len(proposal.objectives) >= 3:
            score += 1
        if len(proposal.expected_outcomes) >= 3:
            score += 1
        if len(proposal.research_question) > 50:
            score += 1
        
        return min(10, score)
    
    def _evaluate_feasibility(self, proposal: ThesisProposal) -> float:
        """Evaluate project feasibility"""
        score = 5.0  # Base score
        
        if len(proposal.timeline) >= 6:  # Detailed timeline
            score += 2
        if len(proposal.resources_needed) >= 3:
            score += 1
        if proposal.thesis_type == ThesisType.APPLIED_PROJECT:
            score += 1
        if len(proposal.methodology) > 200:
            score += 1
        
        return min(10, score)
    
    def _make_committee_decision(self, proposal_id: str, committee_id: str):
        """Make final committee decision on proposal"""
        proposal = self.thesis_proposals[proposal_id]
        committee = self.committees[committee_id]
        
        # Analyze committee feedback
        decisions = [feedback["decision"] for feedback in proposal.committee_feedback]
        approve_count = decisions.count("approve")
        conditional_count = decisions.count("conditional_approval")
        reject_count = decisions.count("reject")
        
        # Make decision based on majority
        if approve_count > reject_count:
            proposal.status = ThesisStatus.PROPOSAL_APPROVED
            # Create thesis document
            self._create_thesis_from_proposal(proposal_id)
        elif reject_count > approve_count:
            proposal.status = ThesisStatus.PROPOSAL_REJECTED
        else:
            # Conditional approval or need for revision
            proposal.status = ThesisStatus.PROPOSAL_APPROVED  # Default to approved for now
            self._create_thesis_from_proposal(proposal_id)
    
    def _create_thesis_from_proposal(self, proposal_id: str):
        """Create thesis document from approved proposal"""
        proposal = self.thesis_proposals[proposal_id]
        thesis_id = f"THESIS_{uuid.uuid4().hex[:8].upper()}"
        
        thesis = Thesis(
            thesis_id=thesis_id,
            student_id=proposal.student_id,
            proposal_id=proposal_id,
            title=proposal.title,
            abstract=proposal.abstract,
            introduction="",  # To be written by student
            literature_review=proposal.literature_review,
            methodology=proposal.methodology,
            results="",  # To be written by student
            discussion="",  # To be written by student
            conclusion="",  # To be written by student
            references=[],  # To be added by student
            appendices=[],  # To be added by student
            status=ThesisStatus.RESEARCH_IN_PROGRESS,
            created_at=datetime.now()
        )
        
        self.theses[thesis_id] = thesis
        
        # Update proposal status
        proposal.status = ThesisStatus.PROPOSAL_APPROVED
    
    def schedule_thesis_defense(self, thesis_id: str, defense_data: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule thesis defense presentation"""
        thesis = self.theses.get(thesis_id)
        if not thesis:
            return {"success": False, "error": "Thesis not found"}
        
        if thesis.status != ThesisStatus.THESIS_SUBMITTED:
            return {"success": False, "error": "Thesis must be submitted before scheduling defense"}
        
        # Find committee for this thesis
        committee = next(
            (c for c in self.committees.values() if c.thesis_id == thesis.proposal_id),
            None
        )
        if not committee:
            return {"success": False, "error": "Thesis committee not found"}
        
        defense_id = f"DEFENSE_{uuid.uuid4().hex[:8].upper()}"
        
        defense = ThesisDefense(
            defense_id=defense_id,
            thesis_id=thesis_id,
            student_id=thesis.student_id,
            committee_id=committee.committee_id,
            scheduled_date=datetime.fromisoformat(defense_data["scheduled_date"]),
            duration_minutes=defense_data.get("duration_minutes", 60),
            presentation_materials=defense_data.get("presentation_materials", []),
            questions_asked=[],
            committee_evaluations=[],
            completed_at=None
        )
        
        self.defenses[defense_id] = defense
        
        # Update thesis status
        thesis.status = ThesisStatus.DEFENSE_SCHEDULED
        thesis.defense_scheduled = defense.scheduled_date
        
        return {
            "success": True,
            "defense_id": defense_id,
            "message": f"Thesis defense scheduled for {defense.scheduled_date.strftime('%Y-%m-%d %H:%M')}",
            "committee_members": [
                {
                    "name": member["name"],
                    "role": member["role"],
                    "specialization": member["specialization"]
                }
                for member in committee.members
            ]
        }
    
    def conduct_thesis_defense(self, defense_id: str) -> Dict[str, Any]:
        """Conduct thesis defense with AI instructor committee"""
        defense = self.defenses.get(defense_id)
        if not defense:
            return {"success": False, "error": "Defense not found"}
        
        thesis = self.theses.get(defense.thesis_id)
        committee = self.committees.get(defense.committee_id)
        
        if not thesis or not committee:
            return {"success": False, "error": "Thesis or committee not found"}
        
        # Simulate defense questions from each committee member
        for member in committee.members:
            professor = next(
                (p for p in self.professor_system.professors if p.professor_id == member["professor_id"]),
                None
            )
            
            if professor:
                questions = self._generate_defense_questions(professor, thesis)
                defense.questions_asked.extend(questions)
                
                # Generate evaluation from this committee member
                evaluation = self._generate_committee_evaluation(professor, thesis, questions)
                defense.committee_evaluations.append(evaluation)
        
        # Make final decision
        final_decision = self._make_defense_decision(defense)
        defense.final_decision = final_decision
        defense.completed_at = datetime.now()
        
        # Update thesis status
        thesis.defense_completed = defense.completed_at
        if final_decision == "approved":
            thesis.status = ThesisStatus.THESIS_APPROVED
            thesis.final_grade = self._calculate_final_grade(defense)
        elif final_decision == "revision_required":
            thesis.status = ThesisStatus.REVISION_REQUIRED
        else:
            thesis.status = ThesisStatus.THESIS_REJECTED
        
        return {
            "success": True,
            "defense_completed": True,
            "final_decision": final_decision,
            "committee_evaluations": defense.committee_evaluations,
            "questions_asked": defense.questions_asked,
            "final_grade": thesis.final_grade,
            "completion_time": defense.completed_at.isoformat()
        }
    
    def _generate_defense_questions(self, professor, thesis: Thesis) -> List[Dict[str, Any]]:
        """Generate defense questions from AI professor"""
        questions = []
        
        # Generate questions based on professor's specialization and teaching style
        if professor.specialization.value == "machine_learning":
            questions.extend([
                {
                    "question": f"How does your methodology address the limitations of existing approaches in {thesis.title.lower()}?",
                    "category": "methodology",
                    "difficulty": "advanced"
                },
                {
                    "question": "What are the computational complexity implications of your proposed solution?",
                    "category": "technical_depth",
                    "difficulty": "advanced"
                }
            ])
        
        elif professor.specialization.value == "ai_ethics":
            questions.extend([
                {
                    "question": "What ethical considerations did you address in your research design?",
                    "category": "ethics",
                    "difficulty": "intermediate"
                },
                {
                    "question": "How might your findings impact society, and what are the potential risks?",
                    "category": "social_impact",
                    "difficulty": "intermediate"
                }
            ])
        
        elif professor.specialization.value == "computer_vision":
            questions.extend([
                {
                    "question": "How does your approach compare to state-of-the-art computer vision methods?",
                    "category": "comparison",
                    "difficulty": "advanced"
                },
                {
                    "question": "What datasets did you use, and how did you ensure their quality and diversity?",
                    "category": "data_quality",
                    "difficulty": "intermediate"
                }
            ])
        
        # Add general questions based on professor's teaching philosophy
        if "hands_on" in professor.persona.teaching_methods:
            questions.append({
                "question": "Can you walk us through a specific example of how your solution works in practice?",
                "category": "practical_application",
                "difficulty": "intermediate"
            })
        
        if "research" in professor.persona.teaching_methods:
            questions.append({
                "question": "What are the key contributions of your work to the existing body of knowledge?",
                "category": "contribution",
                "difficulty": "advanced"
            })
        
        return questions
    
    def _generate_committee_evaluation(self, professor, thesis: Thesis, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate committee member evaluation"""
        evaluation = {
            "professor_id": professor.professor_id,
            "professor_name": professor.name,
            "specialization": professor.specialization.value,
            "evaluation_date": datetime.now().isoformat(),
            "scores": {},
            "comments": "",
            "recommendation": "pending"
        }
        
        # Evaluate different aspects
        evaluation["scores"]["presentation_quality"] = self._evaluate_presentation_quality(thesis)
        evaluation["scores"]["technical_depth"] = self._evaluate_technical_depth(thesis)
        evaluation["scores"]["research_contribution"] = self._evaluate_research_contribution(thesis)
        evaluation["scores"]["defense_performance"] = self._evaluate_defense_performance(questions)
        
        # Generate comments based on professor's personality
        avg_score = sum(evaluation["scores"].values()) / len(evaluation["scores"])
        
        if "enthusiastic" in professor.persona.personality_traits:
            evaluation["comments"] = f"Excellent work! The student demonstrates {'outstanding' if avg_score > 8 else 'strong'} understanding of the research area."
        elif "analytical" in professor.persona.personality_traits:
            evaluation["comments"] = f"The methodology shows {'rigorous' if avg_score > 7 else 'adequate'} analytical approach with {'strong' if avg_score > 7 else 'moderate'} technical foundation."
        elif "empathetic" in professor.persona.personality_traits:
            evaluation["comments"] = f"The student has shown {'exceptional' if avg_score > 8 else 'good'} dedication to their research with clear potential for {'significant' if avg_score > 7 else 'meaningful'} impact."
        
        # Make recommendation
        if avg_score >= 8:
            evaluation["recommendation"] = "approved"
        elif avg_score >= 6:
            evaluation["recommendation"] = "approved_with_minor_revisions"
        elif avg_score >= 4:
            evaluation["recommendation"] = "revision_required"
        else:
            evaluation["recommendation"] = "rejected"
        
        return evaluation
    
    def _evaluate_presentation_quality(self, thesis: Thesis) -> float:
        """Evaluate presentation quality"""
        score = 5.0  # Base score
        
        if len(thesis.abstract) > 200:
            score += 1
        if len(thesis.introduction) > 300:
            score += 1
        if len(thesis.conclusion) > 200:
            score += 1
        if len(thesis.references) > 10:
            score += 1
        if len(thesis.appendices) > 0:
            score += 1
        
        return min(10, score)
    
    def _evaluate_technical_depth(self, thesis: Thesis) -> float:
        """Evaluate technical depth"""
        score = 5.0  # Base score
        
        technical_keywords = ["algorithm", "model", "optimization", "evaluation", "experiment", "analysis"]
        for keyword in technical_keywords:
            if keyword in thesis.methodology.lower():
                score += 0.8
        
        return min(10, score)
    
    def _evaluate_research_contribution(self, thesis: Thesis) -> float:
        """Evaluate research contribution"""
        score = 5.0  # Base score
        
        if len(thesis.literature_review) > 500:
            score += 2
        if "novel" in thesis.title.lower() or "new" in thesis.title.lower():
            score += 2
        if len(thesis.results) > 300:
            score += 1
        
        return min(10, score)
    
    def _evaluate_defense_performance(self, questions: List[Dict[str, Any]]) -> float:
        """Evaluate defense performance"""
        score = 5.0  # Base score
        
        # Simulate performance based on question difficulty
        for question in questions:
            if question["difficulty"] == "advanced":
                score += 1.5
            elif question["difficulty"] == "intermediate":
                score += 1.0
            else:
                score += 0.5
        
        return min(10, score)
    
    def _make_defense_decision(self, defense: ThesisDefense) -> str:
        """Make final defense decision"""
        recommendations = [eval["recommendation"] for eval in defense.committee_evaluations]
        
        approved_count = recommendations.count("approved") + recommendations.count("approved_with_minor_revisions")
        revision_count = recommendations.count("revision_required")
        rejected_count = recommendations.count("rejected")
        
        if rejected_count > 0:
            return "rejected"
        elif revision_count > approved_count:
            return "revision_required"
        else:
            return "approved"
    
    def _calculate_final_grade(self, defense: ThesisDefense) -> float:
        """Calculate final thesis grade"""
        all_scores = []
        for evaluation in defense.committee_evaluations:
            all_scores.extend(evaluation["scores"].values())
        
        if not all_scores:
            return 0.0
        
        average_score = sum(all_scores) / len(all_scores)
        # Convert to GPA scale (0-4.0)
        gpa = (average_score / 10) * 4.0
        return round(gpa, 2)
    
    def get_thesis_progress(self, student_id: str) -> Dict[str, Any]:
        """Get thesis progress for student"""
        student_proposals = [p for p in self.thesis_proposals.values() if p.student_id == student_id]
        student_theses = [t for t in self.theses.values() if t.student_id == student_id]
        
        return {
            "student_id": student_id,
            "proposals": [
                {
                    "proposal_id": p.proposal_id,
                    "title": p.title,
                    "status": p.status.value,
                    "created_at": p.created_at.isoformat(),
                    "submitted_at": p.submitted_at.isoformat() if p.submitted_at else None
                }
                for p in student_proposals
            ],
            "theses": [
                {
                    "thesis_id": t.thesis_id,
                    "title": t.title,
                    "status": t.status.value,
                    "created_at": t.created_at.isoformat(),
                    "defense_scheduled": t.defense_scheduled.isoformat() if t.defense_scheduled else None,
                    "final_grade": t.final_grade
                }
                for t in student_theses
            ],
            "current_status": self._get_current_thesis_status(student_id)
        }
    
    def _get_current_thesis_status(self, student_id: str) -> str:
        """Get current thesis status for student"""
        student_theses = [t for t in self.theses.values() if t.student_id == student_id]
        
        if not student_theses:
            return "No thesis in progress"
        
        latest_thesis = max(student_theses, key=lambda t: t.created_at)
        return latest_thesis.status.value