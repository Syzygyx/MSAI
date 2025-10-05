"""
MS AI Curriculum System - Course Content Generator
Comprehensive content generation for lectures, quizzes, exams, tutorials, and reading materials
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import random

class ContentType(Enum):
    LECTURE = "lecture"
    QUIZ = "quiz"
    MIDTERM = "midterm"
    FINAL = "final"
    TUTORIAL = "tutorial"
    READING_MATERIAL = "reading_material"
    ASSIGNMENT = "assignment"
    PROJECT = "project"
    DEMONSTRATION = "demonstration"

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    CODING = "coding"
    PRACTICAL = "practical"

@dataclass
class LearningObjective:
    """Learning objective for course content"""
    objective_id: str
    description: str
    bloom_taxonomy_level: str  # remember, understand, apply, analyze, evaluate, create
    assessment_methods: List[str]
    prerequisites: List[str] = field(default_factory=list)

@dataclass
class Lecture:
    """Lecture content structure"""
    lecture_id: str
    title: str
    course_id: str
    week_number: int
    duration_minutes: int
    learning_objectives: List[LearningObjective]
    outline: List[str]
    content_sections: List[Dict[str, Any]]
    key_concepts: List[str]
    examples: List[Dict[str, Any]]
    professor_id: str
    created_at: datetime
    slides_count: int = 0
    video_duration: int = 0
    reading_time_minutes: int = 0

@dataclass
class Quiz:
    """Quiz structure"""
    quiz_id: str
    title: str
    course_id: str
    lecture_id: Optional[str]
    questions: List[Dict[str, Any]]
    time_limit_minutes: int
    difficulty: DifficultyLevel
    total_points: int
    passing_score: int
    professor_id: str
    created_at: datetime
    attempts_allowed: int = 3

@dataclass
class Exam:
    """Exam structure (midterm/final)"""
    exam_id: str
    title: str
    course_id: str
    exam_type: str  # midterm or final
    questions: List[Dict[str, Any]]
    time_limit_minutes: int
    difficulty: DifficultyLevel
    total_points: int
    passing_score: int
    professor_id: str
    created_at: datetime
    proctoring_required: bool = False

@dataclass
class Tutorial:
    """Tutorial content"""
    tutorial_id: str
    title: str
    course_id: str
    topic: str
    difficulty: DifficultyLevel
    estimated_time_minutes: int
    prerequisites: List[str]
    learning_objectives: List[str]
    step_by_step_instructions: List[Dict[str, Any]]
    code_examples: List[Dict[str, Any]]
    expected_outcomes: List[str]
    professor_id: str
    created_at: datetime

@dataclass
class ReadingMaterial:
    """Reading material structure"""
    reading_id: str
    title: str
    course_id: str
    material_type: str  # textbook, paper, article, blog_post
    author: str
    url: Optional[str]
    content: str
    reading_time_minutes: int
    difficulty: DifficultyLevel
    key_takeaways: List[str]
    discussion_questions: List[str]
    professor_id: str
    created_at: datetime

class CourseContentGenerator:
    """Comprehensive course content generation system"""
    
    def __init__(self, professor_system=None, curriculum_system=None):
        self.professor_system = professor_system
        self.curriculum_system = curriculum_system
        self.lectures: Dict[str, Lecture] = {}
        self.quizzes: Dict[str, Quiz] = {}
        self.exams: Dict[str, Exam] = {}
        self.tutorials: Dict[str, Tutorial] = {}
        self.reading_materials: Dict[str, ReadingMaterial] = {}
        
        # Course content templates
        self.course_templates = self._initialize_course_templates()
        
    def _initialize_course_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize content templates for each course"""
        return {
            "AI501": {
                "title": "Introduction to Artificial Intelligence",
                "weeks": 16,
                "topics": [
                    "AI History and Foundations",
                    "Problem Solving and Search",
                    "Knowledge Representation",
                    "Machine Learning Basics",
                    "Neural Networks Introduction",
                    "Expert Systems",
                    "AI Ethics and Society",
                    "Future of AI"
                ],
                "learning_objectives": [
                    "Understand fundamental AI concepts and history",
                    "Apply search algorithms to solve problems",
                    "Design knowledge representation systems",
                    "Implement basic machine learning algorithms",
                    "Analyze ethical implications of AI systems"
                ],
                "assessment_types": ["lectures", "quizzes", "assignments", "midterm", "final", "project"]
            },
            "AI502": {
                "title": "Machine Learning Fundamentals",
                "weeks": 16,
                "topics": [
                    "Supervised Learning",
                    "Unsupervised Learning",
                    "Model Evaluation",
                    "Feature Engineering",
                    "Ensemble Methods",
                    "Deep Learning Basics",
                    "ML in Practice",
                    "Advanced Topics"
                ],
                "learning_objectives": [
                    "Master supervised and unsupervised learning algorithms",
                    "Evaluate model performance using appropriate metrics",
                    "Engineer features for machine learning models",
                    "Implement ensemble learning methods",
                    "Apply deep learning techniques to real problems"
                ],
                "assessment_types": ["lectures", "quizzes", "assignments", "midterm", "final", "project"]
            },
            "AI503": {
                "title": "AI Ethics and Responsible Development",
                "weeks": 16,
                "topics": [
                    "Ethical Frameworks",
                    "Bias and Fairness",
                    "Transparency and Explainability",
                    "Privacy and Security",
                    "AI Governance",
                    "Responsible AI Development",
                    "Case Studies",
                    "Future Challenges"
                ],
                "learning_objectives": [
                    "Analyze ethical implications of AI systems",
                    "Identify and mitigate bias in AI models",
                    "Design transparent and explainable AI systems",
                    "Develop responsible AI development practices",
                    "Evaluate AI governance frameworks"
                ],
                "assessment_types": ["lectures", "quizzes", "assignments", "midterm", "final", "project"]
            }
        }
    
    def generate_course_content(self, course_id: str) -> Dict[str, Any]:
        """Generate complete content for a course"""
        if course_id not in self.course_templates:
            return {"success": False, "error": f"No template found for course {course_id}"}
        
        course_template = self.course_templates[course_id]
        
        # Generate all content types
        content_results = {
            "lectures": self._generate_lectures(course_id, course_template),
            "quizzes": self._generate_quizzes(course_id, course_template),
            "exams": self._generate_exams(course_id, course_template),
            "tutorials": self._generate_tutorials(course_id, course_template),
            "reading_materials": self._generate_reading_materials(course_id, course_template)
        }
        
        return {
            "success": True,
            "course_id": course_id,
            "content_summary": {
                "lectures_created": len(content_results["lectures"]),
                "quizzes_created": len(content_results["quizzes"]),
                "exams_created": len(content_results["exams"]),
                "tutorials_created": len(content_results["tutorials"]),
                "reading_materials_created": len(content_results["reading_materials"])
            },
            "content_details": content_results
        }
    
    def _generate_lectures(self, course_id: str, course_template: Dict[str, Any]) -> List[str]:
        """Generate lectures for a course"""
        lecture_ids = []
        topics = course_template["topics"]
        weeks = course_template["weeks"]
        
        # Assign professor based on course
        professor_id = self._get_professor_for_course(course_id)
        
        for week in range(1, weeks + 1):
            topic_index = (week - 1) % len(topics)
            topic = topics[topic_index]
            
            lecture_id = f"LECTURE_{course_id}_{week:02d}"
            
            lecture = Lecture(
                lecture_id=lecture_id,
                title=f"Week {week}: {topic}",
                course_id=course_id,
                week_number=week,
                duration_minutes=90,  # 1.5 hours
                learning_objectives=self._generate_learning_objectives(topic, week),
                outline=self._generate_lecture_outline(topic, week),
                content_sections=self._generate_lecture_content(topic, week),
                key_concepts=self._generate_key_concepts(topic),
                examples=self._generate_examples(topic, week),
                professor_id=professor_id,
                created_at=datetime.now(),
                slides_count=random.randint(25, 40),
                video_duration=90,
                reading_time_minutes=30
            )
            
            self.lectures[lecture_id] = lecture
            lecture_ids.append(lecture_id)
        
        return lecture_ids
    
    def _generate_quizzes(self, course_id: str, course_template: Dict[str, Any]) -> List[str]:
        """Generate quizzes for a course"""
        quiz_ids = []
        weeks = course_template["weeks"]
        professor_id = self._get_professor_for_course(course_id)
        
        # Generate weekly quizzes
        for week in range(1, weeks + 1):
            quiz_id = f"QUIZ_{course_id}_{week:02d}"
            
            quiz = Quiz(
                quiz_id=quiz_id,
                title=f"Week {week} Quiz",
                course_id=course_id,
                lecture_id=f"LECTURE_{course_id}_{week:02d}",
                questions=self._generate_quiz_questions(course_id, week),
                time_limit_minutes=30,
                difficulty=DifficultyLevel.INTERMEDIATE,
                total_points=100,
                passing_score=70,
                professor_id=professor_id,
                created_at=datetime.now(),
                attempts_allowed=3
            )
            
            self.quizzes[quiz_id] = quiz
            quiz_ids.append(quiz_id)
        
        return quiz_ids
    
    def _generate_exams(self, course_id: str, course_template: Dict[str, Any]) -> List[str]:
        """Generate midterm and final exams"""
        exam_ids = []
        professor_id = self._get_professor_for_course(course_id)
        
        # Midterm exam
        midterm_id = f"MIDTERM_{course_id}"
        midterm = Exam(
            exam_id=midterm_id,
            title=f"{course_id} Midterm Exam",
            course_id=course_id,
            exam_type="midterm",
            questions=self._generate_exam_questions(course_id, "midterm"),
            time_limit_minutes=120,
            difficulty=DifficultyLevel.INTERMEDIATE,
            total_points=200,
            passing_score=140,
            professor_id=professor_id,
            created_at=datetime.now(),
            proctoring_required=True
        )
        
        self.exams[midterm_id] = midterm
        exam_ids.append(midterm_id)
        
        # Final exam
        final_id = f"FINAL_{course_id}"
        final = Exam(
            exam_id=final_id,
            title=f"{course_id} Final Exam",
            course_id=course_id,
            exam_type="final",
            questions=self._generate_exam_questions(course_id, "final"),
            time_limit_minutes=180,
            difficulty=DifficultyLevel.ADVANCED,
            total_points=300,
            passing_score=210,
            professor_id=professor_id,
            created_at=datetime.now(),
            proctoring_required=True
        )
        
        self.exams[final_id] = final
        exam_ids.append(final_id)
        
        return exam_ids
    
    def _generate_tutorials(self, course_id: str, course_template: Dict[str, Any]) -> List[str]:
        """Generate tutorials for a course"""
        tutorial_ids = []
        topics = course_template["topics"]
        professor_id = self._get_professor_for_course(course_id)
        
        for i, topic in enumerate(topics):
            tutorial_id = f"TUTORIAL_{course_id}_{i+1:02d}"
            
            tutorial = Tutorial(
                tutorial_id=tutorial_id,
                title=f"Hands-on Tutorial: {topic}",
                course_id=course_id,
                topic=topic,
                difficulty=DifficultyLevel.INTERMEDIATE,
                estimated_time_minutes=60,
                prerequisites=self._get_tutorial_prerequisites(topic),
                learning_objectives=self._generate_tutorial_objectives(topic),
                step_by_step_instructions=self._generate_tutorial_steps(topic),
                code_examples=self._generate_code_examples(topic),
                expected_outcomes=self._generate_tutorial_outcomes(topic),
                professor_id=professor_id,
                created_at=datetime.now()
            )
            
            self.tutorials[tutorial_id] = tutorial
            tutorial_ids.append(tutorial_id)
        
        return tutorial_ids
    
    def _generate_reading_materials(self, course_id: str, course_template: Dict[str, Any]) -> List[str]:
        """Generate reading materials for a course"""
        reading_ids = []
        topics = course_template["topics"]
        professor_id = self._get_professor_for_course(course_id)
        
        for i, topic in enumerate(topics):
            reading_id = f"READING_{course_id}_{i+1:02d}"
            
            reading = ReadingMaterial(
                reading_id=reading_id,
                title=f"Reading: {topic}",
                course_id=course_id,
                material_type="article",
                author="Various Authors",
                url=None,
                content=self._generate_reading_content(topic),
                reading_time_minutes=45,
                difficulty=DifficultyLevel.INTERMEDIATE,
                key_takeaways=self._generate_key_takeaways(topic),
                discussion_questions=self._generate_discussion_questions(topic),
                professor_id=professor_id,
                created_at=datetime.now()
            )
            
            self.reading_materials[reading_id] = reading
            reading_ids.append(reading_id)
        
        return reading_ids
    
    def _get_professor_for_course(self, course_id: str) -> str:
        """Get appropriate professor for course"""
        professor_mapping = {
            "AI501": "PROF_001",  # Dr. Sarah Chen
            "AI502": "PROF_002",  # Dr. Marcus Rodriguez
            "AI503": "PROF_003",  # Dr. Aisha Patel
            "AI504": "PROF_002",  # Dr. Marcus Rodriguez
            "AI505": "PROF_004",  # Dr. James Kim
            "AI506": "PROF_001",  # Dr. Sarah Chen
            "AI507": "PROF_003",  # Dr. Aisha Patel
            "AI508": "PROF_004"   # Dr. James Kim
        }
        return professor_mapping.get(course_id, "PROF_001")
    
    def _generate_learning_objectives(self, topic: str, week: int) -> List[LearningObjective]:
        """Generate learning objectives for a topic"""
        objectives = []
        
        # Generate 3-5 objectives per topic
        objective_templates = {
            "AI History and Foundations": [
                "Trace the historical development of artificial intelligence",
                "Identify key milestones in AI research and development",
                "Analyze the impact of AI on society and technology"
            ],
            "Machine Learning Basics": [
                "Distinguish between supervised and unsupervised learning",
                "Apply basic machine learning algorithms to datasets",
                "Evaluate model performance using appropriate metrics"
            ],
            "AI Ethics and Society": [
                "Analyze ethical implications of AI systems",
                "Identify potential biases in AI algorithms",
                "Develop frameworks for responsible AI development"
            ]
        }
        
        base_objectives = objective_templates.get(topic, [
            f"Understand fundamental concepts in {topic}",
            f"Apply {topic} techniques to solve problems",
            f"Analyze real-world applications of {topic}"
        ])
        
        for i, description in enumerate(base_objectives):
            objective = LearningObjective(
                objective_id=f"OBJ_{uuid.uuid4().hex[:8]}",
                description=description,
                bloom_taxonomy_level=["remember", "understand", "apply", "analyze"][i % 4],
                assessment_methods=["quiz", "assignment", "exam"]
            )
            objectives.append(objective)
        
        return objectives
    
    def _generate_lecture_outline(self, topic: str, week: int) -> List[str]:
        """Generate lecture outline"""
        return [
            f"Introduction to {topic}",
            f"Key concepts and definitions",
            f"Historical context and development",
            f"Current applications and examples",
            f"Challenges and limitations",
            f"Future directions and trends",
            f"Summary and key takeaways",
            "Q&A and discussion"
        ]
    
    def _generate_lecture_content(self, topic: str, week: int) -> List[Dict[str, Any]]:
        """Generate detailed lecture content"""
        sections = []
        
        section_templates = [
            {
                "title": "Introduction",
                "content": f"This lecture introduces students to {topic}, covering fundamental concepts and their practical applications.",
                "duration_minutes": 10,
                "slides": 3
            },
            {
                "title": "Core Concepts",
                "content": f"We'll explore the key concepts in {topic}, including theoretical foundations and practical implementations.",
                "duration_minutes": 25,
                "slides": 8
            },
            {
                "title": "Examples and Applications",
                "content": f"Real-world examples of {topic} in action, showing how these concepts apply in practice.",
                "duration_minutes": 30,
                "slides": 10
            },
            {
                "title": "Discussion and Analysis",
                "content": f"Critical analysis of {topic}, including challenges, limitations, and future opportunities.",
                "duration_minutes": 20,
                "slides": 6
            },
            {
                "title": "Summary",
                "content": f"Key takeaways from today's lecture on {topic} and preparation for next week's material.",
                "duration_minutes": 5,
                "slides": 2
            }
        ]
        
        return section_templates
    
    def _generate_key_concepts(self, topic: str) -> List[str]:
        """Generate key concepts for a topic"""
        concept_templates = {
            "AI History and Foundations": [
                "Turing Test", "Expert Systems", "Machine Learning", "Neural Networks",
                "Natural Language Processing", "Computer Vision", "Robotics"
            ],
            "Machine Learning Basics": [
                "Supervised Learning", "Unsupervised Learning", "Feature Engineering",
                "Model Evaluation", "Cross-validation", "Overfitting", "Bias-Variance Tradeoff"
            ],
            "AI Ethics and Society": [
                "Algorithmic Bias", "Fairness", "Transparency", "Accountability",
                "Privacy", "Autonomy", "Responsible AI", "AI Governance"
            ]
        }
        
        return concept_templates.get(topic, [
            f"{topic} Fundamentals", f"{topic} Applications", f"{topic} Challenges",
            f"{topic} Future Trends", f"{topic} Best Practices"
        ])
    
    def _generate_examples(self, topic: str, week: int) -> List[Dict[str, Any]]:
        """Generate examples for a topic"""
        examples = []
        
        example_templates = {
            "AI History and Foundations": [
                {"title": "ELIZA Chatbot", "description": "Early natural language processing system", "relevance": "Demonstrates early AI capabilities"},
                {"title": "Deep Blue", "description": "IBM's chess-playing computer", "relevance": "Shows AI's problem-solving abilities"}
            ],
            "Machine Learning Basics": [
                {"title": "Email Spam Detection", "description": "Classifying emails as spam or not spam", "relevance": "Real-world supervised learning application"},
                {"title": "Customer Segmentation", "description": "Grouping customers by behavior", "relevance": "Unsupervised learning in business"}
            ],
            "AI Ethics and Society": [
                {"title": "Facial Recognition Bias", "description": "Racial bias in facial recognition systems", "relevance": "Illustrates algorithmic bias issues"},
                {"title": "AI in Hiring", "description": "Automated resume screening", "relevance": "Shows fairness challenges in AI"}
            ]
        }
        
        return example_templates.get(topic, [
            {"title": f"{topic} Example 1", "description": f"Practical application of {topic}", "relevance": "Demonstrates key concepts"},
            {"title": f"{topic} Example 2", "description": f"Real-world use case for {topic}", "relevance": "Shows practical implementation"}
        ])
    
    def _generate_quiz_questions(self, course_id: str, week: int) -> List[Dict[str, Any]]:
        """Generate quiz questions"""
        questions = []
        
        # Generate 10 questions per quiz
        for i in range(10):
            question_types = [QuestionType.MULTIPLE_CHOICE, QuestionType.TRUE_FALSE, QuestionType.SHORT_ANSWER]
            question_type = random.choice(question_types)
            
            if question_type == QuestionType.MULTIPLE_CHOICE:
                question = {
                    "question_id": f"Q_{uuid.uuid4().hex[:8]}",
                    "type": "multiple_choice",
                    "question": f"What is a key concept in {course_id} week {week}?",
                    "options": [
                        "Option A: Correct answer",
                        "Option B: Incorrect answer",
                        "Option C: Incorrect answer",
                        "Option D: Incorrect answer"
                    ],
                    "correct_answer": 0,
                    "points": 10,
                    "explanation": "This is the correct answer because..."
                }
            elif question_type == QuestionType.TRUE_FALSE:
                question = {
                    "question_id": f"Q_{uuid.uuid4().hex[:8]}",
                    "type": "true_false",
                    "question": f"True or False: {course_id} concepts are important for AI development.",
                    "correct_answer": True,
                    "points": 10,
                    "explanation": "This statement is true because..."
                }
            else:  # SHORT_ANSWER
                question = {
                    "question_id": f"Q_{uuid.uuid4().hex[:8]}",
                    "type": "short_answer",
                    "question": f"Explain a key concept from {course_id} week {week}.",
                    "points": 10,
                    "sample_answer": "A key concept is...",
                    "grading_criteria": ["Accuracy", "Completeness", "Clarity"]
                }
            
            questions.append(question)
        
        return questions
    
    def _generate_exam_questions(self, course_id: str, exam_type: str) -> List[Dict[str, Any]]:
        """Generate exam questions"""
        questions = []
        
        # Generate more comprehensive questions for exams
        question_count = 20 if exam_type == "midterm" else 30
        
        for i in range(question_count):
            question_types = [QuestionType.MULTIPLE_CHOICE, QuestionType.ESSAY, QuestionType.CODING]
            question_type = random.choice(question_types)
            
            if question_type == QuestionType.MULTIPLE_CHOICE:
                question = {
                    "question_id": f"EXAM_Q_{uuid.uuid4().hex[:8]}",
                    "type": "multiple_choice",
                    "question": f"Which of the following best describes {course_id} concepts?",
                    "options": [
                        "Option A: Comprehensive answer",
                        "Option B: Partial answer",
                        "Option C: Incorrect answer",
                        "Option D: Misleading answer"
                    ],
                    "correct_answer": 0,
                    "points": 10,
                    "explanation": "Detailed explanation of the correct answer..."
                }
            elif question_type == QuestionType.ESSAY:
                question = {
                    "question_id": f"EXAM_Q_{uuid.uuid4().hex[:8]}",
                    "type": "essay",
                    "question": f"Analyze the impact of {course_id} on modern AI development. Provide specific examples and discuss implications.",
                    "points": 25,
                    "grading_criteria": ["Analysis depth", "Examples quality", "Critical thinking", "Writing clarity"],
                    "expected_length": "500-750 words"
                }
            else:  # CODING
                question = {
                    "question_id": f"EXAM_Q_{uuid.uuid4().hex[:8]}",
                    "type": "coding",
                    "question": f"Implement a solution for a {course_id} problem. Show your code and explain your approach.",
                    "points": 20,
                    "language": "Python",
                    "test_cases": ["Test case 1", "Test case 2", "Test case 3"],
                    "grading_criteria": ["Correctness", "Efficiency", "Code quality", "Documentation"]
                }
            
            questions.append(question)
        
        return questions
    
    def _get_tutorial_prerequisites(self, topic: str) -> List[str]:
        """Get prerequisites for tutorial"""
        return [
            "Basic programming knowledge",
            "Understanding of fundamental concepts",
            "Access to required software tools"
        ]
    
    def _generate_tutorial_objectives(self, topic: str) -> List[str]:
        """Generate tutorial learning objectives"""
        return [
            f"Hands-on experience with {topic}",
            f"Practical implementation of {topic} concepts",
            f"Problem-solving using {topic} techniques"
        ]
    
    def _generate_tutorial_steps(self, topic: str) -> List[Dict[str, Any]]:
        """Generate step-by-step tutorial instructions"""
        steps = []
        
        for i in range(8):  # 8 steps per tutorial
            step = {
                "step_number": i + 1,
                "title": f"Step {i + 1}: {topic} Implementation",
                "description": f"Detailed instructions for step {i + 1} of the {topic} tutorial",
                "estimated_time_minutes": random.randint(5, 15),
                "resources_needed": ["Computer", "Internet connection", "Required software"],
                "expected_outcome": f"Completion of step {i + 1} objectives"
            }
            steps.append(step)
        
        return steps
    
    def _generate_code_examples(self, topic: str) -> List[Dict[str, Any]]:
        """Generate code examples for tutorial"""
        examples = []
        
        for i in range(3):  # 3 code examples per tutorial
            example = {
                "example_id": f"CODE_{uuid.uuid4().hex[:8]}",
                "title": f"{topic} Example {i + 1}",
                "language": "Python",
                "code": f"# {topic} implementation example {i + 1}\n# Code would go here\nprint('Hello, {topic}!')\n",
                "explanation": f"This example demonstrates {topic} concepts in practice",
                "output": f"Expected output for {topic} example {i + 1}"
            }
            examples.append(example)
        
        return examples
    
    def _generate_tutorial_outcomes(self, topic: str) -> List[str]:
        """Generate expected tutorial outcomes"""
        return [
            f"Successful implementation of {topic} solution",
            f"Understanding of {topic} best practices",
            f"Ability to troubleshoot {topic} problems",
            f"Confidence in applying {topic} techniques"
        ]
    
    def _generate_reading_content(self, topic: str) -> str:
        """Generate reading material content"""
        return f"""
# {topic}

## Introduction

This reading material provides comprehensive coverage of {topic}, exploring both theoretical foundations and practical applications.

## Key Concepts

{topic} encompasses several important concepts that are essential for understanding artificial intelligence and machine learning.

## Historical Development

The development of {topic} has been marked by significant milestones and breakthroughs that have shaped the field.

## Current Applications

Today, {topic} is applied in various domains, from healthcare to finance, demonstrating its versatility and impact.

## Challenges and Future Directions

While {topic} offers many opportunities, it also presents challenges that researchers and practitioners continue to address.

## Conclusion

{topic} represents a crucial area of study in artificial intelligence, with ongoing research and development promising exciting future developments.
        """
    
    def _generate_key_takeaways(self, topic: str) -> List[str]:
        """Generate key takeaways for reading material"""
        return [
            f"{topic} is fundamental to AI development",
            f"Understanding {topic} requires both theoretical and practical knowledge",
            f"{topic} applications are widespread across industries",
            f"Future research in {topic} will continue to advance the field"
        ]
    
    def _generate_discussion_questions(self, topic: str) -> List[str]:
        """Generate discussion questions for reading material"""
        return [
            f"How does {topic} relate to other AI concepts?",
            f"What are the practical implications of {topic}?",
            f"How might {topic} evolve in the future?",
            f"What ethical considerations are important for {topic}?"
        ]
    
    def get_course_content_summary(self, course_id: str) -> Dict[str, Any]:
        """Get summary of generated content for a course"""
        lectures = [l for l in self.lectures.values() if l.course_id == course_id]
        quizzes = [q for q in self.quizzes.values() if q.course_id == course_id]
        exams = [e for e in self.exams.values() if e.course_id == course_id]
        tutorials = [t for t in self.tutorials.values() if t.course_id == course_id]
        readings = [r for r in self.reading_materials.values() if r.course_id == course_id]
        
        return {
            "course_id": course_id,
            "content_summary": {
                "lectures": len(lectures),
                "quizzes": len(quizzes),
                "exams": len(exams),
                "tutorials": len(tutorials),
                "reading_materials": len(readings)
            },
            "total_duration_hours": sum(l.duration_minutes for l in lectures) / 60,
            "total_assessment_points": sum(q.total_points for q in quizzes) + sum(e.total_points for e in exams),
            "content_details": {
                "lecture_titles": [l.title for l in lectures],
                "quiz_titles": [q.title for q in quizzes],
                "exam_titles": [e.title for e in exams],
                "tutorial_titles": [t.title for t in tutorials],
                "reading_titles": [r.title for r in readings]
            }
        }