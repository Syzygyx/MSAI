"""
MS AI Curriculum System - Thesis Defense System
Comprehensive thesis defense presentation and evaluation system
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import random

class DefenseStatus(Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    PRESENTATION_COMPLETE = "presentation_complete"
    Q_AND_A_COMPLETE = "q_and_a_complete"
    COMMITTEE_DELIBERATION = "committee_deliberation"
    COMPLETED = "completed"
    DEFERRED = "deferred"
    FAILED = "failed"

class PresentationPhase(Enum):
    INTRODUCTION = "introduction"
    LITERATURE_REVIEW = "literature_review"
    METHODOLOGY = "methodology"
    RESULTS = "results"
    DISCUSSION = "discussion"
    CONCLUSION = "conclusion"
    FUTURE_WORK = "future_work"

class QuestionType(Enum):
    TECHNICAL = "technical"
    METHODOLOGY = "methodology"
    THEORETICAL = "theoretical"
    PRACTICAL = "practical"
    ETHICAL = "ethical"
    FUTURE_WORK = "future_work"

@dataclass
class DefensePresentation:
    """Thesis defense presentation structure"""
    presentation_id: str
    defense_id: str
    student_id: str
    thesis_title: str
    presentation_slides: List[Dict[str, Any]]
    presentation_notes: str
    duration_minutes: int
    current_phase: PresentationPhase
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    presentation_score: float = 0.0
    feedback: List[str] = field(default_factory=list)

@dataclass
class DefenseQuestion:
    """Defense question structure"""
    question_id: str
    defense_id: str
    questioner_id: str
    question_type: QuestionType
    question_text: str
    asked_at: datetime
    student_response: str = ""
    response_time_seconds: int = 0
    follow_up_questions: List[str] = field(default_factory=list)
    question_score: float = 0.0

@dataclass
class ThesisDefense:
    """Thesis defense structure"""
    defense_id: str
    thesis_id: str
    student_id: str
    committee_id: str
    defense_date: datetime
    status: DefenseStatus
    presentation: Optional[DefensePresentation] = None
    questions: List[DefenseQuestion] = field(default_factory=list)
    evaluation_results: Dict[str, Any] = field(default_factory=dict)
    final_decision: str = ""
    decision_reason: str = ""
    completion_time: Optional[datetime] = None
    total_duration_minutes: int = 0

class ThesisDefenseSystem:
    """Comprehensive thesis defense presentation and evaluation system"""
    
    def __init__(self, committee_system=None, professor_system=None):
        self.committee_system = committee_system
        self.professor_system = professor_system
        
        # Defense data
        self.thesis_defenses: Dict[str, ThesisDefense] = {}
        self.defense_templates = self._initialize_defense_templates()
        self.question_banks = self._initialize_question_banks()
        
    def _initialize_defense_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize defense presentation templates"""
        return {
            "standard": {
                "duration_minutes": 30,
                "phases": [
                    {"phase": PresentationPhase.INTRODUCTION, "duration_minutes": 3, "description": "Introduction and motivation"},
                    {"phase": PresentationPhase.LITERATURE_REVIEW, "duration_minutes": 5, "description": "Literature review and related work"},
                    {"phase": PresentationPhase.METHODOLOGY, "duration_minutes": 8, "description": "Research methodology and approach"},
                    {"phase": PresentationPhase.RESULTS, "duration_minutes": 10, "description": "Results and findings"},
                    {"phase": PresentationPhase.DISCUSSION, "duration_minutes": 3, "description": "Discussion and implications"},
                    {"phase": PresentationPhase.CONCLUSION, "duration_minutes": 1, "description": "Conclusion and summary"}
                ],
                "slide_guidelines": {
                    "title_slide": "Clear title, student name, date, committee members",
                    "introduction_slides": "Problem statement, motivation, research questions",
                    "literature_slides": "Related work, gaps, positioning",
                    "methodology_slides": "Approach, experiments, evaluation metrics",
                    "results_slides": "Key findings, visualizations, analysis",
                    "conclusion_slides": "Contributions, limitations, future work"
                }
            },
            "extended": {
                "duration_minutes": 45,
                "phases": [
                    {"phase": PresentationPhase.INTRODUCTION, "duration_minutes": 5, "description": "Introduction and motivation"},
                    {"phase": PresentationPhase.LITERATURE_REVIEW, "duration_minutes": 8, "description": "Comprehensive literature review"},
                    {"phase": PresentationPhase.METHODOLOGY, "duration_minutes": 12, "description": "Detailed methodology and approach"},
                    {"phase": PresentationPhase.RESULTS, "duration_minutes": 15, "description": "Detailed results and analysis"},
                    {"phase": PresentationPhase.DISCUSSION, "duration_minutes": 4, "description": "Discussion and implications"},
                    {"phase": PresentationPhase.CONCLUSION, "duration_minutes": 1, "description": "Conclusion and summary"}
                ],
                "slide_guidelines": {
                    "title_slide": "Clear title, student name, date, committee members",
                    "introduction_slides": "Problem statement, motivation, research questions, contributions",
                    "literature_slides": "Comprehensive related work, gaps, positioning, theoretical foundation",
                    "methodology_slides": "Detailed approach, experiments, evaluation metrics, validation",
                    "results_slides": "Comprehensive findings, visualizations, statistical analysis",
                    "conclusion_slides": "Contributions, limitations, future work, impact"
                }
            }
        }
    
    def _initialize_question_banks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize question banks for different research areas"""
        return {
            "machine_learning": [
                {
                    "question_type": QuestionType.TECHNICAL,
                    "question": "How did you handle overfitting in your model?",
                    "follow_up": "What regularization techniques did you consider?"
                },
                {
                    "question_type": QuestionType.METHODOLOGY,
                    "question": "Why did you choose this particular algorithm?",
                    "follow_up": "How did you validate your choice?"
                },
                {
                    "question_type": QuestionType.THEORETICAL,
                    "question": "What is the theoretical foundation of your approach?",
                    "follow_up": "How does it relate to existing theoretical frameworks?"
                }
            ],
            "computer_vision": [
                {
                    "question_type": QuestionType.TECHNICAL,
                    "question": "How did you preprocess your image data?",
                    "follow_up": "What augmentation techniques did you use?"
                },
                {
                    "question_type": QuestionType.METHODOLOGY,
                    "question": "How did you evaluate your model's performance?",
                    "follow_up": "What metrics did you use and why?"
                },
                {
                    "question_type": QuestionType.PRACTICAL,
                    "question": "What are the practical applications of your work?",
                    "follow_up": "How would you deploy this in a real-world scenario?"
                }
            ],
            "ai_ethics": [
                {
                    "question_type": QuestionType.ETHICAL,
                    "question": "What ethical considerations did you address?",
                    "follow_up": "How did you ensure fairness in your system?"
                },
                {
                    "question_type": QuestionType.THEORETICAL,
                    "question": "What ethical frameworks did you apply?",
                    "follow_up": "How do you handle bias in your approach?"
                },
                {
                    "question_type": QuestionType.PRACTICAL,
                    "question": "What are the societal implications of your research?",
                    "follow_up": "How would you mitigate potential negative impacts?"
                }
            ],
            "general": [
                {
                    "question_type": QuestionType.METHODOLOGY,
                    "question": "What are the limitations of your approach?",
                    "follow_up": "How would you address these limitations?"
                },
                {
                    "question_type": QuestionType.FUTURE_WORK,
                    "question": "What are your plans for future research?",
                    "follow_up": "How would you extend this work?"
                },
                {
                    "question_type": QuestionType.TECHNICAL,
                    "question": "What was the most challenging aspect of your research?",
                    "follow_up": "How did you overcome this challenge?"
                }
            ]
        }
    
    def schedule_thesis_defense(self, thesis_id: str, student_id: str, 
                              committee_id: str, defense_data: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule thesis defense"""
        
        # Check if defense already exists
        existing_defenses = [d for d in self.thesis_defenses.values() if d.thesis_id == thesis_id]
        if existing_defenses:
            return {
                "success": False,
                "error": "Defense already scheduled for this thesis",
                "defense_id": existing_defenses[0].defense_id
            }
        
        # Create defense
        defense_id = f"DEFENSE_{uuid.uuid4().hex[:8]}"
        defense_date = datetime.fromisoformat(defense_data["defense_date"])
        
        defense = ThesisDefense(
            defense_id=defense_id,
            thesis_id=thesis_id,
            student_id=student_id,
            committee_id=committee_id,
            defense_date=defense_date,
            status=DefenseStatus.SCHEDULED
        )
        
        self.thesis_defenses[defense_id] = defense
        
        # Create presentation
        presentation_template = defense_data.get("presentation_template", "standard")
        presentation = self._create_defense_presentation(defense_id, thesis_id, presentation_template)
        defense.presentation = presentation
        
        return {
            "success": True,
            "defense_id": defense_id,
            "thesis_id": thesis_id,
            "student_id": student_id,
            "committee_id": committee_id,
            "defense_date": defense_date.isoformat(),
            "status": DefenseStatus.SCHEDULED.value,
            "presentation_template": presentation_template,
            "presentation_duration": presentation.duration_minutes,
            "preparation_guidelines": self._generate_preparation_guidelines(presentation_template)
        }
    
    def _create_defense_presentation(self, defense_id: str, thesis_id: str, 
                                   template_type: str) -> DefensePresentation:
        """Create defense presentation"""
        
        template = self.defense_templates.get(template_type, self.defense_templates["standard"])
        
        presentation_id = f"PRESENTATION_{uuid.uuid4().hex[:8]}"
        
        # Generate presentation slides
        slides = self._generate_presentation_slides(template)
        
        presentation = DefensePresentation(
            presentation_id=presentation_id,
            defense_id=defense_id,
            student_id="",  # Will be set by caller
            thesis_title="",  # Will be set by caller
            presentation_slides=slides,
            presentation_notes=self._generate_presentation_notes(template),
            duration_minutes=template["duration_minutes"],
            current_phase=PresentationPhase.INTRODUCTION
        )
        
        return presentation
    
    def _generate_presentation_slides(self, template: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate presentation slides based on template"""
        
        slides = []
        slide_number = 1
        
        # Title slide
        slides.append({
            "slide_number": slide_number,
            "slide_type": "title",
            "title": "Thesis Defense Presentation",
            "content": "Student Name, Date, Committee Members",
            "notes": "Introduce yourself and acknowledge committee members"
        })
        slide_number += 1
        
        # Generate slides for each phase
        for phase_info in template["phases"]:
            phase = phase_info["phase"]
            duration = phase_info["duration_minutes"]
            description = phase_info["description"]
            
            slides.append({
                "slide_number": slide_number,
                "slide_type": phase.value,
                "title": description,
                "content": f"Content for {description}",
                "duration_minutes": duration,
                "notes": f"Present {description} clearly and concisely"
            })
            slide_number += 1
        
        return slides
    
    def _generate_presentation_notes(self, template: Dict[str, Any]) -> str:
        """Generate presentation notes"""
        
        notes = "Thesis Defense Presentation Notes:\n\n"
        
        for phase_info in template["phases"]:
            phase = phase_info["phase"]
            duration = phase_info["duration_minutes"]
            description = phase_info["description"]
            
            notes += f"{phase.value.replace('_', ' ').title()} ({duration} minutes):\n"
            notes += f"- {description}\n"
            notes += f"- Key points to cover\n"
            notes += f"- Visual aids to use\n\n"
        
        notes += "General Guidelines:\n"
        notes += "- Speak clearly and at appropriate pace\n"
        notes += "- Maintain eye contact with committee\n"
        notes += "- Use visual aids effectively\n"
        notes += "- Be prepared for questions\n"
        notes += "- Stay within time limits\n"
        
        return notes
    
    def _generate_preparation_guidelines(self, template_type: str) -> List[str]:
        """Generate preparation guidelines"""
        
        guidelines = [
            "Review your thesis thoroughly and prepare concise summaries",
            "Practice your presentation multiple times",
            "Prepare for potential questions from committee members",
            "Ensure all visual aids are clear and professional",
            "Test all technical equipment before the defense",
            "Prepare backup materials in case of technical issues",
            "Dress professionally for the defense",
            "Arrive early to set up and test equipment",
            "Bring copies of your thesis for reference",
            "Prepare a brief introduction of yourself and your work"
        ]
        
        if template_type == "extended":
            guidelines.extend([
                "Prepare detailed explanations for complex concepts",
                "Have additional slides ready for deeper questions",
                "Practice explaining technical details clearly",
                "Prepare examples and case studies to illustrate points"
            ])
        
        return guidelines
    
    def start_defense_presentation(self, defense_id: str) -> Dict[str, Any]:
        """Start thesis defense presentation"""
        
        defense = self.thesis_defenses.get(defense_id)
        if not defense:
            return {"success": False, "error": "Defense not found"}
        
        if defense.status != DefenseStatus.SCHEDULED:
            return {"success": False, "error": "Defense is not scheduled"}
        
        # Update defense status
        defense.status = DefenseStatus.IN_PROGRESS
        defense.presentation.start_time = datetime.now()
        defense.presentation.current_phase = PresentationPhase.INTRODUCTION
        
        return {
            "success": True,
            "defense_id": defense_id,
            "status": DefenseStatus.IN_PROGRESS.value,
            "presentation_started": True,
            "current_phase": PresentationPhase.INTRODUCTION.value,
            "presentation_guidelines": [
                "Speak clearly and at appropriate pace",
                "Maintain eye contact with committee",
                "Use visual aids effectively",
                "Stay within time limits for each section"
            ]
        }
    
    def advance_presentation_phase(self, defense_id: str, new_phase: PresentationPhase) -> Dict[str, Any]:
        """Advance presentation to next phase"""
        
        defense = self.thesis_defenses.get(defense_id)
        if not defense or not defense.presentation:
            return {"success": False, "error": "Defense or presentation not found"}
        
        if defense.status != DefenseStatus.IN_PROGRESS:
            return {"success": False, "error": "Defense is not in progress"}
        
        # Update presentation phase
        defense.presentation.current_phase = new_phase
        
        # Generate phase-specific guidance
        phase_guidance = self._generate_phase_guidance(new_phase)
        
        return {
            "success": True,
            "defense_id": defense_id,
            "current_phase": new_phase.value,
            "phase_guidance": phase_guidance,
            "time_remaining": self._calculate_time_remaining(defense.presentation, new_phase)
        }
    
    def _generate_phase_guidance(self, phase: PresentationPhase) -> Dict[str, Any]:
        """Generate guidance for specific presentation phase"""
        
        guidance_templates = {
            PresentationPhase.INTRODUCTION: {
                "key_points": ["Problem statement", "Motivation", "Research questions", "Contributions"],
                "tips": ["Start with a compelling problem", "Clearly state your research questions", "Highlight your contributions"],
                "common_mistakes": ["Too much background", "Unclear problem statement", "Missing contributions"]
            },
            PresentationPhase.LITERATURE_REVIEW: {
                "key_points": ["Related work", "Gaps in literature", "Your positioning"],
                "tips": ["Focus on most relevant work", "Clearly identify gaps", "Position your work"],
                "common_mistakes": ["Too many papers", "No clear gaps", "Poor positioning"]
            },
            PresentationPhase.METHODOLOGY: {
                "key_points": ["Approach", "Experiments", "Evaluation metrics"],
                "tips": ["Explain your approach clearly", "Justify design choices", "Describe evaluation"],
                "common_mistakes": ["Unclear methodology", "No justification", "Missing evaluation"]
            },
            PresentationPhase.RESULTS: {
                "key_points": ["Key findings", "Visualizations", "Analysis"],
                "tips": ["Present results clearly", "Use effective visualizations", "Analyze findings"],
                "common_mistakes": ["Poor visualizations", "No analysis", "Unclear results"]
            },
            PresentationPhase.DISCUSSION: {
                "key_points": ["Implications", "Limitations", "Comparison"],
                "tips": ["Discuss implications", "Acknowledge limitations", "Compare with related work"],
                "common_mistakes": ["No discussion", "Ignoring limitations", "No comparison"]
            },
            PresentationPhase.CONCLUSION: {
                "key_points": ["Summary", "Contributions", "Future work"],
                "tips": ["Summarize key points", "Highlight contributions", "Suggest future work"],
                "common_mistakes": ["No summary", "Missing contributions", "No future work"]
            }
        }
        
        return guidance_templates.get(phase, {
            "key_points": [],
            "tips": [],
            "common_mistakes": []
        })
    
    def _calculate_time_remaining(self, presentation: DefensePresentation, current_phase: PresentationPhase) -> int:
        """Calculate remaining time for presentation"""
        
        total_time = presentation.duration_minutes
        elapsed_time = 0
        
        # Calculate elapsed time based on current phase
        phase_times = {
            PresentationPhase.INTRODUCTION: 3,
            PresentationPhase.LITERATURE_REVIEW: 5,
            PresentationPhase.METHODOLOGY: 8,
            PresentationPhase.RESULTS: 10,
            PresentationPhase.DISCUSSION: 3,
            PresentationPhase.CONCLUSION: 1
        }
        
        for phase, time in phase_times.items():
            if phase == current_phase:
                break
            elapsed_time += time
        
        return max(0, total_time - elapsed_time)
    
    def complete_presentation(self, defense_id: str, presentation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete thesis defense presentation"""
        
        defense = self.thesis_defenses.get(defense_id)
        if not defense or not defense.presentation:
            return {"success": False, "error": "Defense or presentation not found"}
        
        if defense.status != DefenseStatus.IN_PROGRESS:
            return {"success": False, "error": "Defense is not in progress"}
        
        # Update presentation
        defense.presentation.end_time = datetime.now()
        defense.presentation.presentation_score = presentation_data.get("presentation_score", random.uniform(3.0, 5.0))
        defense.presentation.feedback = presentation_data.get("feedback", [])
        
        # Update defense status
        defense.status = DefenseStatus.PRESENTATION_COMPLETE
        
        # Calculate presentation duration
        if defense.presentation.start_time and defense.presentation.end_time:
            duration = (defense.presentation.end_time - defense.presentation.start_time).total_seconds() / 60
            defense.total_duration_minutes += int(duration)
        
        return {
            "success": True,
            "defense_id": defense_id,
            "status": DefenseStatus.PRESENTATION_COMPLETE.value,
            "presentation_score": defense.presentation.presentation_score,
            "presentation_duration_minutes": defense.total_duration_minutes,
            "feedback": defense.presentation.feedback,
            "next_phase": "Q&A session"
        }
    
    def start_question_session(self, defense_id: str) -> Dict[str, Any]:
        """Start Q&A session"""
        
        defense = self.thesis_defenses.get(defense_id)
        if not defense:
            return {"success": False, "error": "Defense not found"}
        
        if defense.status != DefenseStatus.PRESENTATION_COMPLETE:
            return {"success": False, "error": "Presentation not completed"}
        
        # Update defense status
        defense.status = DefenseStatus.IN_PROGRESS
        
        # Generate initial questions
        initial_questions = self._generate_initial_questions(defense)
        
        return {
            "success": True,
            "defense_id": defense_id,
            "status": "Q&A session started",
            "initial_questions": initial_questions,
            "q_and_a_guidelines": [
                "Listen carefully to each question",
                "Take time to think before answering",
                "Ask for clarification if needed",
                "Be honest about limitations",
                "Provide specific examples when possible"
            ]
        }
    
    def _generate_initial_questions(self, defense: ThesisDefense) -> List[Dict[str, Any]]:
        """Generate initial questions for Q&A session"""
        
        # This would typically be based on the thesis content and committee members
        # For simulation, generate sample questions
        
        questions = [
            {
                "question_id": f"Q_{uuid.uuid4().hex[:8]}",
                "questioner_id": "COMMITTEE_CHAIR",
                "question_type": QuestionType.METHODOLOGY.value,
                "question_text": "Can you explain why you chose this particular methodology?",
                "difficulty": "medium"
            },
            {
                "question_id": f"Q_{uuid.uuid4().hex[:8]}",
                "questioner_id": "COMMITTEE_MEMBER_1",
                "question_type": QuestionType.TECHNICAL.value,
                "question_text": "What were the main technical challenges you faced?",
                "difficulty": "medium"
            },
            {
                "question_id": f"Q_{uuid.uuid4().hex[:8]}",
                "questioner_id": "COMMITTEE_MEMBER_2",
                "question_type": QuestionType.THEORETICAL.value,
                "question_text": "How does your work contribute to the theoretical understanding of this field?",
                "difficulty": "high"
            }
        ]
        
        return questions
    
    def ask_question(self, defense_id: str, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ask question during Q&A session"""
        
        defense = self.thesis_defenses.get(defense_id)
        if not defense:
            return {"success": False, "error": "Defense not found"}
        
        # Create question
        question_id = f"Q_{uuid.uuid4().hex[:8]}"
        question = DefenseQuestion(
            question_id=question_id,
            defense_id=defense_id,
            questioner_id=question_data["questioner_id"],
            question_type=QuestionType(question_data["question_type"]),
            question_text=question_data["question_text"],
            asked_at=datetime.now()
        )
        
        defense.questions.append(question)
        
        return {
            "success": True,
            "question_id": question_id,
            "question_text": question.question_text,
            "question_type": question.question_type.value,
            "questioner_id": question.questioner_id,
            "asked_at": question.asked_at.isoformat()
        }
    
    def answer_question(self, defense_id: str, question_id: str, 
                       response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Answer question during Q&A session"""
        
        defense = self.thesis_defenses.get(defense_id)
        if not defense:
            return {"success": False, "error": "Defense not found"}
        
        # Find question
        question = next((q for q in defense.questions if q.question_id == question_id), None)
        if not question:
            return {"success": False, "error": "Question not found"}
        
        # Update question with response
        question.student_response = response_data["response"]
        question.response_time_seconds = response_data.get("response_time_seconds", 0)
        question.follow_up_questions = response_data.get("follow_up_questions", [])
        question.question_score = response_data.get("question_score", random.uniform(3.0, 5.0))
        
        return {
            "success": True,
            "question_id": question_id,
            "response": question.student_response,
            "response_time_seconds": question.response_time_seconds,
            "question_score": question.question_score,
            "follow_up_questions": question.follow_up_questions
        }
    
    def complete_question_session(self, defense_id: str) -> Dict[str, Any]:
        """Complete Q&A session"""
        
        defense = self.thesis_defenses.get(defense_id)
        if not defense:
            return {"success": False, "error": "Defense not found"}
        
        # Update defense status
        defense.status = DefenseStatus.Q_AND_A_COMPLETE
        
        # Calculate Q&A statistics
        total_questions = len(defense.questions)
        answered_questions = len([q for q in defense.questions if q.student_response])
        average_response_time = sum(q.response_time_seconds for q in defense.questions) / total_questions if total_questions > 0 else 0
        average_question_score = sum(q.question_score for q in defense.questions) / total_questions if total_questions > 0 else 0
        
        return {
            "success": True,
            "defense_id": defense_id,
            "status": DefenseStatus.Q_AND_A_COMPLETE.value,
            "q_and_a_statistics": {
                "total_questions": total_questions,
                "answered_questions": answered_questions,
                "average_response_time_seconds": average_response_time,
                "average_question_score": average_question_score
            },
            "next_phase": "Committee deliberation"
        }
    
    def start_committee_deliberation(self, defense_id: str) -> Dict[str, Any]:
        """Start committee deliberation"""
        
        defense = self.thesis_defenses.get(defense_id)
        if not defense:
            return {"success": False, "error": "Defense not found"}
        
        if defense.status != DefenseStatus.Q_AND_A_COMPLETE:
            return {"success": False, "error": "Q&A session not completed"}
        
        # Update defense status
        defense.status = DefenseStatus.COMMITTEE_DELIBERATION
        
        return {
            "success": True,
            "defense_id": defense_id,
            "status": DefenseStatus.COMMITTEE_DELIBERATION.value,
            "deliberation_guidelines": [
                "Evaluate presentation quality",
                "Assess research contribution",
                "Review methodology and results",
                "Consider student's responses to questions",
                "Make final recommendation"
            ]
        }
    
    def complete_defense(self, defense_id: str, final_decision: str, 
                        decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete thesis defense with final decision"""
        
        defense = self.thesis_defenses.get(defense_id)
        if not defense:
            return {"success": False, "error": "Defense not found"}
        
        # Update defense
        defense.status = DefenseStatus.COMPLETED
        defense.final_decision = final_decision
        defense.decision_reason = decision_data.get("decision_reason", "")
        defense.completion_time = datetime.now()
        defense.evaluation_results = decision_data.get("evaluation_results", {})
        
        return {
            "success": True,
            "defense_id": defense_id,
            "status": DefenseStatus.COMPLETED.value,
            "final_decision": final_decision,
            "decision_reason": defense.decision_reason,
            "completion_time": defense.completion_time.isoformat(),
            "total_duration_minutes": defense.total_duration_minutes,
            "evaluation_results": defense.evaluation_results
        }
    
    def get_defense_status(self, defense_id: str) -> Dict[str, Any]:
        """Get defense status and information"""
        
        defense = self.thesis_defenses.get(defense_id)
        if not defense:
            return {"error": "Defense not found"}
        
        return {
            "defense_id": defense_id,
            "thesis_id": defense.thesis_id,
            "student_id": defense.student_id,
            "committee_id": defense.committee_id,
            "defense_date": defense.defense_date.isoformat(),
            "status": defense.status.value,
            "presentation": {
                "presentation_id": defense.presentation.presentation_id if defense.presentation else None,
                "duration_minutes": defense.presentation.duration_minutes if defense.presentation else 0,
                "current_phase": defense.presentation.current_phase.value if defense.presentation else None,
                "presentation_score": defense.presentation.presentation_score if defense.presentation else 0,
                "start_time": defense.presentation.start_time.isoformat() if defense.presentation and defense.presentation.start_time else None,
                "end_time": defense.presentation.end_time.isoformat() if defense.presentation and defense.presentation.end_time else None
            },
            "questions": [
                {
                    "question_id": q.question_id,
                    "questioner_id": q.questioner_id,
                    "question_type": q.question_type.value,
                    "question_text": q.question_text,
                    "student_response": q.student_response,
                    "question_score": q.question_score
                }
                for q in defense.questions
            ],
            "final_decision": defense.final_decision,
            "decision_reason": defense.decision_reason,
            "completion_time": defense.completion_time.isoformat() if defense.completion_time else None,
            "total_duration_minutes": defense.total_duration_minutes
        }
    
    def get_defense_analytics(self) -> Dict[str, Any]:
        """Get defense system analytics"""
        
        total_defenses = len(self.thesis_defenses)
        
        if total_defenses == 0:
            return {"message": "No defenses conducted yet"}
        
        # Status distribution
        status_counts = {}
        for status in DefenseStatus:
            status_counts[status.value] = len([d for d in self.thesis_defenses.values() if d.status == status])
        
        # Decision distribution
        decision_counts = {}
        decisions = [d.final_decision for d in self.thesis_defenses.values() if d.final_decision]
        for decision in set(decisions):
            decision_counts[decision] = decisions.count(decision)
        
        # Performance statistics
        completed_defenses = [d for d in self.thesis_defenses.values() if d.status == DefenseStatus.COMPLETED]
        
        presentation_scores = [d.presentation.presentation_score for d in completed_defenses if d.presentation]
        question_scores = []
        for defense in completed_defenses:
            question_scores.extend([q.question_score for q in defense.questions])
        
        avg_presentation_score = sum(presentation_scores) / len(presentation_scores) if presentation_scores else 0
        avg_question_score = sum(question_scores) / len(question_scores) if question_scores else 0
        
        # Duration statistics
        durations = [d.total_duration_minutes for d in completed_defenses]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "total_defenses": total_defenses,
            "status_distribution": status_counts,
            "decision_distribution": decision_counts,
            "performance_statistics": {
                "completed_defenses": len(completed_defenses),
                "average_presentation_score": avg_presentation_score,
                "average_question_score": avg_question_score,
                "average_duration_minutes": avg_duration
            },
            "question_statistics": {
                "total_questions_asked": sum(len(d.questions) for d in self.thesis_defenses.values()),
                "average_questions_per_defense": sum(len(d.questions) for d in self.thesis_defenses.values()) / total_defenses if total_defenses > 0 else 0
            }
        }