"""
MS AI Curriculum System - Demo Library System
Comprehensive demonstration management and generation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
import json
import uuid
import asyncio
from pathlib import Path

from playwright_demo_system import PlaywrightDemoSystem, DemoType, NarrationStyle
from ai_narration_system import AINarrationSystem, NarrationConfig, VoiceProfile
from video_enhancement_system import VideoEnhancementSystem, VideoEnhancementConfig

class DemoCategory(Enum):
    MACHINE_LEARNING = "machine_learning"
    DEEP_LEARNING = "deep_learning"
    COMPUTER_VISION = "computer_vision"
    NATURAL_LANGUAGE_PROCESSING = "natural_language_processing"
    AI_ETHICS = "ai_ethics"
    DATA_SCIENCE = "data_science"
    ROBOTICS = "robotics"
    AI_TOOLS = "ai_tools"

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class DemoTemplate:
    """Template for generating demonstrations"""
    template_id: str
    title: str
    description: str
    category: DemoCategory
    difficulty: DifficultyLevel
    estimated_duration: int  # minutes
    target_url: str
    professor_preference: str
    demo_type: DemoType
    narration_style: NarrationStyle
    steps_template: List[Dict[str, Any]]
    learning_objectives: List[str]
    prerequisites: List[str]
    tools_required: List[str]

@dataclass
class DemoLibrary:
    """Complete demonstration library"""
    library_id: str
    course_id: str
    demos: List[str]  # Demo IDs
    created_at: datetime
    last_updated: datetime
    total_duration: float = 0.0
    status: str = "active"

class DemoLibrarySystem:
    """Comprehensive demonstration library management system"""
    
    def __init__(self, professor_system=None):
        self.professor_system = professor_system
        self.playwright_system = PlaywrightDemoSystem(professor_system)
        self.narration_system = AINarrationSystem(professor_system)
        self.enhancement_system = VideoEnhancementSystem()
        
        self.demo_templates = self._initialize_demo_templates()
        self.demo_libraries: Dict[str, DemoLibrary] = {}
        self.output_dir = Path("demonstrations/library")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _initialize_demo_templates(self) -> List[DemoTemplate]:
        """Initialize comprehensive demo templates for MS AI curriculum"""
        return [
            # Machine Learning Demos
            DemoTemplate(
                template_id="ML_001",
                title="Introduction to Machine Learning with TensorFlow Playground",
                description="Interactive exploration of neural networks and machine learning concepts",
                category=DemoCategory.MACHINE_LEARNING,
                difficulty=DifficultyLevel.BEGINNER,
                estimated_duration=15,
                target_url="https://playground.tensorflow.org/",
                professor_preference="Dr. Sarah Chen",
                demo_type=DemoType.TUTORIAL,
                narration_style=NarrationStyle.PROFESSOR_LECTURE,
                steps_template=[
                    {
                        "action": "navigate",
                        "target": "https://playground.tensorflow.org/",
                        "description": "Navigate to TensorFlow Playground",
                        "narration": "Let's start our machine learning journey with TensorFlow Playground!",
                        "duration_seconds": 3.0,
                        "screenshot_timing": "after"
                    },
                    {
                        "action": "click",
                        "target": ".dataset-button",
                        "description": "Select spiral dataset",
                        "narration": "I'll choose the spiral dataset - it's perfect for understanding classification!",
                        "duration_seconds": 2.0,
                        "highlight_element": True
                    },
                    {
                        "action": "click",
                        "target": ".play-button",
                        "description": "Start neural network training",
                        "narration": "Watch the magic happen as our neural network learns!",
                        "duration_seconds": 8.0,
                        "screenshot_timing": "after"
                    }
                ],
                learning_objectives=[
                    "Understand basic neural network concepts",
                    "Visualize how neural networks learn",
                    "Explore different datasets and their characteristics"
                ],
                prerequisites=["Basic understanding of mathematics"],
                tools_required=["Web browser", "TensorFlow Playground"]
            ),
            
            # Deep Learning Demos
            DemoTemplate(
                template_id="DL_001",
                title="Building Your First Neural Network with PyTorch",
                description="Hands-on tutorial for creating neural networks from scratch",
                category=DemoCategory.DEEP_LEARNING,
                difficulty=DifficultyLevel.INTERMEDIATE,
                estimated_duration=25,
                target_url="https://colab.research.google.com/",
                professor_preference="Dr. Marcus Rodriguez",
                demo_type=DemoType.CODE_WALKTHROUGH,
                narration_style=NarrationStyle.TUTORIAL_GUIDE,
                steps_template=[
                    {
                        "action": "navigate",
                        "target": "https://colab.research.google.com/",
                        "description": "Open Google Colab",
                        "narration": "Let's use Google Colab for our PyTorch adventure!",
                        "duration_seconds": 3.0
                    },
                    {
                        "action": "type",
                        "target": "textarea",
                        "description": "Import PyTorch libraries",
                        "narration": "First, we'll import the essential PyTorch libraries.",
                        "metadata": {"text": "import torch\nimport torch.nn as nn\nimport torch.optim as optim"},
                        "duration_seconds": 4.0
                    },
                    {
                        "action": "type",
                        "target": "textarea",
                        "description": "Define neural network class",
                        "narration": "Now let's define our neural network architecture.",
                        "metadata": {"text": "class SimpleNN(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.fc1 = nn.Linear(784, 128)\n        self.fc2 = nn.Linear(128, 10)\n    def forward(self, x):\n        x = torch.relu(self.fc1(x))\n        x = self.fc2(x)\n        return x"},
                        "duration_seconds": 8.0
                    }
                ],
                learning_objectives=[
                    "Learn PyTorch fundamentals",
                    "Build neural networks from scratch",
                    "Understand forward and backward propagation"
                ],
                prerequisites=["Python programming", "Basic linear algebra"],
                tools_required=["Google Colab", "PyTorch"]
            ),
            
            # Computer Vision Demos
            DemoTemplate(
                template_id="CV_001",
                title="Image Classification with Convolutional Neural Networks",
                description="Practical demonstration of CNN architecture and image processing",
                category=DemoCategory.COMPUTER_VISION,
                difficulty=DifficultyLevel.INTERMEDIATE,
                estimated_duration=20,
                target_url="https://teachablemachine.withgoogle.com/",
                professor_preference="Dr. Marcus Rodriguez",
                demo_type=DemoType.TOOL_DEMONSTRATION,
                narration_style=NarrationStyle.EXPERT_DEMONSTRATION,
                steps_template=[
                    {
                        "action": "navigate",
                        "target": "https://teachablemachine.withgoogle.com/",
                        "description": "Open Teachable Machine",
                        "narration": "Let's explore computer vision with Teachable Machine!",
                        "duration_seconds": 3.0
                    },
                    {
                        "action": "click",
                        "target": ".image-project",
                        "description": "Select image project",
                        "narration": "We'll create an image classification project.",
                        "duration_seconds": 2.0,
                        "highlight_element": True
                    },
                    {
                        "action": "click",
                        "target": ".train-button",
                        "description": "Train the model",
                        "narration": "Watch as our CNN learns to classify images!",
                        "duration_seconds": 10.0,
                        "screenshot_timing": "after"
                    }
                ],
                learning_objectives=[
                    "Understand CNN architecture",
                    "Learn image preprocessing techniques",
                    "Experience model training process"
                ],
                prerequisites=["Basic machine learning concepts"],
                tools_required=["Teachable Machine", "Web camera"]
            ),
            
            # NLP Demos
            DemoTemplate(
                template_id="NLP_001",
                title="Natural Language Processing with Transformers",
                description="Introduction to transformer models and language understanding",
                category=DemoCategory.NATURAL_LANGUAGE_PROCESSING,
                difficulty=DifficultyLevel.INTERMEDIATE,
                estimated_duration=18,
                target_url="https://huggingface.co/spaces",
                professor_preference="Dr. James Kim",
                demo_type=DemoType.INTERACTIVE_SESSION,
                narration_style=NarrationStyle.CONVERSATIONAL,
                steps_template=[
                    {
                        "action": "navigate",
                        "target": "https://huggingface.co/spaces",
                        "description": "Open Hugging Face Spaces",
                        "narration": "Let's dive into the world of transformers!",
                        "duration_seconds": 3.0
                    },
                    {
                        "action": "click",
                        "target": ".text-classification",
                        "description": "Select text classification demo",
                        "narration": "We'll explore text classification with BERT.",
                        "duration_seconds": 2.0
                    },
                    {
                        "action": "type",
                        "target": "textarea",
                        "description": "Enter sample text",
                        "narration": "Let's test our model with some sample text.",
                        "metadata": {"text": "This movie is absolutely fantastic!"},
                        "duration_seconds": 5.0,
                        "screenshot_timing": "after"
                    }
                ],
                learning_objectives=[
                    "Understand transformer architecture",
                    "Learn about pre-trained language models",
                    "Experience NLP applications"
                ],
                prerequisites=["Basic NLP concepts"],
                tools_required=["Hugging Face", "Web browser"]
            ),
            
            # AI Ethics Demos
            DemoTemplate(
                template_id="ETHICS_001",
                title="AI Bias Detection and Fairness Analysis",
                description="Exploring bias in AI systems and methods for fairness",
                category=DemoCategory.AI_ETHICS,
                difficulty=DifficultyLevel.INTERMEDIATE,
                estimated_duration=22,
                target_url="https://pair.withgoogle.com/",
                professor_preference="Dr. Aisha Patel",
                demo_type=DemoType.TUTORIAL,
                narration_style=NarrationStyle.PEER_EXPLANATION,
                steps_template=[
                    {
                        "action": "navigate",
                        "target": "https://pair.withgoogle.com/",
                        "description": "Open PAIR tools",
                        "narration": "Let's explore AI fairness with Google's PAIR tools.",
                        "duration_seconds": 3.0
                    },
                    {
                        "action": "click",
                        "target": ".what-if-tool",
                        "description": "Open What-If Tool",
                        "narration": "We'll use the What-If Tool to analyze model fairness.",
                        "duration_seconds": 2.0,
                        "highlight_element": True
                    },
                    {
                        "action": "click",
                        "target": ".bias-analysis",
                        "description": "Run bias analysis",
                        "narration": "Let's examine how our model performs across different groups.",
                        "duration_seconds": 8.0,
                        "screenshot_timing": "after"
                    }
                ],
                learning_objectives=[
                    "Understand AI bias concepts",
                    "Learn fairness evaluation methods",
                    "Explore bias mitigation techniques"
                ],
                prerequisites=["Basic machine learning knowledge"],
                tools_required=["Google PAIR", "Web browser"]
            )
        ]
    
    def generate_course_demo_library(self, course_id: str) -> Dict[str, Any]:
        """Generate complete demonstration library for a course"""
        
        # Filter templates by course relevance
        relevant_templates = self._get_templates_for_course(course_id)
        
        if not relevant_templates:
            return {
                "success": False,
                "error": f"No demo templates found for course {course_id}"
            }
        
        # Create demo library
        library_id = f"LIB_{uuid.uuid4().hex[:8].upper()}"
        demo_ids = []
        
        for template in relevant_templates:
            # Generate demonstration from template
            demo_data = self._template_to_demo_data(template, course_id)
            demo_result = self.playwright_system.create_demonstration(demo_data)
            
            if demo_result["success"]:
                demo_ids.append(demo_result["demo_id"])
        
        # Create library record
        library = DemoLibrary(
            library_id=library_id,
            course_id=course_id,
            demos=demo_ids,
            created_at=datetime.now(),
            last_updated=datetime.now(),
            total_duration=sum(template.estimated_duration for template in relevant_templates)
        )
        
        self.demo_libraries[library_id] = library
        
        return {
            "success": True,
            "library_id": library_id,
            "course_id": course_id,
            "demos_created": len(demo_ids),
            "total_duration_minutes": library.total_duration,
            "demo_ids": demo_ids
        }
    
    def _get_templates_for_course(self, course_id: str) -> List[DemoTemplate]:
        """Get relevant demo templates for a course"""
        # Map course IDs to relevant categories
        course_mapping = {
            "AI501": [DemoCategory.MACHINE_LEARNING, DemoCategory.DATA_SCIENCE],
            "AI502": [DemoCategory.DEEP_LEARNING, DemoCategory.MACHINE_LEARNING],
            "AI503": [DemoCategory.AI_ETHICS, DemoCategory.AI_TOOLS],
            "AI504": [DemoCategory.COMPUTER_VISION, DemoCategory.DEEP_LEARNING],
            "AI505": [DemoCategory.NATURAL_LANGUAGE_PROCESSING, DemoCategory.DEEP_LEARNING],
            "AI506": [DemoCategory.ROBOTICS, DemoCategory.AI_TOOLS],
            "AI507": [DemoCategory.AI_ETHICS, DemoCategory.MACHINE_LEARNING],
            "AI508": [DemoCategory.DATA_SCIENCE, DemoCategory.AI_TOOLS]
        }
        
        relevant_categories = course_mapping.get(course_id, [])
        
        return [
            template for template in self.demo_templates
            if template.category in relevant_categories
        ]
    
    def _template_to_demo_data(self, template: DemoTemplate, course_id: str) -> Dict[str, Any]:
        """Convert template to demonstration data"""
        return {
            "title": template.title,
            "description": template.description,
            "course_id": course_id,
            "topic": template.category.value.replace("_", " ").title(),
            "demo_type": template.demo_type.value,
            "narration_style": template.narration_style.value,
            "target_url": template.target_url,
            "steps": template.steps_template.copy()
        }
    
    async def execute_demo_library(self, library_id: str) -> Dict[str, Any]:
        """Execute all demonstrations in a library"""
        library = self.demo_libraries.get(library_id)
        if not library:
            return {"success": False, "error": "Library not found"}
        
        execution_results = []
        
        for demo_id in library.demos:
            # Execute demonstration
            demo_result = await self.playwright_system.execute_demonstration(demo_id)
            
            if demo_result["success"]:
                # Get demonstration data for enhancement
                demonstration = self.playwright_system.demonstrations.get(demo_id)
                
                # Generate AI narration
                narration_config = self.narration_system.create_narration_config(
                    demonstration.narration_style.value, 
                    demonstration.demo_type.value
                )
                
                narration_segments = self.narration_system.generate_narration_script(
                    {
                        "title": demonstration.title,
                        "description": demonstration.description,
                        "topic": demonstration.topic,
                        "steps": [
                            {
                                "action": step.action,
                                "target": step.target,
                                "description": step.description,
                                "narration": step.narration
                            }
                            for step in demonstration.steps
                        ]
                    },
                    narration_config
                )
                
                # Generate audio narration
                audio_path = await self.narration_system.generate_audio_narration(
                    narration_segments, narration_config
                )
                
                # Enhance video
                enhancement_config = VideoEnhancementConfig(
                    add_professor_avatar=True,
                    add_step_numbers=True,
                    add_progress_bar=True,
                    color_scheme="professional"
                )
                
                enhancement_result = self.enhancement_system.enhance_demonstration_video(
                    demo_result["video_path"],
                    audio_path,
                    {
                        "title": demonstration.title,
                        "steps": [
                            {
                                "action": step.action,
                                "target": step.target,
                                "description": step.description,
                                "highlight_element": step.highlight_element
                            }
                            for step in demonstration.steps
                        ]
                    },
                    narration_segments,
                    enhancement_config
                )
                
                execution_results.append({
                    "demo_id": demo_id,
                    "status": "completed",
                    "video_path": enhancement_result.get("enhanced_video_path"),
                    "audio_path": audio_path,
                    "duration_minutes": enhancement_result.get("duration_seconds", 0) / 60
                })
            else:
                execution_results.append({
                    "demo_id": demo_id,
                    "status": "failed",
                    "error": demo_result.get("error")
                })
        
        # Update library status
        library.last_updated = datetime.now()
        
        return {
            "success": True,
            "library_id": library_id,
            "total_demos": len(library.demos),
            "completed_demos": len([r for r in execution_results if r["status"] == "completed"]),
            "failed_demos": len([r for r in execution_results if r["status"] == "failed"]),
            "execution_results": execution_results
        }
    
    def get_demo_library_status(self, library_id: str) -> Dict[str, Any]:
        """Get status of demo library"""
        library = self.demo_libraries.get(library_id)
        if not library:
            return {"error": "Library not found"}
        
        # Get demo statuses
        demo_statuses = []
        for demo_id in library.demos:
            demo_status = self.playwright_system.get_demonstration_status(demo_id)
            demo_statuses.append(demo_status)
        
        return {
            "library_id": library_id,
            "course_id": library.course_id,
            "total_demos": len(library.demos),
            "created_at": library.created_at.isoformat(),
            "last_updated": library.last_updated.isoformat(),
            "total_duration_minutes": library.total_duration,
            "status": library.status,
            "demo_statuses": demo_statuses
        }
    
    def list_available_templates(self, category: Optional[DemoCategory] = None) -> List[Dict[str, Any]]:
        """List available demo templates"""
        templates = self.demo_templates
        
        if category:
            templates = [t for t in templates if t.category == category]
        
        return [
            {
                "template_id": template.template_id,
                "title": template.title,
                "description": template.description,
                "category": template.category.value,
                "difficulty": template.difficulty.value,
                "estimated_duration": template.estimated_duration,
                "professor_preference": template.professor_preference,
                "learning_objectives": template.learning_objectives,
                "prerequisites": template.prerequisites,
                "tools_required": template.tools_required
            }
            for template in templates
        ]
    
    def create_custom_demo(self, demo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create custom demonstration"""
        return self.playwright_system.create_demonstration(demo_data)
    
    def get_demo_statistics(self) -> Dict[str, Any]:
        """Get comprehensive demo statistics"""
        total_libraries = len(self.demo_libraries)
        total_demos = sum(len(lib.demos) for lib in self.demo_libraries.values())
        
        # Count by category
        category_counts = {}
        for template in self.demo_templates:
            category = template.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Count by difficulty
        difficulty_counts = {}
        for template in self.demo_templates:
            difficulty = template.difficulty.value
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
        
        return {
            "total_libraries": total_libraries,
            "total_demos": total_demos,
            "total_templates": len(self.demo_templates),
            "category_distribution": category_counts,
            "difficulty_distribution": difficulty_counts,
            "average_duration_minutes": sum(t.estimated_duration for t in self.demo_templates) / len(self.demo_templates),
            "professor_distribution": {
                "Dr. Sarah Chen": len([t for t in self.demo_templates if t.professor_preference == "Dr. Sarah Chen"]),
                "Dr. Marcus Rodriguez": len([t for t in self.demo_templates if t.professor_preference == "Dr. Marcus Rodriguez"]),
                "Dr. Aisha Patel": len([t for t in self.demo_templates if t.professor_preference == "Dr. Aisha Patel"]),
                "Dr. James Kim": len([t for t in self.demo_templates if t.professor_preference == "Dr. James Kim"])
            }
        }

# Example usage
async def create_sample_demo_library():
    """Create sample demo library for testing"""
    demo_library = DemoLibrarySystem()
    
    # Generate library for AI501 course
    result = demo_library.generate_course_demo_library("AI501")
    print(f"Library created: {result}")
    
    if result["success"]:
        # Execute the library
        execution_result = await demo_library.execute_demo_library(result["library_id"])
        print(f"Library executed: {execution_result}")
    
    return demo_library

if __name__ == "__main__":
    asyncio.run(create_sample_demo_library())