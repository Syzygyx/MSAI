"""
MS AI Curriculum System - Playwright Demonstration System
AI-powered browser automation with screen capture and narration
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
from datetime import datetime
import json
import uuid
import asyncio
import os
import subprocess
from pathlib import Path

try:
    from playwright.async_api import async_playwright, Browser, BrowserContext, Page
except ImportError:
    print("Playwright not installed. Run: pip install playwright && playwright install")
    async_playwright = None

class DemoType(Enum):
    TUTORIAL = "tutorial"
    LECTURE_DEMO = "lecture_demo"
    HANDS_ON_EXERCISE = "hands_on_exercise"
    TOOL_DEMONSTRATION = "tool_demonstration"
    CODE_WALKTHROUGH = "code_walkthrough"
    INTERACTIVE_SESSION = "interactive_session"

class NarrationStyle(Enum):
    PROFESSOR_LECTURE = "professor_lecture"
    TUTORIAL_GUIDE = "tutorial_guide"
    PEER_EXPLANATION = "peer_explanation"
    EXPERT_DEMONSTRATION = "expert_demonstration"
    CONVERSATIONAL = "conversational"

@dataclass
class DemoStep:
    """Individual step in a demonstration"""
    step_id: str
    action: str  # click, type, navigate, wait, screenshot, highlight
    target: str  # selector, URL, text
    description: str
    narration: str
    duration_seconds: float = 2.0
    highlight_element: bool = False
    screenshot_timing: str = "after"  # before, after, both
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Demonstration:
    """Complete demonstration session"""
    demo_id: str
    title: str
    description: str
    course_id: str
    topic: str
    demo_type: DemoType
    steps: List[DemoStep]
    narration_style: NarrationStyle
    target_url: str
    created_at: datetime
    duration_minutes: float = 0.0
    video_path: Optional[str] = None
    audio_path: Optional[str] = None
    transcript_path: Optional[str] = None
    status: str = "created"

@dataclass
class AINarrator:
    """AI-powered narration system"""
    narrator_id: str
    name: str
    voice_profile: str
    speaking_rate: float = 1.0
    tone: str = "professional"
    expertise_level: str = "expert"

class PlaywrightDemoSystem:
    """Comprehensive demonstration system using Playwright"""
    
    def __init__(self, professor_system=None):
        self.professor_system = professor_system
        self.demonstrations: Dict[str, Demonstration] = {}
        self.narrators = self._initialize_narrators()
        self.output_dir = Path("demonstrations/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _initialize_narrators(self) -> List[AINarrator]:
        """Initialize AI narrators with different styles"""
        return [
            AINarrator(
                narrator_id="NARRATOR_001",
                name="Dr. Sarah Chen",
                voice_profile="enthusiastic_expert",
                speaking_rate=1.1,
                tone="enthusiastic",
                expertise_level="expert"
            ),
            AINarrator(
                narrator_id="NARRATOR_002", 
                name="Dr. Marcus Rodriguez",
                voice_profile="analytical_guide",
                speaking_rate=0.9,
                tone="analytical",
                expertise_level="expert"
            ),
            AINarrator(
                narrator_id="NARRATOR_003",
                name="Dr. Aisha Patel", 
                voice_profile="empathetic_mentor",
                speaking_rate=1.0,
                tone="empathetic",
                expertise_level="expert"
            ),
            AINarrator(
                narrator_id="NARRATOR_004",
                name="Dr. James Kim",
                voice_profile="conversational_peer",
                speaking_rate=1.2,
                tone="conversational",
                expertise_level="expert"
            )
        ]
    
    def create_demonstration(self, demo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new demonstration"""
        demo_id = f"DEMO_{uuid.uuid4().hex[:8].upper()}"
        
        # Create demo steps
        steps = []
        for i, step_data in enumerate(demo_data["steps"]):
            step = DemoStep(
                step_id=f"STEP_{i+1:03d}",
                action=step_data["action"],
                target=step_data["target"],
                description=step_data["description"],
                narration=step_data.get("narration", ""),
                duration_seconds=step_data.get("duration_seconds", 2.0),
                highlight_element=step_data.get("highlight_element", False),
                screenshot_timing=step_data.get("screenshot_timing", "after"),
                metadata=step_data.get("metadata", {})
            )
            steps.append(step)
        
        demonstration = Demonstration(
            demo_id=demo_id,
            title=demo_data["title"],
            description=demo_data["description"],
            course_id=demo_data["course_id"],
            topic=demo_data["topic"],
            demo_type=DemoType(demo_data["demo_type"]),
            steps=steps,
            narration_style=NarrationStyle(demo_data["narration_style"]),
            target_url=demo_data["target_url"],
            created_at=datetime.now()
        )
        
        self.demonstrations[demo_id] = demonstration
        
        return {
            "success": True,
            "demo_id": demo_id,
            "message": "Demonstration created successfully"
        }
    
    async def execute_demonstration(self, demo_id: str) -> Dict[str, Any]:
        """Execute demonstration with Playwright and generate video"""
        if not async_playwright:
            return {"success": False, "error": "Playwright not available"}
        
        demonstration = self.demonstrations.get(demo_id)
        if not demonstration:
            return {"success": False, "error": "Demonstration not found"}
        
        try:
            async with async_playwright() as p:
                # Launch browser with video recording
                browser = await p.chromium.launch(
                    headless=False,  # Show browser for better demos
                    args=['--start-maximized']
                )
                
                # Create context with video recording
                context = await browser.new_context(
                    record_video_dir=str(self.output_dir / "videos"),
                    viewport={'width': 1920, 'height': 1080}
                )
                
                page = await context.new_page()
                
                # Navigate to target URL
                await page.goto(demonstration.target_url)
                await page.wait_for_load_state('networkidle')
                
                # Execute demonstration steps
                execution_results = await self._execute_demo_steps(page, demonstration)
                
                # Close browser to finalize video
                await context.close()
                await browser.close()
                
                # Process video and add AI narration
                video_path = execution_results["video_path"]
                enhanced_video = await self._enhance_video_with_ai(
                    video_path, demonstration, execution_results
                )
                
                # Update demonstration with results
                demonstration.video_path = enhanced_video["video_path"]
                demonstration.audio_path = enhanced_video["audio_path"]
                demonstration.transcript_path = enhanced_video["transcript_path"]
                demonstration.duration_minutes = enhanced_video["duration_minutes"]
                demonstration.status = "completed"
                
                return {
                    "success": True,
                    "demo_id": demo_id,
                    "video_path": enhanced_video["video_path"],
                    "audio_path": enhanced_video["audio_path"],
                    "transcript_path": enhanced_video["transcript_path"],
                    "duration_minutes": enhanced_video["duration_minutes"],
                    "execution_summary": execution_results["summary"]
                }
                
        except Exception as e:
            demonstration.status = "failed"
            return {
                "success": False,
                "error": f"Demonstration execution failed: {str(e)}"
            }
    
    async def _execute_demo_steps(self, page: Page, demonstration: Demonstration) -> Dict[str, Any]:
        """Execute individual demonstration steps"""
        execution_log = []
        screenshots = []
        
        for step in demonstration.steps:
            try:
                # Take screenshot before action if requested
                if step.screenshot_timing in ["before", "both"]:
                    screenshot_path = await self._take_screenshot(page, step.step_id, "before")
                    screenshots.append(screenshot_path)
                
                # Highlight element if requested
                if step.highlight_element and step.target:
                    await self._highlight_element(page, step.target)
                
                # Execute the action
                await self._execute_action(page, step)
                
                # Wait for specified duration
                await page.wait_for_timeout(int(step.duration_seconds * 1000))
                
                # Take screenshot after action if requested
                if step.screenshot_timing in ["after", "both"]:
                    screenshot_path = await self._take_screenshot(page, step.step_id, "after")
                    screenshots.append(screenshot_path)
                
                execution_log.append({
                    "step_id": step.step_id,
                    "action": step.action,
                    "target": step.target,
                    "status": "success",
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                execution_log.append({
                    "step_id": step.step_id,
                    "action": step.action,
                    "target": step.target,
                    "status": "failed",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        # Get video path (Playwright saves it automatically)
        video_path = await page.video.path()
        
        return {
            "video_path": str(video_path),
            "screenshots": screenshots,
            "execution_log": execution_log,
            "summary": {
                "total_steps": len(demonstration.steps),
                "successful_steps": len([log for log in execution_log if log["status"] == "success"]),
                "failed_steps": len([log for log in execution_log if log["status"] == "failed"])
            }
        }
    
    async def _execute_action(self, page: Page, step: DemoStep):
        """Execute a single demonstration action"""
        action = step.action.lower()
        target = step.target
        
        if action == "navigate":
            await page.goto(target)
            await page.wait_for_load_state('networkidle')
        
        elif action == "click":
            await page.click(target)
            await page.wait_for_timeout(500)  # Brief pause after click
        
        elif action == "type":
            # Extract text from metadata or use target
            text = step.metadata.get("text", target)
            await page.fill(target, text)
            await page.wait_for_timeout(500)
        
        elif action == "select":
            value = step.metadata.get("value", target)
            await page.select_option(target, value)
            await page.wait_for_timeout(500)
        
        elif action == "hover":
            await page.hover(target)
            await page.wait_for_timeout(1000)
        
        elif action == "scroll":
            direction = step.metadata.get("direction", "down")
            if direction == "down":
                await page.mouse.wheel(0, 500)
            else:
                await page.mouse.wheel(0, -500)
            await page.wait_for_timeout(1000)
        
        elif action == "wait":
            await page.wait_for_timeout(int(float(target) * 1000))
        
        elif action == "wait_for_element":
            await page.wait_for_selector(target)
        
        elif action == "screenshot":
            await self._take_screenshot(page, step.step_id, "action")
        
        else:
            raise ValueError(f"Unknown action: {action}")
    
    async def _highlight_element(self, page: Page, selector: str):
        """Highlight an element on the page"""
        await page.evaluate(f"""
            const element = document.querySelector('{selector}');
            if (element) {{
                element.style.border = '3px solid #ff6b6b';
                element.style.boxShadow = '0 0 10px rgba(255, 107, 107, 0.5)';
                element.style.transition = 'all 0.3s ease';
            }}
        """)
        await page.wait_for_timeout(1000)
        
        # Remove highlight
        await page.evaluate(f"""
            const element = document.querySelector('{selector}');
            if (element) {{
                element.style.border = '';
                element.style.boxShadow = '';
            }}
        """)
    
    async def _take_screenshot(self, page: Page, step_id: str, timing: str) -> str:
        """Take a screenshot of the current page"""
        screenshot_dir = self.output_dir / "screenshots"
        screenshot_dir.mkdir(exist_ok=True)
        
        screenshot_path = screenshot_dir / f"{step_id}_{timing}.png"
        await page.screenshot(path=str(screenshot_path), full_page=True)
        
        return str(screenshot_path)
    
    async def _enhance_video_with_ai(self, video_path: str, demonstration: Demonstration, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance video with AI narration and annotations"""
        # Generate AI narration script
        narration_script = self._generate_narration_script(demonstration, execution_results)
        
        # Create audio narration
        audio_path = await self._generate_ai_narration(narration_script, demonstration.narration_style)
        
        # Combine video and audio
        enhanced_video_path = await self._combine_video_audio(video_path, audio_path, demonstration.demo_id)
        
        # Save transcript
        transcript_path = self._save_transcript(narration_script, demonstration.demo_id)
        
        # Calculate duration
        duration_minutes = len(narration_script) * 0.1  # Rough estimate
        
        return {
            "video_path": enhanced_video_path,
            "audio_path": audio_path,
            "transcript_path": transcript_path,
            "duration_minutes": duration_minutes
        }
    
    def _generate_narration_script(self, demonstration: Demonstration, execution_results: Dict[str, Any]) -> List[str]:
        """Generate AI-powered narration script"""
        script = []
        
        # Introduction
        narrator = self._get_narrator_for_style(demonstration.narration_style)
        script.append(f"Welcome! I'm {narrator.name}, and today we'll be exploring {demonstration.title}.")
        script.append(f"This demonstration is part of our {demonstration.topic} module.")
        script.append(f"We'll be working with {demonstration.target_url} to show you practical applications.")
        
        # Step-by-step narration
        for i, step in enumerate(demonstration.steps):
            script.append(f"Step {i+1}: {step.narration or step.description}")
            
            # Add contextual explanations based on demo type
            if demonstration.demo_type == DemoType.TUTORIAL:
                script.append(f"Notice how this action demonstrates the key concept we're learning.")
            elif demonstration.demo_type == DemoType.CODE_WALKTHROUGH:
                script.append(f"This code pattern is commonly used in {demonstration.topic} applications.")
            elif demonstration.demo_type == DemoType.TOOL_DEMONSTRATION:
                script.append(f"This tool feature helps us achieve our learning objectives efficiently.")
        
        # Conclusion
        script.append(f"That concludes our demonstration of {demonstration.title}.")
        script.append(f"Try practicing these steps yourself to reinforce your understanding.")
        script.append(f"Thank you for watching, and happy learning!")
        
        return script
    
    def _get_narrator_for_style(self, style: NarrationStyle) -> AINarrator:
        """Get appropriate narrator for the style"""
        style_mapping = {
            NarrationStyle.PROFESSOR_LECTURE: self.narrators[0],  # Dr. Sarah Chen
            NarrationStyle.TUTORIAL_GUIDE: self.narrators[1],     # Dr. Marcus Rodriguez
            NarrationStyle.PEER_EXPLANATION: self.narrators[3],    # Dr. James Kim
            NarrationStyle.EXPERT_DEMONSTRATION: self.narrators[0], # Dr. Sarah Chen
            NarrationStyle.CONVERSATIONAL: self.narrators[3]       # Dr. James Kim
        }
        return style_mapping.get(style, self.narrators[0])
    
    async def _generate_ai_narration(self, script: List[str], style: NarrationStyle) -> str:
        """Generate AI narration audio"""
        # This would integrate with text-to-speech services
        # For now, we'll create a placeholder
        audio_dir = self.output_dir / "audio"
        audio_dir.mkdir(exist_ok=True)
        
        audio_path = audio_dir / f"narration_{uuid.uuid4().hex[:8]}.wav"
        
        # In a real implementation, this would:
        # 1. Use Azure Cognitive Services, Google Cloud TTS, or AWS Polly
        # 2. Apply voice profiles based on narrator
        # 3. Adjust speaking rate and tone
        # 4. Generate natural-sounding speech
        
        # Placeholder: Save script as text file
        with open(audio_path.with_suffix('.txt'), 'w') as f:
            f.write('\n'.join(script))
        
        return str(audio_path)
    
    async def _combine_video_audio(self, video_path: str, audio_path: str, demo_id: str) -> str:
        """Combine video and audio using FFmpeg"""
        enhanced_dir = self.output_dir / "enhanced"
        enhanced_dir.mkdir(exist_ok=True)
        
        enhanced_video_path = enhanced_dir / f"enhanced_{demo_id}.mp4"
        
        # FFmpeg command to combine video and audio
        # This is a placeholder - in production, you'd use subprocess or ffmpeg-python
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                str(enhanced_video_path)
            ]
            
            # For now, just copy the original video
            import shutil
            shutil.copy2(video_path, enhanced_video_path)
            
        except Exception as e:
            print(f"Video enhancement failed: {e}")
            # Fallback to original video
            enhanced_video_path = Path(video_path)
        
        return str(enhanced_video_path)
    
    def _save_transcript(self, script: List[str], demo_id: str) -> str:
        """Save narration transcript"""
        transcript_dir = self.output_dir / "transcripts"
        transcript_dir.mkdir(exist_ok=True)
        
        transcript_path = transcript_dir / f"transcript_{demo_id}.txt"
        
        with open(transcript_path, 'w') as f:
            f.write('\n'.join(script))
        
        return str(transcript_path)
    
    def generate_course_demonstrations(self, course_id: str) -> Dict[str, Any]:
        """Generate demonstrations for an entire course"""
        # This would integrate with the curriculum system
        # For now, return a placeholder
        return {
            "success": True,
            "course_id": course_id,
            "demonstrations_created": 0,
            "message": "Course demonstrations generation not yet implemented"
        }
    
    def get_demonstration_status(self, demo_id: str) -> Dict[str, Any]:
        """Get status of a demonstration"""
        demonstration = self.demonstrations.get(demo_id)
        if not demonstration:
            return {"error": "Demonstration not found"}
        
        return {
            "demo_id": demo_id,
            "title": demonstration.title,
            "status": demonstration.status,
            "created_at": demonstration.created_at.isoformat(),
            "video_path": demonstration.video_path,
            "audio_path": demonstration.audio_path,
            "transcript_path": demonstration.transcript_path,
            "duration_minutes": demonstration.duration_minutes,
            "steps_count": len(demonstration.steps)
        }
    
    def list_demonstrations(self, course_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all demonstrations, optionally filtered by course"""
        demos = list(self.demonstrations.values())
        
        if course_id:
            demos = [d for d in demos if d.course_id == course_id]
        
        return [
            {
                "demo_id": demo.demo_id,
                "title": demo.title,
                "course_id": demo.course_id,
                "topic": demo.topic,
                "demo_type": demo.demo_type.value,
                "status": demo.status,
                "created_at": demo.created_at.isoformat(),
                "duration_minutes": demo.duration_minutes
            }
            for demo in demos
        ]

# Example usage and demo creation
async def create_sample_demonstration():
    """Create a sample demonstration for testing"""
    demo_system = PlaywrightDemoSystem()
    
    # Sample demo data
    demo_data = {
        "title": "Introduction to Machine Learning with TensorFlow",
        "description": "Learn the basics of ML using TensorFlow Playground",
        "course_id": "AI501",
        "topic": "Machine Learning Fundamentals",
        "demo_type": "tutorial",
        "narration_style": "professor_lecture",
        "target_url": "https://playground.tensorflow.org/",
        "steps": [
            {
                "action": "navigate",
                "target": "https://playground.tensorflow.org/",
                "description": "Navigate to TensorFlow Playground",
                "narration": "Let's start by opening TensorFlow Playground, an interactive tool for learning machine learning concepts.",
                "duration_seconds": 3.0,
                "screenshot_timing": "after"
            },
            {
                "action": "click",
                "target": ".dataset-button",
                "description": "Select a dataset",
                "narration": "First, let's choose a dataset to work with. I'll select the spiral dataset which is great for understanding classification.",
                "duration_seconds": 2.0,
                "highlight_element": True
            },
            {
                "action": "click",
                "target": ".play-button",
                "description": "Start training",
                "narration": "Now let's start training our neural network. Watch how the model learns to separate the data points.",
                "duration_seconds": 5.0,
                "screenshot_timing": "after"
            }
        ]
    }
    
    # Create demonstration
    result = demo_system.create_demonstration(demo_data)
    print(f"Demo created: {result}")
    
    # Execute demonstration
    if result["success"]:
        execution_result = await demo_system.execute_demonstration(result["demo_id"])
        print(f"Demo executed: {execution_result}")
    
    return demo_system

if __name__ == "__main__":
    # Run sample demonstration
    asyncio.run(create_sample_demonstration())