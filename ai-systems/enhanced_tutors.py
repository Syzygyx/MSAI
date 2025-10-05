"""
MS AI Curriculum System - Enhanced AI Tutor System
Advanced personalized learning support with human-centered approach
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import random

class LearningStyle(Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"
    MULTIMODAL = "multimodal"

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class TutoringMode(Enum):
    GUIDED_DISCOVERY = "guided_discovery"
    SCAFFOLDED_LEARNING = "scaffolded_learning"
    PEER_COLLABORATION = "peer_collaboration"
    MENTOR_GUIDANCE = "mentor_guidance"
    INDEPENDENT_EXPLORATION = "independent_exploration"

class EmotionalState(Enum):
    CONFIDENT = "confident"
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"
    EXCITED = "excited"
    ANXIOUS = "anxious"
    CURIOUS = "curious"
    OVERWHELMED = "overwhelmed"
    MOTIVATED = "motivated"

@dataclass
class StudentProfile:
    """Comprehensive student learning profile"""
    student_id: str
    name: str
    email: str
    learning_style: LearningStyle
    preferred_difficulty: DifficultyLevel
    current_level: DifficultyLevel
    emotional_state: EmotionalState
    learning_preferences: Dict[str, Any]
    strengths: List[str]
    challenges: List[str]
    goals: List[str]
    interests: List[str]
    cultural_background: str
    language_preference: str
    accessibility_needs: List[str]
    created_at: datetime
    last_updated: datetime
    total_sessions: int = 0
    total_hours: float = 0.0
    progress_score: float = 0.0

@dataclass
class TutoringSession:
    """Individual tutoring session"""
    session_id: str
    student_id: str
    tutor_id: str
    course_id: str
    topic: str
    session_type: str
    mode: TutoringMode
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: float = 0.0
    objectives: List[str] = field(default_factory=list)
    activities: List[Dict[str, Any]] = field(default_factory=list)
    student_responses: List[Dict[str, Any]] = field(default_factory=list)
    tutor_feedback: List[Dict[str, Any]] = field(default_factory=list)
    emotional_journey: List[Dict[str, Any]] = field(default_factory=list)
    learning_outcomes: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    session_rating: Optional[float] = None
    student_feedback: Optional[str] = None

@dataclass
class LearningPath:
    """Personalized learning path for student"""
    path_id: str
    student_id: str
    course_id: str
    current_topic: str
    topics_sequence: List[str]
    completed_topics: List[str]
    learning_milestones: List[Dict[str, Any]]
    adaptive_adjustments: List[Dict[str, Any]]
    created_at: datetime
    last_updated: datetime
    estimated_completion_time: int = 0  # days
    progress_percentage: float = 0.0

@dataclass
class AITutor:
    """AI Tutor with human-centered approach"""
    tutor_id: str
    name: str
    specialization: str
    personality_traits: List[str]
    teaching_philosophy: str
    communication_style: str
    expertise_areas: List[str]
    emotional_intelligence_level: str
    cultural_sensitivity: str
    accessibility_support: List[str]
    status: str = "active"
    total_sessions: int = 0
    average_rating: float = 0.0
    student_satisfaction: float = 0.0

class EnhancedAITutorSystem:
    """Advanced AI Tutor system with human-centered learning"""
    
    def __init__(self, professor_system=None):
        self.professor_system = professor_system
        self.student_profiles: Dict[str, StudentProfile] = {}
        self.tutoring_sessions: Dict[str, TutoringSession] = {}
        self.learning_paths: Dict[str, LearningPath] = {}
        self.ai_tutors = self._initialize_ai_tutors()
        
    def _initialize_ai_tutors(self) -> List[AITutor]:
        """Initialize AI tutors with distinct personalities and specializations"""
        return [
            AITutor(
                tutor_id="TUTOR_001",
                name="Alex Chen",
                specialization="Machine Learning Fundamentals",
                personality_traits=["patient", "encouraging", "analytical", "empathetic"],
                teaching_philosophy="Learning happens best when students feel supported and can make connections to their own experiences",
                communication_style="Warm and encouraging, with clear explanations and plenty of examples",
                expertise_areas=["Supervised Learning", "Model Evaluation", "Feature Engineering", "Python Programming"],
                emotional_intelligence_level="high",
                cultural_sensitivity="high",
                accessibility_support=["Visual learners", "Non-native English speakers", "Learning differences"]
            ),
            AITutor(
                tutor_id="TUTOR_002",
                name="Jordan Rodriguez",
                specialization="Deep Learning and Neural Networks",
                personality_traits=["enthusiastic", "creative", "innovative", "supportive"],
                teaching_philosophy="Every student has unique strengths, and learning should be an exciting journey of discovery",
                communication_style="Energetic and inspiring, using analogies and visual explanations",
                expertise_areas=["Neural Networks", "Computer Vision", "Natural Language Processing", "PyTorch"],
                emotional_intelligence_level="high",
                cultural_sensitivity="high",
                accessibility_support=["Kinesthetic learners", "Creative thinkers", "Visual learners"]
            ),
            AITutor(
                tutor_id="TUTOR_003",
                name="Sam Patel",
                specialization="AI Ethics and Responsible Development",
                personality_traits=["thoughtful", "compassionate", "ethical", "inclusive"],
                teaching_philosophy="Learning should empower students to make positive contributions to society",
                communication_style="Thoughtful and inclusive, encouraging critical thinking and ethical reasoning",
                expertise_areas=["AI Ethics", "Bias Detection", "Fairness", "Responsible AI"],
                emotional_intelligence_level="very_high",
                cultural_sensitivity="very_high",
                accessibility_support=["All learning styles", "Diverse backgrounds", "Ethical considerations"]
            ),
            AITutor(
                tutor_id="TUTOR_004",
                name="Casey Kim",
                specialization="Data Science and Analytics",
                personality_traits=["practical", "collaborative", "problem-solving", "adaptable"],
                teaching_philosophy="Learning is most effective when it's collaborative and connected to real-world problems",
                communication_style="Collaborative and practical, focusing on real-world applications",
                expertise_areas=["Data Analysis", "Statistics", "Data Visualization", "SQL"],
                emotional_intelligence_level="high",
                cultural_sensitivity="high",
                accessibility_support=["Practical learners", "Collaborative learners", "Problem-solvers"]
            )
        ]
    
    def create_student_profile(self, student_id: str, name: str, email: str, 
                             initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive student learning profile"""
        
        # Assess learning style
        learning_style = self._assess_learning_style(initial_data.get("learning_style_quiz", {}))
        
        # Determine initial difficulty level
        difficulty_level = self._assess_initial_difficulty(initial_data.get("background", {}))
        
        # Create profile
        profile = StudentProfile(
            student_id=student_id,
            name=name,
            email=email,
            learning_style=learning_style,
            preferred_difficulty=difficulty_level,
            current_level=difficulty_level,
            emotional_state=EmotionalState.CURIOUS,
            learning_preferences=initial_data.get("preferences", {}),
            strengths=initial_data.get("strengths", []),
            challenges=initial_data.get("challenges", []),
            goals=initial_data.get("goals", []),
            interests=initial_data.get("interests", []),
            cultural_background=initial_data.get("cultural_background", "Not specified"),
            language_preference=initial_data.get("language_preference", "English"),
            accessibility_needs=initial_data.get("accessibility_needs", []),
            created_at=datetime.now(),
            last_updated=datetime.now()
        )
        
        self.student_profiles[student_id] = profile
        
        # Create initial learning path
        learning_path = self._create_initial_learning_path(student_id, profile)
        self.learning_paths[student_id] = learning_path
        
        return {
            "success": True,
            "student_id": student_id,
            "profile_created": True,
            "learning_style": learning_style.value,
            "initial_difficulty": difficulty_level.value,
            "learning_path_id": learning_path.path_id
        }
    
    def _assess_learning_style(self, quiz_responses: Dict[str, Any]) -> LearningStyle:
        """Assess student's learning style from quiz responses"""
        if not quiz_responses:
            return LearningStyle.MULTIMODAL
        
        # Simple scoring system
        scores = {
            "visual": 0,
            "auditory": 0,
            "kinesthetic": 0,
            "reading_writing": 0
        }
        
        # Analyze responses (simplified)
        for response in quiz_responses.values():
            if "visual" in str(response).lower():
                scores["visual"] += 1
            elif "audio" in str(response).lower() or "listen" in str(response).lower():
                scores["auditory"] += 1
            elif "hands" in str(response).lower() or "practice" in str(response).lower():
                scores["kinesthetic"] += 1
            elif "read" in str(response).lower() or "write" in str(response).lower():
                scores["reading_writing"] += 1
        
        # Return dominant style or multimodal if tied
        max_score = max(scores.values())
        if max_score == 0:
            return LearningStyle.MULTIMODAL
        
        dominant_styles = [style for style, score in scores.items() if score == max_score]
        
        if len(dominant_styles) > 1:
            return LearningStyle.MULTIMODAL
        else:
            return LearningStyle(dominant_styles[0])
    
    def _assess_initial_difficulty(self, background: Dict[str, Any]) -> DifficultyLevel:
        """Assess initial difficulty level based on student background"""
        programming_experience = background.get("programming_experience", "none")
        math_background = background.get("math_background", "basic")
        ai_knowledge = background.get("ai_knowledge", "none")
        
        # Scoring system
        score = 0
        
        # Programming experience
        if programming_experience == "expert":
            score += 3
        elif programming_experience == "advanced":
            score += 2
        elif programming_experience == "intermediate":
            score += 1
        
        # Math background
        if math_background == "advanced":
            score += 2
        elif math_background == "intermediate":
            score += 1
        
        # AI knowledge
        if ai_knowledge == "advanced":
            score += 2
        elif ai_knowledge == "intermediate":
            score += 1
        
        # Determine difficulty level
        if score >= 5:
            return DifficultyLevel.ADVANCED
        elif score >= 3:
            return DifficultyLevel.INTERMEDIATE
        else:
            return DifficultyLevel.BEGINNER
    
    def _create_initial_learning_path(self, student_id: str, profile: StudentProfile) -> LearningPath:
        """Create initial personalized learning path"""
        path_id = f"PATH_{uuid.uuid4().hex[:8]}"
        
        # Generate topic sequence based on profile
        topics_sequence = self._generate_topic_sequence(profile)
        
        learning_path = LearningPath(
            path_id=path_id,
            student_id=student_id,
            course_id="AI501",  # Default to first course
            current_topic=topics_sequence[0] if topics_sequence else "Introduction to AI",
            topics_sequence=topics_sequence,
            completed_topics=[],
            learning_milestones=self._generate_learning_milestones(topics_sequence),
            adaptive_adjustments=[],
            created_at=datetime.now(),
            last_updated=datetime.now(),
            estimated_completion_time=len(topics_sequence) * 7,  # 7 days per topic
            progress_percentage=0.0
        )
        
        return learning_path
    
    def _generate_topic_sequence(self, profile: StudentProfile) -> List[str]:
        """Generate personalized topic sequence"""
        base_topics = [
            "Introduction to AI",
            "Problem Solving and Search",
            "Knowledge Representation",
            "Machine Learning Basics",
            "Neural Networks",
            "Expert Systems",
            "AI Ethics",
            "Future of AI"
        ]
        
        # Adjust sequence based on profile
        if profile.interests:
            # Prioritize topics based on interests
            if "machine learning" in profile.interests:
                base_topics.insert(3, "Advanced Machine Learning")
            if "ethics" in profile.interests:
                base_topics.insert(6, "AI Ethics Deep Dive")
        
        return base_topics
    
    def _generate_learning_milestones(self, topics: List[str]) -> List[Dict[str, Any]]:
        """Generate learning milestones for topics"""
        milestones = []
        
        for i, topic in enumerate(topics):
            milestone = {
                "milestone_id": f"MILESTONE_{i+1}",
                "topic": topic,
                "description": f"Complete understanding of {topic}",
                "target_date": datetime.now() + timedelta(days=(i+1)*7),
                "skills_to_demonstrate": [
                    f"Explain {topic} concepts",
                    f"Apply {topic} to solve problems",
                    f"Analyze {topic} applications"
                ],
                "assessment_methods": ["quiz", "practical_exercise", "discussion"],
                "completed": False
            }
            milestones.append(milestone)
        
        return milestones
    
    def start_tutoring_session(self, student_id: str, course_id: str, topic: str, 
                              session_type: str = "guided_learning") -> Dict[str, Any]:
        """Start a new tutoring session"""
        profile = self.student_profiles.get(student_id)
        if not profile:
            return {"success": False, "error": "Student profile not found"}
        
        # Select appropriate tutor
        tutor = self._select_optimal_tutor(profile, course_id, topic)
        
        # Create session
        session_id = f"SESSION_{uuid.uuid4().hex[:8]}"
        
        session = TutoringSession(
            session_id=session_id,
            student_id=student_id,
            tutor_id=tutor.tutor_id,
            course_id=course_id,
            topic=topic,
            session_type=session_type,
            mode=self._determine_tutoring_mode(profile, topic),
            start_time=datetime.now(),
            objectives=self._generate_session_objectives(topic, profile),
            activities=self._generate_session_activities(topic, profile, tutor),
            emotional_journey=[{
                "timestamp": datetime.now(),
                "state": profile.emotional_state.value,
                "context": "Session started"
            }]
        )
        
        self.tutoring_sessions[session_id] = session
        
        # Update profile
        profile.total_sessions += 1
        profile.last_updated = datetime.now()
        
        return {
            "success": True,
            "session_id": session_id,
            "tutor_name": tutor.name,
            "tutor_specialization": tutor.specialization,
            "session_mode": session.mode.value,
            "objectives": session.objectives,
            "estimated_duration": 45  # minutes
        }
    
    def _select_optimal_tutor(self, profile: StudentProfile, course_id: str, topic: str) -> AITutor:
        """Select the most appropriate tutor for the student and topic"""
        # Score tutors based on compatibility
        tutor_scores = {}
        
        for tutor in self.ai_tutors:
            score = 0
            
            # Match specialization to topic
            if topic.lower() in tutor.specialization.lower():
                score += 3
            
            # Match expertise areas
            for area in tutor.expertise_areas:
                if area.lower() in topic.lower():
                    score += 2
            
            # Consider learning style compatibility
            if profile.learning_style == LearningStyle.VISUAL and "Visual" in tutor.accessibility_support:
                score += 1
            elif profile.learning_style == LearningStyle.KINESTHETIC and "Kinesthetic" in tutor.accessibility_support:
                score += 1
            
            # Consider cultural sensitivity
            if profile.cultural_background != "Not specified" and tutor.cultural_sensitivity == "very_high":
                score += 1
            
            # Consider accessibility needs
            for need in profile.accessibility_needs:
                if need in tutor.accessibility_support:
                    score += 1
            
            tutor_scores[tutor.tutor_id] = score
        
        # Select tutor with highest score
        best_tutor_id = max(tutor_scores, key=tutor_scores.get)
        return next(tutor for tutor in self.ai_tutors if tutor.tutor_id == best_tutor_id)
    
    def _determine_tutoring_mode(self, profile: StudentProfile, topic: str) -> TutoringMode:
        """Determine optimal tutoring mode based on profile and topic"""
        # Consider emotional state
        if profile.emotional_state == EmotionalState.FRUSTRATED:
            return TutoringMode.SCAFFOLDED_LEARNING
        elif profile.emotional_state == EmotionalState.CONFUSED:
            return TutoringMode.GUIDED_DISCOVERY
        elif profile.emotional_state == EmotionalState.CURIOUS:
            return TutoringMode.INDEPENDENT_EXPLORATION
        elif profile.emotional_state == EmotionalState.CONFIDENT:
            return TutoringMode.PEER_COLLABORATION
        else:
            return TutoringMode.MENTOR_GUIDANCE
    
    def _generate_session_objectives(self, topic: str, profile: StudentProfile) -> List[str]:
        """Generate session objectives based on topic and profile"""
        objectives = [
            f"Understand key concepts in {topic}",
            f"Apply {topic} knowledge to solve problems",
            f"Connect {topic} to real-world applications"
        ]
        
        # Add personalized objectives based on profile
        if profile.challenges:
            objectives.append(f"Address specific challenges in {topic}")
        
        if profile.goals:
            objectives.append(f"Progress toward personal learning goals")
        
        return objectives
    
    def _generate_session_activities(self, topic: str, profile: StudentProfile, tutor: AITutor) -> List[Dict[str, Any]]:
        """Generate session activities based on learning style and tutor"""
        activities = []
        
        # Base activities
        activities.append({
            "activity_id": f"ACT_{uuid.uuid4().hex[:8]}",
            "type": "concept_explanation",
            "title": f"Introduction to {topic}",
            "description": f"Explore fundamental concepts of {topic}",
            "duration_minutes": 10,
            "learning_style": "multimodal"
        })
        
        # Add activities based on learning style
        if profile.learning_style == LearningStyle.VISUAL:
            activities.append({
                "activity_id": f"ACT_{uuid.uuid4().hex[:8]}",
                "type": "visual_demonstration",
                "title": f"Visualizing {topic}",
                "description": f"Use diagrams and visual aids to understand {topic}",
                "duration_minutes": 15,
                "learning_style": "visual"
            })
        elif profile.learning_style == LearningStyle.KINESTHETIC:
            activities.append({
                "activity_id": f"ACT_{uuid.uuid4().hex[:8]}",
                "type": "hands_on_practice",
                "title": f"Hands-on {topic}",
                "description": f"Practice {topic} concepts through interactive exercises",
                "duration_minutes": 20,
                "learning_style": "kinesthetic"
            })
        
        # Add tutor-specific activities
        if "creative" in tutor.personality_traits:
            activities.append({
                "activity_id": f"ACT_{uuid.uuid4().hex[:8]}",
                "type": "creative_exploration",
                "title": f"Creative {topic} Project",
                "description": f"Explore {topic} through creative problem-solving",
                "duration_minutes": 15,
                "learning_style": "creative"
            })
        
        return activities
    
    def conduct_tutoring_session(self, session_id: str, student_responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Conduct tutoring session with student interactions"""
        session = self.tutoring_sessions.get(session_id)
        if not session:
            return {"success": False, "error": "Session not found"}
        
        # Update session with student responses
        session.student_responses.extend(student_responses)
        
        # Generate tutor feedback
        tutor_feedback = self._generate_tutor_feedback(session, student_responses)
        session.tutor_feedback.extend(tutor_feedback)
        
        # Track emotional journey
        emotional_state = self._assess_emotional_state(student_responses)
        session.emotional_journey.append({
            "timestamp": datetime.now(),
            "state": emotional_state.value,
            "context": "During session interaction"
        })
        
        # Generate learning outcomes
        learning_outcomes = self._generate_learning_outcomes(session, student_responses)
        session.learning_outcomes.extend(learning_outcomes)
        
        # Generate next steps
        next_steps = self._generate_next_steps(session, student_responses)
        session.next_steps.extend(next_steps)
        
        return {
            "success": True,
            "session_id": session_id,
            "tutor_feedback": tutor_feedback,
            "emotional_state": emotional_state.value,
            "learning_outcomes": learning_outcomes,
            "next_steps": next_steps,
            "session_progress": len(session.student_responses) / len(session.activities) * 100
        }
    
    def _generate_tutor_feedback(self, session: TutoringSession, responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate personalized tutor feedback"""
        tutor = next(tutor for tutor in self.ai_tutors if tutor.tutor_id == session.tutor_id)
        feedback = []
        
        for response in responses:
            # Analyze response quality
            quality_score = self._assess_response_quality(response)
            
            # Generate feedback based on tutor's personality
            if "encouraging" in tutor.personality_traits:
                if quality_score >= 7:
                    feedback_text = f"Excellent work! Your understanding of {session.topic} is really coming together. Keep up the great progress!"
                elif quality_score >= 5:
                    feedback_text = f"Good effort! You're making solid progress with {session.topic}. Let's build on this foundation."
                else:
                    feedback_text = f"I can see you're working hard on {session.topic}. Let's break this down into smaller steps - you've got this!"
            
            elif "analytical" in tutor.personality_traits:
                if quality_score >= 7:
                    feedback_text = f"Your analysis of {session.topic} demonstrates strong conceptual understanding. The logical connections you're making are excellent."
                elif quality_score >= 5:
                    feedback_text = f"Your approach to {session.topic} shows good analytical thinking. Let's refine some of the technical details."
                else:
                    feedback_text = f"Let's analyze {session.topic} more systematically. I'll help you break down the key components."
            
            feedback.append({
                "feedback_id": f"FB_{uuid.uuid4().hex[:8]}",
                "response_id": response.get("response_id"),
                "feedback_text": feedback_text,
                "quality_score": quality_score,
                "suggestions": self._generate_suggestions(response, quality_score),
                "encouragement": self._generate_encouragement(tutor, quality_score),
                "timestamp": datetime.now()
            })
        
        return feedback
    
    def _assess_response_quality(self, response: Dict[str, Any]) -> float:
        """Assess quality of student response"""
        # Simple scoring based on response characteristics
        score = 5.0  # Base score
        
        response_text = response.get("response", "").lower()
        
        # Positive indicators
        if len(response_text) > 50:
            score += 1
        if any(word in response_text for word in ["because", "therefore", "however", "analysis"]):
            score += 1
        if any(word in response_text for word in ["example", "instance", "case"]):
            score += 1
        if any(word in response_text for word in ["understand", "learned", "realize"]):
            score += 1
        
        # Negative indicators
        if "don't know" in response_text or "confused" in response_text:
            score -= 1
        if len(response_text) < 10:
            score -= 1
        
        return max(0, min(10, score))
    
    def _generate_suggestions(self, response: Dict[str, Any], quality_score: float) -> List[str]:
        """Generate suggestions for improvement"""
        suggestions = []
        
        if quality_score < 5:
            suggestions.extend([
                "Try to provide more specific examples",
                "Consider explaining your reasoning step by step",
                "Connect this concept to something you already know"
            ])
        elif quality_score < 7:
            suggestions.extend([
                "Great start! Now try to go deeper into the details",
                "Consider the broader implications of this concept",
                "Think about how this applies to real-world situations"
            ])
        else:
            suggestions.extend([
                "Excellent understanding! Now try to teach this concept to someone else",
                "Consider exploring advanced applications of this concept",
                "Think about how this connects to other topics you've learned"
            ])
        
        return suggestions
    
    def _generate_encouragement(self, tutor: AITutor, quality_score: float) -> str:
        """Generate encouragement based on tutor personality"""
        if "empathetic" in tutor.personality_traits:
            return "Remember, learning is a journey, and every step forward is progress worth celebrating!"
        elif "enthusiastic" in tutor.personality_traits:
            return "Your curiosity and effort are inspiring! Keep exploring and asking great questions!"
        elif "patient" in tutor.personality_traits:
            return "Take your time - understanding comes at your own pace, and that's perfectly okay!"
        else:
            return "You're doing great work! Keep pushing forward with your learning!"
    
    def _assess_emotional_state(self, responses: List[Dict[str, Any]]) -> EmotionalState:
        """Assess student's current emotional state from responses"""
        # Analyze response patterns for emotional indicators
        emotional_indicators = {
            "confident": 0,
            "confused": 0,
            "frustrated": 0,
            "excited": 0,
            "anxious": 0,
            "curious": 0,
            "overwhelmed": 0,
            "motivated": 0
        }
        
        for response in responses:
            response_text = response.get("response", "").lower()
            
            # Look for emotional keywords
            if any(word in response_text for word in ["confident", "sure", "understand", "got it"]):
                emotional_indicators["confident"] += 1
            if any(word in response_text for word in ["confused", "don't understand", "unclear"]):
                emotional_indicators["confused"] += 1
            if any(word in response_text for word in ["frustrated", "difficult", "hard", "struggling"]):
                emotional_indicators["frustrated"] += 1
            if any(word in response_text for word in ["excited", "interesting", "cool", "amazing"]):
                emotional_indicators["excited"] += 1
            if any(word in response_text for word in ["anxious", "worried", "nervous", "concerned"]):
                emotional_indicators["anxious"] += 1
            if any(word in response_text for word in ["curious", "wonder", "question", "explore"]):
                emotional_indicators["curious"] += 1
            if any(word in response_text for word in ["overwhelmed", "too much", "complex", "complicated"]):
                emotional_indicators["overwhelmed"] += 1
            if any(word in response_text for word in ["motivated", "ready", "want to learn", "determined"]):
                emotional_indicators["motivated"] += 1
        
        # Return dominant emotional state
        max_count = max(emotional_indicators.values())
        if max_count == 0:
            return EmotionalState.CURIOUS  # Default
        
        dominant_emotions = [emotion for emotion, count in emotional_indicators.items() if count == max_count]
        return EmotionalState(dominant_emotions[0])
    
    def _generate_learning_outcomes(self, session: TutoringSession, responses: List[Dict[str, Any]]) -> List[str]:
        """Generate learning outcomes from session"""
        outcomes = []
        
        # Analyze responses for learning indicators
        for response in responses:
            response_text = response.get("response", "").lower()
            
            if "understand" in response_text or "learned" in response_text:
                outcomes.append(f"Demonstrated understanding of {session.topic} concepts")
            
            if "apply" in response_text or "use" in response_text:
                outcomes.append(f"Showed ability to apply {session.topic} knowledge")
            
            if "connect" in response_text or "relate" in response_text:
                outcomes.append(f"Made connections between {session.topic} and other concepts")
        
        return outcomes
    
    def _generate_next_steps(self, session: TutoringSession, responses: List[Dict[str, Any]]) -> List[str]:
        """Generate next steps for continued learning"""
        next_steps = []
        
        # Analyze session progress
        if len(session.student_responses) >= len(session.activities) * 0.8:
            next_steps.extend([
                f"Practice applying {session.topic} concepts independently",
                f"Explore advanced applications of {session.topic}",
                f"Connect {session.topic} to real-world problems"
            ])
        else:
            next_steps.extend([
                f"Review fundamental concepts of {session.topic}",
                f"Practice with simpler {session.topic} examples",
                f"Schedule follow-up session to continue {session.topic} learning"
            ])
        
        return next_steps
    
    def end_tutoring_session(self, session_id: str, student_rating: float, 
                           student_feedback: str) -> Dict[str, Any]:
        """End tutoring session and update records"""
        session = self.tutoring_sessions.get(session_id)
        if not session:
            return {"success": False, "error": "Session not found"}
        
        # Update session
        session.end_time = datetime.now()
        session.duration_minutes = (session.end_time - session.start_time).total_seconds() / 60
        session.session_rating = student_rating
        session.student_feedback = student_feedback
        
        # Update student profile
        profile = self.student_profiles[session.student_id]
        profile.total_hours += session.duration_minutes / 60
        profile.last_updated = datetime.now()
        
        # Update tutor stats
        tutor = next(tutor for tutor in self.ai_tutors if tutor.tutor_id == session.tutor_id)
        tutor.total_sessions += 1
        tutor.average_rating = (tutor.average_rating * (tutor.total_sessions - 1) + student_rating) / tutor.total_sessions
        
        # Update learning path progress
        learning_path = self.learning_paths.get(session.student_id)
        if learning_path and session.topic in learning_path.topics_sequence:
            if session.topic not in learning_path.completed_topics:
                learning_path.completed_topics.append(session.topic)
                learning_path.progress_percentage = len(learning_path.completed_topics) / len(learning_path.topics_sequence) * 100
                learning_path.last_updated = datetime.now()
        
        return {
            "success": True,
            "session_id": session_id,
            "duration_minutes": session.duration_minutes,
            "learning_outcomes": session.learning_outcomes,
            "next_steps": session.next_steps,
            "updated_progress": learning_path.progress_percentage if learning_path else 0
        }
    
    def get_student_progress(self, student_id: str) -> Dict[str, Any]:
        """Get comprehensive student progress report"""
        profile = self.student_profiles.get(student_id)
        if not profile:
            return {"error": "Student profile not found"}
        
        learning_path = self.learning_paths.get(student_id)
        student_sessions = [s for s in self.tutoring_sessions.values() if s.student_id == student_id]
        
        return {
            "student_id": student_id,
            "profile": {
                "name": profile.name,
                "learning_style": profile.learning_style.value,
                "current_level": profile.current_level.value,
                "emotional_state": profile.emotional_state.value,
                "total_sessions": profile.total_sessions,
                "total_hours": profile.total_hours,
                "progress_score": profile.progress_score
            },
            "learning_path": {
                "current_topic": learning_path.current_topic if learning_path else "Not started",
                "progress_percentage": learning_path.progress_percentage if learning_path else 0,
                "completed_topics": learning_path.completed_topics if learning_path else [],
                "remaining_topics": learning_path.topics_sequence[len(learning_path.completed_topics):] if learning_path else []
            },
            "recent_sessions": [
                {
                    "session_id": s.session_id,
                    "topic": s.topic,
                    "tutor_id": s.tutor_id,
                    "duration_minutes": s.duration_minutes,
                    "rating": s.session_rating,
                    "date": s.start_time.isoformat()
                }
                for s in sorted(student_sessions, key=lambda x: x.start_time, reverse=True)[:5]
            ],
            "recommendations": self._generate_student_recommendations(profile, learning_path)
        }
    
    def _generate_student_recommendations(self, profile: StudentProfile, learning_path: LearningPath) -> List[str]:
        """Generate personalized recommendations for student"""
        recommendations = []
        
        # Based on emotional state
        if profile.emotional_state == EmotionalState.FRUSTRATED:
            recommendations.append("Consider taking a break and returning with a fresh perspective")
            recommendations.append("Try breaking down complex topics into smaller, manageable pieces")
        
        elif profile.emotional_state == EmotionalState.CONFUSED:
            recommendations.append("Schedule additional tutoring sessions for challenging topics")
            recommendations.append("Try different learning approaches (visual, hands-on, etc.)")
        
        elif profile.emotional_state == EmotionalState.CURIOUS:
            recommendations.append("Explore advanced topics and real-world applications")
            recommendations.append("Consider joining study groups or peer learning sessions")
        
        # Based on learning style
        if profile.learning_style == LearningStyle.VISUAL:
            recommendations.append("Use diagrams, charts, and visual aids in your studies")
            recommendations.append("Watch demonstration videos and tutorials")
        
        elif profile.learning_style == LearningStyle.KINESTHETIC:
            recommendations.append("Engage in hands-on projects and practical exercises")
            recommendations.append("Try coding exercises and interactive simulations")
        
        # Based on progress
        if learning_path and learning_path.progress_percentage < 30:
            recommendations.append("Focus on building strong foundational knowledge")
            recommendations.append("Don't rush - take time to fully understand each concept")
        
        elif learning_path and learning_path.progress_percentage > 70:
            recommendations.append("Consider exploring advanced topics and specializations")
            recommendations.append("Share your knowledge by helping other students")
        
        return recommendations