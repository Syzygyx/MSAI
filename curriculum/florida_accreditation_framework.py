"""
MS AI Curriculum System - Florida Accreditation Framework
Comprehensive curriculum framework meeting Florida state and SACSCOC accreditation standards
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
import json
import uuid

class AccreditationStandard(Enum):
    SACSCOC = "sacscoc"
    FLORIDA_STATE = "florida_state"
    ABET = "abet"
    AACSB = "aacsb"

class LearningOutcomeCategory(Enum):
    KNOWLEDGE = "knowledge"
    SKILLS = "skills"
    COMPETENCIES = "competencies"
    ATTITUDES = "attitudes"
    VALUES = "values"

class AssessmentMethod(Enum):
    EXAMINATIONS = "examinations"
    PROJECTS = "projects"
    PORTFOLIOS = "portfolios"
    PRESENTATIONS = "presentations"
    PEER_REVIEW = "peer_review"
    SELF_ASSESSMENT = "self_assessment"
    PRACTICAL_DEMONSTRATIONS = "practical_demonstrations"

@dataclass
class AccreditationRequirement:
    """Accreditation requirement structure"""
    requirement_id: str
    standard: AccreditationStandard
    category: str
    description: str
    criteria: List[str]
    evidence_required: List[str]
    assessment_methods: List[AssessmentMethod]
    compliance_level: str  # required, recommended, optional

@dataclass
class LearningOutcome:
    """Learning outcome structure"""
    outcome_id: str
    category: LearningOutcomeCategory
    description: str
    level: str  # introductory, intermediate, advanced
    assessment_methods: List[AssessmentMethod]
    success_criteria: List[str]
    accreditation_alignment: List[str]

@dataclass
class Course:
    """Course structure"""
    course_id: str
    title: str
    credits: int
    level: str
    prerequisites: List[str]
    learning_outcomes: List[LearningOutcome]
    assessment_methods: List[AssessmentMethod]
    accreditation_alignment: List[str]
    created_at: datetime

@dataclass
class CurriculumFramework:
    """Complete curriculum framework"""
    framework_id: str
    program_name: str
    degree_level: str
    total_credits: int
    core_courses: List[Course]
    elective_courses: List[Course]
    capstone_requirement: Dict[str, Any]
    accreditation_requirements: List[AccreditationRequirement]
    learning_outcomes: List[LearningOutcome]
    assessment_framework: Dict[str, Any]
    created_at: datetime

class FloridaAccreditationFramework:
    """Florida accreditation framework for MS AI program"""
    
    def __init__(self):
        self.framework = self._create_ms_ai_framework()
        
    def _create_ms_ai_framework(self) -> CurriculumFramework:
        """Create MS AI curriculum framework meeting Florida standards"""
        
        # Define accreditation requirements
        accreditation_requirements = self._define_accreditation_requirements()
        
        # Define program learning outcomes
        learning_outcomes = self._define_program_learning_outcomes()
        
        # Define core courses
        core_courses = self._define_core_courses()
        
        # Define elective courses
        elective_courses = self._define_elective_courses()
        
        # Define capstone requirement
        capstone_requirement = self._define_capstone_requirement()
        
        # Define assessment framework
        assessment_framework = self._define_assessment_framework()
        
        return CurriculumFramework(
            framework_id="MS_AI_FRAMEWORK_001",
            program_name="Master of Science in Artificial Intelligence",
            degree_level="Graduate",
            total_credits=36,
            core_courses=core_courses,
            elective_courses=elective_courses,
            capstone_requirement=capstone_requirement,
            accreditation_requirements=accreditation_requirements,
            learning_outcomes=learning_outcomes,
            assessment_framework=assessment_framework,
            created_at=datetime.now()
        )
    
    def _define_accreditation_requirements(self) -> List[AccreditationRequirement]:
        """Define accreditation requirements for Florida and SACSCOC"""
        
        return [
            # SACSCOC Requirements
            AccreditationRequirement(
                requirement_id="SACSCOC_001",
                standard=AccreditationStandard.SACSCOC,
                category="Program Quality",
                description="Program demonstrates academic quality and rigor",
                criteria=[
                    "Clear program objectives and learning outcomes",
                    "Appropriate curriculum depth and breadth",
                    "Qualified faculty with relevant expertise",
                    "Adequate resources and facilities",
                    "Systematic assessment and improvement processes"
                ],
                evidence_required=[
                    "Program learning outcomes documentation",
                    "Curriculum mapping to outcomes",
                    "Faculty qualifications and credentials",
                    "Resource allocation documentation",
                    "Assessment results and improvement plans"
                ],
                assessment_methods=[
                    AssessmentMethod.EXAMINATIONS,
                    AssessmentMethod.PROJECTS,
                    AssessmentMethod.PORTFOLIOS,
                    AssessmentMethod.PRESENTATIONS
                ],
                compliance_level="required"
            ),
            
            AccreditationRequirement(
                requirement_id="SACSCOC_002",
                standard=AccreditationStandard.SACSCOC,
                category="Student Learning",
                description="Program ensures student learning and achievement",
                criteria=[
                    "Clear student learning outcomes",
                    "Appropriate assessment methods",
                    "Regular evaluation of student progress",
                    "Support for student success",
                    "Documentation of learning achievement"
                ],
                evidence_required=[
                    "Student learning outcomes assessment results",
                    "Grade distribution and performance data",
                    "Student success and retention rates",
                    "Graduate employment and career outcomes",
                    "Student satisfaction surveys"
                ],
                assessment_methods=[
                    AssessmentMethod.EXAMINATIONS,
                    AssessmentMethod.PROJECTS,
                    AssessmentMethod.PEER_REVIEW,
                    AssessmentMethod.SELF_ASSESSMENT
                ],
                compliance_level="required"
            ),
            
            # Florida State Requirements
            AccreditationRequirement(
                requirement_id="FL_001",
                standard=AccreditationStandard.FLORIDA_STATE,
                category="Program Approval",
                description="Program meets Florida state approval requirements",
                criteria=[
                    "Program aligns with state workforce needs",
                    "Appropriate degree level and credit requirements",
                    "Qualified faculty and staff",
                    "Adequate facilities and resources",
                    "Compliance with state regulations"
                ],
                evidence_required=[
                    "Workforce demand analysis",
                    "Program approval documentation",
                    "Faculty credentials and qualifications",
                    "Facility and resource documentation",
                    "State compliance documentation"
                ],
                assessment_methods=[
                    AssessmentMethod.PROJECTS,
                    AssessmentMethod.PRESENTATIONS,
                    AssessmentMethod.PRACTICAL_DEMONSTRATIONS
                ],
                compliance_level="required"
            ),
            
            AccreditationRequirement(
                requirement_id="FL_002",
                standard=AccreditationStandard.FLORIDA_STATE,
                category="Student Success",
                description="Program supports student success and completion",
                criteria=[
                    "Clear admission requirements and processes",
                    "Academic support and advising services",
                    "Career development and placement support",
                    "Student retention and completion rates",
                    "Graduate success outcomes"
                ],
                evidence_required=[
                    "Admission criteria and processes",
                    "Academic support service documentation",
                    "Career placement statistics",
                    "Retention and completion data",
                    "Graduate outcome surveys"
                ],
                assessment_methods=[
                    AssessmentMethod.PORTFOLIOS,
                    AssessmentMethod.SELF_ASSESSMENT,
                    AssessmentMethod.PEER_REVIEW
                ],
                compliance_level="required"
            ),
            
            # ABET Requirements (for engineering programs)
            AccreditationRequirement(
                requirement_id="ABET_001",
                standard=AccreditationStandard.ABET,
                category="Program Educational Objectives",
                description="Program has clear educational objectives",
                criteria=[
                    "Program educational objectives are clearly defined",
                    "Objectives align with program mission",
                    "Objectives are measurable and achievable",
                    "Stakeholder input is incorporated",
                    "Objectives are regularly reviewed and updated"
                ],
                evidence_required=[
                    "Program educational objectives statement",
                    "Stakeholder input documentation",
                    "Objective review and update records",
                    "Alignment with program mission",
                    "Measurability criteria"
                ],
                assessment_methods=[
                    AssessmentMethod.PROJECTS,
                    AssessmentMethod.PRESENTATIONS,
                    AssessmentMethod.PRACTICAL_DEMONSTRATIONS
                ],
                compliance_level="recommended"
            ),
            
            AccreditationRequirement(
                requirement_id="ABET_002",
                standard=AccreditationStandard.ABET,
                category="Student Outcomes",
                description="Program has clear student outcomes",
                criteria=[
                    "Student outcomes are clearly defined",
                    "Outcomes align with program objectives",
                    "Outcomes are measurable and assessable",
                    "Assessment methods are appropriate",
                    "Outcomes are regularly evaluated"
                ],
                evidence_required=[
                    "Student outcomes documentation",
                    "Outcome assessment results",
                    "Assessment method documentation",
                    "Evaluation and improvement records",
                    "Alignment with objectives"
                ],
                assessment_methods=[
                    AssessmentMethod.EXAMINATIONS,
                    AssessmentMethod.PROJECTS,
                    AssessmentMethod.PORTFOLIOS,
                    AssessmentMethod.PRESENTATIONS
                ],
                compliance_level="recommended"
            )
        ]
    
    def _define_program_learning_outcomes(self) -> List[LearningOutcome]:
        """Define program learning outcomes"""
        
        return [
            # Knowledge Outcomes
            LearningOutcome(
                outcome_id="LO_001",
                category=LearningOutcomeCategory.KNOWLEDGE,
                description="Demonstrate comprehensive knowledge of artificial intelligence principles, theories, and applications",
                level="advanced",
                assessment_methods=[
                    AssessmentMethod.EXAMINATIONS,
                    AssessmentMethod.PROJECTS,
                    AssessmentMethod.PRESENTATIONS
                ],
                success_criteria=[
                    "Achieve 80% or higher on comprehensive AI knowledge examinations",
                    "Successfully complete AI project demonstrating theoretical understanding",
                    "Present AI concepts clearly and accurately to peers and faculty"
                ],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "ABET_002"]
            ),
            
            LearningOutcome(
                outcome_id="LO_002",
                category=LearningOutcomeCategory.KNOWLEDGE,
                description="Understand the mathematical foundations of machine learning, deep learning, and neural networks",
                level="advanced",
                assessment_methods=[
                    AssessmentMethod.EXAMINATIONS,
                    AssessmentMethod.PROJECTS,
                    AssessmentMethod.PRACTICAL_DEMONSTRATIONS
                ],
                success_criteria=[
                    "Solve complex mathematical problems in AI and ML",
                    "Implement algorithms from mathematical principles",
                    "Demonstrate understanding of optimization and statistical methods"
                ],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "ABET_002"]
            ),
            
            # Skills Outcomes
            LearningOutcome(
                outcome_id="LO_003",
                category=LearningOutcomeCategory.SKILLS,
                description="Develop proficiency in programming languages and tools commonly used in AI development",
                level="advanced",
                assessment_methods=[
                    AssessmentMethod.PROJECTS,
                    AssessmentMethod.PRACTICAL_DEMONSTRATIONS,
                    AssessmentMethod.PORTFOLIOS
                ],
                success_criteria=[
                    "Complete programming projects in Python, R, and other AI languages",
                    "Demonstrate proficiency with AI frameworks and libraries",
                    "Create portfolio of programming projects demonstrating AI skills"
                ],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001", "ABET_002"]
            ),
            
            LearningOutcome(
                outcome_id="LO_004",
                category=LearningOutcomeCategory.SKILLS,
                description="Apply AI and machine learning techniques to solve real-world problems",
                level="advanced",
                assessment_methods=[
                    AssessmentMethod.PROJECTS,
                    AssessmentMethod.PRESENTATIONS,
                    AssessmentMethod.PRACTICAL_DEMONSTRATIONS
                ],
                success_criteria=[
                    "Complete capstone project solving real-world AI problem",
                    "Present project results and methodology effectively",
                    "Demonstrate practical application of AI techniques"
                ],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001", "ABET_002"]
            ),
            
            # Competencies Outcomes
            LearningOutcome(
                outcome_id="LO_005",
                category=LearningOutcomeCategory.COMPETENCIES,
                description="Evaluate and select appropriate AI methodologies for specific applications",
                level="advanced",
                assessment_methods=[
                    AssessmentMethod.PROJECTS,
                    AssessmentMethod.PRESENTATIONS,
                    AssessmentMethod.PEER_REVIEW
                ],
                success_criteria=[
                    "Compare and contrast different AI approaches",
                    "Justify methodology selection for specific problems",
                    "Evaluate trade-offs between different AI solutions"
                ],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "ABET_002"]
            ),
            
            LearningOutcome(
                outcome_id="LO_006",
                category=LearningOutcomeCategory.COMPETENCIES,
                description="Design and implement AI systems with consideration for ethical, social, and legal implications",
                level="advanced",
                assessment_methods=[
                    AssessmentMethod.PROJECTS,
                    AssessmentMethod.PRESENTATIONS,
                    AssessmentMethod.SELF_ASSESSMENT
                ],
                success_criteria=[
                    "Identify ethical implications of AI applications",
                    "Design AI systems with ethical considerations",
                    "Demonstrate awareness of social and legal implications"
                ],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001", "ABET_002"]
            ),
            
            # Attitudes Outcomes
            LearningOutcome(
                outcome_id="LO_007",
                category=LearningOutcomeCategory.ATTITUDES,
                description="Develop professional attitudes and behaviors appropriate for AI practitioners",
                level="advanced",
                assessment_methods=[
                    AssessmentMethod.PEER_REVIEW,
                    AssessmentMethod.SELF_ASSESSMENT,
                    AssessmentMethod.PORTFOLIOS
                ],
                success_criteria=[
                    "Demonstrate professional communication skills",
                    "Show respect for diverse perspectives and approaches",
                    "Maintain ethical standards in AI practice"
                ],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_002"]
            ),
            
            # Values Outcomes
            LearningOutcome(
                outcome_id="LO_008",
                category=LearningOutcomeCategory.VALUES,
                description="Commit to lifelong learning and professional development in AI field",
                level="advanced",
                assessment_methods=[
                    AssessmentMethod.SELF_ASSESSMENT,
                    AssessmentMethod.PORTFOLIOS,
                    AssessmentMethod.PEER_REVIEW
                ],
                success_criteria=[
                    "Develop personal learning plan for continued AI education",
                    "Engage in professional AI communities and activities",
                    "Demonstrate commitment to staying current with AI developments"
                ],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_002"]
            )
        ]
    
    def _define_core_courses(self) -> List[Course]:
        """Define core courses for MS AI program"""
        
        return [
            Course(
                course_id="AI501",
                title="Foundations of Artificial Intelligence",
                credits=3,
                level="graduate",
                prerequisites=[],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI501_LO_001",
                        category=LearningOutcomeCategory.KNOWLEDGE,
                        description="Understand fundamental AI concepts and approaches",
                        level="intermediate",
                        assessment_methods=[AssessmentMethod.EXAMINATIONS, AssessmentMethod.PROJECTS],
                        success_criteria=["Pass comprehensive AI foundations exam", "Complete AI project"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002"]
                    )
                ],
                assessment_methods=[AssessmentMethod.EXAMINATIONS, AssessmentMethod.PROJECTS],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001"],
                created_at=datetime.now()
            ),
            
            Course(
                course_id="AI502",
                title="Machine Learning and Data Mining",
                credits=3,
                level="graduate",
                prerequisites=["AI501"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI502_LO_001",
                        category=LearningOutcomeCategory.SKILLS,
                        description="Apply machine learning algorithms to real-world problems",
                        level="advanced",
                        assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRACTICAL_DEMONSTRATIONS],
                        success_criteria=["Complete ML project", "Demonstrate algorithm implementation"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "ABET_002"]
                    )
                ],
                assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRACTICAL_DEMONSTRATIONS],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001", "ABET_002"],
                created_at=datetime.now()
            ),
            
            Course(
                course_id="AI503",
                title="AI Ethics and Responsible Development",
                credits=3,
                level="graduate",
                prerequisites=["AI501"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI503_LO_001",
                        category=LearningOutcomeCategory.COMPETENCIES,
                        description="Evaluate ethical implications of AI systems",
                        level="advanced",
                        assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRESENTATIONS],
                        success_criteria=["Complete ethics analysis project", "Present ethical considerations"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001"]
                    )
                ],
                assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRESENTATIONS],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001"],
                created_at=datetime.now()
            ),
            
            Course(
                course_id="AI504",
                title="Deep Learning and Neural Networks",
                credits=3,
                level="graduate",
                prerequisites=["AI502"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI504_LO_001",
                        category=LearningOutcomeCategory.SKILLS,
                        description="Implement deep learning models and architectures",
                        level="advanced",
                        assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRACTICAL_DEMONSTRATIONS],
                        success_criteria=["Complete deep learning project", "Demonstrate model implementation"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "ABET_002"]
                    )
                ],
                assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRACTICAL_DEMONSTRATIONS],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001", "ABET_002"],
                created_at=datetime.now()
            ),
            
            Course(
                course_id="AI505",
                title="Natural Language Processing",
                credits=3,
                level="graduate",
                prerequisites=["AI502"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI505_LO_001",
                        category=LearningOutcomeCategory.SKILLS,
                        description="Apply NLP techniques to text analysis and generation",
                        level="advanced",
                        assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRACTICAL_DEMONSTRATIONS],
                        success_criteria=["Complete NLP project", "Demonstrate text processing skills"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "ABET_002"]
                    )
                ],
                assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRACTICAL_DEMONSTRATIONS],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001", "ABET_002"],
                created_at=datetime.now()
            ),
            
            Course(
                course_id="AI506",
                title="Computer Vision and Image Processing",
                credits=3,
                level="graduate",
                prerequisites=["AI502"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI506_LO_001",
                        category=LearningOutcomeCategory.SKILLS,
                        description="Implement computer vision algorithms and applications",
                        level="advanced",
                        assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRACTICAL_DEMONSTRATIONS],
                        success_criteria=["Complete computer vision project", "Demonstrate image processing skills"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "ABET_002"]
                    )
                ],
                assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRACTICAL_DEMONSTRATIONS],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001", "ABET_002"],
                created_at=datetime.now()
            ),
            
            Course(
                course_id="AI507",
                title="AI Research Methods and Statistics",
                credits=3,
                level="graduate",
                prerequisites=["AI501"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI507_LO_001",
                        category=LearningOutcomeCategory.COMPETENCIES,
                        description="Apply research methods and statistical analysis to AI problems",
                        level="advanced",
                        assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRESENTATIONS],
                        success_criteria=["Complete research project", "Present statistical analysis"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "ABET_002"]
                    )
                ],
                assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRESENTATIONS],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001", "ABET_002"],
                created_at=datetime.now()
            ),
            
            Course(
                course_id="AI508",
                title="AI Capstone Project",
                credits=6,
                level="graduate",
                prerequisites=["AI501", "AI502", "AI503", "AI504"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI508_LO_001",
                        category=LearningOutcomeCategory.COMPETENCIES,
                        description="Complete comprehensive AI project demonstrating mastery of program outcomes",
                        level="advanced",
                        assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRESENTATIONS, AssessmentMethod.PORTFOLIOS],
                        success_criteria=["Complete capstone project", "Present project results", "Demonstrate mastery of AI skills"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001", "ABET_002"]
                    )
                ],
                assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRESENTATIONS, AssessmentMethod.PORTFOLIOS],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001", "ABET_002"],
                created_at=datetime.now()
            )
        ]
    
    def _define_elective_courses(self) -> List[Course]:
        """Define elective courses for MS AI program"""
        
        return [
            Course(
                course_id="AI601",
                title="Advanced Machine Learning",
                credits=3,
                level="graduate",
                prerequisites=["AI502"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI601_LO_001",
                        category=LearningOutcomeCategory.KNOWLEDGE,
                        description="Understand advanced machine learning techniques and algorithms",
                        level="advanced",
                        assessment_methods=[AssessmentMethod.EXAMINATIONS, AssessmentMethod.PROJECTS],
                        success_criteria=["Pass advanced ML exam", "Complete advanced ML project"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002"]
                    )
                ],
                assessment_methods=[AssessmentMethod.EXAMINATIONS, AssessmentMethod.PROJECTS],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001"],
                created_at=datetime.now()
            ),
            
            Course(
                course_id="AI602",
                title="Robotics and Autonomous Systems",
                credits=3,
                level="graduate",
                prerequisites=["AI501", "AI502"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI602_LO_001",
                        category=LearningOutcomeCategory.SKILLS,
                        description="Apply AI techniques to robotics and autonomous systems",
                        level="advanced",
                        assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRACTICAL_DEMONSTRATIONS],
                        success_criteria=["Complete robotics project", "Demonstrate autonomous system implementation"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "ABET_002"]
                    )
                ],
                assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRACTICAL_DEMONSTRATIONS],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001", "ABET_002"],
                created_at=datetime.now()
            ),
            
            Course(
                course_id="AI603",
                title="AI in Healthcare",
                credits=3,
                level="graduate",
                prerequisites=["AI501", "AI502"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI603_LO_001",
                        category=LearningOutcomeCategory.COMPETENCIES,
                        description="Apply AI techniques to healthcare applications",
                        level="advanced",
                        assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRESENTATIONS],
                        success_criteria=["Complete healthcare AI project", "Present healthcare AI application"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001"]
                    )
                ],
                assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRESENTATIONS],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001"],
                created_at=datetime.now()
            ),
            
            Course(
                course_id="AI604",
                title="AI for Business and Finance",
                credits=3,
                level="graduate",
                prerequisites=["AI501", "AI502"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI604_LO_001",
                        category=LearningOutcomeCategory.COMPETENCIES,
                        description="Apply AI techniques to business and financial applications",
                        level="advanced",
                        assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRESENTATIONS],
                        success_criteria=["Complete business AI project", "Present financial AI application"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001"]
                    )
                ],
                assessment_methods=[AssessmentMethod.PROJECTS, AssessmentMethod.PRESENTATIONS],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "FL_001"],
                created_at=datetime.now()
            ),
            
            Course(
                course_id="AI605",
                title="AI Research Seminar",
                credits=3,
                level="graduate",
                prerequisites=["AI507"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI605_LO_001",
                        category=LearningOutcomeCategory.COMPETENCIES,
                        description="Engage in AI research and present research findings",
                        level="advanced",
                        assessment_methods=[AssessmentMethod.PRESENTATIONS, AssessmentMethod.PEER_REVIEW],
                        success_criteria=["Present research findings", "Participate in research discussions"],
                        accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "ABET_002"]
                    )
                ],
                assessment_methods=[AssessmentMethod.PRESENTATIONS, AssessmentMethod.PEER_REVIEW],
                accreditation_alignment=["SACSCOC_001", "SACSCOC_002", "ABET_002"],
                created_at=datetime.now()
            )
        ]
    
    def _define_capstone_requirement(self) -> Dict[str, Any]:
        """Define capstone requirement"""
        
        return {
            "requirement_type": "capstone_project",
            "course_id": "AI508",
            "credits": 6,
            "description": "Comprehensive AI project demonstrating mastery of program outcomes",
            "requirements": [
                "Complete original AI research or application project",
                "Demonstrate integration of multiple AI techniques",
                "Present project results to faculty and peers",
                "Submit comprehensive project report",
                "Demonstrate ethical considerations in AI development"
            ],
            "assessment_methods": [
                AssessmentMethod.PROJECTS.value,
                AssessmentMethod.PRESENTATIONS.value,
                AssessmentMethod.PORTFOLIOS.value
            ],
            "success_criteria": [
                "Project demonstrates mastery of AI concepts and techniques",
                "Presentation effectively communicates project results",
                "Report demonstrates professional writing and analysis",
                "Project shows consideration of ethical implications",
                "Project contributes to AI knowledge or practice"
            ],
            "accreditation_alignment": [
                "SACSCOC_001",
                "SACSCOC_002",
                "FL_001",
                "ABET_002"
            ]
        }
    
    def _define_assessment_framework(self) -> Dict[str, Any]:
        """Define assessment framework"""
        
        return {
            "assessment_philosophy": "Comprehensive assessment of student learning through multiple methods",
            "assessment_methods": {
                "formative": [
                    "Regular quizzes and assignments",
                    "Peer review and feedback",
                    "Self-assessment activities",
                    "Progress presentations"
                ],
                "summative": [
                    "Comprehensive examinations",
                    "Capstone project evaluation",
                    "Portfolio assessment",
                    "Final presentations"
                ]
            },
            "assessment_schedule": {
                "continuous": "Ongoing assessment throughout each course",
                "midterm": "Mid-semester comprehensive assessment",
                "final": "End-of-semester comprehensive assessment",
                "capstone": "Final capstone project assessment"
            },
            "assessment_criteria": {
                "knowledge": "Demonstration of understanding of AI concepts and principles",
                "skills": "Ability to apply AI techniques and tools",
                "competencies": "Integration of knowledge and skills in complex situations",
                "attitudes": "Professional behavior and ethical considerations",
                "values": "Commitment to lifelong learning and professional development"
            },
            "assessment_standards": {
                "excellent": "4.0-5.0 (A range)",
                "good": "3.0-3.9 (B range)",
                "satisfactory": "2.0-2.9 (C range)",
                "needs_improvement": "1.0-1.9 (D range)",
                "unsatisfactory": "0.0-0.9 (F range)"
            },
            "assessment_reporting": {
                "individual": "Individual student assessment results",
                "aggregate": "Class and program-level assessment results",
                "trend": "Assessment trends over time",
                "improvement": "Assessment-driven improvement plans"
            }
        }
    
    def get_framework_summary(self) -> Dict[str, Any]:
        """Get framework summary"""
        
        return {
            "framework_id": self.framework.framework_id,
            "program_name": self.framework.program_name,
            "degree_level": self.framework.degree_level,
            "total_credits": self.framework.total_credits,
            "core_courses_count": len(self.framework.core_courses),
            "elective_courses_count": len(self.framework.elective_courses),
            "learning_outcomes_count": len(self.framework.learning_outcomes),
            "accreditation_requirements_count": len(self.framework.accreditation_requirements),
            "accreditation_standards": list(set(req.standard.value for req in self.framework.accreditation_requirements)),
            "created_at": self.framework.created_at.isoformat()
        }
    
    def get_accreditation_compliance_report(self) -> Dict[str, Any]:
        """Get accreditation compliance report"""
        
        compliance_report = {
            "framework_id": self.framework.framework_id,
            "program_name": self.framework.program_name,
            "compliance_summary": {
                "total_requirements": len(self.framework.accreditation_requirements),
                "required_compliance": len([req for req in self.framework.accreditation_requirements if req.compliance_level == "required"]),
                "recommended_compliance": len([req for req in self.framework.accreditation_requirements if req.compliance_level == "recommended"]),
                "optional_compliance": len([req for req in self.framework.accreditation_requirements if req.compliance_level == "optional"])
            },
            "accreditation_standards": {}
        }
        
        # Group requirements by standard
        for standard in AccreditationStandard:
            standard_requirements = [
                req for req in self.framework.accreditation_requirements 
                if req.standard == standard
            ]
            
            compliance_report["accreditation_standards"][standard.value] = {
                "requirements_count": len(standard_requirements),
                "requirements": [
                    {
                        "requirement_id": req.requirement_id,
                        "category": req.category,
                        "description": req.description,
                        "compliance_level": req.compliance_level,
                        "criteria_count": len(req.criteria),
                        "evidence_required_count": len(req.evidence_required)
                    }
                    for req in standard_requirements
                ]
            }
        
        return compliance_report
    
    def get_curriculum_mapping(self) -> Dict[str, Any]:
        """Get curriculum mapping to learning outcomes"""
        
        mapping = {
            "program_learning_outcomes": [
                {
                    "outcome_id": outcome.outcome_id,
                    "category": outcome.category.value,
                    "description": outcome.description,
                    "level": outcome.level,
                    "accreditation_alignment": outcome.accreditation_alignment
                }
                for outcome in self.framework.learning_outcomes
            ],
            "course_mapping": {}
        }
        
        # Map courses to learning outcomes
        for course in self.framework.core_courses + self.framework.elective_courses:
            mapping["course_mapping"][course.course_id] = {
                "title": course.title,
                "credits": course.credits,
                "level": course.level,
                "learning_outcomes": [
                    {
                        "outcome_id": outcome.outcome_id,
                        "category": outcome.category.value,
                        "description": outcome.description,
                        "level": outcome.level
                    }
                    for outcome in course.learning_outcomes
                ],
                "assessment_methods": [method.value for method in course.assessment_methods],
                "accreditation_alignment": course.accreditation_alignment
            }
        
        return mapping