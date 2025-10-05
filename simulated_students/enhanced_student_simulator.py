"""
MS AI Curriculum System - Enhanced Student Simulator
Advanced simulated students with human-like learning behaviors and neural network training
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import random
import asyncio
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class LearningStyle(Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"
    MULTIMODAL = "multimodal"

class StudentLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class EmotionalState(Enum):
    CONFIDENT = "confident"
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"
    EXCITED = "excited"
    ANXIOUS = "anxious"
    CURIOUS = "curious"
    OVERWHELMED = "overwhelmed"
    MOTIVATED = "motivated"

class AssignmentType(Enum):
    LECTURE = "lecture"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    PROJECT = "project"
    EXAM = "exam"
    TUTORIAL = "tutorial"
    READING = "reading"
    NEURAL_NETWORK_PROJECT = "neural_network_project"

@dataclass
class SimulatedStudent:
    """Enhanced simulated student with human-like characteristics"""
    student_id: str
    name: str
    email: str
    learning_style: LearningStyle
    current_level: StudentLevel
    emotional_state: EmotionalState
    background: Dict[str, Any]
    strengths: List[str]
    challenges: List[str]
    interests: List[str]
    goals: List[str]
    cultural_background: str
    language_preference: str
    accessibility_needs: List[str]
    created_at: datetime
    last_activity: datetime
    total_study_hours: float = 0.0
    courses_enrolled: List[str] = field(default_factory=list)
    assignments_completed: List[str] = field(default_factory=list)
    current_gpa: float = 0.0
    learning_progress: Dict[str, float] = field(default_factory=dict)
    interaction_history: List[Dict[str, Any]] = field(default_factory=list)
    neural_network_projects: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class NeuralNetworkProject:
    """Neural network project completed by student"""
    project_id: str
    student_id: str
    course_id: str
    project_type: str
    dataset_type: str
    model_architecture: str
    training_metrics: Dict[str, float]
    model_performance: Dict[str, float]
    created_at: datetime
    completion_time_minutes: int
    code_snippets: List[str] = field(default_factory=list)
    insights_discovered: List[str] = field(default_factory=list)

class NeuralNetworkTrainer:
    """Advanced neural network training system for students"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_templates = self._initialize_model_templates()
        
    def _initialize_model_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize neural network model templates"""
        return {
            "simple_classifier": {
                "description": "Simple feedforward neural network for classification",
                "architecture": "feedforward",
                "layers": [64, 32, 16],
                "activation": "relu",
                "output_activation": "softmax",
                "use_case": "Binary and multi-class classification"
            },
            "regression_network": {
                "description": "Neural network for regression tasks",
                "architecture": "feedforward",
                "layers": [128, 64, 32],
                "activation": "relu",
                "output_activation": "linear",
                "use_case": "Continuous value prediction"
            },
            "cnn_classifier": {
                "description": "Convolutional Neural Network for image classification",
                "architecture": "cnn",
                "layers": [32, 64, 128],
                "activation": "relu",
                "output_activation": "softmax",
                "use_case": "Image classification and computer vision"
            },
            "rnn_classifier": {
                "description": "Recurrent Neural Network for sequence data",
                "architecture": "rnn",
                "layers": [64, 32],
                "activation": "tanh",
                "output_activation": "softmax",
                "use_case": "Text classification and sequence modeling"
            }
        }
    
    def create_model(self, architecture: str, input_size: int, output_size: int, 
                    hidden_layers: List[int] = None) -> nn.Module:
        """Create neural network model"""
        if architecture == "feedforward":
            return self._create_feedforward_model(input_size, output_size, hidden_layers or [64, 32])
        elif architecture == "cnn":
            return self._create_cnn_model(input_size, output_size, hidden_layers or [32, 64])
        elif architecture == "rnn":
            return self._create_rnn_model(input_size, output_size, hidden_layers or [64, 32])
        else:
            raise ValueError(f"Unknown architecture: {architecture}")
    
    def _create_feedforward_model(self, input_size: int, output_size: int, hidden_layers: List[int]) -> nn.Module:
        """Create feedforward neural network"""
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_layers:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.ReLU(),
                nn.Dropout(0.2)
            ])
            prev_size = hidden_size
        
        layers.append(nn.Linear(prev_size, output_size))
        
        return nn.Sequential(*layers)
    
    def _create_cnn_model(self, input_size: int, output_size: int, hidden_layers: List[int]) -> nn.Module:
        """Create CNN model"""
        class SimpleCNN(nn.Module):
            def __init__(self, input_channels=1, num_classes=output_size):
                super(SimpleCNN, self).__init__()
                self.conv1 = nn.Conv2d(input_channels, 32, kernel_size=3, padding=1)
                self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
                self.pool = nn.MaxPool2d(2, 2)
                self.fc1 = nn.Linear(64 * 7 * 7, 128)
                self.fc2 = nn.Linear(128, num_classes)
                self.dropout = nn.Dropout(0.2)
                
            def forward(self, x):
                x = self.pool(torch.relu(self.conv1(x)))
                x = self.pool(torch.relu(self.conv2(x)))
                x = x.view(-1, 64 * 7 * 7)
                x = torch.relu(self.fc1(x))
                x = self.dropout(x)
                x = self.fc2(x)
                return x
        
        return SimpleCNN()
    
    def _create_rnn_model(self, input_size: int, output_size: int, hidden_layers: List[int]) -> nn.Module:
        """Create RNN model"""
        class SimpleRNN(nn.Module):
            def __init__(self, input_size=input_size, hidden_size=hidden_layers[0], 
                        num_layers=len(hidden_layers), num_classes=output_size):
                super(SimpleRNN, self).__init__()
                self.hidden_size = hidden_size
                self.num_layers = num_layers
                self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
                self.fc = nn.Linear(hidden_size, num_classes)
                
            def forward(self, x):
                h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
                out, _ = self.rnn(x, h0)
                out = self.fc(out[:, -1, :])
                return out
        
        return SimpleRNN()
    
    def create_dataset(self, dataset_type: str, n_samples: int = 1000, n_features: int = 20) -> Tuple[np.ndarray, np.ndarray]:
        """Create synthetic dataset for training"""
        if dataset_type == "classification":
            X, y = make_classification(
                n_samples=n_samples,
                n_features=n_features,
                n_informative=n_features//2,
                n_redundant=n_features//4,
                n_classes=2,
                random_state=42
            )
        elif dataset_type == "regression":
            X, y = make_regression(
                n_samples=n_samples,
                n_features=n_features,
                noise=0.1,
                random_state=42
            )
        elif dataset_type == "multiclass":
            X, y = make_classification(
                n_samples=n_samples,
                n_features=n_features,
                n_informative=n_features//2,
                n_classes=3,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
        
        return X, y
    
    def train_model(self, model: nn.Module, X_train: np.ndarray, y_train: np.ndarray,
                   X_val: np.ndarray, y_val: np.ndarray, epochs: int = 100,
                   learning_rate: float = 0.001) -> Dict[str, List[float]]:
        """Train neural network model"""
        model = model.to(self.device)
        
        # Convert to PyTorch tensors
        X_train_tensor = torch.FloatTensor(X_train).to(self.device)
        y_train_tensor = torch.LongTensor(y_train).to(self.device) if len(np.unique(y_train)) < 10 else torch.FloatTensor(y_train).to(self.device)
        X_val_tensor = torch.FloatTensor(X_val).to(self.device)
        y_val_tensor = torch.LongTensor(y_val).to(self.device) if len(np.unique(y_val)) < 10 else torch.FloatTensor(y_val).to(self.device)
        
        # Define loss and optimizer
        if len(np.unique(y_train)) < 10:  # Classification
            criterion = nn.CrossEntropyLoss()
        else:  # Regression
            criterion = nn.MSELoss()
        
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        
        # Training history
        train_losses = []
        val_losses = []
        train_accuracies = []
        val_accuracies = []
        
        for epoch in range(epochs):
            # Training
            model.train()
            optimizer.zero_grad()
            outputs = model(X_train_tensor)
            loss = criterion(outputs, y_train_tensor)
            loss.backward()
            optimizer.step()
            
            train_losses.append(loss.item())
            
            # Validation
            model.eval()
            with torch.no_grad():
                val_outputs = model(X_val_tensor)
                val_loss = criterion(val_outputs, y_val_tensor)
                val_losses.append(val_loss.item())
                
                # Calculate accuracy for classification
                if len(np.unique(y_train)) < 10:
                    train_acc = (torch.argmax(outputs, dim=1) == y_train_tensor).float().mean().item()
                    val_acc = (torch.argmax(val_outputs, dim=1) == y_val_tensor).float().mean().item()
                    train_accuracies.append(train_acc)
                    val_accuracies.append(val_acc)
        
        return {
            "train_losses": train_losses,
            "val_losses": val_losses,
            "train_accuracies": train_accuracies,
            "val_accuracies": val_accuracies
        }
    
    def evaluate_model(self, model: nn.Module, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate model performance"""
        model.eval()
        X_test_tensor = torch.FloatTensor(X_test).to(self.device)
        y_test_tensor = torch.LongTensor(y_test).to(self.device) if len(np.unique(y_test)) < 10 else torch.FloatTensor(y_test).to(self.device)
        
        with torch.no_grad():
            outputs = model(X_test_tensor)
            
            if len(np.unique(y_test)) < 10:  # Classification
                predictions = torch.argmax(outputs, dim=1)
                accuracy = (predictions == y_test_tensor).float().mean().item()
                return {"accuracy": accuracy, "predictions": predictions.cpu().numpy()}
            else:  # Regression
                mse = nn.MSELoss()(outputs.squeeze(), y_test_tensor).item()
                mae = nn.L1Loss()(outputs.squeeze(), y_test_tensor).item()
                return {"mse": mse, "mae": mae, "predictions": outputs.squeeze().cpu().numpy()}

class EnhancedStudentSimulator:
    """Advanced student simulator with human-like behaviors"""
    
    def __init__(self, tutor_system=None, assistant_system=None, professor_system=None):
        self.tutor_system = tutor_system
        self.assistant_system = assistant_system
        self.professor_system = professor_system
        self.neural_trainer = NeuralNetworkTrainer()
        self.simulated_students: Dict[str, SimulatedStudent] = {}
        self.student_behaviors = self._initialize_student_behaviors()
        
    def _initialize_student_behaviors(self) -> Dict[str, Dict[str, Any]]:
        """Initialize different student behavior patterns"""
        return {
            "enthusiastic_learner": {
                "study_frequency": "daily",
                "assignment_completion_rate": 0.95,
                "tutor_interaction_frequency": "high",
                "emotional_responses": {
                    "success": "excited",
                    "failure": "motivated",
                    "confusion": "curious"
                },
                "learning_preferences": ["hands_on", "visual", "collaborative"]
            },
            "methodical_student": {
                "study_frequency": "scheduled",
                "assignment_completion_rate": 0.90,
                "tutor_interaction_frequency": "medium",
                "emotional_responses": {
                    "success": "confident",
                    "failure": "analytical",
                    "confusion": "systematic"
                },
                "learning_preferences": ["structured", "reading", "step_by_step"]
            },
            "struggling_learner": {
                "study_frequency": "irregular",
                "assignment_completion_rate": 0.70,
                "tutor_interaction_frequency": "high",
                "emotional_responses": {
                    "success": "relieved",
                    "failure": "frustrated",
                    "confusion": "overwhelmed"
                },
                "learning_preferences": ["supportive", "visual", "simplified"]
            },
            "independent_learner": {
                "study_frequency": "self_directed",
                "assignment_completion_rate": 0.85,
                "tutor_interaction_frequency": "low",
                "emotional_responses": {
                    "success": "satisfied",
                    "failure": "determined",
                    "confusion": "curious"
                },
                "learning_preferences": ["self_paced", "research", "experimental"]
            }
        }
    
    def create_simulated_student(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new simulated student"""
        student_id = f"SIM_STUDENT_{uuid.uuid4().hex[:8]}"
        
        # Determine behavior pattern
        behavior_pattern = random.choice(list(self.student_behaviors.keys()))
        behavior = self.student_behaviors[behavior_pattern]
        
        student = SimulatedStudent(
            student_id=student_id,
            name=student_data["name"],
            email=student_data["email"],
            learning_style=LearningStyle(student_data.get("learning_style", "multimodal")),
            current_level=StudentLevel(student_data.get("level", "beginner")),
            emotional_state=EmotionalState.CURIOUS,
            background=student_data.get("background", {}),
            strengths=student_data.get("strengths", []),
            challenges=student_data.get("challenges", []),
            interests=student_data.get("interests", []),
            goals=student_data.get("goals", []),
            cultural_background=student_data.get("cultural_background", "Not specified"),
            language_preference=student_data.get("language_preference", "English"),
            accessibility_needs=student_data.get("accessibility_needs", []),
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        self.simulated_students[student_id] = student
        
        return {
            "success": True,
            "student_id": student_id,
            "behavior_pattern": behavior_pattern,
            "message": f"Simulated student '{student_data['name']}' created successfully"
        }
    
    async def simulate_student_learning_journey(self, student_id: str, course_id: str, 
                                               duration_days: int = 30) -> Dict[str, Any]:
        """Simulate complete student learning journey"""
        student = self.simulated_students.get(student_id)
        if not student:
            return {"success": False, "error": "Student not found"}
        
        journey_log = []
        start_date = datetime.now()
        
        # Simulate daily learning activities
        for day in range(duration_days):
            current_date = start_date + timedelta(days=day)
            
            # Daily learning activities
            daily_activities = await self._simulate_daily_activities(student, course_id, current_date)
            journey_log.extend(daily_activities)
            
            # Update student state
            self._update_student_state(student, daily_activities)
        
        return {
            "success": True,
            "student_id": student_id,
            "course_id": course_id,
            "duration_days": duration_days,
            "journey_log": journey_log,
            "final_state": {
                "emotional_state": student.emotional_state.value,
                "study_hours": student.total_study_hours,
                "assignments_completed": len(student.assignments_completed),
                "current_gpa": student.current_gpa,
                "neural_network_projects": len(student.neural_network_projects)
            }
        }
    
    async def _simulate_daily_activities(self, student: SimulatedStudent, course_id: str, 
                                       current_date: datetime) -> List[Dict[str, Any]]:
        """Simulate daily learning activities"""
        activities = []
        
        # Determine if student studies today (based on behavior pattern)
        behavior_pattern = self._get_student_behavior_pattern(student)
        study_probability = self._get_study_probability(behavior_pattern)
        
        if random.random() < study_probability:
            # Study session
            study_activity = await self._simulate_study_session(student, course_id, current_date)
            activities.append(study_activity)
            
            # Assignment work
            if random.random() < 0.3:  # 30% chance of working on assignment
                assignment_activity = await self._simulate_assignment_work(student, course_id, current_date)
                activities.append(assignment_activity)
            
            # AI Tutor interaction
            if random.random() < self._get_tutor_interaction_probability(behavior_pattern):
                tutor_activity = await self._simulate_tutor_interaction(student, course_id, current_date)
                activities.append(tutor_activity)
            
            # AI Assistant interaction
            if random.random() < 0.1:  # 10% chance of needing assistance
                assistant_activity = await self._simulate_assistant_interaction(student, current_date)
                activities.append(assistant_activity)
        
        return activities
    
    def _get_student_behavior_pattern(self, student: SimulatedStudent) -> str:
        """Determine student's behavior pattern"""
        # Simple heuristic based on student characteristics
        if "enthusiastic" in student.strengths or "motivated" in student.strengths:
            return "enthusiastic_learner"
        elif "analytical" in student.strengths or "systematic" in student.strengths:
            return "methodical_student"
        elif "struggling" in student.challenges or "difficult" in student.challenges:
            return "struggling_learner"
        else:
            return "independent_learner"
    
    def _get_study_probability(self, behavior_pattern: str) -> float:
        """Get probability of studying based on behavior pattern"""
        probabilities = {
            "enthusiastic_learner": 0.9,
            "methodical_student": 0.8,
            "struggling_learner": 0.6,
            "independent_learner": 0.7
        }
        return probabilities.get(behavior_pattern, 0.7)
    
    def _get_tutor_interaction_probability(self, behavior_pattern: str) -> float:
        """Get probability of tutor interaction based on behavior pattern"""
        probabilities = {
            "enthusiastic_learner": 0.3,
            "methodical_student": 0.2,
            "struggling_learner": 0.5,
            "independent_learner": 0.1
        }
        return probabilities.get(behavior_pattern, 0.2)
    
    async def _simulate_study_session(self, student: SimulatedStudent, course_id: str, 
                                    current_date: datetime) -> Dict[str, Any]:
        """Simulate study session"""
        session_duration = random.uniform(30, 120)  # 30-120 minutes
        topics_studied = random.sample([
            "Introduction to AI", "Machine Learning Basics", "Neural Networks",
            "Deep Learning", "Computer Vision", "Natural Language Processing",
            "AI Ethics", "Data Preprocessing", "Model Evaluation"
        ], random.randint(1, 3))
        
        # Update study hours
        student.total_study_hours += session_duration / 60
        
        # Simulate learning progress
        for topic in topics_studied:
            current_progress = student.learning_progress.get(topic, 0.0)
            progress_increase = random.uniform(0.05, 0.15)
            student.learning_progress[topic] = min(1.0, current_progress + progress_increase)
        
        return {
            "activity_type": "study_session",
            "timestamp": current_date.isoformat(),
            "duration_minutes": session_duration,
            "topics_studied": topics_studied,
            "learning_progress": student.learning_progress.copy(),
            "emotional_state": student.emotional_state.value
        }
    
    async def _simulate_assignment_work(self, student: SimulatedStudent, course_id: str, 
                                     current_date: datetime) -> Dict[str, Any]:
        """Simulate assignment work"""
        assignment_types = [
            "reading_assignment", "quiz", "programming_assignment", 
            "neural_network_project", "research_paper", "discussion_post"
        ]
        
        assignment_type = random.choice(assignment_types)
        completion_probability = random.uniform(0.6, 0.95)
        
        if random.random() < completion_probability:
            # Assignment completed
            assignment_id = f"ASSIGN_{uuid.uuid4().hex[:8]}"
            student.assignments_completed.append(assignment_id)
            
            # Simulate grade
            grade = self._simulate_assignment_grade(student, assignment_type)
            
            # Update GPA
            self._update_gpa(student, grade)
            
            # Special handling for neural network projects
            if assignment_type == "neural_network_project":
                nn_project = await self._create_neural_network_project(student, course_id, assignment_id)
                student.neural_network_projects.append(nn_project)
            
            return {
                "activity_type": "assignment_completion",
                "timestamp": current_date.isoformat(),
                "assignment_type": assignment_type,
                "assignment_id": assignment_id,
                "grade": grade,
                "completion_time_minutes": random.uniform(60, 240),
                "emotional_state": self._get_emotional_response_to_grade(student, grade)
            }
        else:
            # Assignment not completed
            return {
                "activity_type": "assignment_attempt",
                "timestamp": current_date.isoformat(),
                "assignment_type": assignment_type,
                "completion_status": "incomplete",
                "reason": random.choice(["time_constraints", "difficulty", "confusion", "technical_issues"]),
                "emotional_state": "frustrated"
            }
    
    def _simulate_assignment_grade(self, student: SimulatedStudent, assignment_type: str) -> float:
        """Simulate assignment grade based on student characteristics"""
        base_grade = random.uniform(70, 95)
        
        # Adjust based on student level
        level_adjustments = {
            StudentLevel.BEGINNER: -5,
            StudentLevel.INTERMEDIATE: 0,
            StudentLevel.ADVANCED: +5,
            StudentLevel.EXPERT: +10
        }
        
        # Adjust based on assignment type difficulty
        difficulty_adjustments = {
            "reading_assignment": +5,
            "quiz": 0,
            "programming_assignment": -5,
            "neural_network_project": -10,
            "research_paper": -3,
            "discussion_post": +3
        }
        
        grade = base_grade + level_adjustments.get(student.current_level, 0) + difficulty_adjustments.get(assignment_type, 0)
        return max(0, min(100, grade))
    
    def _get_emotional_response_to_grade(self, student: SimulatedStudent, grade: float) -> str:
        """Get emotional response to grade"""
        behavior_pattern = self._get_student_behavior_pattern(student)
        behavior = self.student_behaviors[behavior_pattern]
        
        if grade >= 90:
            return behavior["emotional_responses"]["success"]
        elif grade >= 70:
            return "satisfied"
        else:
            return behavior["emotional_responses"]["failure"]
    
    def _update_gpa(self, student: SimulatedStudent, grade: float):
        """Update student GPA"""
        if student.current_gpa == 0:
            student.current_gpa = grade
        else:
            # Weighted average
            total_assignments = len(student.assignments_completed)
            student.current_gpa = (student.current_gpa * (total_assignments - 1) + grade) / total_assignments
    
    async def _create_neural_network_project(self, student: SimulatedStudent, course_id: str, 
                                           assignment_id: str) -> NeuralNetworkProject:
        """Create neural network project for student"""
        project_types = ["classification", "regression", "image_classification", "text_analysis"]
        project_type = random.choice(project_types)
        
        # Create dataset
        dataset_type = "classification" if project_type in ["classification", "image_classification"] else "regression"
        X, y = self.neural_trainer.create_dataset(dataset_type, n_samples=random.randint(500, 2000))
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
        
        # Create and train model
        model = self.neural_trainer.create_model("feedforward", X.shape[1], len(np.unique(y)))
        training_history = self.neural_trainer.train_model(model, X_train, y_train, X_val, y_val, epochs=50)
        
        # Evaluate model
        performance = self.neural_trainer.evaluate_model(model, X_test, y_test)
        
        # Generate insights
        insights = self._generate_project_insights(project_type, performance, training_history)
        
        project = NeuralNetworkProject(
            project_id=f"NN_PROJECT_{uuid.uuid4().hex[:8]}",
            student_id=student.student_id,
            course_id=course_id,
            project_type=project_type,
            dataset_type=dataset_type,
            model_architecture="feedforward",
            training_metrics=training_history,
            model_performance=performance,
            created_at=datetime.now(),
            completion_time_minutes=random.randint(120, 300),
            insights_discovered=insights
        )
        
        return project
    
    def _generate_project_insights(self, project_type: str, performance: Dict[str, float], 
                                 training_history: Dict[str, List[float]]) -> List[str]:
        """Generate insights from neural network project"""
        insights = []
        
        if "accuracy" in performance:
            accuracy = performance["accuracy"]
            if accuracy > 0.9:
                insights.append("Achieved excellent classification accuracy")
            elif accuracy > 0.8:
                insights.append("Good classification performance")
            else:
                insights.append("Model needs improvement for better accuracy")
        
        if "mse" in performance:
            mse = performance["mse"]
            if mse < 0.1:
                insights.append("Low prediction error in regression model")
            else:
                insights.append("Model shows room for improvement in prediction accuracy")
        
        # Analyze training history
        if training_history["train_losses"]:
            final_train_loss = training_history["train_losses"][-1]
            final_val_loss = training_history["val_losses"][-1]
            
            if final_val_loss > final_train_loss * 1.2:
                insights.append("Model shows signs of overfitting")
            elif final_train_loss > 0.5:
                insights.append("Model may need more training or different architecture")
            else:
                insights.append("Model training converged successfully")
        
        return insights
    
    async def _simulate_tutor_interaction(self, student: SimulatedStudent, course_id: str, 
                                        current_date: datetime) -> Dict[str, Any]:
        """Simulate AI Tutor interaction"""
        if not self.tutor_system:
            return {
                "activity_type": "tutor_interaction",
                "timestamp": current_date.isoformat(),
                "status": "unavailable",
                "reason": "Tutor system not available"
            }
        
        # Determine interaction type
        interaction_types = ["concept_explanation", "problem_solving", "assignment_help", "study_guidance"]
        interaction_type = random.choice(interaction_types)
        
        # Simulate tutor session
        session_duration = random.uniform(15, 45)  # 15-45 minutes
        
        # Update emotional state based on interaction
        if student.emotional_state == EmotionalState.FRUSTRATED:
            student.emotional_state = EmotionalState.CONFIDENT
        elif student.emotional_state == EmotionalState.CONFUSED:
            student.emotional_state = EmotionalState.CURIOUS
        
        return {
            "activity_type": "tutor_interaction",
            "timestamp": current_date.isoformat(),
            "interaction_type": interaction_type,
            "duration_minutes": session_duration,
            "topics_discussed": random.sample([
                "Neural Networks", "Machine Learning", "Data Preprocessing",
                "Model Evaluation", "Python Programming", "AI Ethics"
            ], random.randint(1, 2)),
            "emotional_state_before": student.emotional_state.value,
            "emotional_state_after": student.emotional_state.value,
            "satisfaction_rating": random.uniform(4.0, 5.0)
        }
    
    async def _simulate_assistant_interaction(self, student: SimulatedStudent, 
                                            current_date: datetime) -> Dict[str, Any]:
        """Simulate AI Assistant interaction"""
        if not self.assistant_system:
            return {
                "activity_type": "assistant_interaction",
                "timestamp": current_date.isoformat(),
                "status": "unavailable",
                "reason": "Assistant system not available"
            }
        
        # Determine request type
        request_types = [
            "technical_support", "academic_advice", "career_guidance", 
            "administrative_help", "accessibility_support"
        ]
        request_type = random.choice(request_types)
        
        return {
            "activity_type": "assistant_interaction",
            "timestamp": current_date.isoformat(),
            "request_type": request_type,
            "request_description": f"Student requested help with {request_type}",
            "resolution_time_minutes": random.uniform(5, 30),
            "satisfaction_rating": random.uniform(4.0, 5.0)
        }
    
    def _update_student_state(self, student: SimulatedStudent, activities: List[Dict[str, Any]]):
        """Update student state based on activities"""
        student.last_activity = datetime.now()
        
        # Update emotional state based on recent activities
        recent_emotions = [activity.get("emotional_state") for activity in activities if "emotional_state" in activity]
        if recent_emotions:
            # Simple emotion tracking
            if "excited" in recent_emotions or "confident" in recent_emotions:
                student.emotional_state = EmotionalState.MOTIVATED
            elif "frustrated" in recent_emotions:
                student.emotional_state = EmotionalState.FRUSTRATED
            elif "curious" in recent_emotions:
                student.emotional_state = EmotionalState.CURIOUS
        
        # Update interaction history
        student.interaction_history.extend(activities)
    
    def get_student_analytics(self, student_id: str) -> Dict[str, Any]:
        """Get comprehensive student analytics"""
        student = self.simulated_students.get(student_id)
        if not student:
            return {"error": "Student not found"}
        
        return {
            "student_id": student_id,
            "analytics": {
                "learning_progress": {
                    "total_study_hours": student.total_study_hours,
                    "assignments_completed": len(student.assignments_completed),
                    "current_gpa": student.current_gpa,
                    "topics_mastered": len([topic for topic, progress in student.learning_progress.items() if progress > 0.8]),
                    "learning_velocity": self._calculate_learning_velocity(student)
                },
                "neural_network_projects": {
                    "total_projects": len(student.neural_network_projects),
                    "project_types": [project.project_type for project in student.neural_network_projects],
                    "average_performance": self._calculate_average_project_performance(student),
                    "insights_generated": sum(len(project.insights_discovered) for project in student.neural_network_projects)
                },
                "interaction_patterns": {
                    "total_interactions": len(student.interaction_history),
                    "tutor_interactions": len([a for a in student.interaction_history if a.get("activity_type") == "tutor_interaction"]),
                    "assistant_interactions": len([a for a in student.interaction_history if a.get("activity_type") == "assistant_interaction"]),
                    "study_sessions": len([a for a in student.interaction_history if a.get("activity_type") == "study_session"])
                },
                "emotional_journey": {
                    "current_state": student.emotional_state.value,
                    "emotional_transitions": self._analyze_emotional_transitions(student),
                    "motivation_level": self._assess_motivation_level(student)
                }
            }
        }
    
    def _calculate_learning_velocity(self, student: SimulatedStudent) -> float:
        """Calculate learning velocity (progress per hour)"""
        if student.total_study_hours == 0:
            return 0.0
        
        total_progress = sum(student.learning_progress.values())
        return total_progress / student.total_study_hours
    
    def _calculate_average_project_performance(self, student: SimulatedStudent) -> float:
        """Calculate average performance across neural network projects"""
        if not student.neural_network_projects:
            return 0.0
        
        total_performance = 0
        for project in student.neural_network_projects:
            if "accuracy" in project.model_performance:
                total_performance += project.model_performance["accuracy"]
            elif "mse" in project.model_performance:
                # Convert MSE to performance score (lower MSE = higher performance)
                total_performance += max(0, 1 - project.model_performance["mse"])
        
        return total_performance / len(student.neural_network_projects)
    
    def _analyze_emotional_transitions(self, student: SimulatedStudent) -> List[Dict[str, Any]]:
        """Analyze emotional transitions throughout learning journey"""
        transitions = []
        previous_emotion = None
        
        for activity in student.interaction_history:
            if "emotional_state" in activity:
                current_emotion = activity["emotional_state"]
                if previous_emotion and previous_emotion != current_emotion:
                    transitions.append({
                        "from": previous_emotion,
                        "to": current_emotion,
                        "timestamp": activity.get("timestamp"),
                        "trigger": activity.get("activity_type")
                    })
                previous_emotion = current_emotion
        
        return transitions
    
    def _assess_motivation_level(self, student: SimulatedStudent) -> str:
        """Assess student's motivation level"""
        # Simple heuristic based on recent activities and emotional state
        recent_activities = student.interaction_history[-10:] if len(student.interaction_history) > 10 else student.interaction_history
        
        study_sessions = len([a for a in recent_activities if a.get("activity_type") == "study_session"])
        completed_assignments = len([a for a in recent_activities if a.get("activity_type") == "assignment_completion"])
        
        if study_sessions >= 5 and completed_assignments >= 3:
            return "high"
        elif study_sessions >= 3 and completed_assignments >= 2:
            return "medium"
        else:
            return "low"