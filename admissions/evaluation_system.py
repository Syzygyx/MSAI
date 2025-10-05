"""
MS AI Curriculum System - Automated Evaluation System
Advanced AI-powered application evaluation and scoring system
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import random
import re
from collections import Counter

class EvaluationCriteria(Enum):
    ACADEMIC_EXCELLENCE = "academic_excellence"
    TECHNICAL_COMPETENCY = "technical_competency"
    RESEARCH_POTENTIAL = "research_potential"
    PROFESSIONAL_EXPERIENCE = "professional_experience"
    PERSONAL_STATEMENT_QUALITY = "personal_statement_quality"
    DIVERSITY_CONTRIBUTION = "diversity_contribution"
    LEADERSHIP_POTENTIAL = "leadership_potential"
    COMMUNICATION_SKILLS = "communication_skills"

class EvaluationWeight(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class EvaluationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REVIEW_REQUIRED = "review_required"
    DISPUTED = "disputed"

@dataclass
class EvaluationCriteria:
    """Individual evaluation criteria"""
    criteria_id: str
    name: str
    description: str
    weight: EvaluationWeight
    max_score: float
    evaluation_method: str
    ai_model_used: str
    human_review_required: bool = False

@dataclass
class EvaluationResult:
    """Result of application evaluation"""
    evaluation_id: str
    application_id: str
    evaluator_id: str
    criteria_scores: Dict[str, float]
    overall_score: float
    recommendation: str
    confidence_score: float
    evaluation_notes: str
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]
    evaluated_at: datetime
    evaluation_time_minutes: float
    status: EvaluationStatus

@dataclass
class EvaluationModel:
    """AI model for evaluation"""
    model_id: str
    name: str
    specialization: str
    version: str
    accuracy_score: float
    last_trained: datetime
    evaluation_criteria: List[str]
    performance_metrics: Dict[str, float]

class AutomatedEvaluationSystem:
    """Advanced AI-powered application evaluation system"""
    
    def __init__(self, admissions_system=None, professor_system=None):
        self.admissions_system = admissions_system
        self.professor_system = professor_system
        
        # Evaluation data
        self.evaluation_results: Dict[str, EvaluationResult] = {}
        self.evaluation_criteria = self._initialize_evaluation_criteria()
        self.evaluation_models = self._initialize_evaluation_models()
        
        # Scoring algorithms
        self.scoring_algorithms = self._initialize_scoring_algorithms()
        
    def _initialize_evaluation_criteria(self) -> List[EvaluationCriteria]:
        """Initialize evaluation criteria for MS AI program"""
        return [
            EvaluationCriteria(
                criteria_id="CRIT_001",
                name="Academic Excellence",
                description="Evaluation of academic background, GPA, and educational achievements",
                weight=EvaluationWeight.HIGH,
                max_score=25.0,
                evaluation_method="gpa_analysis",
                ai_model_used="academic_scorer_v1"
            ),
            EvaluationCriteria(
                criteria_id="CRIT_002",
                name="Technical Competency",
                description="Assessment of programming skills, technical knowledge, and AI/ML experience",
                weight=EvaluationWeight.HIGH,
                max_score=25.0,
                evaluation_method="technical_assessment",
                ai_model_used="technical_scorer_v1"
            ),
            EvaluationCriteria(
                criteria_id="CRIT_003",
                name="Research Potential",
                description="Evaluation of research experience, publications, and research interests",
                weight=EvaluationWeight.MEDIUM,
                max_score=20.0,
                evaluation_method="research_analyzer",
                ai_model_used="research_scorer_v1"
            ),
            EvaluationCriteria(
                criteria_id="CRIT_004",
                name="Professional Experience",
                description="Assessment of work experience, projects, and industry relevance",
                weight=EvaluationWeight.MEDIUM,
                max_score=15.0,
                evaluation_method="experience_evaluator",
                ai_model_used="experience_scorer_v1"
            ),
            EvaluationCriteria(
                criteria_id="CRIT_005",
                name="Personal Statement Quality",
                description="Analysis of motivation, goals, and communication skills",
                weight=EvaluationWeight.MEDIUM,
                max_score=10.0,
                evaluation_method="nlp_analyzer",
                ai_model_used="statement_scorer_v1",
                human_review_required=True
            ),
            EvaluationCriteria(
                criteria_id="CRIT_006",
                name="Diversity Contribution",
                description="Evaluation of diverse background and contribution to program diversity",
                weight=EvaluationWeight.LOW,
                max_score=5.0,
                evaluation_method="diversity_assessor",
                ai_model_used="diversity_scorer_v1"
            )
        ]
    
    def _initialize_evaluation_models(self) -> List[EvaluationModel]:
        """Initialize AI evaluation models"""
        return [
            EvaluationModel(
                model_id="MODEL_001",
                name="Academic Excellence Scorer",
                specialization="Academic background analysis",
                version="1.0",
                accuracy_score=0.92,
                last_trained=datetime.now() - timedelta(days=30),
                evaluation_criteria=["CRIT_001"],
                performance_metrics={
                    "precision": 0.89,
                    "recall": 0.91,
                    "f1_score": 0.90,
                    "processing_time_ms": 150
                }
            ),
            EvaluationModel(
                model_id="MODEL_002",
                name="Technical Competency Analyzer",
                specialization="Technical skills assessment",
                version="1.2",
                accuracy_score=0.88,
                last_trained=datetime.now() - timedelta(days=15),
                evaluation_criteria=["CRIT_002"],
                performance_metrics={
                    "precision": 0.87,
                    "recall": 0.89,
                    "f1_score": 0.88,
                    "processing_time_ms": 200
                }
            ),
            EvaluationModel(
                model_id="MODEL_003",
                name="Research Potential Evaluator",
                specialization="Research experience analysis",
                version="1.1",
                accuracy_score=0.85,
                last_trained=datetime.now() - timedelta(days=20),
                evaluation_criteria=["CRIT_003"],
                performance_metrics={
                    "precision": 0.84,
                    "recall": 0.86,
                    "f1_score": 0.85,
                    "processing_time_ms": 180
                }
            ),
            EvaluationModel(
                model_id="MODEL_004",
                name="Professional Experience Assessor",
                specialization="Work experience evaluation",
                version="1.0",
                accuracy_score=0.90,
                last_trained=datetime.now() - timedelta(days=25),
                evaluation_criteria=["CRIT_004"],
                performance_metrics={
                    "precision": 0.89,
                    "recall": 0.91,
                    "f1_score": 0.90,
                    "processing_time_ms": 120
                }
            ),
            EvaluationModel(
                model_id="MODEL_005",
                name="Personal Statement NLP Analyzer",
                specialization="Natural language processing for personal statements",
                version="2.0",
                accuracy_score=0.87,
                last_trained=datetime.now() - timedelta(days=10),
                evaluation_criteria=["CRIT_005"],
                performance_metrics={
                    "precision": 0.86,
                    "recall": 0.88,
                    "f1_score": 0.87,
                    "processing_time_ms": 300
                }
            ),
            EvaluationModel(
                model_id="MODEL_006",
                name="Diversity Contribution Assessor",
                specialization="Diversity and inclusion evaluation",
                version="1.0",
                accuracy_score=0.83,
                last_trained=datetime.now() - timedelta(days=35),
                evaluation_criteria=["CRIT_006"],
                performance_metrics={
                    "precision": 0.82,
                    "recall": 0.84,
                    "f1_score": 0.83,
                    "processing_time_ms": 100
                }
            )
        ]
    
    def _initialize_scoring_algorithms(self) -> Dict[str, Dict[str, Any]]:
        """Initialize scoring algorithms for different criteria"""
        return {
            "gpa_analysis": {
                "algorithm": "weighted_gpa_scoring",
                "parameters": {
                    "gpa_weight": 0.7,
                    "institution_weight": 0.2,
                    "course_relevance_weight": 0.1
                },
                "scoring_rules": {
                    "gpa_4.0": 25.0,
                    "gpa_3.8": 22.0,
                    "gpa_3.5": 18.0,
                    "gpa_3.0": 12.0,
                    "gpa_2.5": 6.0
                }
            },
            "technical_assessment": {
                "algorithm": "skill_matrix_scoring",
                "parameters": {
                    "programming_weight": 0.4,
                    "ai_ml_weight": 0.3,
                    "tools_weight": 0.2,
                    "projects_weight": 0.1
                },
                "skill_levels": {
                    "expert": 25.0,
                    "advanced": 20.0,
                    "intermediate": 15.0,
                    "beginner": 8.0,
                    "none": 0.0
                }
            },
            "research_analyzer": {
                "algorithm": "research_experience_scoring",
                "parameters": {
                    "publications_weight": 0.4,
                    "research_experience_weight": 0.3,
                    "research_interests_weight": 0.2,
                    "academic_honors_weight": 0.1
                }
            },
            "experience_evaluator": {
                "algorithm": "professional_experience_scoring",
                "parameters": {
                    "years_experience_weight": 0.3,
                    "ai_ml_relevance_weight": 0.4,
                    "leadership_weight": 0.2,
                    "projects_weight": 0.1
                }
            },
            "nlp_analyzer": {
                "algorithm": "sentiment_and_content_analysis",
                "parameters": {
                    "motivation_score_weight": 0.3,
                    "clarity_score_weight": 0.25,
                    "goals_alignment_weight": 0.25,
                    "writing_quality_weight": 0.2
                }
            },
            "diversity_assessor": {
                "algorithm": "diversity_contribution_scoring",
                "parameters": {
                    "background_diversity_weight": 0.4,
                    "perspective_contribution_weight": 0.3,
                    "inclusion_commitment_weight": 0.3
                }
            }
        }
    
    def evaluate_application(self, application_id: str, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive application evaluation"""
        
        start_time = datetime.now()
        
        # Initialize evaluation result
        evaluation_id = f"EVAL_{uuid.uuid4().hex[:8]}"
        criteria_scores = {}
        evaluation_notes = []
        strengths = []
        weaknesses = []
        improvement_suggestions = []
        
        # Evaluate each criteria
        for criteria in self.evaluation_criteria:
            criteria_result = self._evaluate_criteria(criteria, application_data)
            criteria_scores[criteria.criteria_id] = criteria_result["score"]
            evaluation_notes.append(f"{criteria.name}: {criteria_result['notes']}")
            
            if criteria_result["strengths"]:
                strengths.extend(criteria_result["strengths"])
            if criteria_result["weaknesses"]:
                weaknesses.extend(criteria_result["weaknesses"])
            if criteria_result["suggestions"]:
                improvement_suggestions.extend(criteria_result["suggestions"])
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(criteria_scores)
        
        # Determine recommendation
        recommendation = self._determine_recommendation(overall_score, criteria_scores)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(criteria_scores, application_data)
        
        # Create evaluation result
        evaluation_result = EvaluationResult(
            evaluation_id=evaluation_id,
            application_id=application_id,
            evaluator_id="AI_EVALUATOR_SYSTEM",
            criteria_scores=criteria_scores,
            overall_score=overall_score,
            recommendation=recommendation,
            confidence_score=confidence_score,
            evaluation_notes="; ".join(evaluation_notes),
            strengths=strengths,
            weaknesses=weaknesses,
            improvement_suggestions=improvement_suggestions,
            evaluated_at=datetime.now(),
            evaluation_time_minutes=(datetime.now() - start_time).total_seconds() / 60,
            status=EvaluationStatus.COMPLETED
        )
        
        # Store evaluation result
        self.evaluation_results[evaluation_id] = evaluation_result
        
        return {
            "success": True,
            "evaluation_id": evaluation_id,
            "application_id": application_id,
            "overall_score": overall_score,
            "recommendation": recommendation,
            "confidence_score": confidence_score,
            "criteria_scores": criteria_scores,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "improvement_suggestions": improvement_suggestions,
            "evaluation_time_minutes": evaluation_result.evaluation_time_minutes,
            "evaluation_summary": self._generate_evaluation_summary(evaluation_result)
        }
    
    def _evaluate_criteria(self, criteria: EvaluationCriteria, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate specific criteria using appropriate model and algorithm"""
        
        criteria_id = criteria.criteria_id
        evaluation_method = criteria.evaluation_method
        
        # Get appropriate scoring algorithm
        algorithm = self.scoring_algorithms.get(evaluation_method, {})
        
        if criteria_id == "CRIT_001":  # Academic Excellence
            return self._evaluate_academic_excellence(application_data, algorithm)
        elif criteria_id == "CRIT_002":  # Technical Competency
            return self._evaluate_technical_competency(application_data, algorithm)
        elif criteria_id == "CRIT_003":  # Research Potential
            return self._evaluate_research_potential(application_data, algorithm)
        elif criteria_id == "CRIT_004":  # Professional Experience
            return self._evaluate_professional_experience(application_data, algorithm)
        elif criteria_id == "CRIT_005":  # Personal Statement Quality
            return self._evaluate_personal_statement(application_data, algorithm)
        elif criteria_id == "CRIT_006":  # Diversity Contribution
            return self._evaluate_diversity_contribution(application_data, algorithm)
        else:
            return {
                "score": 0.0,
                "notes": "Unknown criteria",
                "strengths": [],
                "weaknesses": [],
                "suggestions": []
            }
    
    def _evaluate_academic_excellence(self, application_data: Dict[str, Any], algorithm: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate academic excellence"""
        
        academic_data = application_data.get("academic_background", {})
        gpa = academic_data.get("gpa", 0.0)
        institution = academic_data.get("undergraduate_institution", "")
        major = academic_data.get("major", "")
        
        # Calculate GPA score
        gpa_score = 0.0
        if gpa >= 4.0:
            gpa_score = 25.0
        elif gpa >= 3.8:
            gpa_score = 22.0
        elif gpa >= 3.5:
            gpa_score = 18.0
        elif gpa >= 3.0:
            gpa_score = 12.0
        elif gpa >= 2.5:
            gpa_score = 6.0
        
        # Institution bonus
        institution_bonus = 0.0
        if any(keyword in institution.lower() for keyword in ["university", "college", "institute"]):
            institution_bonus = 2.0
        
        # Major relevance bonus
        major_bonus = 0.0
        relevant_majors = ["computer science", "engineering", "mathematics", "statistics", "physics"]
        if any(keyword in major.lower() for keyword in relevant_majors):
            major_bonus = 3.0
        
        total_score = min(25.0, gpa_score + institution_bonus + major_bonus)
        
        # Generate feedback
        strengths = []
        weaknesses = []
        suggestions = []
        
        if gpa >= 3.5:
            strengths.append("Strong academic performance")
        else:
            weaknesses.append("GPA below program average")
            suggestions.append("Consider highlighting relevant coursework and projects")
        
        if major_bonus > 0:
            strengths.append("Relevant academic background")
        else:
            suggestions.append("Emphasize transferable skills from your field")
        
        notes = f"GPA: {gpa}, Institution: {institution}, Major: {major}"
        
        return {
            "score": total_score,
            "notes": notes,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions
        }
    
    def _evaluate_technical_competency(self, application_data: Dict[str, Any], algorithm: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate technical competency"""
        
        work_data = application_data.get("work_experience", {})
        tech_data = application_data.get("technical_skills", {})
        
        programming_languages = work_data.get("programming_languages", "")
        technical_skills = work_data.get("technical_skills", "")
        ai_ml_experience = work_data.get("ai_ml_experience", "")
        projects = work_data.get("projects", "")
        
        # Programming languages score
        prog_score = 0.0
        if programming_languages:
            languages = programming_languages.lower()
            if "python" in languages:
                prog_score += 8.0
            if "java" in languages or "javascript" in languages:
                prog_score += 4.0
            if "c++" in languages or "c#" in languages:
                prog_score += 3.0
            if "r" in languages:
                prog_score += 2.0
        
        # AI/ML experience score
        ai_score = 0.0
        if ai_ml_experience:
            experience = ai_ml_experience.lower()
            if any(keyword in experience for keyword in ["machine learning", "deep learning", "neural network"]):
                ai_score += 10.0
            if any(keyword in experience for keyword in ["tensorflow", "pytorch", "scikit-learn"]):
                ai_score += 5.0
            if any(keyword in experience for keyword in ["data science", "analytics", "statistics"]):
                ai_score += 3.0
        
        # Technical skills score
        tech_score = 0.0
        if technical_skills:
            skills = technical_skills.lower()
            if any(keyword in skills for keyword in ["algorithm", "data structure", "software development"]):
                tech_score += 5.0
            if any(keyword in skills for keyword in ["database", "sql", "nosql"]):
                tech_score += 2.0
        
        # Projects score
        project_score = 0.0
        if projects:
            project_score += 3.0  # Base score for having projects
        
        total_score = min(25.0, prog_score + ai_score + tech_score + project_score)
        
        # Generate feedback
        strengths = []
        weaknesses = []
        suggestions = []
        
        if prog_score >= 8.0:
            strengths.append("Strong programming background")
        else:
            weaknesses.append("Limited programming experience")
            suggestions.append("Consider taking programming courses or working on coding projects")
        
        if ai_score >= 8.0:
            strengths.append("Relevant AI/ML experience")
        else:
            weaknesses.append("Limited AI/ML experience")
            suggestions.append("Gain hands-on experience with machine learning tools and projects")
        
        if total_score >= 20.0:
            strengths.append("Excellent technical competency")
        elif total_score >= 15.0:
            strengths.append("Good technical foundation")
        else:
            weaknesses.append("Technical skills need development")
            suggestions.append("Focus on building technical skills through courses and projects")
        
        notes = f"Programming: {prog_score:.1f}, AI/ML: {ai_score:.1f}, Technical: {tech_score:.1f}, Projects: {project_score:.1f}"
        
        return {
            "score": total_score,
            "notes": notes,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions
        }
    
    def _evaluate_research_potential(self, application_data: Dict[str, Any], algorithm: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate research potential"""
        
        academic_data = application_data.get("academic_background", {})
        personal_data = application_data.get("personal_statement", {})
        
        research_experience = academic_data.get("research_experience", "")
        academic_honors = academic_data.get("academic_honors", "")
        research_interests = personal_data.get("research_interests", "")
        
        # Research experience score
        research_score = 0.0
        if research_experience:
            experience = research_experience.lower()
            if any(keyword in experience for keyword in ["publication", "paper", "journal", "conference"]):
                research_score += 15.0
            if any(keyword in experience for keyword in ["research", "study", "investigation"]):
                research_score += 10.0
            if any(keyword in experience for keyword in ["thesis", "dissertation", "capstone"]):
                research_score += 8.0
        
        # Academic honors score
        honors_score = 0.0
        if academic_honors:
            honors_score += 5.0  # Base score for having honors
        
        # Research interests score
        interests_score = 0.0
        if research_interests:
            interests = research_interests.lower()
            if len(interests) > 100:  # Detailed research interests
                interests_score += 5.0
            else:
                interests_score += 2.0
        
        total_score = min(20.0, research_score + honors_score + interests_score)
        
        # Generate feedback
        strengths = []
        weaknesses = []
        suggestions = []
        
        if research_score >= 10.0:
            strengths.append("Strong research background")
        else:
            weaknesses.append("Limited research experience")
            suggestions.append("Consider gaining research experience through internships or projects")
        
        if interests_score >= 3.0:
            strengths.append("Clear research interests")
        else:
            weaknesses.append("Unclear research direction")
            suggestions.append("Develop and articulate specific research interests")
        
        notes = f"Research: {research_score:.1f}, Honors: {honors_score:.1f}, Interests: {interests_score:.1f}"
        
        return {
            "score": total_score,
            "notes": notes,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions
        }
    
    def _evaluate_professional_experience(self, application_data: Dict[str, Any], algorithm: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate professional experience"""
        
        work_data = application_data.get("work_experience", {})
        
        years_experience = work_data.get("years_experience", 0)
        current_position = work_data.get("current_position", "")
        current_company = work_data.get("current_company", "")
        ai_ml_experience = work_data.get("ai_ml_experience", "")
        projects = work_data.get("projects", "")
        
        # Years of experience score
        experience_score = 0.0
        if years_experience >= 5:
            experience_score = 8.0
        elif years_experience >= 3:
            experience_score = 6.0
        elif years_experience >= 1:
            experience_score = 4.0
        else:
            experience_score = 1.0
        
        # AI/ML relevance score
        relevance_score = 0.0
        if ai_ml_experience:
            experience = ai_ml_experience.lower()
            if any(keyword in experience for keyword in ["machine learning", "ai", "artificial intelligence"]):
                relevance_score += 5.0
            if any(keyword in experience for keyword in ["data", "analytics", "algorithm"]):
                relevance_score += 3.0
        
        # Position relevance score
        position_score = 0.0
        if current_position:
            position = current_position.lower()
            if any(keyword in position for keyword in ["engineer", "developer", "scientist", "analyst"]):
                position_score += 2.0
        
        # Projects score
        project_score = 0.0
        if projects:
            project_score += 2.0  # Base score for having projects
        
        total_score = min(15.0, experience_score + relevance_score + position_score + project_score)
        
        # Generate feedback
        strengths = []
        weaknesses = []
        suggestions = []
        
        if experience_score >= 6.0:
            strengths.append("Significant work experience")
        else:
            weaknesses.append("Limited work experience")
            suggestions.append("Gain relevant work experience through internships or projects")
        
        if relevance_score >= 5.0:
            strengths.append("Relevant AI/ML work experience")
        else:
            weaknesses.append("Limited AI/ML work experience")
            suggestions.append("Seek opportunities to work with AI/ML technologies")
        
        notes = f"Experience: {experience_score:.1f}, Relevance: {relevance_score:.1f}, Position: {position_score:.1f}, Projects: {project_score:.1f}"
        
        return {
            "score": total_score,
            "notes": notes,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions
        }
    
    def _evaluate_personal_statement(self, application_data: Dict[str, Any], algorithm: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate personal statement quality using NLP"""
        
        personal_data = application_data.get("personal_statement", {})
        
        motivation = personal_data.get("motivation", "")
        career_goals = personal_data.get("career_goals", "")
        research_interests = personal_data.get("research_interests", "")
        contribution = personal_data.get("contribution", "")
        
        # Combine all text for analysis
        full_text = f"{motivation} {career_goals} {research_interests} {contribution}"
        
        # Motivation score (0-3 points)
        motivation_score = 0.0
        if len(motivation) >= 200:
            motivation_score += 1.0
        if any(keyword in motivation.lower() for keyword in ["passion", "interest", "excited", "motivated"]):
            motivation_score += 1.0
        if any(keyword in motivation.lower() for keyword in ["ai", "artificial intelligence", "machine learning"]):
            motivation_score += 1.0
        
        # Career goals score (0-3 points)
        goals_score = 0.0
        if len(career_goals) >= 150:
            goals_score += 1.0
        if any(keyword in career_goals.lower() for keyword in ["career", "future", "goal", "aspire"]):
            goals_score += 1.0
        if any(keyword in career_goals.lower() for keyword in ["research", "industry", "academia", "leadership"]):
            goals_score += 1.0
        
        # Research interests score (0-2 points)
        interests_score = 0.0
        if len(research_interests) >= 100:
            interests_score += 1.0
        if any(keyword in research_interests.lower() for keyword in ["research", "study", "investigate", "explore"]):
            interests_score += 1.0
        
        # Contribution score (0-2 points)
        contribution_score = 0.0
        if len(contribution) >= 150:
            contribution_score += 1.0
        if any(keyword in contribution.lower() for keyword in ["contribute", "bring", "offer", "add"]):
            contribution_score += 1.0
        
        total_score = min(10.0, motivation_score + goals_score + interests_score + contribution_score)
        
        # Generate feedback
        strengths = []
        weaknesses = []
        suggestions = []
        
        if motivation_score >= 2.0:
            strengths.append("Clear motivation for pursuing AI")
        else:
            weaknesses.append("Unclear motivation")
            suggestions.append("Articulate your specific reasons for pursuing AI")
        
        if goals_score >= 2.0:
            strengths.append("Well-defined career goals")
        else:
            weaknesses.append("Vague career goals")
            suggestions.append("Develop specific career objectives")
        
        if total_score >= 8.0:
            strengths.append("Excellent personal statement")
        elif total_score >= 6.0:
            strengths.append("Good personal statement")
        else:
            weaknesses.append("Personal statement needs improvement")
            suggestions.append("Revise personal statement for clarity and specificity")
        
        notes = f"Motivation: {motivation_score:.1f}, Goals: {goals_score:.1f}, Interests: {interests_score:.1f}, Contribution: {contribution_score:.1f}"
        
        return {
            "score": total_score,
            "notes": notes,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions
        }
    
    def _evaluate_diversity_contribution(self, application_data: Dict[str, Any], algorithm: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate diversity contribution"""
        
        personal_data = application_data.get("personal_info", {})
        personal_statement = application_data.get("personal_statement", {})
        
        # This is a simplified evaluation - in practice, this would be more sophisticated
        diversity_score = 0.0
        
        # Check for diverse background indicators
        full_text = str(personal_data) + str(personal_statement)
        text_lower = full_text.lower()
        
        # Diversity indicators
        diversity_keywords = [
            "international", "immigrant", "first generation", "underrepresented",
            "diverse", "multicultural", "global", "different perspective"
        ]
        
        for keyword in diversity_keywords:
            if keyword in text_lower:
                diversity_score += 1.0
        
        # Contribution to diversity
        contribution_keywords = [
            "bring unique perspective", "diverse experience", "different background",
            "cultural", "international experience", "multilingual"
        ]
        
        for keyword in contribution_keywords:
            if keyword in text_lower:
                diversity_score += 1.0
        
        total_score = min(5.0, diversity_score)
        
        # Generate feedback
        strengths = []
        weaknesses = []
        suggestions = []
        
        if total_score >= 3.0:
            strengths.append("Diverse background and perspective")
        else:
            suggestions.append("Consider highlighting unique experiences and perspectives")
        
        notes = f"Diversity indicators: {total_score:.1f}"
        
        return {
            "score": total_score,
            "notes": notes,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions
        }
    
    def _calculate_overall_score(self, criteria_scores: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        
        # Define weights for each criteria
        weights = {
            "CRIT_001": 0.25,  # Academic Excellence
            "CRIT_002": 0.25,  # Technical Competency
            "CRIT_003": 0.20,  # Research Potential
            "CRIT_004": 0.15,  # Professional Experience
            "CRIT_005": 0.10,  # Personal Statement Quality
            "CRIT_006": 0.05   # Diversity Contribution
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for criteria_id, score in criteria_scores.items():
            weight = weights.get(criteria_id, 0.0)
            weighted_sum += score * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _determine_recommendation(self, overall_score: float, criteria_scores: Dict[str, float]) -> str:
        """Determine admission recommendation based on scores"""
        
        # Check minimum requirements
        academic_score = criteria_scores.get("CRIT_001", 0.0)
        technical_score = criteria_scores.get("CRIT_002", 0.0)
        
        if academic_score < 12.0 or technical_score < 12.0:
            return "reject"
        elif overall_score >= 18.0:
            return "accept"
        elif overall_score >= 15.0:
            return "waitlist"
        else:
            return "reject"
    
    def _calculate_confidence_score(self, criteria_scores: Dict[str, float], application_data: Dict[str, Any]) -> float:
        """Calculate confidence score for evaluation"""
        
        # Base confidence on completeness and consistency
        completeness_score = 0.0
        
        # Check data completeness
        required_sections = ["personal_info", "academic_background", "work_experience", "technical_skills", "personal_statement"]
        for section in required_sections:
            if section in application_data and application_data[section]:
                completeness_score += 0.2
        
        # Check score consistency
        scores = list(criteria_scores.values())
        if scores:
            score_variance = sum((score - sum(scores)/len(scores))**2 for score in scores) / len(scores)
            consistency_score = max(0.0, 1.0 - score_variance / 100.0)
        else:
            consistency_score = 0.0
        
        confidence = (completeness_score + consistency_score) / 2.0
        return min(1.0, max(0.0, confidence))
    
    def _generate_evaluation_summary(self, evaluation_result: EvaluationResult) -> Dict[str, Any]:
        """Generate comprehensive evaluation summary"""
        
        return {
            "overall_assessment": f"Score: {evaluation_result.overall_score:.1f}/25.0, Recommendation: {evaluation_result.recommendation}",
            "top_strengths": evaluation_result.strengths[:3],
            "key_weaknesses": evaluation_result.weaknesses[:3],
            "improvement_areas": evaluation_result.improvement_suggestions[:3],
            "confidence_level": f"{evaluation_result.confidence_score:.1%}",
            "evaluation_time": f"{evaluation_result.evaluation_time_minutes:.1f} minutes"
        }
    
    def get_evaluation_report(self, evaluation_id: str) -> Dict[str, Any]:
        """Get detailed evaluation report"""
        
        evaluation_result = self.evaluation_results.get(evaluation_id)
        if not evaluation_result:
            return {"error": "Evaluation not found"}
        
        return {
            "evaluation_id": evaluation_id,
            "application_id": evaluation_result.application_id,
            "overall_score": evaluation_result.overall_score,
            "recommendation": evaluation_result.recommendation,
            "confidence_score": evaluation_result.confidence_score,
            "criteria_scores": evaluation_result.criteria_scores,
            "strengths": evaluation_result.strengths,
            "weaknesses": evaluation_result.weaknesses,
            "improvement_suggestions": evaluation_result.improvement_suggestions,
            "evaluation_notes": evaluation_result.evaluation_notes,
            "evaluated_at": evaluation_result.evaluated_at.isoformat(),
            "evaluation_time_minutes": evaluation_result.evaluation_time_minutes,
            "status": evaluation_result.status.value
        }
    
    def get_evaluation_statistics(self) -> Dict[str, Any]:
        """Get evaluation system statistics"""
        
        total_evaluations = len(self.evaluation_results)
        
        if total_evaluations == 0:
            return {"message": "No evaluations completed yet"}
        
        # Recommendation distribution
        recommendations = [eval_result.recommendation for eval_result in self.evaluation_results.values()]
        recommendation_counts = Counter(recommendations)
        
        # Score distribution
        scores = [eval_result.overall_score for eval_result in self.evaluation_results.values()]
        avg_score = sum(scores) / len(scores)
        
        # Confidence distribution
        confidences = [eval_result.confidence_score for eval_result in self.evaluation_results.values()]
        avg_confidence = sum(confidences) / len(confidences)
        
        # Evaluation time statistics
        times = [eval_result.evaluation_time_minutes for eval_result in self.evaluation_results.values()]
        avg_time = sum(times) / len(times)
        
        return {
            "total_evaluations": total_evaluations,
            "recommendation_distribution": dict(recommendation_counts),
            "score_statistics": {
                "average_score": avg_score,
                "min_score": min(scores),
                "max_score": max(scores)
            },
            "confidence_statistics": {
                "average_confidence": avg_confidence,
                "min_confidence": min(confidences),
                "max_confidence": max(confidences)
            },
            "performance_metrics": {
                "average_evaluation_time_minutes": avg_time,
                "total_evaluation_time_hours": sum(times) / 60
            },
            "model_performance": [
                {
                    "model_name": model.name,
                    "accuracy_score": model.accuracy_score,
                    "last_trained": model.last_trained.isoformat()
                }
                for model in self.evaluation_models
            ]
        }