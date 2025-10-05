#!/usr/bin/env python3
"""
MS AI Curriculum System - Course Management and Prerequisites
Creates individual course pages and curriculum graph visualization
"""

import json
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

@dataclass
class Course:
    """Individual course data structure"""
    course_id: str
    course_code: str
    title: str
    credits: int
    level: str  # Foundational, Intermediate, Advanced
    description: str
    detailed_description: str
    learning_outcomes: List[str]
    prerequisites: List[str]  # Course IDs
    corequisites: List[str]   # Course IDs that can be taken together
    modules: List[Dict[str, any]]
    ai_generated_content: Dict[str, any]
    career_pathways: List[str]
    difficulty: int  # 1-5 scale
    estimated_hours: int
    semester: str  # Fall, Spring, Summer
    year: int  # 1 or 2
    specialization_tracks: List[str]

@dataclass
class CurriculumGraph:
    """Curriculum graph data structure"""
    courses: Dict[str, Course]
    prerequisites: Dict[str, List[str]]
    learning_paths: List[List[str]]
    specialization_tracks: Dict[str, List[str]]

class CurriculumBuilder:
    """Builds comprehensive curriculum with courses and prerequisites"""
    
    def __init__(self):
        self.courses = {}
        self.prerequisites = {}
        self.specialization_tracks = {
            "ML_DATA_SCIENCE": [],
            "NLP_TRACK": [],
            "CV_ROBOTICS": []
        }
    
    def create_comprehensive_curriculum(self) -> CurriculumGraph:
        """Create the complete MS AI curriculum with all courses"""
        print("🎓 Building comprehensive MS AI curriculum...")
        
        # Create all courses
        self._create_foundational_courses()
        self._create_intermediate_courses()
        self._create_advanced_courses()
        self._create_specialization_courses()
        self._create_capstone_courses()
        
        # Build prerequisite relationships
        self._build_prerequisite_relationships()
        
        # Create learning paths
        learning_paths = self._create_learning_paths()
        
        # Create curriculum graph
        curriculum = CurriculumGraph(
            courses=self.courses,
            prerequisites=self.prerequisites,
            learning_paths=learning_paths,
            specialization_tracks=self.specialization_tracks
        )
        
        print(f"✅ Curriculum created with {len(self.courses)} courses")
        return curriculum
    
    def _create_foundational_courses(self):
        """Create foundational courses (Year 1, Semester 1)"""
        
        # AI-501: Foundations of Artificial Intelligence
        self.courses["AI_FUNDAMENTALS"] = Course(
            course_id="AI_FUNDAMENTALS",
            course_code="AI-501",
            title="Foundations of Artificial Intelligence",
            credits=3,
            level="Foundational",
            description="Comprehensive introduction to AI concepts, history, and foundational theories.",
            detailed_description="This foundational course provides students with a comprehensive understanding of artificial intelligence, covering its historical development, core theoretical frameworks, and fundamental concepts. Students will explore the philosophical foundations of AI, understand different approaches to machine intelligence, and examine the ethical implications of AI development.",
            learning_outcomes=[
                "Define and explain core AI concepts and terminology",
                "Analyze historical development of AI and key milestones",
                "Evaluate different AI approaches and their applications",
                "Discuss ethical implications of AI development",
                "Apply AI problem-solving methodologies to real-world scenarios"
            ],
            prerequisites=[],
            corequisites=[],
            modules=[
                {
                    "title": "Introduction to AI and Machine Intelligence",
                    "duration_weeks": 2,
                    "key_topics": ["Definition of AI", "Turing Test", "Chinese Room Argument", "Strong vs Weak AI"],
                    "hands_on_projects": ["Build a simple chatbot", "Design an AI ethics framework"]
                },
                {
                    "title": "History and Evolution of AI",
                    "duration_weeks": 2,
                    "key_topics": ["Dartmouth Conference", "AI Winters", "Modern AI Renaissance", "Current AI Landscape"],
                    "hands_on_projects": ["Create AI timeline visualization", "Research historical AI failures"]
                },
                {
                    "title": "AI Problem-Solving and Search",
                    "duration_weeks": 3,
                    "key_topics": ["Search Algorithms", "Heuristics", "Constraint Satisfaction", "Game Theory"],
                    "hands_on_projects": ["Implement A* search", "Build a puzzle solver"]
                },
                {
                    "title": "Knowledge Representation and Reasoning",
                    "duration_weeks": 3,
                    "key_topics": ["Logic Systems", "Rule-Based Systems", "Ontologies", "Semantic Networks"],
                    "hands_on_projects": ["Create knowledge base", "Build expert system"]
                }
            ],
            ai_generated_content={
                "adaptive_learning_paths": "Personalized curriculum based on student background",
                "ai_tutors": ["Dr. Sarah Chen (ML Specialist)", "Dr. Michael Rodriguez (NLP Expert)"],
                "content_generation": "Dynamic course materials based on current AI research"
            },
            career_pathways=["AI Researcher", "Machine Learning Engineer", "AI Product Manager", "AI Consultant"],
            difficulty=2,
            estimated_hours=120,
            semester="Fall",
            year=1,
            specialization_tracks=["ML_DATA_SCIENCE", "NLP_TRACK", "CV_ROBOTICS"]
        )
        
        # AI-502: Machine Learning Fundamentals
        self.courses["ML_FUNDAMENTALS"] = Course(
            course_id="ML_FUNDAMENTALS",
            course_code="AI-502",
            title="Machine Learning Fundamentals",
            credits=3,
            level="Foundational",
            description="Hands-on introduction to machine learning algorithms, implementation, and real-world applications.",
            detailed_description="This course provides a comprehensive, hands-on introduction to machine learning algorithms and their practical implementation. Students will learn to build, train, and evaluate machine learning models using modern tools and frameworks. The course emphasizes practical application through AI-generated projects that adapt to student interests and career goals.",
            learning_outcomes=[
                "Implement supervised learning algorithms",
                "Apply unsupervised learning techniques",
                "Evaluate model performance using appropriate metrics",
                "Optimize models for real-world deployment",
                "Understand bias and fairness in ML systems"
            ],
            prerequisites=["AI_FUNDAMENTALS"],
            corequisites=[],
            modules=[
                {
                    "title": "Supervised Learning Algorithms",
                    "duration_weeks": 4,
                    "key_topics": ["Linear Regression", "Decision Trees", "Random Forest", "SVM", "Neural Networks"],
                    "hands_on_projects": ["Predict housing prices", "Classify images", "Build recommendation system"]
                },
                {
                    "title": "Unsupervised Learning",
                    "duration_weeks": 3,
                    "key_topics": ["K-Means Clustering", "Hierarchical Clustering", "PCA", "t-SNE", "DBSCAN"],
                    "hands_on_projects": ["Customer segmentation", "Anomaly detection", "Data visualization"]
                },
                {
                    "title": "Model Evaluation and Validation",
                    "duration_weeks": 2,
                    "key_topics": ["Cross-validation", "Metrics", "Overfitting", "Bias-Variance Tradeoff"],
                    "hands_on_projects": ["Model comparison framework", "Bias detection tool"]
                }
            ],
            ai_generated_content={
                "personalized_datasets": "Custom datasets based on student interests",
                "adaptive_projects": "Projects that scale with student skill level",
                "ai_code_review": "Automated feedback on code quality and ML best practices"
            },
            career_pathways=["Data Scientist", "Machine Learning Engineer", "AI Research Scientist", "MLOps Engineer"],
            difficulty=3,
            estimated_hours=120,
            semester="Fall",
            year=1,
            specialization_tracks=["ML_DATA_SCIENCE", "NLP_TRACK", "CV_ROBOTICS"]
        )
        
        # AI-503: Mathematics for AI
        self.courses["MATH_FOR_AI"] = Course(
            course_id="MATH_FOR_AI",
            course_code="AI-503",
            title="Mathematics for Artificial Intelligence",
            credits=3,
            level="Foundational",
            description="Essential mathematical foundations for AI including linear algebra, calculus, probability, and statistics.",
            detailed_description="This course provides the mathematical foundation necessary for understanding and implementing AI algorithms. Students will develop proficiency in linear algebra, calculus, probability theory, and statistics as they apply to machine learning and AI systems.",
            learning_outcomes=[
                "Apply linear algebra concepts to AI problems",
                "Use calculus for optimization in ML algorithms",
                "Apply probability theory to uncertainty in AI",
                "Use statistical methods for data analysis",
                "Implement mathematical concepts in code"
            ],
            prerequisites=[],
            corequisites=["AI_FUNDAMENTALS"],
            modules=[
                {
                    "title": "Linear Algebra for AI",
                    "duration_weeks": 3,
                    "key_topics": ["Vectors", "Matrices", "Eigenvalues", "Singular Value Decomposition"],
                    "hands_on_projects": ["Matrix operations library", "PCA implementation"]
                },
                {
                    "title": "Calculus and Optimization",
                    "duration_weeks": 3,
                    "key_topics": ["Gradients", "Partial Derivatives", "Gradient Descent", "Convex Optimization"],
                    "hands_on_projects": ["Gradient descent implementation", "Optimization visualizer"]
                },
                {
                    "title": "Probability and Statistics",
                    "duration_weeks": 3,
                    "key_topics": ["Probability Distributions", "Bayesian Inference", "Hypothesis Testing", "Information Theory"],
                    "hands_on_projects": ["Bayesian classifier", "Statistical analysis tool"]
                }
            ],
            ai_generated_content={
                "adaptive_problems": "Math problems tailored to student's AI interests",
                "visual_learning": "Interactive visualizations of mathematical concepts",
                "ai_tutor": "Personalized math tutor for AI applications"
            },
            career_pathways=["AI Researcher", "Machine Learning Engineer", "Data Scientist", "AI Research Scientist"],
            difficulty=3,
            estimated_hours=120,
            semester="Fall",
            year=1,
            specialization_tracks=["ML_DATA_SCIENCE", "NLP_TRACK", "CV_ROBOTICS"]
        )
    
    def _create_intermediate_courses(self):
        """Create intermediate courses (Year 1, Semester 2)"""
        
        # AI-504: Deep Learning and Neural Networks
        self.courses["DEEP_LEARNING"] = Course(
            course_id="DEEP_LEARNING",
            course_code="AI-504",
            title="Deep Learning and Neural Networks",
            credits=3,
            level="Intermediate",
            description="Advanced course covering deep neural networks, architectures, and cutting-edge applications.",
            detailed_description="This advanced course delves into deep learning architectures, from basic neural networks to state-of-the-art models like Transformers and GANs. Students will build and train complex neural networks for various applications including computer vision, natural language processing, and generative AI.",
            learning_outcomes=[
                "Design and implement deep neural networks",
                "Apply CNNs for computer vision tasks",
                "Implement RNNs and Transformers for NLP",
                "Develop generative models (GANs, VAEs)",
                "Optimize deep learning models for production"
            ],
            prerequisites=["ML_FUNDAMENTALS", "MATH_FOR_AI"],
            corequisites=[],
            modules=[
                {
                    "title": "Neural Network Fundamentals",
                    "duration_weeks": 3,
                    "key_topics": ["Feedforward Networks", "Backpropagation", "Activation Functions", "Optimizers"],
                    "hands_on_projects": ["Build neural network from scratch", "Implement optimization algorithms"]
                },
                {
                    "title": "Convolutional Neural Networks",
                    "duration_weeks": 4,
                    "key_topics": ["CNN Architecture", "Image Classification", "Object Detection", "Transfer Learning"],
                    "hands_on_projects": ["Image classifier", "Object detection system", "Style transfer application"]
                },
                {
                    "title": "Recurrent Neural Networks and Transformers",
                    "duration_weeks": 4,
                    "key_topics": ["RNNs", "LSTMs", "GRUs", "Attention Mechanisms", "Transformers"],
                    "hands_on_projects": ["Language model", "Text generator", "Translation system"]
                }
            ],
            ai_generated_content={
                "research_integration": "Latest papers automatically integrated into curriculum",
                "architecture_exploration": "AI suggests novel network architectures",
                "performance_optimization": "AI helps optimize model performance"
            },
            career_pathways=["Deep Learning Engineer", "AI Research Scientist", "Computer Vision Engineer", "NLP Engineer"],
            difficulty=4,
            estimated_hours=120,
            semester="Spring",
            year=1,
            specialization_tracks=["ML_DATA_SCIENCE", "NLP_TRACK", "CV_ROBOTICS"]
        )
        
        # AI-505: Natural Language Processing
        self.courses["NLP_FUNDAMENTALS"] = Course(
            course_id="NLP_FUNDAMENTALS",
            course_code="AI-505",
            title="Natural Language Processing",
            credits=3,
            level="Intermediate",
            description="Comprehensive introduction to NLP techniques, from traditional methods to modern transformer-based approaches.",
            detailed_description="This course covers the fundamental concepts and techniques in natural language processing, from traditional rule-based systems to modern deep learning approaches. Students will learn to build systems that can understand, process, and generate human language.",
            learning_outcomes=[
                "Implement text preprocessing and feature extraction",
                "Apply traditional NLP techniques (TF-IDF, N-grams)",
                "Use modern transformer models for NLP tasks",
                "Build end-to-end NLP applications",
                "Evaluate and compare different NLP approaches"
            ],
            prerequisites=["ML_FUNDAMENTALS"],
            corequisites=["DEEP_LEARNING"],
            modules=[
                {
                    "title": "Text Preprocessing and Feature Engineering",
                    "duration_weeks": 2,
                    "key_topics": ["Tokenization", "Stemming", "Lemmatization", "TF-IDF", "Word Embeddings"],
                    "hands_on_projects": ["Text preprocessing pipeline", "Feature extraction tool"]
                },
                {
                    "title": "Traditional NLP Techniques",
                    "duration_weeks": 3,
                    "key_topics": ["Part-of-Speech Tagging", "Named Entity Recognition", "Sentiment Analysis", "Topic Modeling"],
                    "hands_on_projects": ["Sentiment analyzer", "Topic modeling system"]
                },
                {
                    "title": "Modern NLP with Transformers",
                    "duration_weeks": 4,
                    "key_topics": ["BERT", "GPT", "T5", "Fine-tuning", "Prompt Engineering"],
                    "hands_on_projects": ["Question answering system", "Text generation app"]
                }
            ],
            ai_generated_content={
                "multilingual_curriculum": "Content adapts to student's language background",
                "ai_tutor": "NLP expert AI tutor with multilingual capabilities",
                "real_world_datasets": "Curated datasets from current events and trends"
            },
            career_pathways=["NLP Engineer", "Conversational AI Developer", "Language Technology Specialist", "AI Research Scientist"],
            difficulty=4,
            estimated_hours=120,
            semester="Spring",
            year=1,
            specialization_tracks=["NLP_TRACK", "ML_DATA_SCIENCE"]
        )
        
        # AI-506: Computer Vision
        self.courses["COMPUTER_VISION"] = Course(
            course_id="COMPUTER_VISION",
            course_code="AI-506",
            title="Computer Vision",
            credits=3,
            level="Intermediate",
            description="Introduction to computer vision techniques, from image processing to deep learning applications.",
            detailed_description="This course covers the fundamental concepts and techniques in computer vision, from traditional image processing methods to modern deep learning approaches. Students will learn to build systems that can interpret and understand visual information.",
            learning_outcomes=[
                "Apply image processing and feature extraction techniques",
                "Implement computer vision algorithms",
                "Use deep learning for computer vision tasks",
                "Build real-world computer vision applications",
                "Evaluate and optimize computer vision models"
            ],
            prerequisites=["ML_FUNDAMENTALS"],
            corequisites=["DEEP_LEARNING"],
            modules=[
                {
                    "title": "Image Processing Fundamentals",
                    "duration_weeks": 3,
                    "key_topics": ["Image Representation", "Filtering", "Edge Detection", "Feature Detection"],
                    "hands_on_projects": ["Image filter library", "Edge detection tool"]
                },
                {
                    "title": "Feature Extraction and Matching",
                    "duration_weeks": 2,
                    "key_topics": ["SIFT", "SURF", "ORB", "Feature Matching", "Homography"],
                    "hands_on_projects": ["Feature matching system", "Image stitching app"]
                },
                {
                    "title": "Deep Learning for Computer Vision",
                    "duration_weeks": 4,
                    "key_topics": ["CNNs", "Object Detection", "Semantic Segmentation", "Instance Segmentation"],
                    "hands_on_projects": ["Object detection system", "Image segmentation tool"]
                }
            ],
            ai_generated_content={
                "adaptive_datasets": "Image datasets tailored to student interests",
                "visual_learning": "Interactive visualizations of computer vision concepts",
                "ai_tutor": "Computer vision expert with visual teaching methods"
            },
            career_pathways=["Computer Vision Engineer", "Autonomous Vehicle Engineer", "Robotics Engineer", "Medical AI Specialist"],
            difficulty=4,
            estimated_hours=120,
            semester="Spring",
            year=1,
            specialization_tracks=["CV_ROBOTICS", "ML_DATA_SCIENCE"]
        )
    
    def _create_advanced_courses(self):
        """Create advanced courses (Year 2, Semester 1)"""
        
        # AI-601: Advanced Machine Learning
        self.courses["ADVANCED_ML"] = Course(
            course_id="ADVANCED_ML",
            course_code="AI-601",
            title="Advanced Machine Learning",
            credits=3,
            level="Advanced",
            description="Advanced topics in machine learning including ensemble methods, reinforcement learning, and model interpretability.",
            detailed_description="This course covers advanced machine learning topics including ensemble methods, reinforcement learning, model interpretability, and advanced optimization techniques. Students will learn to build sophisticated ML systems and understand the theoretical foundations behind modern ML algorithms.",
            learning_outcomes=[
                "Implement advanced ensemble methods",
                "Apply reinforcement learning algorithms",
                "Build interpretable ML models",
                "Optimize ML systems for production",
                "Understand theoretical foundations of ML"
            ],
            prerequisites=["DEEP_LEARNING"],
            corequisites=[],
            modules=[
                {
                    "title": "Ensemble Methods",
                    "duration_weeks": 3,
                    "key_topics": ["Bagging", "Boosting", "Stacking", "Random Forest", "XGBoost"],
                    "hands_on_projects": ["Ensemble model builder", "Model comparison framework"]
                },
                {
                    "title": "Reinforcement Learning",
                    "duration_weeks": 4,
                    "key_topics": ["Q-Learning", "Policy Gradient", "Actor-Critic", "Deep RL", "Multi-Agent RL"],
                    "hands_on_projects": ["RL game agent", "Multi-agent simulation"]
                },
                {
                    "title": "Model Interpretability",
                    "duration_weeks": 2,
                    "key_topics": ["SHAP", "LIME", "Feature Importance", "Model Debugging", "Fairness"],
                    "hands_on_projects": ["Model explainer tool", "Bias detection system"]
                }
            ],
            ai_generated_content={
                "adaptive_algorithms": "RL algorithms that adapt to student's learning style",
                "research_integration": "Latest ML research automatically integrated",
                "ai_tutor": "Advanced ML expert with research background"
            },
            career_pathways=["ML Research Scientist", "MLOps Engineer", "AI Research Scientist", "ML Engineer"],
            difficulty=5,
            estimated_hours=120,
            semester="Fall",
            year=2,
            specialization_tracks=["ML_DATA_SCIENCE"]
        )
        
        # AI-602: AI Ethics and Responsible AI
        self.courses["AI_ETHICS"] = Course(
            course_id="AI_ETHICS",
            course_code="AI-602",
            title="AI Ethics and Responsible AI",
            credits=3,
            level="Advanced",
            description="Comprehensive study of ethical implications, bias, fairness, and responsible development of AI systems.",
            detailed_description="This course examines the ethical implications of AI development and deployment, covering topics such as bias, fairness, transparency, accountability, and the societal impact of AI systems. Students will learn to develop AI systems responsibly and understand the broader implications of their work.",
            learning_outcomes=[
                "Identify and mitigate bias in AI systems",
                "Apply fairness metrics and evaluation methods",
                "Design transparent and accountable AI systems",
                "Understand legal and regulatory frameworks for AI",
                "Develop responsible AI development practices"
            ],
            prerequisites=["AI_FUNDAMENTALS"],
            corequisites=[],
            modules=[
                {
                    "title": "Bias and Fairness in AI",
                    "duration_weeks": 3,
                    "key_topics": ["Types of Bias", "Fairness Metrics", "Bias Detection", "Mitigation Strategies"],
                    "hands_on_projects": ["Bias detection tool", "Fairness evaluation framework"]
                },
                {
                    "title": "Transparency and Interpretability",
                    "duration_weeks": 2,
                    "key_topics": ["Explainable AI", "Model Transparency", "Algorithmic Accountability", "Audit Trails"],
                    "hands_on_projects": ["Explainable AI system", "Transparency dashboard"]
                },
                {
                    "title": "AI and Society",
                    "duration_weeks": 2,
                    "key_topics": ["Economic Impact", "Job Displacement", "Privacy", "Security", "Governance"],
                    "hands_on_projects": ["Impact assessment tool", "Policy recommendation system"]
                }
            ],
            ai_generated_content={
                "case_studies": "Real-world ethical dilemmas and case studies",
                "ai_tutor": "Ethics expert with diverse perspectives",
                "debate_platform": "AI-powered debate and discussion platform"
            },
            career_pathways=["AI Ethics Consultant", "Responsible AI Engineer", "AI Policy Advisor", "AI Research Scientist"],
            difficulty=3,
            estimated_hours=120,
            semester="Fall",
            year=2,
            specialization_tracks=["ML_DATA_SCIENCE", "NLP_TRACK", "CV_ROBOTICS"]
        )
    
    def _create_specialization_courses(self):
        """Create specialization-specific courses"""
        
        # ML Specialization Courses
        self.courses["MLOPS"] = Course(
            course_id="MLOPS",
            course_code="AI-701",
            title="MLOps and Model Deployment",
            credits=3,
            level="Advanced",
            description="Production deployment and management of machine learning models at scale.",
            detailed_description="This course covers the complete MLOps pipeline from model development to production deployment, including versioning, monitoring, and maintenance of ML systems in production environments.",
            learning_outcomes=[
                "Design and implement MLOps pipelines",
                "Deploy ML models to production",
                "Monitor and maintain ML systems",
                "Implement model versioning and rollback",
                "Optimize ML systems for scale"
            ],
            prerequisites=["ADVANCED_ML"],
            corequisites=[],
            modules=[
                {
                    "title": "Model Deployment Strategies",
                    "duration_weeks": 3,
                    "key_topics": ["Containerization", "Microservices", "Serverless", "Edge Deployment"],
                    "hands_on_projects": ["Model deployment pipeline", "Container orchestration"]
                },
                {
                    "title": "Model Monitoring and Maintenance",
                    "duration_weeks": 3,
                    "key_topics": ["Performance Monitoring", "Data Drift", "Model Drift", "A/B Testing"],
                    "hands_on_projects": ["Monitoring dashboard", "Drift detection system"]
                }
            ],
            ai_generated_content={
                "production_scenarios": "Real-world production challenges and solutions",
                "ai_tutor": "MLOps expert with industry experience"
            },
            career_pathways=["MLOps Engineer", "ML Platform Engineer", "DevOps Engineer", "ML Engineer"],
            difficulty=4,
            estimated_hours=120,
            semester="Spring",
            year=2,
            specialization_tracks=["ML_DATA_SCIENCE"]
        )
        
        # NLP Specialization Courses
        self.courses["ADVANCED_NLP"] = Course(
            course_id="ADVANCED_NLP",
            course_code="AI-702",
            title="Advanced Natural Language Processing",
            credits=3,
            level="Advanced",
            description="Advanced NLP techniques including large language models, multilingual processing, and conversational AI.",
            detailed_description="This course covers advanced topics in natural language processing, including large language models, multilingual processing, conversational AI, and cutting-edge NLP research.",
            learning_outcomes=[
                "Work with large language models",
                "Implement multilingual NLP systems",
                "Build conversational AI applications",
                "Apply advanced NLP techniques",
                "Contribute to NLP research"
            ],
            prerequisites=["NLP_FUNDAMENTALS", "DEEP_LEARNING"],
            corequisites=[],
            modules=[
                {
                    "title": "Large Language Models",
                    "duration_weeks": 4,
                    "key_topics": ["GPT", "BERT", "T5", "Fine-tuning", "Prompt Engineering"],
                    "hands_on_projects": ["LLM application", "Fine-tuning pipeline"]
                },
                {
                    "title": "Multilingual and Cross-lingual NLP",
                    "duration_weeks": 3,
                    "key_topics": ["Multilingual Models", "Cross-lingual Transfer", "Low-resource Languages"],
                    "hands_on_projects": ["Multilingual system", "Cross-lingual application"]
                }
            ],
            ai_generated_content={
                "multilingual_curriculum": "Content in multiple languages",
                "ai_tutor": "Multilingual NLP expert",
                "research_integration": "Latest NLP research and papers"
            },
            career_pathways=["NLP Research Scientist", "Conversational AI Engineer", "Language Technology Specialist"],
            difficulty=5,
            estimated_hours=120,
            semester="Spring",
            year=2,
            specialization_tracks=["NLP_TRACK"]
        )
        
        # Computer Vision Specialization Courses
        self.courses["ADVANCED_CV"] = Course(
            course_id="ADVANCED_CV",
            course_code="AI-703",
            title="Advanced Computer Vision",
            credits=3,
            level="Advanced",
            description="Advanced computer vision techniques including 3D vision, video analysis, and real-time systems.",
            detailed_description="This course covers advanced topics in computer vision, including 3D computer vision, video analysis, real-time systems, and cutting-edge CV research.",
            learning_outcomes=[
                "Implement 3D computer vision techniques",
                "Build video analysis systems",
                "Develop real-time computer vision applications",
                "Apply advanced CV algorithms",
                "Contribute to CV research"
            ],
            prerequisites=["COMPUTER_VISION", "DEEP_LEARNING"],
            corequisites=[],
            modules=[
                {
                    "title": "3D Computer Vision",
                    "duration_weeks": 4,
                    "key_topics": ["Stereo Vision", "Depth Estimation", "3D Reconstruction", "Point Clouds"],
                    "hands_on_projects": ["3D reconstruction system", "Depth estimation tool"]
                },
                {
                    "title": "Video Analysis and Understanding",
                    "duration_weeks": 3,
                    "key_topics": ["Video Classification", "Action Recognition", "Video Object Detection", "Temporal Analysis"],
                    "hands_on_projects": ["Video analysis system", "Action recognition app"]
                }
            ],
            ai_generated_content={
                "visual_learning": "Interactive 3D visualizations",
                "ai_tutor": "Computer vision expert with visual teaching",
                "real_world_applications": "Industry-specific CV applications"
            },
            career_pathways=["Computer Vision Research Scientist", "Autonomous Vehicle Engineer", "Robotics Engineer"],
            difficulty=5,
            estimated_hours=120,
            semester="Spring",
            year=2,
            specialization_tracks=["CV_ROBOTICS"]
        )
    
    def _create_capstone_courses(self):
        """Create capstone and research courses"""
        
        # AI-801: Capstone Project
        self.courses["CAPSTONE_PROJECT"] = Course(
            course_id="CAPSTONE_PROJECT",
            course_code="AI-801",
            title="AI Capstone Project",
            credits=6,
            level="Advanced",
            description="Comprehensive capstone project demonstrating mastery of AI concepts and techniques.",
            detailed_description="This capstone course requires students to complete a comprehensive AI project that demonstrates their mastery of the program's learning outcomes. Students will work on real-world problems with industry partners or research labs.",
            learning_outcomes=[
                "Design and implement a comprehensive AI solution",
                "Apply multiple AI techniques to solve complex problems",
                "Present and defend AI solutions to stakeholders",
                "Demonstrate professional AI development practices",
                "Contribute to the AI community through open source or research"
            ],
            prerequisites=["ADVANCED_ML", "AI_ETHICS"],
            corequisites=[],
            modules=[
                {
                    "title": "Project Planning and Design",
                    "duration_weeks": 3,
                    "key_topics": ["Problem Definition", "Solution Design", "Project Planning", "Stakeholder Management"],
                    "hands_on_projects": ["Project proposal", "Technical design document"]
                },
                {
                    "title": "Implementation and Testing",
                    "duration_weeks": 8,
                    "key_topics": ["Agile Development", "Testing Strategies", "Performance Optimization", "Documentation"],
                    "hands_on_projects": ["Complete AI system", "Comprehensive testing suite"]
                },
                {
                    "title": "Presentation and Evaluation",
                    "duration_weeks": 2,
                    "key_topics": ["Technical Presentation", "Demo Preparation", "Evaluation Metrics", "Future Work"],
                    "hands_on_projects": ["Final presentation", "Demo system"]
                }
            ],
            ai_generated_content={
                "project_mentoring": "AI mentor for project guidance",
                "peer_collaboration": "AI-facilitated peer review and collaboration",
                "industry_connections": "AI-powered matching with industry partners"
            },
            career_pathways=["AI Engineer", "AI Research Scientist", "AI Product Manager", "AI Consultant"],
            difficulty=5,
            estimated_hours=240,
            semester="Spring",
            year=2,
            specialization_tracks=["ML_DATA_SCIENCE", "NLP_TRACK", "CV_ROBOTICS"]
        )
    
    def _build_prerequisite_relationships(self):
        """Build prerequisite relationships between courses"""
        for course_id, course in self.courses.items():
            self.prerequisites[course_id] = course.prerequisites
            
            # Add to specialization tracks
            for track in course.specialization_tracks:
                if track in self.specialization_tracks:
                    self.specialization_tracks[track].append(course_id)
    
    def _create_learning_paths(self) -> List[List[str]]:
        """Create recommended learning paths through the curriculum"""
        paths = []
        
        # ML Data Science Path
        ml_path = [
            "AI_FUNDAMENTALS", "MATH_FOR_AI", "ML_FUNDAMENTALS",
            "DEEP_LEARNING", "ADVANCED_ML", "MLOPS", "CAPSTONE_PROJECT"
        ]
        paths.append(ml_path)
        
        # NLP Track Path
        nlp_path = [
            "AI_FUNDAMENTALS", "MATH_FOR_AI", "ML_FUNDAMENTALS",
            "NLP_FUNDAMENTALS", "DEEP_LEARNING", "ADVANCED_NLP", "CAPSTONE_PROJECT"
        ]
        paths.append(nlp_path)
        
        # Computer Vision Path
        cv_path = [
            "AI_FUNDAMENTALS", "MATH_FOR_AI", "ML_FUNDAMENTALS",
            "COMPUTER_VISION", "DEEP_LEARNING", "ADVANCED_CV", "CAPSTONE_PROJECT"
        ]
        paths.append(cv_path)
        
        # Ethics-focused Path
        ethics_path = [
            "AI_FUNDAMENTALS", "AI_ETHICS", "ML_FUNDAMENTALS",
            "DEEP_LEARNING", "ADVANCED_ML", "CAPSTONE_PROJECT"
        ]
        paths.append(ethics_path)
        
        return paths
    
    def generate_curriculum_graph(self, curriculum: CurriculumGraph) -> str:
        """Generate a visual representation of the curriculum graph"""
        try:
            import matplotlib.pyplot as plt
            import networkx as nx
            
            # Create directed graph
            G = nx.DiGraph()
            
            # Add nodes (courses)
            for course_id, course in curriculum.courses.items():
                G.add_node(course_id, 
                          title=course.title,
                          level=course.level,
                          credits=course.credits,
                          year=course.year,
                          semester=course.semester)
            
            # Add edges (prerequisites)
            for course_id, prereqs in curriculum.prerequisites.items():
                for prereq in prereqs:
                    G.add_edge(prereq, course_id)
            
            # Create visualization
            plt.figure(figsize=(20, 16))
            
            # Define layout
            pos = nx.spring_layout(G, k=3, iterations=50)
            
            # Color nodes by year
            year_colors = {1: 'lightblue', 2: 'lightgreen'}
            node_colors = [year_colors.get(curriculum.courses[node].year, 'lightgray') 
                          for node in G.nodes()]
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                 node_size=2000, alpha=0.8)
            
            # Draw edges
            nx.draw_networkx_edges(G, pos, edge_color='gray', 
                                 arrows=True, arrowsize=20, alpha=0.6)
            
            # Draw labels
            labels = {node: f"{curriculum.courses[node].course_code}\n{curriculum.courses[node].title[:30]}..." 
                     for node in G.nodes()}
            nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
            
            # Add title and legend
            plt.title("MS AI Curriculum - Course Prerequisites and Learning Paths", 
                     fontsize=16, fontweight='bold', pad=20)
            
            # Create legend
            year1_patch = mpatches.Patch(color='lightblue', label='Year 1')
            year2_patch = mpatches.Patch(color='lightgreen', label='Year 2')
            plt.legend(handles=[year1_patch, year2_patch], loc='upper right')
            
            plt.axis('off')
            plt.tight_layout()
            
            # Save the graph
            graph_filename = "curriculum_graph.png"
            plt.savefig(graph_filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            return graph_filename
            
        except ImportError:
            print("⚠️  matplotlib not available, skipping graph generation")
            return None
    
    def save_curriculum_data(self, curriculum: CurriculumGraph, filename: str = "curriculum_data.json"):
        """Save curriculum data to JSON file"""
        curriculum_data = {
            'courses': {course_id: asdict(course) for course_id, course in curriculum.courses.items()},
            'prerequisites': curriculum.prerequisites,
            'learning_paths': curriculum.learning_paths,
            'specialization_tracks': curriculum.specialization_tracks,
            'generated_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(curriculum_data, f, indent=2)
        
        print(f"📄 Curriculum data saved to: {filename}")
        return filename

def main():
    """Main function to build the curriculum system"""
    print("🎓 Building MS AI Curriculum System with Prerequisites and Learning Paths")
    print("=" * 80)
    
    # Create curriculum builder
    builder = CurriculumBuilder()
    
    # Build comprehensive curriculum
    curriculum = builder.create_comprehensive_curriculum()
    
    # Generate curriculum graph
    print("\n📊 Generating curriculum graph...")
    graph_file = builder.generate_curriculum_graph(curriculum)
    if graph_file:
        print(f"📈 Curriculum graph saved to: {graph_file}")
    
    # Save curriculum data
    data_file = builder.save_curriculum_data(curriculum)
    
    # Print summary
    print(f"\n✅ Curriculum System Complete!")
    print(f"📚 Total Courses: {len(curriculum.courses)}")
    print(f"🔗 Prerequisite Relationships: {sum(len(prereqs) for prereqs in curriculum.prerequisites.values())}")
    print(f"🛤️  Learning Paths: {len(curriculum.learning_paths)}")
    print(f"🎯 Specialization Tracks: {len(curriculum.specialization_tracks)}")
    
    # Print course summary by year
    year1_courses = [c for c in curriculum.courses.values() if c.year == 1]
    year2_courses = [c for c in curriculum.courses.values() if c.year == 2]
    
    print(f"\n📅 Year 1 Courses ({len(year1_courses)}):")
    for course in year1_courses:
        prereqs = ", ".join(course.prerequisites) if course.prerequisites else "None"
        print(f"   • {course.course_code}: {course.title} (Prereqs: {prereqs})")
    
    print(f"\n📅 Year 2 Courses ({len(year2_courses)}):")
    for course in year2_courses:
        prereqs = ", ".join(course.prerequisites) if course.prerequisites else "None"
        print(f"   • {course.course_code}: {course.title} (Prereqs: {prereqs})")
    
    print(f"\n🎯 Specialization Tracks:")
    for track, courses in curriculum.specialization_tracks.items():
        print(f"   • {track}: {len(courses)} courses")

if __name__ == "__main__":
    main()