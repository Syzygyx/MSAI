"""
MS AI Curriculum System - Thesis Evaluation System
Comprehensive thesis evaluation and grading system
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import random

class EvaluationCriteria(Enum):
    RESEARCH_CONTRIBUTION = "research_contribution"
    METHODOLOGY = "methodology"
    TECHNICAL_QUALITY = "technical_quality"
    PRESENTATION = "presentation"
    DEFENSE_PERFORMANCE = "defense_performance"
    LITERATURE_REVIEW = "literature_review"
    INNOVATION = "innovation"
    PRACTICAL_APPLICATION = "practical_application"

class EvaluationWeight(Enum):
    LOW = 0.1
    MEDIUM = 0.2
    HIGH = 0.3
    CRITICAL = 0.4

class GradeLevel(Enum):
    A_PLUS = "A+"
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D = "D"
    F = "F"

@dataclass
class EvaluationRubric:
    """Evaluation rubric structure"""
    rubric_id: str
    research_area: str
    criteria: Dict[EvaluationCriteria, Dict[str, Any]]
    total_weight: float
    grade_thresholds: Dict[GradeLevel, float]
    created_at: datetime

@dataclass
class EvaluationResult:
    """Individual evaluation result"""
    evaluation_id: str
    evaluator_id: str
    evaluator_role: str
    thesis_id: str
    criteria_scores: Dict[EvaluationCriteria, float]
    overall_score: float
    grade: GradeLevel
    detailed_feedback: Dict[str, str]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    evaluation_date: datetime
    evaluation_time_minutes: float

@dataclass
class ThesisEvaluation:
    """Complete thesis evaluation"""
    evaluation_id: str
    thesis_id: str
    student_id: str
    committee_id: str
    evaluation_results: List[EvaluationResult]
    final_grade: GradeLevel
    final_score: float
    consensus_reached: bool
    evaluation_summary: str
    completed_at: datetime
    evaluation_rubric: EvaluationRubric

class ThesisEvaluationSystem:
    """Comprehensive thesis evaluation and grading system"""
    
    def __init__(self, committee_system=None, professor_system=None):
        self.committee_system = committee_system
        self.professor_system = professor_system
        
        # Evaluation data
        self.thesis_evaluations: Dict[str, ThesisEvaluation] = {}
        self.evaluation_rubrics: Dict[str, EvaluationRubric] = {}
        
        # Initialize evaluation rubrics
        self._initialize_evaluation_rubrics()
        
    def _initialize_evaluation_rubrics(self):
        """Initialize evaluation rubrics for different research areas"""
        
        # Machine Learning Rubric
        ml_rubric = EvaluationRubric(
            rubric_id="ML_RUBRIC_001",
            research_area="machine_learning",
            criteria={
                EvaluationCriteria.RESEARCH_CONTRIBUTION: {
                    "weight": 0.25,
                    "description": "Originality and contribution to machine learning field",
                    "evaluation_points": [
                        "Novel algorithm or approach",
                        "Significant improvement over existing methods",
                        "Theoretical contribution",
                        "Practical impact"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.METHODOLOGY: {
                    "weight": 0.20,
                    "description": "Research methodology and experimental design",
                    "evaluation_points": [
                        "Appropriate methodology selection",
                        "Rigorous experimental design",
                        "Proper evaluation metrics",
                        "Statistical significance"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.TECHNICAL_QUALITY: {
                    "weight": 0.20,
                    "description": "Technical implementation and code quality",
                    "evaluation_points": [
                        "Code quality and documentation",
                        "Algorithm implementation",
                        "System performance",
                        "Reproducibility"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.PRESENTATION: {
                    "weight": 0.15,
                    "description": "Thesis presentation and communication",
                    "evaluation_points": [
                        "Clear writing and organization",
                        "Effective visualizations",
                        "Proper citations",
                        "Professional presentation"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.DEFENSE_PERFORMANCE: {
                    "weight": 0.10,
                    "description": "Thesis defense performance",
                    "evaluation_points": [
                        "Understanding of research",
                        "Ability to answer questions",
                        "Defense of methodology",
                        "Future work discussion"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.LITERATURE_REVIEW: {
                    "weight": 0.10,
                    "description": "Literature review quality",
                    "evaluation_points": [
                        "Comprehensive coverage",
                        "Critical analysis",
                        "Proper citations",
                        "Identification of gaps"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                }
            },
            total_weight=1.0,
            grade_thresholds={
                GradeLevel.A_PLUS: 4.8,
                GradeLevel.A: 4.5,
                GradeLevel.A_MINUS: 4.2,
                GradeLevel.B_PLUS: 3.8,
                GradeLevel.B: 3.5,
                GradeLevel.B_MINUS: 3.2,
                GradeLevel.C_PLUS: 2.8,
                GradeLevel.C: 2.5,
                GradeLevel.C_MINUS: 2.2,
                GradeLevel.D: 2.0,
                GradeLevel.F: 1.0
            },
            created_at=datetime.now()
        )
        
        # Computer Vision Rubric
        cv_rubric = EvaluationRubric(
            rubric_id="CV_RUBRIC_001",
            research_area="computer_vision",
            criteria={
                EvaluationCriteria.RESEARCH_CONTRIBUTION: {
                    "weight": 0.25,
                    "description": "Originality and contribution to computer vision field",
                    "evaluation_points": [
                        "Novel vision algorithm or approach",
                        "Improvement in accuracy or efficiency",
                        "New application domain",
                        "Theoretical contribution"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.METHODOLOGY: {
                    "weight": 0.20,
                    "description": "Research methodology and experimental design",
                    "evaluation_points": [
                        "Appropriate dataset selection",
                        "Proper evaluation metrics",
                        "Baseline comparisons",
                        "Statistical validation"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.TECHNICAL_QUALITY: {
                    "weight": 0.20,
                    "description": "Technical implementation and system quality",
                    "evaluation_points": [
                        "Algorithm implementation",
                        "System performance",
                        "Code quality",
                        "Reproducibility"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.PRESENTATION: {
                    "weight": 0.15,
                    "description": "Thesis presentation and communication",
                    "evaluation_points": [
                        "Clear visualizations",
                        "Effective presentation of results",
                        "Proper citations",
                        "Professional writing"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.DEFENSE_PERFORMANCE: {
                    "weight": 0.10,
                    "description": "Thesis defense performance",
                    "evaluation_points": [
                        "Understanding of vision concepts",
                        "Ability to explain technical details",
                        "Defense of approach",
                        "Future work discussion"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.LITERATURE_REVIEW: {
                    "weight": 0.10,
                    "description": "Literature review quality",
                    "evaluation_points": [
                        "Comprehensive coverage of vision literature",
                        "Critical analysis of approaches",
                        "Proper citations",
                        "Identification of research gaps"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                }
            },
            total_weight=1.0,
            grade_thresholds={
                GradeLevel.A_PLUS: 4.8,
                GradeLevel.A: 4.5,
                GradeLevel.A_MINUS: 4.2,
                GradeLevel.B_PLUS: 3.8,
                GradeLevel.B: 3.5,
                GradeLevel.B_MINUS: 3.2,
                GradeLevel.C_PLUS: 2.8,
                GradeLevel.C: 2.5,
                GradeLevel.C_MINUS: 2.2,
                GradeLevel.D: 2.0,
                GradeLevel.F: 1.0
            },
            created_at=datetime.now()
        )
        
        # AI Ethics Rubric
        ethics_rubric = EvaluationRubric(
            rubric_id="ETHICS_RUBRIC_001",
            research_area="ai_ethics",
            criteria={
                EvaluationCriteria.RESEARCH_CONTRIBUTION: {
                    "weight": 0.20,
                    "description": "Originality and contribution to AI ethics field",
                    "evaluation_points": [
                        "Novel ethical framework or approach",
                        "Significant ethical insight",
                        "Practical ethical guidelines",
                        "Social impact contribution"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.METHODOLOGY: {
                    "weight": 0.20,
                    "description": "Research methodology and approach",
                    "evaluation_points": [
                        "Appropriate ethical methodology",
                        "Case study analysis",
                        "Stakeholder consideration",
                        "Ethical framework application"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.TECHNICAL_QUALITY: {
                    "weight": 0.15,
                    "description": "Technical implementation and analysis",
                    "evaluation_points": [
                        "Ethical analysis quality",
                        "Framework implementation",
                        "Case study depth",
                        "Analysis rigor"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.PRESENTATION: {
                    "weight": 0.15,
                    "description": "Thesis presentation and communication",
                    "evaluation_points": [
                        "Clear ethical argumentation",
                        "Effective case study presentation",
                        "Proper citations",
                        "Professional writing"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.DEFENSE_PERFORMANCE: {
                    "weight": 0.10,
                    "description": "Thesis defense performance",
                    "evaluation_points": [
                        "Understanding of ethical concepts",
                        "Ability to defend ethical positions",
                        "Response to ethical challenges",
                        "Future ethical considerations"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.LITERATURE_REVIEW: {
                    "weight": 0.10,
                    "description": "Literature review quality",
                    "evaluation_points": [
                        "Comprehensive ethical literature coverage",
                        "Critical analysis of ethical frameworks",
                        "Proper citations",
                        "Identification of ethical gaps"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                },
                EvaluationCriteria.ETHICAL_CONSIDERATIONS: {
                    "weight": 0.10,
                    "description": "Ethical considerations and implications",
                    "evaluation_points": [
                        "Bias and fairness analysis",
                        "Privacy considerations",
                        "Transparency and accountability",
                        "Social impact assessment"
                    ],
                    "scoring_scale": {
                        "excellent": 5.0,
                        "good": 4.0,
                        "satisfactory": 3.0,
                        "needs_improvement": 2.0,
                        "unsatisfactory": 1.0
                    }
                }
            },
            total_weight=1.0,
            grade_thresholds={
                GradeLevel.A_PLUS: 4.8,
                GradeLevel.A: 4.5,
                GradeLevel.A_MINUS: 4.2,
                GradeLevel.B_PLUS: 3.8,
                GradeLevel.B: 3.5,
                GradeLevel.B_MINUS: 3.2,
                GradeLevel.C_PLUS: 2.8,
                GradeLevel.C: 2.5,
                GradeLevel.C_MINUS: 2.2,
                GradeLevel.D: 2.0,
                GradeLevel.F: 1.0
            },
            created_at=datetime.now()
        )
        
        # Store rubrics
        self.evaluation_rubrics["machine_learning"] = ml_rubric
        self.evaluation_rubrics["computer_vision"] = cv_rubric
        self.evaluation_rubrics["ai_ethics"] = ethics_rubric
    
    def evaluate_thesis(self, thesis_id: str, student_id: str, committee_id: str, 
                      research_area: str, thesis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate thesis using appropriate rubric"""
        
        # Check if evaluation already exists
        existing_evaluations = [e for e in self.thesis_evaluations.values() if e.thesis_id == thesis_id]
        if existing_evaluations:
            return {
                "success": False,
                "error": "Evaluation already exists for this thesis",
                "evaluation_id": existing_evaluations[0].evaluation_id
            }
        
        # Get appropriate rubric
        rubric = self.evaluation_rubrics.get(research_area, self.evaluation_rubrics["machine_learning"])
        
        # Create evaluation
        evaluation_id = f"EVAL_{uuid.uuid4().hex[:8]}"
        
        # Get committee members
        committee_members = []
        if self.committee_system:
            committee = self.committee_system.thesis_committees.get(committee_id)
            if committee:
                committee_members = committee.committee_members
        
        # Generate individual evaluations
        evaluation_results = []
        for member in committee_members:
            result = self._generate_individual_evaluation(
                evaluation_id, member, thesis_id, rubric, thesis_data
            )
            evaluation_results.append(result)
        
        # Calculate final grade
        final_grade, final_score, consensus_reached = self._calculate_final_grade(
            evaluation_results, rubric
        )
        
        # Create evaluation summary
        evaluation_summary = self._generate_evaluation_summary(
            evaluation_results, final_grade, final_score
        )
        
        # Create thesis evaluation
        thesis_evaluation = ThesisEvaluation(
            evaluation_id=evaluation_id,
            thesis_id=thesis_id,
            student_id=student_id,
            committee_id=committee_id,
            evaluation_results=evaluation_results,
            final_grade=final_grade,
            final_score=final_score,
            consensus_reached=consensus_reached,
            evaluation_summary=evaluation_summary,
            completed_at=datetime.now(),
            evaluation_rubric=rubric
        )
        
        self.thesis_evaluations[evaluation_id] = thesis_evaluation
        
        return {
            "success": True,
            "evaluation_id": evaluation_id,
            "thesis_id": thesis_id,
            "student_id": student_id,
            "committee_id": committee_id,
            "final_grade": final_grade.value,
            "final_score": final_score,
            "consensus_reached": consensus_reached,
            "evaluation_summary": evaluation_summary,
            "individual_evaluations": [
                {
                    "evaluator_id": result.evaluator_id,
                    "evaluator_role": result.evaluator_role,
                    "overall_score": result.overall_score,
                    "grade": result.grade.value,
                    "strengths": result.strengths,
                    "weaknesses": result.weaknesses,
                    "recommendations": result.recommendations
                }
                for result in evaluation_results
            ],
            "completed_at": thesis_evaluation.completed_at.isoformat()
        }
    
    def _generate_individual_evaluation(self, evaluation_id: str, member: Any, 
                                      thesis_id: str, rubric: EvaluationRubric, 
                                      thesis_data: Dict[str, Any]) -> EvaluationResult:
        """Generate individual evaluation from committee member"""
        
        evaluator_id = f"EVAL_{uuid.uuid4().hex[:8]}"
        start_time = datetime.now()
        
        # Generate scores for each criteria
        criteria_scores = {}
        detailed_feedback = {}
        strengths = []
        weaknesses = []
        recommendations = []
        
        for criteria, criteria_info in rubric.criteria.items():
            # Generate score based on criteria
            score = self._generate_criteria_score(criteria, criteria_info, thesis_data)
            criteria_scores[criteria] = score
            
            # Generate feedback
            feedback = self._generate_criteria_feedback(criteria, score, criteria_info)
            detailed_feedback[criteria.value] = feedback
            
            # Collect strengths and weaknesses
            if score >= 4.0:
                strengths.append(f"Strong performance in {criteria.value}")
            elif score <= 2.0:
                weaknesses.append(f"Needs improvement in {criteria.value}")
            
            # Generate recommendations
            if score < 3.0:
                recommendations.append(f"Improve {criteria.value} implementation")
        
        # Calculate overall score
        overall_score = sum(
            score * criteria_info["weight"]
            for criteria, score in criteria_scores.items()
            for criteria_info in [rubric.criteria[criteria]]
        )
        
        # Determine grade
        grade = self._determine_grade(overall_score, rubric.grade_thresholds)
        
        # Calculate evaluation time
        evaluation_time = (datetime.now() - start_time).total_seconds() / 60
        
        return EvaluationResult(
            evaluation_id=evaluator_id,
            evaluator_id=member.member_id,
            evaluator_role=member.role.value,
            thesis_id=thesis_id,
            criteria_scores=criteria_scores,
            overall_score=overall_score,
            grade=grade,
            detailed_feedback=detailed_feedback,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            evaluation_date=datetime.now(),
            evaluation_time_minutes=evaluation_time
        )
    
    def _generate_criteria_score(self, criteria: EvaluationCriteria, 
                               criteria_info: Dict[str, Any], 
                               thesis_data: Dict[str, Any]) -> float:
        """Generate score for specific criteria"""
        
        # Base score generation (would be more sophisticated in real implementation)
        base_score = random.uniform(3.0, 5.0)
        
        # Adjust based on thesis data
        if criteria == EvaluationCriteria.RESEARCH_CONTRIBUTION:
            if "novel_approach" in thesis_data.get("methodology", "").lower():
                base_score += 0.5
            if "significant_improvement" in thesis_data.get("results", "").lower():
                base_score += 0.3
        
        elif criteria == EvaluationCriteria.METHODOLOGY:
            if "rigorous_experiments" in thesis_data.get("methodology", "").lower():
                base_score += 0.4
            if "proper_evaluation" in thesis_data.get("methodology", "").lower():
                base_score += 0.3
        
        elif criteria == EvaluationCriteria.TECHNICAL_QUALITY:
            if "high_quality_code" in thesis_data.get("implementation", "").lower():
                base_score += 0.4
            if "good_documentation" in thesis_data.get("implementation", "").lower():
                base_score += 0.3
        
        elif criteria == EvaluationCriteria.PRESENTATION:
            if "clear_writing" in thesis_data.get("presentation", "").lower():
                base_score += 0.3
            if "effective_visualizations" in thesis_data.get("presentation", "").lower():
                base_score += 0.4
        
        elif criteria == EvaluationCriteria.DEFENSE_PERFORMANCE:
            if "strong_defense" in thesis_data.get("defense", "").lower():
                base_score += 0.5
            if "good_answers" in thesis_data.get("defense", "").lower():
                base_score += 0.3
        
        elif criteria == EvaluationCriteria.LITERATURE_REVIEW:
            if "comprehensive_review" in thesis_data.get("literature", "").lower():
                base_score += 0.4
            if "critical_analysis" in thesis_data.get("literature", "").lower():
                base_score += 0.3
        
        # Ensure score is within valid range
        return max(1.0, min(5.0, base_score))
    
    def _generate_criteria_feedback(self, criteria: EvaluationCriteria, score: float, 
                                  criteria_info: Dict[str, Any]) -> str:
        """Generate feedback for specific criteria"""
        
        if score >= 4.5:
            return f"Excellent performance in {criteria.value}. {criteria_info['description']} demonstrates outstanding quality."
        elif score >= 4.0:
            return f"Good performance in {criteria.value}. {criteria_info['description']} shows solid quality with minor areas for improvement."
        elif score >= 3.0:
            return f"Satisfactory performance in {criteria.value}. {criteria_info['description']} meets basic requirements."
        elif score >= 2.0:
            return f"Needs improvement in {criteria.value}. {criteria_info['description']} requires significant enhancement."
        else:
            return f"Unsatisfactory performance in {criteria.value}. {criteria_info['description']} does not meet minimum standards."
    
    def _determine_grade(self, score: float, grade_thresholds: Dict[GradeLevel, float]) -> GradeLevel:
        """Determine grade based on score and thresholds"""
        
        for grade, threshold in sorted(grade_thresholds.items(), key=lambda x: x[1], reverse=True):
            if score >= threshold:
                return grade
        
        return GradeLevel.F
    
    def _calculate_final_grade(self, evaluation_results: List[EvaluationResult], 
                             rubric: EvaluationRubric) -> tuple[GradeLevel, float, bool]:
        """Calculate final grade from individual evaluations"""
        
        if not evaluation_results:
            return GradeLevel.F, 0.0, False
        
        # Calculate weighted average score
        total_score = 0.0
        total_weight = 0.0
        
        for result in evaluation_results:
            # Weight by evaluator role
            weight = self._get_evaluator_weight(result.evaluator_role)
            total_score += result.overall_score * weight
            total_weight += weight
        
        final_score = total_score / total_weight if total_weight > 0 else 0.0
        
        # Determine final grade
        final_grade = self._determine_grade(final_score, rubric.grade_thresholds)
        
        # Check for consensus
        consensus_reached = self._check_consensus(evaluation_results, final_grade)
        
        return final_grade, final_score, consensus_reached
    
    def _get_evaluator_weight(self, evaluator_role: str) -> float:
        """Get weight for evaluator based on role"""
        
        role_weights = {
            "chair": 1.5,
            "member": 1.0,
            "external_examiner": 1.2,
            "graduate_coordinator": 1.0
        }
        
        return role_weights.get(evaluator_role.lower(), 1.0)
    
    def _check_consensus(self, evaluation_results: List[EvaluationResult], 
                        final_grade: GradeLevel) -> bool:
        """Check if there's consensus among evaluators"""
        
        if len(evaluation_results) < 2:
            return True
        
        # Check if all grades are within one level
        grades = [result.grade for result in evaluation_results]
        grade_values = [self._get_grade_value(grade) for grade in grades]
        
        min_grade = min(grade_values)
        max_grade = max(grade_values)
        
        # Consensus if all grades are within one level
        return (max_grade - min_grade) <= 1
    
    def _get_grade_value(self, grade: GradeLevel) -> int:
        """Get numeric value for grade"""
        
        grade_values = {
            GradeLevel.A_PLUS: 12,
            GradeLevel.A: 11,
            GradeLevel.A_MINUS: 10,
            GradeLevel.B_PLUS: 9,
            GradeLevel.B: 8,
            GradeLevel.B_MINUS: 7,
            GradeLevel.C_PLUS: 6,
            GradeLevel.C: 5,
            GradeLevel.C_MINUS: 4,
            GradeLevel.D: 3,
            GradeLevel.F: 2
        }
        
        return grade_values.get(grade, 2)
    
    def _generate_evaluation_summary(self, evaluation_results: List[EvaluationResult], 
                                    final_grade: GradeLevel, final_score: float) -> str:
        """Generate evaluation summary"""
        
        summary = f"Thesis Evaluation Summary\n\n"
        summary += f"Final Grade: {final_grade.value}\n"
        summary += f"Final Score: {final_score:.2f}/5.0\n\n"
        
        # Collect common strengths and weaknesses
        all_strengths = []
        all_weaknesses = []
        all_recommendations = []
        
        for result in evaluation_results:
            all_strengths.extend(result.strengths)
            all_weaknesses.extend(result.weaknesses)
            all_recommendations.extend(result.recommendations)
        
        # Summary of strengths
        if all_strengths:
            summary += "Key Strengths:\n"
            strength_counts = {}
            for strength in all_strengths:
                strength_counts[strength] = strength_counts.get(strength, 0) + 1
            
            for strength, count in sorted(strength_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
                summary += f"- {strength} (mentioned by {count} evaluators)\n"
            summary += "\n"
        
        # Summary of weaknesses
        if all_weaknesses:
            summary += "Areas for Improvement:\n"
            weakness_counts = {}
            for weakness in all_weaknesses:
                weakness_counts[weakness] = weakness_counts.get(weakness, 0) + 1
            
            for weakness, count in sorted(weakness_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
                summary += f"- {weakness} (mentioned by {count} evaluators)\n"
            summary += "\n"
        
        # Summary of recommendations
        if all_recommendations:
            summary += "Recommendations:\n"
            recommendation_counts = {}
            for rec in all_recommendations:
                recommendation_counts[rec] = recommendation_counts.get(rec, 0) + 1
            
            for rec, count in sorted(recommendation_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
                summary += f"- {rec} (mentioned by {count} evaluators)\n"
        
        return summary
    
    def get_evaluation_report(self, evaluation_id: str) -> Dict[str, Any]:
        """Get detailed evaluation report"""
        
        evaluation = self.thesis_evaluations.get(evaluation_id)
        if not evaluation:
            return {"error": "Evaluation not found"}
        
        return {
            "evaluation_id": evaluation_id,
            "thesis_id": evaluation.thesis_id,
            "student_id": evaluation.student_id,
            "committee_id": evaluation.committee_id,
            "final_grade": evaluation.final_grade.value,
            "final_score": evaluation.final_score,
            "consensus_reached": evaluation.consensus_reached,
            "evaluation_summary": evaluation.evaluation_summary,
            "completed_at": evaluation.completed_at.isoformat(),
            "rubric_used": {
                "rubric_id": evaluation.evaluation_rubric.rubric_id,
                "research_area": evaluation.evaluation_rubric.research_area,
                "criteria": {
                    criteria.value: {
                        "weight": criteria_info["weight"],
                        "description": criteria_info["description"]
                    }
                    for criteria, criteria_info in evaluation.evaluation_rubric.criteria.items()
                }
            },
            "individual_evaluations": [
                {
                    "evaluator_id": result.evaluator_id,
                    "evaluator_role": result.evaluator_role,
                    "overall_score": result.overall_score,
                    "grade": result.grade.value,
                    "criteria_scores": {
                        criteria.value: score
                        for criteria, score in result.criteria_scores.items()
                    },
                    "detailed_feedback": result.detailed_feedback,
                    "strengths": result.strengths,
                    "weaknesses": result.weaknesses,
                    "recommendations": result.recommendations,
                    "evaluation_date": result.evaluation_date.isoformat(),
                    "evaluation_time_minutes": result.evaluation_time_minutes
                }
                for result in evaluation.evaluation_results
            ]
        }
    
    def get_evaluation_analytics(self) -> Dict[str, Any]:
        """Get evaluation system analytics"""
        
        total_evaluations = len(self.thesis_evaluations)
        
        if total_evaluations == 0:
            return {"message": "No evaluations completed yet"}
        
        # Grade distribution
        grade_counts = {}
        for grade in GradeLevel:
            grade_counts[grade.value] = len([e for e in self.thesis_evaluations.values() if e.final_grade == grade])
        
        # Score statistics
        scores = [e.final_score for e in self.thesis_evaluations.values()]
        avg_score = sum(scores) / len(scores) if scores else 0
        min_score = min(scores) if scores else 0
        max_score = max(scores) if scores else 0
        
        # Consensus statistics
        consensus_count = len([e for e in self.thesis_evaluations.values() if e.consensus_reached])
        consensus_rate = (consensus_count / total_evaluations * 100) if total_evaluations > 0 else 0
        
        # Evaluation time statistics
        evaluation_times = []
        for evaluation in self.thesis_evaluations.values():
            evaluation_times.extend([result.evaluation_time_minutes for result in evaluation.evaluation_results])
        
        avg_evaluation_time = sum(evaluation_times) / len(evaluation_times) if evaluation_times else 0
        
        # Criteria performance
        criteria_performance = {}
        for criteria in EvaluationCriteria:
            criteria_scores = []
            for evaluation in self.thesis_evaluations.values():
                for result in evaluation.evaluation_results:
                    if criteria in result.criteria_scores:
                        criteria_scores.append(result.criteria_scores[criteria])
            
            if criteria_scores:
                criteria_performance[criteria.value] = {
                    "average_score": sum(criteria_scores) / len(criteria_scores),
                    "min_score": min(criteria_scores),
                    "max_score": max(criteria_scores)
                }
        
        return {
            "total_evaluations": total_evaluations,
            "grade_distribution": grade_counts,
            "score_statistics": {
                "average_score": avg_score,
                "minimum_score": min_score,
                "maximum_score": max_score,
                "score_range": max_score - min_score
            },
            "consensus_statistics": {
                "consensus_reached": consensus_count,
                "consensus_rate_percentage": consensus_rate,
                "disagreements": total_evaluations - consensus_count
            },
            "evaluation_time_statistics": {
                "average_evaluation_time_minutes": avg_evaluation_time,
                "total_evaluation_time_hours": sum(evaluation_times) / 60 if evaluation_times else 0
            },
            "criteria_performance": criteria_performance,
            "rubric_usage": {
                "total_rubrics": len(self.evaluation_rubrics),
                "rubric_areas": list(self.evaluation_rubrics.keys())
            }
        }