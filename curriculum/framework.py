"""
MS AI Curriculum Framework
Designed for Florida accreditation compliance
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class CourseLevel(Enum):
    FOUNDATIONAL = "foundational"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    CAPSTONE = "capstone"

class SpecializationTrack(Enum):
    APPLIED_AI = "applied_ai"
    RESEARCH_AI = "research_ai"
    INDUSTRY_AI = "industry_ai"
    AI_ETHICS = "ai_ethics"

@dataclass
class LearningOutcome:
    """Defines specific learning outcomes for accreditation"""
    outcome_id: str
    description: str
    assessment_method: str
    bloom_taxonomy_level: str
    industry_relevance: bool

@dataclass
class Course:
    """Individual course structure"""
    course_id: str
    title: str
    credits: int
    level: CourseLevel
    prerequisites: List[str]
    learning_outcomes: List[LearningOutcome]
    specialization_tracks: List[SpecializationTrack]
    accreditation_alignment: Dict[str, str]

@dataclass
class Curriculum:
    """Complete MS AI curriculum structure"""
    program_name: str
    total_credits: int
    core_courses: List[Course]
    specialization_courses: Dict[SpecializationTrack, List[Course]]
    capstone_requirements: Dict[str, str]
    accreditation_body: str
    state_compliance: Dict[str, str]

class MS_AICurriculumGenerator:
    """Generates AI-driven curriculum meeting Florida standards"""
    
    def __init__(self):
        self.florida_requirements = self._load_florida_requirements()
        self.sacscoc_standards = self._load_sacscoc_standards()
        
    def _load_florida_requirements(self) -> Dict[str, str]:
        """Load Florida Department of Education requirements"""
        return {
            "minimum_credits": "30",
            "core_competencies": [
                "mathematical_foundations",
                "programming_fundamentals", 
                "machine_learning",
                "data_science",
                "ai_ethics",
                "research_methods"
            ],
            "practical_experience": "required",
            "assessment_standards": "continuous_evaluation"
        }
    
    def _load_sacscoc_standards(self) -> Dict[str, str]:
        """Load SACSCOC accreditation standards"""
        return {
            "faculty_qualifications": "terminal_degree_required",
            "curriculum_rigor": "graduate_level_standards",
            "assessment_plan": "comprehensive_evaluation",
            "student_learning_outcomes": "measurable_objectives",
            "institutional_effectiveness": "continuous_improvement"
        }
    
    def generate_core_courses(self) -> List[Course]:
        """Generate core curriculum courses"""
        core_courses = [
            Course(
                course_id="AI501",
                title="Mathematical Foundations for AI",
                credits=3,
                level=CourseLevel.FOUNDATIONAL,
                prerequisites=[],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI501-1",
                        description="Apply linear algebra, calculus, and statistics to AI problems",
                        assessment_method="exams_and_projects",
                        bloom_taxonomy_level="application",
                        industry_relevance=True
                    )
                ],
                specialization_tracks=[SpecializationTrack.APPLIED_AI, SpecializationTrack.RESEARCH_AI],
                accreditation_alignment={"sacscoc": "mathematical_rigor", "florida": "core_competency"}
            ),
            Course(
                course_id="AI502", 
                title="Machine Learning Fundamentals",
                credits=3,
                level=CourseLevel.FOUNDATIONAL,
                prerequisites=["AI501"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI502-1",
                        description="Implement supervised and unsupervised learning algorithms",
                        assessment_method="programming_projects",
                        bloom_taxonomy_level="application",
                        industry_relevance=True
                    )
                ],
                specialization_tracks=[SpecializationTrack.APPLIED_AI, SpecializationTrack.RESEARCH_AI],
                accreditation_alignment={"sacscoc": "technical_competency", "florida": "core_competency"}
            ),
            Course(
                course_id="AI503",
                title="AI Ethics and Responsible Development",
                credits=3,
                level=CourseLevel.INTERMEDIATE,
                prerequisites=["AI502"],
                learning_outcomes=[
                    LearningOutcome(
                        outcome_id="AI503-1",
                        description="Analyze ethical implications of AI systems",
                        assessment_method="case_studies_and_essays",
                        bloom_taxonomy_level="analysis",
                        industry_relevance=True
                    )
                ],
                specialization_tracks=[SpecializationTrack.AI_ETHICS],
                accreditation_alignment={"sacscoc": "ethical_considerations", "florida": "core_competency"}
            )
        ]
        return core_courses
    
    def generate_specialization_tracks(self) -> Dict[SpecializationTrack, List[Course]]:
        """Generate specialization track courses"""
        specializations = {
            SpecializationTrack.APPLIED_AI: [
                Course(
                    course_id="AI601",
                    title="Computer Vision and Image Processing",
                    credits=3,
                    level=CourseLevel.ADVANCED,
                    prerequisites=["AI502"],
                    learning_outcomes=[
                        LearningOutcome(
                            outcome_id="AI601-1",
                            description="Develop computer vision applications",
                            assessment_method="project_portfolio",
                            bloom_taxonomy_level="creation",
                            industry_relevance=True
                        )
                    ],
                    specialization_tracks=[SpecializationTrack.APPLIED_AI],
                    accreditation_alignment={"sacscoc": "advanced_competency", "florida": "specialization"}
                )
            ],
            SpecializationTrack.RESEARCH_AI: [
                Course(
                    course_id="AI701",
                    title="Advanced Research Methods in AI",
                    credits=3,
                    level=CourseLevel.ADVANCED,
                    prerequisites=["AI502"],
                    learning_outcomes=[
                        LearningOutcome(
                            outcome_id="AI701-1",
                            description="Design and conduct original AI research",
                            assessment_method="research_proposal_and_paper",
                            bloom_taxonomy_level="creation",
                            industry_relevance=True
                        )
                    ],
                    specialization_tracks=[SpecializationTrack.RESEARCH_AI],
                    accreditation_alignment={"sacscoc": "research_competency", "florida": "specialization"}
                )
            ]
        }
        return specializations
    
    def generate_complete_curriculum(self) -> Curriculum:
        """Generate complete MS AI curriculum"""
        return Curriculum(
            program_name="Master of Science in Artificial Intelligence",
            total_credits=36,
            core_courses=self.generate_core_courses(),
            specialization_courses=self.generate_specialization_tracks(),
            capstone_requirements={
                "thesis_option": "Original research project with defense",
                "project_option": "Industry-sponsored AI application",
                "minimum_credits": "6"
            },
            accreditation_body="SACSCOC",
            state_compliance=self.florida_requirements
        )

if __name__ == "__main__":
    generator = MS_AICurriculumGenerator()
    curriculum = generator.generate_complete_curriculum()
    print(f"Generated curriculum: {curriculum.program_name}")
    print(f"Total credits: {curriculum.total_credits}")
    print(f"Core courses: {len(curriculum.core_courses)}")