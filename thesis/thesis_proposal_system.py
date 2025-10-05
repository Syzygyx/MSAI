"""
MS AI Curriculum System - Thesis Proposal System
AI Professor-guided thesis proposal development and management
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import random

class ProposalStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    REVISION_REQUIRED = "revision_required"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEFERRED = "deferred"

class ResearchArea(Enum):
    MACHINE_LEARNING = "machine_learning"
    DEEP_LEARNING = "deep_learning"
    COMPUTER_VISION = "computer_vision"
    NATURAL_LANGUAGE_PROCESSING = "natural_language_processing"
    ROBOTICS = "robotics"
    AI_ETHICS = "ai_ethics"
    NEURAL_NETWORKS = "neural_networks"
    REINFORCEMENT_LEARNING = "reinforcement_learning"
    DATA_SCIENCE = "data_science"
    AI_THEORY = "ai_theory"

class ProposalType(Enum):
    RESEARCH_THESIS = "research_thesis"
    APPLIED_PROJECT = "applied_project"
    INDUSTRY_COLLABORATION = "industry_collaboration"
    INTERDISCIPLINARY = "interdisciplinary"

@dataclass
class ThesisProposal:
    """Thesis proposal structure"""
    proposal_id: str
    student_id: str
    title: str
    research_area: ResearchArea
    proposal_type: ProposalType
    abstract: str
    research_question: str
    objectives: List[str]
    methodology: str
    literature_review: str
    expected_outcomes: List[str]
    timeline: Dict[str, str]
    resources_needed: List[str]
    advisor_id: str
    status: ProposalStatus
    created_at: datetime
    updated_at: datetime
    submission_date: Optional[datetime] = None
    review_deadline: Optional[datetime] = None
    feedback: List[Dict[str, Any]] = field(default_factory=list)
    revisions_count: int = 0
    ai_guidance_sessions: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class ProposalTemplate:
    """Template for thesis proposals"""
    template_id: str
    research_area: ResearchArea
    proposal_type: ProposalType
    template_name: str
    description: str
    sections: List[Dict[str, Any]]
    word_limits: Dict[str, int]
    example_content: Dict[str, str]

class ThesisProposalSystem:
    """AI Professor-guided thesis proposal system"""
    
    def __init__(self, professor_system=None, user_manager=None):
        self.professor_system = professor_system
        self.user_manager = user_manager
        
        # Proposal data
        self.thesis_proposals: Dict[str, ThesisProposal] = {}
        self.proposal_templates = self._initialize_proposal_templates()
        
    def _initialize_proposal_templates(self) -> List[ProposalTemplate]:
        """Initialize thesis proposal templates"""
        return [
            ProposalTemplate(
                template_id="TEMPLATE_001",
                research_area=ResearchArea.MACHINE_LEARNING,
                proposal_type=ProposalType.RESEARCH_THESIS,
                template_name="Machine Learning Research Thesis",
                description="Template for machine learning research thesis proposals",
                sections=[
                    {"name": "title", "required": True, "description": "Clear, concise thesis title"},
                    {"name": "abstract", "required": True, "description": "Brief summary of research"},
                    {"name": "research_question", "required": True, "description": "Main research question"},
                    {"name": "objectives", "required": True, "description": "Specific research objectives"},
                    {"name": "literature_review", "required": True, "description": "Review of relevant literature"},
                    {"name": "methodology", "required": True, "description": "Research methodology and approach"},
                    {"name": "expected_outcomes", "required": True, "description": "Expected research outcomes"},
                    {"name": "timeline", "required": True, "description": "Research timeline and milestones"},
                    {"name": "resources_needed", "required": True, "description": "Required resources and support"}
                ],
                word_limits={
                    "abstract": 300,
                    "research_question": 100,
                    "objectives": 500,
                    "literature_review": 1500,
                    "methodology": 1000,
                    "expected_outcomes": 400,
                    "timeline": 300,
                    "resources_needed": 200
                },
                example_content={
                    "title": "Deep Learning Approaches for Natural Language Understanding",
                    "research_question": "How can transformer-based models be improved for better semantic understanding in low-resource languages?",
                    "objectives": [
                        "Develop novel attention mechanisms for transformer models",
                        "Evaluate performance on low-resource language datasets",
                        "Compare with existing state-of-the-art approaches"
                    ]
                }
            ),
            ProposalTemplate(
                template_id="TEMPLATE_002",
                research_area=ResearchArea.COMPUTER_VISION,
                proposal_type=ProposalType.APPLIED_PROJECT,
                template_name="Computer Vision Applied Project",
                description="Template for computer vision applied project proposals",
                sections=[
                    {"name": "title", "required": True, "description": "Project title"},
                    {"name": "abstract", "required": True, "description": "Project summary"},
                    {"name": "problem_statement", "required": True, "description": "Problem being addressed"},
                    {"name": "solution_approach", "required": True, "description": "Proposed solution approach"},
                    {"name": "technical_requirements", "required": True, "description": "Technical requirements"},
                    {"name": "implementation_plan", "required": True, "description": "Implementation plan"},
                    {"name": "evaluation_metrics", "required": True, "description": "Success metrics and evaluation"},
                    {"name": "timeline", "required": True, "description": "Project timeline"},
                    {"name": "resources_needed", "required": True, "description": "Required resources"}
                ],
                word_limits={
                    "abstract": 250,
                    "problem_statement": 400,
                    "solution_approach": 800,
                    "technical_requirements": 300,
                    "implementation_plan": 600,
                    "evaluation_metrics": 300,
                    "timeline": 250,
                    "resources_needed": 200
                },
                example_content={
                    "title": "Real-time Object Detection for Autonomous Vehicles",
                    "problem_statement": "Current object detection systems in autonomous vehicles have limitations in real-time performance and accuracy.",
                    "solution_approach": "Develop a lightweight CNN architecture optimized for real-time object detection in autonomous vehicle scenarios."
                }
            ),
            ProposalTemplate(
                template_id="TEMPLATE_003",
                research_area=ResearchArea.AI_ETHICS,
                proposal_type=ProposalType.INTERDISCIPLINARY,
                template_name="AI Ethics Interdisciplinary Research",
                description="Template for AI ethics interdisciplinary research proposals",
                sections=[
                    {"name": "title", "required": True, "description": "Research title"},
                    {"name": "abstract", "required": True, "description": "Research summary"},
                    {"name": "ethical_framework", "required": True, "description": "Ethical framework and principles"},
                    {"name": "research_questions", "required": True, "description": "Research questions"},
                    {"name": "interdisciplinary_approach", "required": True, "description": "Interdisciplinary methodology"},
                    {"name": "stakeholder_analysis", "required": True, "description": "Stakeholder analysis"},
                    {"name": "impact_assessment", "required": True, "description": "Potential impact assessment"},
                    {"name": "timeline", "required": True, "description": "Research timeline"},
                    {"name": "resources_needed", "required": True, "description": "Required resources"}
                ],
                word_limits={
                    "abstract": 300,
                    "ethical_framework": 600,
                    "research_questions": 400,
                    "interdisciplinary_approach": 800,
                    "stakeholder_analysis": 500,
                    "impact_assessment": 400,
                    "timeline": 300,
                    "resources_needed": 200
                },
                example_content={
                    "title": "Ethical Implications of AI in Healthcare Decision-Making",
                    "ethical_framework": "Based on principles of beneficence, non-maleficence, autonomy, and justice in healthcare AI applications.",
                    "research_questions": [
                        "How do AI systems impact patient autonomy in healthcare decisions?",
                        "What are the ethical considerations in AI-assisted diagnosis?"
                    ]
                }
            )
        ]
    
    def start_thesis_proposal(self, student_id: str, research_area: ResearchArea, 
                            proposal_type: ProposalType) -> Dict[str, Any]:
        """Start new thesis proposal with AI Professor guidance"""
        
        # Check if student already has a proposal
        existing_proposals = [p for p in self.thesis_proposals.values() if p.student_id == student_id]
        if existing_proposals:
            return {
                "success": False,
                "error": "Student already has a thesis proposal",
                "existing_proposal_id": existing_proposals[0].proposal_id
            }
        
        # Create proposal
        proposal_id = f"PROPOSAL_{uuid.uuid4().hex[:8]}"
        
        # Assign AI Professor advisor
        advisor_id = self._assign_ai_professor_advisor(research_area)
        
        proposal = ThesisProposal(
            proposal_id=proposal_id,
            student_id=student_id,
            title="",
            research_area=research_area,
            proposal_type=proposal_type,
            abstract="",
            research_question="",
            objectives=[],
            methodology="",
            literature_review="",
            expected_outcomes=[],
            timeline={},
            resources_needed=[],
            advisor_id=advisor_id,
            status=ProposalStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.thesis_proposals[proposal_id] = proposal
        
        # Get appropriate template
        template = self._get_proposal_template(research_area, proposal_type)
        
        # Generate initial AI guidance
        ai_guidance = self._generate_initial_ai_guidance(proposal, template)
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "advisor_id": advisor_id,
            "template": {
                "template_id": template.template_id,
                "template_name": template.template_name,
                "sections": template.sections,
                "word_limits": template.word_limits,
                "example_content": template.example_content
            },
            "ai_guidance": ai_guidance,
            "next_steps": [
                "Review the proposal template and examples",
                "Start with the title and abstract",
                "Schedule AI Professor guidance session",
                "Begin literature review research"
            ]
        }
    
    def _assign_ai_professor_advisor(self, research_area: ResearchArea) -> str:
        """Assign appropriate AI Professor as advisor"""
        
        if not self.professor_system:
            return "PROF_001"  # Default professor
        
        # Map research areas to professor specializations
        area_mapping = {
            ResearchArea.MACHINE_LEARNING: "machine_learning",
            ResearchArea.DEEP_LEARNING: "deep_learning",
            ResearchArea.COMPUTER_VISION: "computer_vision",
            ResearchArea.NATURAL_LANGUAGE_PROCESSING: "natural_language_processing",
            ResearchArea.AI_ETHICS: "ai_ethics",
            ResearchArea.ROBOTICS: "robotics",
            ResearchArea.NEURAL_NETWORKS: "neural_networks",
            ResearchArea.REINFORCEMENT_LEARNING: "reinforcement_learning",
            ResearchArea.DATA_SCIENCE: "data_science",
            ResearchArea.AI_THEORY: "ai_theory"
        }
        
        target_specialization = area_mapping.get(research_area, "machine_learning")
        
        # Find professor with matching specialization
        professors = self.professor_system.professors
        matching_professors = [
            prof for prof in professors
            if target_specialization in prof.specialization.value.lower()
        ]
        
        if matching_professors:
            return matching_professors[0].professor_id
        else:
            return professors[0].professor_id  # Default to first professor
    
    def _get_proposal_template(self, research_area: ResearchArea, proposal_type: ProposalType) -> ProposalTemplate:
        """Get appropriate proposal template"""
        
        # Find matching template
        for template in self.proposal_templates:
            if template.research_area == research_area and template.proposal_type == proposal_type:
                return template
        
        # Return default template
        return self.proposal_templates[0]
    
    def _generate_initial_ai_guidance(self, proposal: ThesisProposal, template: ProposalTemplate) -> Dict[str, Any]:
        """Generate initial AI guidance for proposal development"""
        
        guidance_session_id = f"GUIDANCE_{uuid.uuid4().hex[:8]}"
        
        guidance = {
            "session_id": guidance_session_id,
            "advisor_id": proposal.advisor_id,
            "research_area": proposal.research_area.value,
            "proposal_type": proposal.proposal_type.value,
            "guidance_topics": [
                "Research question formulation",
                "Literature review strategy",
                "Methodology selection",
                "Timeline planning",
                "Resource requirements"
            ],
            "specific_advice": {
                "research_question": f"Focus on a specific, answerable question in {proposal.research_area.value}",
                "literature_review": "Start with recent papers (last 3 years) and work backwards",
                "methodology": "Choose methodology appropriate for your research question and data availability",
                "timeline": "Plan for 6-12 months of research work with clear milestones",
                "resources": "Identify computational resources, datasets, and collaboration needs early"
            },
            "recommended_resources": [
                "IEEE Xplore for technical papers",
                "Google Scholar for comprehensive literature search",
                "arXiv for latest preprints",
                "ACM Digital Library for computer science papers"
            ],
            "next_steps": [
                "Develop a clear research question",
                "Conduct preliminary literature review",
                "Identify potential datasets or experimental setup",
                "Create detailed timeline with milestones"
            ]
        }
        
        # Store guidance session
        proposal.ai_guidance_sessions.append({
            "session_id": guidance_session_id,
            "session_type": "initial_guidance",
            "guidance_content": guidance,
            "created_at": datetime.now().isoformat()
        })
        
        return guidance
    
    def update_proposal_section(self, proposal_id: str, section_name: str, 
                              content: str) -> Dict[str, Any]:
        """Update specific section of thesis proposal"""
        
        proposal = self.thesis_proposals.get(proposal_id)
        if not proposal:
            return {"success": False, "error": "Proposal not found"}
        
        if proposal.status != ProposalStatus.DRAFT:
            return {"success": False, "error": "Proposal is not in draft status"}
        
        # Update section based on section name
        if section_name == "title":
            proposal.title = content
        elif section_name == "abstract":
            proposal.abstract = content
        elif section_name == "research_question":
            proposal.research_question = content
        elif section_name == "methodology":
            proposal.methodology = content
        elif section_name == "literature_review":
            proposal.literature_review = content
        else:
            return {"success": False, "error": f"Unknown section: {section_name}"}
        
        proposal.updated_at = datetime.now()
        
        # Generate AI feedback for the section
        ai_feedback = self._generate_section_feedback(proposal, section_name, content)
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "section_updated": section_name,
            "ai_feedback": ai_feedback,
            "updated_at": proposal.updated_at.isoformat()
        }
    
    def _generate_section_feedback(self, proposal: ThesisProposal, section_name: str, content: str) -> Dict[str, Any]:
        """Generate AI feedback for proposal section"""
        
        feedback = {
            "section": section_name,
            "content_length": len(content),
            "feedback_type": "constructive",
            "strengths": [],
            "suggestions": [],
            "improvements": []
        }
        
        # Generate section-specific feedback
        if section_name == "title":
            if len(content) < 10:
                feedback["suggestions"].append("Consider making the title more descriptive")
            if len(content) > 100:
                feedback["suggestions"].append("Consider shortening the title for clarity")
            if content:
                feedback["strengths"].append("Title is present")
        
        elif section_name == "abstract":
            word_count = len(content.split())
            if word_count < 100:
                feedback["suggestions"].append("Abstract should be at least 100 words")
            elif word_count > 300:
                feedback["suggestions"].append("Abstract should be concise (under 300 words)")
            else:
                feedback["strengths"].append("Abstract length is appropriate")
            
            if "research question" in content.lower():
                feedback["strengths"].append("Abstract mentions research question")
            else:
                feedback["suggestions"].append("Consider including the main research question in the abstract")
        
        elif section_name == "research_question":
            if len(content) < 20:
                feedback["suggestions"].append("Research question should be more detailed")
            if "?" not in content:
                feedback["suggestions"].append("Research question should end with a question mark")
            if content:
                feedback["strengths"].append("Research question is present")
        
        elif section_name == "methodology":
            methodology_keywords = ["experiment", "analysis", "model", "algorithm", "dataset", "evaluation"]
            found_keywords = [kw for kw in methodology_keywords if kw in content.lower()]
            if found_keywords:
                feedback["strengths"].append(f"Methodology includes relevant terms: {', '.join(found_keywords)}")
            else:
                feedback["suggestions"].append("Consider including specific methodological approaches")
        
        elif section_name == "literature_review":
            if len(content) < 200:
                feedback["suggestions"].append("Literature review should be more comprehensive")
            if "et al." in content or "(" in content:
                feedback["strengths"].append("Literature review includes citations")
            else:
                feedback["suggestions"].append("Consider including proper citations in literature review")
        
        return feedback
    
    def request_ai_guidance(self, proposal_id: str, guidance_topic: str, 
                          specific_question: str) -> Dict[str, Any]:
        """Request AI Professor guidance for specific topic"""
        
        proposal = self.thesis_proposals.get(proposal_id)
        if not proposal:
            return {"success": False, "error": "Proposal not found"}
        
        # Generate AI guidance
        guidance_session_id = f"GUIDANCE_{uuid.uuid4().hex[:8]}"
        
        guidance = self._generate_topic_guidance(proposal, guidance_topic, specific_question)
        
        # Store guidance session
        proposal.ai_guidance_sessions.append({
            "session_id": guidance_session_id,
            "session_type": "topic_guidance",
            "guidance_topic": guidance_topic,
            "specific_question": specific_question,
            "guidance_content": guidance,
            "created_at": datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "guidance_session_id": guidance_session_id,
            "guidance_topic": guidance_topic,
            "ai_guidance": guidance,
            "advisor_id": proposal.advisor_id
        }
    
    def _generate_topic_guidance(self, proposal: ThesisProposal, guidance_topic: str, 
                               specific_question: str) -> Dict[str, Any]:
        """Generate AI guidance for specific topic"""
        
        guidance_templates = {
            "research_question": {
                "advice": "A good research question should be specific, answerable, and contribute to the field. Consider: What problem are you trying to solve? What gap in knowledge are you addressing?",
                "examples": [
                    "How can deep learning models be improved for real-time object detection?",
                    "What are the ethical implications of AI in healthcare decision-making?",
                    "How can natural language processing be adapted for low-resource languages?"
                ],
                "criteria": [
                    "Specific and focused",
                    "Answerable with available methods",
                    "Contributes to existing knowledge",
                    "Feasible within time constraints"
                ]
            },
            "methodology": {
                "advice": "Choose methodology that best answers your research question. Consider: What data do you need? What experiments or analyses are required?",
                "examples": [
                    "Experimental design with control groups",
                    "Comparative analysis of existing methods",
                    "Case study approach",
                    "Mixed methods combining quantitative and qualitative analysis"
                ],
                "criteria": [
                    "Appropriate for research question",
                    "Feasible with available resources",
                    "Ethically sound",
                    "Reproducible"
                ]
            },
            "literature_review": {
                "advice": "Conduct comprehensive literature review to understand current state of research. Focus on recent work and identify gaps.",
                "examples": [
                    "Systematic review of papers from last 5 years",
                    "Meta-analysis of existing studies",
                    "Critical analysis of key papers",
                    "Comparative study of different approaches"
                ],
                "criteria": [
                    "Comprehensive coverage",
                    "Recent and relevant sources",
                    "Critical analysis",
                    "Identification of research gaps"
                ]
            },
            "timeline": {
                "advice": "Create realistic timeline with clear milestones. Consider dependencies between tasks and potential delays.",
                "examples": [
                    "Month 1-2: Literature review and research question refinement",
                    "Month 3-4: Methodology development and pilot study",
                    "Month 5-8: Main research work and data collection",
                    "Month 9-10: Analysis and thesis writing"
                ],
                "criteria": [
                    "Realistic time estimates",
                    "Clear milestones",
                    "Buffer time for delays",
                    "Regular progress reviews"
                ]
            }
        }
        
        template = guidance_templates.get(guidance_topic, {
            "advice": "Consider consulting with your advisor for specific guidance on this topic.",
            "examples": [],
            "criteria": []
        })
        
        return {
            "guidance_topic": guidance_topic,
            "specific_question": specific_question,
            "advisor_response": template["advice"],
            "examples": template["examples"],
            "evaluation_criteria": template["criteria"],
            "research_area_context": f"Given your research area ({proposal.research_area.value}), consider how this applies to your specific context.",
            "next_steps": [
                "Review the provided examples and criteria",
                "Apply the guidance to your specific proposal",
                "Schedule follow-up guidance session if needed",
                "Update your proposal based on the guidance"
            ]
        }
    
    def submit_proposal_for_review(self, proposal_id: str) -> Dict[str, Any]:
        """Submit proposal for review"""
        
        proposal = self.thesis_proposals.get(proposal_id)
        if not proposal:
            return {"success": False, "error": "Proposal not found"}
        
        if proposal.status != ProposalStatus.DRAFT:
            return {"success": False, "error": "Proposal is not in draft status"}
        
        # Validate proposal completeness
        validation_result = self._validate_proposal_completeness(proposal)
        if not validation_result["is_complete"]:
            return {
                "success": False,
                "error": "Proposal is incomplete",
                "missing_sections": validation_result["missing_sections"],
                "suggestions": validation_result["suggestions"]
            }
        
        # Update proposal status
        proposal.status = ProposalStatus.UNDER_REVIEW
        proposal.submission_date = datetime.now()
        proposal.review_deadline = datetime.now() + timedelta(days=14)  # 2 weeks for review
        proposal.updated_at = datetime.now()
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "status": ProposalStatus.UNDER_REVIEW.value,
            "submission_date": proposal.submission_date.isoformat(),
            "review_deadline": proposal.review_deadline.isoformat(),
            "message": "Proposal submitted for review successfully"
        }
    
    def _validate_proposal_completeness(self, proposal: ThesisProposal) -> Dict[str, Any]:
        """Validate proposal completeness"""
        
        missing_sections = []
        suggestions = []
        
        # Check required sections
        if not proposal.title:
            missing_sections.append("title")
            suggestions.append("Add a clear, descriptive title")
        
        if not proposal.abstract:
            missing_sections.append("abstract")
            suggestions.append("Write a comprehensive abstract (200-300 words)")
        
        if not proposal.research_question:
            missing_sections.append("research_question")
            suggestions.append("Formulate a clear research question")
        
        if not proposal.objectives:
            missing_sections.append("objectives")
            suggestions.append("Define specific research objectives")
        
        if not proposal.methodology:
            missing_sections.append("methodology")
            suggestions.append("Describe your research methodology")
        
        if not proposal.literature_review:
            missing_sections.append("literature_review")
            suggestions.append("Include comprehensive literature review")
        
        if not proposal.expected_outcomes:
            missing_sections.append("expected_outcomes")
            suggestions.append("Specify expected research outcomes")
        
        if not proposal.timeline:
            missing_sections.append("timeline")
            suggestions.append("Create detailed research timeline")
        
        if not proposal.resources_needed:
            missing_sections.append("resources_needed")
            suggestions.append("List required resources and support")
        
        return {
            "is_complete": len(missing_sections) == 0,
            "missing_sections": missing_sections,
            "suggestions": suggestions
        }
    
    def review_proposal(self, proposal_id: str, reviewer_id: str, 
                       review_data: Dict[str, Any]) -> Dict[str, Any]:
        """Review thesis proposal"""
        
        proposal = self.thesis_proposals.get(proposal_id)
        if not proposal:
            return {"success": False, "error": "Proposal not found"}
        
        if proposal.status != ProposalStatus.UNDER_REVIEW:
            return {"success": False, "error": "Proposal is not under review"}
        
        # Create review feedback
        review_feedback = {
            "reviewer_id": reviewer_id,
            "review_date": datetime.now().isoformat(),
            "overall_rating": review_data.get("overall_rating", 0),
            "section_ratings": review_data.get("section_ratings", {}),
            "strengths": review_data.get("strengths", []),
            "weaknesses": review_data.get("weaknesses", []),
            "suggestions": review_data.get("suggestions", []),
            "recommendation": review_data.get("recommendation", "revision_required"),
            "detailed_feedback": review_data.get("detailed_feedback", "")
        }
        
        # Add feedback to proposal
        proposal.feedback.append(review_feedback)
        
        # Update proposal status based on recommendation
        recommendation = review_data.get("recommendation", "revision_required")
        if recommendation == "approve":
            proposal.status = ProposalStatus.APPROVED
        elif recommendation == "reject":
            proposal.status = ProposalStatus.REJECTED
        else:
            proposal.status = ProposalStatus.REVISION_REQUIRED
            proposal.revisions_count += 1
        
        proposal.updated_at = datetime.now()
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "review_feedback": review_feedback,
            "new_status": proposal.status.value,
            "revisions_count": proposal.revisions_count
        }
    
    def get_proposal_status(self, proposal_id: str) -> Dict[str, Any]:
        """Get proposal status and progress"""
        
        proposal = self.thesis_proposals.get(proposal_id)
        if not proposal:
            return {"error": "Proposal not found"}
        
        # Calculate completion percentage
        required_sections = ["title", "abstract", "research_question", "objectives", 
                           "methodology", "literature_review", "expected_outcomes", 
                           "timeline", "resources_needed"]
        
        completed_sections = 0
        for section in required_sections:
            if hasattr(proposal, section) and getattr(proposal, section):
                completed_sections += 1
        
        completion_percentage = (completed_sections / len(required_sections)) * 100
        
        return {
            "proposal_id": proposal_id,
            "student_id": proposal.student_id,
            "title": proposal.title,
            "research_area": proposal.research_area.value,
            "proposal_type": proposal.proposal_type.value,
            "status": proposal.status.value,
            "completion_percentage": completion_percentage,
            "advisor_id": proposal.advisor_id,
            "created_at": proposal.created_at.isoformat(),
            "updated_at": proposal.updated_at.isoformat(),
            "submission_date": proposal.submission_date.isoformat() if proposal.submission_date else None,
            "review_deadline": proposal.review_deadline.isoformat() if proposal.review_deadline else None,
            "revisions_count": proposal.revisions_count,
            "ai_guidance_sessions": len(proposal.ai_guidance_sessions),
            "feedback_count": len(proposal.feedback),
            "recent_feedback": proposal.feedback[-1] if proposal.feedback else None
        }
    
    def get_proposal_analytics(self) -> Dict[str, Any]:
        """Get proposal system analytics"""
        
        total_proposals = len(self.thesis_proposals)
        
        if total_proposals == 0:
            return {"message": "No proposals created yet"}
        
        # Status distribution
        status_counts = {}
        for status in ProposalStatus:
            status_counts[status.value] = len([p for p in self.thesis_proposals.values() if p.status == status])
        
        # Research area distribution
        area_counts = {}
        for area in ResearchArea:
            area_counts[area.value] = len([p for p in self.thesis_proposals.values() if p.research_area == area])
        
        # Proposal type distribution
        type_counts = {}
        for proposal_type in ProposalType:
            type_counts[proposal_type.value] = len([p for p in self.thesis_proposals.values() if p.proposal_type == proposal_type])
        
        # Average completion time
        completed_proposals = [p for p in self.thesis_proposals.values() if p.status == ProposalStatus.APPROVED]
        completion_times = []
        for proposal in completed_proposals:
            if proposal.submission_date:
                completion_time = (proposal.submission_date - proposal.created_at).total_seconds() / 3600  # hours
                completion_times.append(completion_time)
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        # AI guidance statistics
        total_guidance_sessions = sum(len(p.ai_guidance_sessions) for p in self.thesis_proposals.values())
        
        return {
            "total_proposals": total_proposals,
            "status_distribution": status_counts,
            "research_area_distribution": area_counts,
            "proposal_type_distribution": type_counts,
            "completion_statistics": {
                "approved_proposals": len(completed_proposals),
                "average_completion_time_hours": avg_completion_time,
                "approval_rate": (len(completed_proposals) / total_proposals * 100) if total_proposals > 0 else 0
            },
            "ai_guidance_statistics": {
                "total_guidance_sessions": total_guidance_sessions,
                "average_sessions_per_proposal": total_guidance_sessions / total_proposals if total_proposals > 0 else 0
            },
            "review_statistics": {
                "total_reviews": sum(len(p.feedback) for p in self.thesis_proposals.values()),
                "average_revisions": sum(p.revisions_count for p in self.thesis_proposals.values()) / total_proposals if total_proposals > 0 else 0
            }
        }