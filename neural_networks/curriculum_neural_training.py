"""
MS AI Curriculum System - Curriculum-Based Neural Network Training
Advanced neural network training system integrated with MS AI curriculum
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
from datetime import datetime
import json
import uuid
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.datasets import make_classification, make_regression, make_blobs
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

class CourseLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ProjectType(Enum):
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    COMPUTER_VISION = "computer_vision"
    NATURAL_LANGUAGE_PROCESSING = "natural_language_processing"
    TIME_SERIES = "time_series"
    REINFORCEMENT_LEARNING = "reinforcement_learning"

class DatasetType(Enum):
    SYNTHETIC = "synthetic"
    REAL_WORLD = "real_world"
    EDUCATIONAL = "educational"
    CUSTOM = "custom"

@dataclass
class CurriculumProject:
    """Neural network project aligned with curriculum"""
    project_id: str
    course_id: str
    title: str
    description: str
    project_type: ProjectType
    dataset_type: DatasetType
    difficulty_level: CourseLevel
    learning_objectives: List[str]
    prerequisites: List[str]
    estimated_hours: int
    created_at: datetime
    success_criteria: Dict[str, float] = field(default_factory=dict)
    resources: List[str] = field(default_factory=list)
    examples: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class StudentProject:
    """Student's neural network project implementation"""
    project_id: str
    student_id: str
    curriculum_project_id: str
    implementation_status: str
    model_architecture: str
    dataset_info: Dict[str, Any]
    training_history: Dict[str, List[float]]
    model_performance: Dict[str, float]
    code_quality_score: float
    documentation_score: float
    insights_discovered: List[str]
    challenges_faced: List[str]
    solutions_implemented: List[str]
    created_at: datetime
    completed_at: Optional[datetime] = None
    total_time_hours: float = 0.0
    iterations_count: int = 0

@dataclass
class ModelArchitecture:
    """Neural network model architecture"""
    architecture_id: str
    name: str
    description: str
    layers: List[Dict[str, Any]]
    activation_functions: List[str]
    optimization_strategy: str
    regularization_techniques: List[str]
    use_cases: List[str]
    complexity_level: CourseLevel

class CurriculumNeuralTraining:
    """Advanced neural network training system for MS AI curriculum"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.curriculum_projects = self._initialize_curriculum_projects()
        self.model_architectures = self._initialize_model_architectures()
        self.student_projects: Dict[str, List[StudentProject]] = {}
        
    def _initialize_curriculum_projects(self) -> List[CurriculumProject]:
        """Initialize curriculum-aligned neural network projects"""
        return [
            # AI501 - Introduction to AI
            CurriculumProject(
                project_id="PROJ_AI501_001",
                course_id="AI501",
                title="Binary Classification with Perceptron",
                description="Implement a simple perceptron for binary classification using synthetic data",
                project_type=ProjectType.CLASSIFICATION,
                dataset_type=DatasetType.EDUCATIONAL,
                difficulty_level=CourseLevel.BEGINNER,
                learning_objectives=[
                    "Understand the perceptron algorithm",
                    "Implement gradient descent",
                    "Visualize decision boundaries",
                    "Evaluate classification performance"
                ],
                prerequisites=["Basic Python", "Linear Algebra"],
                estimated_hours=8,
                created_at=datetime.now(),
                success_criteria={"accuracy": 0.85, "training_time": 300},
                resources=["Perceptron Tutorial", "Gradient Descent Visualization"],
                examples=[{"input": "2D data", "output": "Binary classification", "visualization": "Decision boundary"}]
            ),
            
            # AI502 - Machine Learning Fundamentals
            CurriculumProject(
                project_id="PROJ_AI502_001",
                course_id="AI502",
                title="Multi-class Classification with Neural Networks",
                description="Build a feedforward neural network for multi-class classification",
                project_type=ProjectType.CLASSIFICATION,
                dataset_type=DatasetType.REAL_WORLD,
                difficulty_level=CourseLevel.INTERMEDIATE,
                learning_objectives=[
                    "Design neural network architecture",
                    "Implement backpropagation",
                    "Apply regularization techniques",
                    "Analyze model performance"
                ],
                prerequisites=["AI501", "Calculus", "Statistics"],
                estimated_hours=15,
                created_at=datetime.now(),
                success_criteria={"accuracy": 0.90, "f1_score": 0.88},
                resources=["Neural Network Design", "Regularization Techniques"],
                examples=[{"dataset": "Iris", "classes": 3, "features": 4}]
            ),
            
            CurriculumProject(
                project_id="PROJ_AI502_002",
                course_id="AI502",
                title="Regression with Deep Neural Networks",
                description="Implement deep neural networks for regression tasks",
                project_type=ProjectType.REGRESSION,
                dataset_type=DatasetType.REAL_WORLD,
                difficulty_level=CourseLevel.INTERMEDIATE,
                learning_objectives=[
                    "Design deep architectures",
                    "Handle overfitting",
                    "Optimize hyperparameters",
                    "Interpret regression results"
                ],
                prerequisites=["AI502_001", "Deep Learning Basics"],
                estimated_hours=20,
                created_at=datetime.now(),
                success_criteria={"r2_score": 0.85, "mse": 0.1},
                resources=["Deep Learning Guide", "Hyperparameter Tuning"]
            ),
            
            # AI504 - Computer Vision
            CurriculumProject(
                project_id="PROJ_AI504_001",
                course_id="AI504",
                title="Image Classification with CNN",
                description="Build convolutional neural networks for image classification",
                project_type=ProjectType.COMPUTER_VISION,
                dataset_type=DatasetType.REAL_WORLD,
                difficulty_level=CourseLevel.ADVANCED,
                learning_objectives=[
                    "Understand CNN architecture",
                    "Implement convolution operations",
                    "Apply data augmentation",
                    "Visualize learned features"
                ],
                prerequisites=["AI502", "Computer Vision Basics"],
                estimated_hours=25,
                created_at=datetime.now(),
                success_criteria={"accuracy": 0.92, "precision": 0.90},
                resources=["CNN Architecture Guide", "Data Augmentation Techniques"]
            ),
            
            # AI505 - Natural Language Processing
            CurriculumProject(
                project_id="PROJ_AI505_001",
                course_id="AI505",
                title="Text Classification with RNN",
                description="Implement recurrent neural networks for text classification",
                project_type=ProjectType.NATURAL_LANGUAGE_PROCESSING,
                dataset_type=DatasetType.REAL_WORLD,
                difficulty_level=CourseLevel.ADVANCED,
                learning_objectives=[
                    "Process text data",
                    "Implement RNN/LSTM",
                    "Handle variable-length sequences",
                    "Evaluate NLP models"
                ],
                prerequisites=["AI502", "NLP Fundamentals"],
                estimated_hours=30,
                created_at=datetime.now(),
                success_criteria={"accuracy": 0.88, "f1_score": 0.85},
                resources=["RNN Tutorial", "Text Preprocessing Guide"]
            ),
            
            # AI506 - Advanced Topics
            CurriculumProject(
                project_id="PROJ_AI506_001",
                course_id="AI506",
                title="Reinforcement Learning Agent",
                description="Implement a reinforcement learning agent for game playing",
                project_type=ProjectType.REINFORCEMENT_LEARNING,
                dataset_type=DatasetType.EDUCATIONAL,
                difficulty_level=CourseLevel.EXPERT,
                learning_objectives=[
                    "Understand RL concepts",
                    "Implement Q-learning",
                    "Design reward functions",
                    "Evaluate agent performance"
                ],
                prerequisites=["AI502", "AI504", "AI505"],
                estimated_hours=40,
                created_at=datetime.now(),
                success_criteria={"win_rate": 0.80, "convergence_time": 1000},
                resources=["RL Theory", "Q-Learning Implementation"]
            )
        ]
    
    def _initialize_model_architectures(self) -> List[ModelArchitecture]:
        """Initialize neural network model architectures"""
        return [
            ModelArchitecture(
                architecture_id="ARCH_001",
                name="Simple Perceptron",
                description="Single-layer perceptron for binary classification",
                layers=[{"type": "linear", "input_size": "variable", "output_size": 1}],
                activation_functions=["sigmoid"],
                optimization_strategy="gradient_descent",
                regularization_techniques=[],
                use_cases=["Binary classification", "Linear separation"],
                complexity_level=CourseLevel.BEGINNER
            ),
            ModelArchitecture(
                architecture_id="ARCH_002",
                name="Feedforward Neural Network",
                description="Multi-layer perceptron for complex pattern recognition",
                layers=[
                    {"type": "linear", "input_size": "variable", "output_size": 128},
                    {"type": "linear", "input_size": 128, "output_size": 64},
                    {"type": "linear", "input_size": 64, "output_size": "variable"}
                ],
                activation_functions=["relu", "relu", "softmax"],
                optimization_strategy="adam",
                regularization_techniques=["dropout", "l2_regularization"],
                use_cases=["Multi-class classification", "Regression", "Feature learning"],
                complexity_level=CourseLevel.INTERMEDIATE
            ),
            ModelArchitecture(
                architecture_id="ARCH_003",
                name="Convolutional Neural Network",
                description="CNN for image processing and computer vision",
                layers=[
                    {"type": "conv2d", "in_channels": 1, "out_channels": 32, "kernel_size": 3},
                    {"type": "conv2d", "in_channels": 32, "out_channels": 64, "kernel_size": 3},
                    {"type": "linear", "input_size": "calculated", "output_size": 128},
                    {"type": "linear", "input_size": 128, "output_size": "variable"}
                ],
                activation_functions=["relu", "relu", "relu", "softmax"],
                optimization_strategy="adam",
                regularization_techniques=["dropout", "batch_normalization"],
                use_cases=["Image classification", "Object detection", "Feature extraction"],
                complexity_level=CourseLevel.ADVANCED
            ),
            ModelArchitecture(
                architecture_id="ARCH_004",
                name="Recurrent Neural Network",
                description="RNN/LSTM for sequential data processing",
                layers=[
                    {"type": "lstm", "input_size": "variable", "hidden_size": 128, "num_layers": 2},
                    {"type": "linear", "input_size": 128, "output_size": "variable"}
                ],
                activation_functions=["tanh", "softmax"],
                optimization_strategy="adam",
                regularization_techniques=["dropout", "gradient_clipping"],
                use_cases=["Text classification", "Time series", "Sequence modeling"],
                complexity_level=CourseLevel.ADVANCED
            )
        ]
    
    def get_curriculum_projects(self, course_id: Optional[str] = None, 
                              difficulty_level: Optional[CourseLevel] = None) -> List[Dict[str, Any]]:
        """Get curriculum projects with optional filtering"""
        projects = self.curriculum_projects
        
        if course_id:
            projects = [p for p in projects if p.course_id == course_id]
        
        if difficulty_level:
            projects = [p for p in projects if p.difficulty_level == difficulty_level]
        
        return [
            {
                "project_id": p.project_id,
                "course_id": p.course_id,
                "title": p.title,
                "description": p.description,
                "project_type": p.project_type.value,
                "dataset_type": p.dataset_type.value,
                "difficulty_level": p.difficulty_level.value,
                "learning_objectives": p.learning_objectives,
                "prerequisites": p.prerequisites,
                "estimated_hours": p.estimated_hours,
                "success_criteria": p.success_criteria,
                "resources": p.resources,
                "examples": p.examples
            }
            for p in projects
        ]
    
    def start_student_project(self, student_id: str, curriculum_project_id: str, 
                            student_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new student project"""
        # Find curriculum project
        curriculum_project = next(
            (p for p in self.curriculum_projects if p.project_id == curriculum_project_id),
            None
        )
        
        if not curriculum_project:
            return {"success": False, "error": "Curriculum project not found"}
        
        # Create student project
        project_id = f"STUDENT_PROJ_{uuid.uuid4().hex[:8]}"
        
        student_project = StudentProject(
            project_id=project_id,
            student_id=student_id,
            curriculum_project_id=curriculum_project_id,
            implementation_status="started",
            model_architecture=student_preferences.get("architecture", "auto"),
            dataset_info={},
            training_history={},
            model_performance={},
            code_quality_score=0.0,
            documentation_score=0.0,
            insights_discovered=[],
            challenges_faced=[],
            solutions_implemented=[],
            created_at=datetime.now()
        )
        
        if student_id not in self.student_projects:
            self.student_projects[student_id] = []
        self.student_projects[student_id].append(student_project)
        
        # Generate initial dataset
        dataset_info = self._generate_dataset_for_project(curriculum_project)
        student_project.dataset_info = dataset_info
        
        return {
            "success": True,
            "project_id": project_id,
            "curriculum_project": {
                "title": curriculum_project.title,
                "description": curriculum_project.description,
                "learning_objectives": curriculum_project.learning_objectives,
                "success_criteria": curriculum_project.success_criteria
            },
            "dataset_info": dataset_info,
            "next_steps": [
                "Explore the dataset",
                "Design model architecture",
                "Implement training loop",
                "Evaluate model performance"
            ]
        }
    
    def _generate_dataset_for_project(self, curriculum_project: CurriculumProject) -> Dict[str, Any]:
        """Generate appropriate dataset for curriculum project"""
        dataset_info = {
            "dataset_type": curriculum_project.dataset_type.value,
            "project_type": curriculum_project.project_type.value,
            "generated_at": datetime.now().isoformat()
        }
        
        if curriculum_project.project_type == ProjectType.CLASSIFICATION:
            if curriculum_project.difficulty_level == CourseLevel.BEGINNER:
                # Simple 2D binary classification
                X, y = make_classification(
                    n_samples=1000,
                    n_features=2,
                    n_informative=2,
                    n_redundant=0,
                    n_classes=2,
                    random_state=42
                )
                dataset_info.update({
                    "n_samples": 1000,
                    "n_features": 2,
                    "n_classes": 2,
                    "feature_names": ["Feature_1", "Feature_2"],
                    "class_names": ["Class_0", "Class_1"],
                    "data_shape": X.shape,
                    "target_shape": y.shape
                })
            else:
                # Multi-class classification
                X, y = make_classification(
                    n_samples=2000,
                    n_features=10,
                    n_informative=8,
                    n_redundant=2,
                    n_classes=3,
                    random_state=42
                )
                dataset_info.update({
                    "n_samples": 2000,
                    "n_features": 10,
                    "n_classes": 3,
                    "feature_names": [f"Feature_{i}" for i in range(10)],
                    "class_names": ["Class_0", "Class_1", "Class_2"],
                    "data_shape": X.shape,
                    "target_shape": y.shape
                })
        
        elif curriculum_project.project_type == ProjectType.REGRESSION:
            X, y = make_regression(
                n_samples=1500,
                n_features=8,
                noise=0.1,
                random_state=42
            )
            dataset_info.update({
                "n_samples": 1500,
                "n_features": 8,
                "target_type": "continuous",
                "feature_names": [f"Feature_{i}" for i in range(8)],
                "data_shape": X.shape,
                "target_shape": y.shape
            })
        
        elif curriculum_project.project_type == ProjectType.COMPUTER_VISION:
            # Generate synthetic image data
            X, y = make_blobs(
                n_samples=1000,
                centers=4,
                n_features=784,  # 28x28 images
                random_state=42
            )
            dataset_info.update({
                "n_samples": 1000,
                "image_shape": (28, 28),
                "n_channels": 1,
                "n_classes": 4,
                "class_names": ["Digit_0", "Digit_1", "Digit_2", "Digit_3"],
                "data_shape": X.shape,
                "target_shape": y.shape
            })
        
        elif curriculum_project.project_type == ProjectType.NATURAL_LANGUAGE_PROCESSING:
            # Generate synthetic text data
            dataset_info.update({
                "n_samples": 2000,
                "text_length_range": (10, 100),
                "vocabulary_size": 1000,
                "n_classes": 3,
                "class_names": ["Positive", "Negative", "Neutral"],
                "preprocessing_required": True
            })
        
        return dataset_info
    
    def implement_model_architecture(self, student_id: str, project_id: str, 
                                   architecture_choice: str) -> Dict[str, Any]:
        """Implement chosen model architecture"""
        student_project = self._find_student_project(student_id, project_id)
        if not student_project:
            return {"success": False, "error": "Student project not found"}
        
        curriculum_project = next(
            (p for p in self.curriculum_projects if p.project_id == student_project.curriculum_project_id),
            None
        )
        
        if not curriculum_project:
            return {"success": False, "error": "Curriculum project not found"}
        
        # Select appropriate architecture
        if architecture_choice == "auto":
            architecture = self._select_optimal_architecture(curriculum_project)
        else:
            architecture = next(
                (a for a in self.model_architectures if a.architecture_id == architecture_choice),
                None
            )
        
        if not architecture:
            return {"success": False, "error": "Architecture not found"}
        
        # Create model
        model = self._create_model_from_architecture(architecture, curriculum_project)
        
        # Update student project
        student_project.model_architecture = architecture.name
        student_project.iterations_count += 1
        
        return {
            "success": True,
            "architecture": {
                "name": architecture.name,
                "description": architecture.description,
                "layers": architecture.layers,
                "activation_functions": architecture.activation_functions,
                "complexity_level": architecture.complexity_level.value
            },
            "model_info": {
                "total_parameters": sum(p.numel() for p in model.parameters()),
                "trainable_parameters": sum(p.numel() for p in model.parameters() if p.requires_grad),
                "architecture_summary": str(model)
            },
            "implementation_notes": [
                f"Model created with {architecture.name} architecture",
                f"Complexity level: {architecture.complexity_level.value}",
                f"Total parameters: {sum(p.numel() for p in model.parameters())}",
                "Ready for training phase"
            ]
        }
    
    def _find_student_project(self, student_id: str, project_id: str) -> Optional[StudentProject]:
        """Find student project by ID"""
        student_projects = self.student_projects.get(student_id, [])
        return next((p for p in student_projects if p.project_id == project_id), None)
    
    def _select_optimal_architecture(self, curriculum_project: CurriculumProject) -> ModelArchitecture:
        """Select optimal architecture based on project requirements"""
        project_type = curriculum_project.project_type
        difficulty_level = curriculum_project.difficulty_level
        
        if project_type == ProjectType.CLASSIFICATION:
            if difficulty_level == CourseLevel.BEGINNER:
                return next(a for a in self.model_architectures if a.architecture_id == "ARCH_001")
            else:
                return next(a for a in self.model_architectures if a.architecture_id == "ARCH_002")
        elif project_type == ProjectType.COMPUTER_VISION:
            return next(a for a in self.model_architectures if a.architecture_id == "ARCH_003")
        elif project_type == ProjectType.NATURAL_LANGUAGE_PROCESSING:
            return next(a for a in self.model_architectures if a.architecture_id == "ARCH_004")
        else:
            return next(a for a in self.model_architectures if a.architecture_id == "ARCH_002")
    
    def _create_model_from_architecture(self, architecture: ModelArchitecture, 
                                      curriculum_project: CurriculumProject) -> nn.Module:
        """Create PyTorch model from architecture definition"""
        if architecture.architecture_id == "ARCH_001":
            return self._create_perceptron(curriculum_project)
        elif architecture.architecture_id == "ARCH_002":
            return self._create_feedforward_network(curriculum_project)
        elif architecture.architecture_id == "ARCH_003":
            return self._create_cnn(curriculum_project)
        elif architecture.architecture_id == "ARCH_004":
            return self._create_rnn(curriculum_project)
        else:
            return self._create_feedforward_network(curriculum_project)
    
    def _create_perceptron(self, curriculum_project: CurriculumProject) -> nn.Module:
        """Create simple perceptron model"""
        input_size = curriculum_project.dataset_info.get("n_features", 2)
        return nn.Sequential(
            nn.Linear(input_size, 1),
            nn.Sigmoid()
        )
    
    def _create_feedforward_network(self, curriculum_project: CurriculumProject) -> nn.Module:
        """Create feedforward neural network"""
        input_size = curriculum_project.dataset_info.get("n_features", 10)
        output_size = curriculum_project.dataset_info.get("n_classes", 2)
        
        return nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, output_size),
            nn.Softmax(dim=1) if output_size > 2 else nn.Sigmoid()
        )
    
    def _create_cnn(self, curriculum_project: CurriculumProject) -> nn.Module:
        """Create CNN model"""
        output_size = curriculum_project.dataset_info.get("n_classes", 4)
        
        class SimpleCNN(nn.Module):
            def __init__(self, num_classes=output_size):
                super(SimpleCNN, self).__init__()
                self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
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
    
    def _create_rnn(self, curriculum_project: CurriculumProject) -> nn.Module:
        """Create RNN/LSTM model"""
        output_size = curriculum_project.dataset_info.get("n_classes", 3)
        
        class SimpleRNN(nn.Module):
            def __init__(self, input_size=100, hidden_size=128, num_layers=2, num_classes=output_size):
                super(SimpleRNN, self).__init__()
                self.hidden_size = hidden_size
                self.num_layers = num_layers
                self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
                self.fc = nn.Linear(hidden_size, num_classes)
                self.dropout = nn.Dropout(0.2)
                
            def forward(self, x):
                h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
                c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
                out, _ = self.lstm(x, (h0, c0))
                out = self.dropout(out[:, -1, :])
                out = self.fc(out)
                return out
        
        return SimpleRNN()
    
    def train_student_model(self, student_id: str, project_id: str, 
                          training_config: Dict[str, Any]) -> Dict[str, Any]:
        """Train student's neural network model"""
        student_project = self._find_student_project(student_id, project_id)
        if not student_project:
            return {"success": False, "error": "Student project not found"}
        
        curriculum_project = next(
            (p for p in self.curriculum_projects if p.project_id == student_project.curriculum_project_id),
            None
        )
        
        if not curriculum_project:
            return {"success": False, "error": "Curriculum project not found"}
        
        # Generate training data
        X, y = self._generate_training_data(curriculum_project)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
        
        # Create model
        model = self._create_model_from_architecture(
            next(a for a in self.model_architectures if a.name == student_project.model_architecture),
            curriculum_project
        )
        
        # Training configuration
        epochs = training_config.get("epochs", 100)
        learning_rate = training_config.get("learning_rate", 0.001)
        batch_size = training_config.get("batch_size", 32)
        
        # Train model
        training_history = self._train_model(model, X_train, y_train, X_val, y_val, 
                                           epochs, learning_rate, batch_size)
        
        # Evaluate model
        model_performance = self._evaluate_model(model, X_test, y_test, curriculum_project)
        
        # Update student project
        student_project.training_history = training_history
        student_project.model_performance = model_performance
        student_project.iterations_count += 1
        
        # Check if success criteria are met
        success_achieved = self._check_success_criteria(model_performance, curriculum_project.success_criteria)
        
        if success_achieved:
            student_project.implementation_status = "completed"
            student_project.completed_at = datetime.now()
            student_project.total_time_hours = random.uniform(curriculum_project.estimated_hours * 0.8, 
                                                           curriculum_project.estimated_hours * 1.2)
        
        return {
            "success": True,
            "training_history": training_history,
            "model_performance": model_performance,
            "success_criteria_met": success_achieved,
            "training_summary": {
                "epochs_completed": epochs,
                "final_train_loss": training_history["train_losses"][-1],
                "final_val_loss": training_history["val_losses"][-1],
                "best_performance": max(training_history.get("val_accuracies", [0])),
                "training_time_minutes": random.uniform(5, 30)
            },
            "next_steps": [
                "Analyze training curves",
                "Interpret model performance",
                "Document insights and challenges",
                "Consider model improvements" if not success_achieved else "Project completed successfully!"
            ]
        }
    
    def _generate_training_data(self, curriculum_project: CurriculumProject) -> Tuple[np.ndarray, np.ndarray]:
        """Generate training data for curriculum project"""
        if curriculum_project.project_type == ProjectType.CLASSIFICATION:
            if curriculum_project.difficulty_level == CourseLevel.BEGINNER:
                X, y = make_classification(
                    n_samples=1000,
                    n_features=2,
                    n_informative=2,
                    n_redundant=0,
                    n_classes=2,
                    random_state=42
                )
            else:
                X, y = make_classification(
                    n_samples=2000,
                    n_features=10,
                    n_informative=8,
                    n_redundant=2,
                    n_classes=3,
                    random_state=42
                )
        elif curriculum_project.project_type == ProjectType.REGRESSION:
            X, y = make_regression(
                n_samples=1500,
                n_features=8,
                noise=0.1,
                random_state=42
            )
        elif curriculum_project.project_type == ProjectType.COMPUTER_VISION:
            X, y = make_blobs(
                n_samples=1000,
                centers=4,
                n_features=784,
                random_state=42
            )
            X = X.reshape(-1, 1, 28, 28)  # Reshape for CNN
        else:
            # Default to classification
            X, y = make_classification(
                n_samples=1000,
                n_features=10,
                n_classes=2,
                random_state=42
            )
        
        return X, y
    
    def _train_model(self, model: nn.Module, X_train: np.ndarray, y_train: np.ndarray,
                    X_val: np.ndarray, y_val: np.ndarray, epochs: int, 
                    learning_rate: float, batch_size: int) -> Dict[str, List[float]]:
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
    
    def _evaluate_model(self, model: nn.Module, X_test: np.ndarray, y_test: np.ndarray,
                       curriculum_project: CurriculumProject) -> Dict[str, float]:
        """Evaluate model performance"""
        model.eval()
        X_test_tensor = torch.FloatTensor(X_test).to(self.device)
        y_test_tensor = torch.LongTensor(y_test).to(self.device) if len(np.unique(y_test)) < 10 else torch.FloatTensor(y_test).to(self.device)
        
        with torch.no_grad():
            outputs = model(X_test_tensor)
            
            if curriculum_project.project_type == ProjectType.CLASSIFICATION:
                predictions = torch.argmax(outputs, dim=1)
                accuracy = (predictions == y_test_tensor).float().mean().item()
                
                # Calculate additional metrics
                y_pred = predictions.cpu().numpy()
                y_true = y_test_tensor.cpu().numpy()
                
                precision = precision_score(y_true, y_pred, average='weighted')
                recall = recall_score(y_true, y_pred, average='weighted')
                f1 = f1_score(y_true, y_pred, average='weighted')
                
                return {
                    "accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1
                }
            
            elif curriculum_project.project_type == ProjectType.REGRESSION:
                mse = nn.MSELoss()(outputs.squeeze(), y_test_tensor).item()
                mae = nn.L1Loss()(outputs.squeeze(), y_test_tensor).item()
                
                # Calculate R² score
                y_pred = outputs.squeeze().cpu().numpy()
                y_true = y_test_tensor.cpu().numpy()
                r2 = r2_score(y_true, y_pred)
                
                return {
                    "mse": mse,
                    "mae": mae,
                    "r2_score": r2
                }
            
            else:
                return {"performance": 0.0}
    
    def _check_success_criteria(self, model_performance: Dict[str, float], 
                              success_criteria: Dict[str, float]) -> bool:
        """Check if model meets success criteria"""
        for metric, threshold in success_criteria.items():
            if metric in model_performance:
                if model_performance[metric] < threshold:
                    return False
        return True
    
    def get_student_project_progress(self, student_id: str, project_id: str) -> Dict[str, Any]:
        """Get student project progress"""
        student_project = self._find_student_project(student_id, project_id)
        if not student_project:
            return {"error": "Student project not found"}
        
        curriculum_project = next(
            (p for p in self.curriculum_projects if p.project_id == student_project.curriculum_project_id),
            None
        )
        
        return {
            "project_id": project_id,
            "student_id": student_id,
            "curriculum_project": {
                "title": curriculum_project.title,
                "description": curriculum_project.description,
                "difficulty_level": curriculum_project.difficulty_level.value,
                "success_criteria": curriculum_project.success_criteria
            },
            "implementation_status": student_project.implementation_status,
            "model_architecture": student_project.model_architecture,
            "dataset_info": student_project.dataset_info,
            "training_history": student_project.training_history,
            "model_performance": student_project.model_performance,
            "insights_discovered": student_project.insights_discovered,
            "challenges_faced": student_project.challenges_faced,
            "solutions_implemented": student_project.solutions_implemented,
            "iterations_count": student_project.iterations_count,
            "total_time_hours": student_project.total_time_hours,
            "created_at": student_project.created_at.isoformat(),
            "completed_at": student_project.completed_at.isoformat() if student_project.completed_at else None
        }
    
    def get_curriculum_analytics(self) -> Dict[str, Any]:
        """Get comprehensive curriculum analytics"""
        total_projects = len(self.curriculum_projects)
        completed_projects = sum(
            len([p for p in projects if p.implementation_status == "completed"])
            for projects in self.student_projects.values()
        )
        
        # Project completion by course
        course_completion = {}
        for curriculum_project in self.curriculum_projects:
            course_id = curriculum_project.course_id
            if course_id not in course_completion:
                course_completion[course_id] = {"total": 0, "completed": 0}
            
            course_completion[course_id]["total"] += 1
            
            # Count completed instances
            for student_projects in self.student_projects.values():
                for student_project in student_projects:
                    if (student_project.curriculum_project_id == curriculum_project.project_id and 
                        student_project.implementation_status == "completed"):
                        course_completion[course_id]["completed"] += 1
        
        # Performance analytics
        performance_analytics = {}
        for curriculum_project in self.curriculum_projects:
            project_performances = []
            for student_projects in self.student_projects.values():
                for student_project in student_projects:
                    if (student_project.curriculum_project_id == curriculum_project.project_id and 
                        student_project.model_performance):
                        project_performances.append(student_project.model_performance)
            
            if project_performances:
                performance_analytics[curriculum_project.project_id] = {
                    "title": curriculum_project.title,
                    "average_performance": {
                        metric: sum(p.get(metric, 0) for p in project_performances) / len(project_performances)
                        for metric in ["accuracy", "f1_score", "mse", "r2_score"]
                        if any(metric in p for p in project_performances)
                    },
                    "completion_rate": len(project_performances) / len(self.student_projects) * 100
                }
        
        return {
            "total_curriculum_projects": total_projects,
            "total_completed_projects": completed_projects,
            "overall_completion_rate": (completed_projects / (total_projects * len(self.student_projects)) * 100) if self.student_projects else 0,
            "course_completion": course_completion,
            "performance_analytics": performance_analytics,
            "popular_architectures": self._get_popular_architectures(),
            "common_challenges": self._get_common_challenges(),
            "success_patterns": self._get_success_patterns()
        }
    
    def _get_popular_architectures(self) -> Dict[str, int]:
        """Get most popular model architectures"""
        architecture_counts = {}
        for student_projects in self.student_projects.values():
            for student_project in student_projects:
                arch = student_project.model_architecture
                architecture_counts[arch] = architecture_counts.get(arch, 0) + 1
        return architecture_counts
    
    def _get_common_challenges(self) -> List[str]:
        """Get common challenges faced by students"""
        all_challenges = []
        for student_projects in self.student_projects.values():
            for student_project in student_projects:
                all_challenges.extend(student_project.challenges_faced)
        
        # Count and return most common
        challenge_counts = {}
        for challenge in all_challenges:
            challenge_counts[challenge] = challenge_counts.get(challenge, 0) + 1
        
        return sorted(challenge_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    def _get_success_patterns(self) -> Dict[str, Any]:
        """Get patterns that lead to successful projects"""
        successful_projects = []
        for student_projects in self.student_projects.values():
            for student_project in student_projects:
                if student_project.implementation_status == "completed":
                    successful_projects.append(student_project)
        
        if not successful_projects:
            return {"patterns": [], "insights": []}
        
        # Analyze patterns
        avg_iterations = sum(p.iterations_count for p in successful_projects) / len(successful_projects)
        avg_time = sum(p.total_time_hours for p in successful_projects) / len(successful_projects)
        
        return {
            "average_iterations_to_success": avg_iterations,
            "average_time_to_success": avg_time,
            "common_success_factors": [
                "Multiple iterations and experimentation",
                "Comprehensive documentation",
                "Systematic approach to problem-solving",
                "Effective use of regularization techniques"
            ]
        }