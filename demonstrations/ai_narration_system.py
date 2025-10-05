"""
MS AI Curriculum System - AI Narration System
Advanced text-to-speech with AI Professor personalities
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum
import json
import uuid
import asyncio
from pathlib import Path

class VoiceProfile(Enum):
    ENTHUSIASTIC_EXPERT = "enthusiastic_expert"
    ANALYTICAL_GUIDE = "analytical_guide"
    EMPATHETIC_MENTOR = "empathetic_mentor"
    CONVERSATIONAL_PEER = "conversational_peer"
    PROFESSIONAL_LECTURER = "professional_lecturer"

class SpeechEmotion(Enum):
    NEUTRAL = "neutral"
    ENTHUSIASTIC = "enthusiastic"
    ANALYTICAL = "analytical"
    EMPATHETIC = "empathetic"
    CONVERSATIONAL = "conversational"
    EXCITED = "excited"
    THOUGHTFUL = "thoughtful"

@dataclass
class NarrationConfig:
    """Configuration for AI narration"""
    voice_profile: VoiceProfile
    speaking_rate: float = 1.0
    pitch: float = 1.0
    volume: float = 1.0
    emotion: SpeechEmotion = SpeechEmotion.NEUTRAL
    pause_duration: float = 0.5
    emphasis_words: List[str] = None
    background_music: bool = False
    music_volume: float = 0.3

@dataclass
class NarrationSegment:
    """Individual segment of narration"""
    segment_id: str
    text: str
    start_time: float
    duration: float
    emotion: SpeechEmotion
    emphasis_words: List[str]
    professor_name: str
    context: str

class AINarrationSystem:
    """Advanced AI-powered narration system"""
    
    def __init__(self, professor_system=None):
        self.professor_system = professor_system
        self.voice_profiles = self._initialize_voice_profiles()
        self.output_dir = Path("demonstrations/narration")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _initialize_voice_profiles(self) -> Dict[VoiceProfile, Dict[str, Any]]:
        """Initialize voice profiles for AI Professors"""
        return {
            VoiceProfile.ENTHUSIASTIC_EXPERT: {
                "professor": "Dr. Sarah Chen",
                "voice_settings": {
                    "rate": 1.1,
                    "pitch": 1.05,
                    "volume": 1.0,
                    "emotion": SpeechEmotion.ENTHUSIASTIC
                },
                "speaking_patterns": [
                    "Let's dive into this exciting topic!",
                    "This is absolutely fascinating!",
                    "I'm thrilled to show you this!",
                    "You're going to love this!"
                ],
                "transition_phrases": [
                    "Now, here's something really interesting...",
                    "But wait, there's more!",
                    "This is where it gets exciting!",
                    "Let me show you something amazing!"
                ]
            },
            VoiceProfile.ANALYTICAL_GUIDE: {
                "professor": "Dr. Marcus Rodriguez",
                "voice_settings": {
                    "rate": 0.9,
                    "pitch": 0.95,
                    "volume": 1.0,
                    "emotion": SpeechEmotion.ANALYTICAL
                },
                "speaking_patterns": [
                    "Let's analyze this step by step.",
                    "From a technical perspective...",
                    "The methodology here is...",
                    "Let's examine the data carefully."
                ],
                "transition_phrases": [
                    "Now, let's consider the implications...",
                    "From an analytical standpoint...",
                    "The key insight here is...",
                    "Let's break this down systematically..."
                ]
            },
            VoiceProfile.EMPATHETIC_MENTOR: {
                "professor": "Dr. Aisha Patel",
                "voice_settings": {
                    "rate": 1.0,
                    "pitch": 1.0,
                    "volume": 1.0,
                    "emotion": SpeechEmotion.EMPATHETIC
                },
                "speaking_patterns": [
                    "I understand this might seem challenging...",
                    "Let's work through this together...",
                    "Remember, learning takes time...",
                    "You're doing great! Let's continue..."
                ],
                "transition_phrases": [
                    "Don't worry if this feels complex...",
                    "Let's take this one step at a time...",
                    "I'm here to support your learning...",
                    "Remember, every expert was once a beginner..."
                ]
            },
            VoiceProfile.CONVERSATIONAL_PEER: {
                "professor": "Dr. James Kim",
                "voice_settings": {
                    "rate": 1.2,
                    "pitch": 1.1,
                    "volume": 1.0,
                    "emotion": SpeechEmotion.CONVERSATIONAL
                },
                "speaking_patterns": [
                    "So, here's the thing...",
                    "You know what's cool about this?",
                    "I've been thinking about this...",
                    "Let me tell you what I discovered..."
                ],
                "transition_phrases": [
                    "By the way, did you know...",
                    "Here's something I found interesting...",
                    "Speaking of which...",
                    "Oh, and here's a fun fact..."
                ]
            }
        }
    
    def generate_narration_script(self, demonstration_data: Dict[str, Any], config: NarrationConfig) -> List[NarrationSegment]:
        """Generate AI-powered narration script"""
        voice_profile = self.voice_profiles[config.voice_profile]
        professor_name = voice_profile["professor"]
        
        segments = []
        current_time = 0.0
        
        # Introduction segment
        intro_text = self._generate_introduction(demonstration_data, voice_profile)
        intro_duration = self._estimate_duration(intro_text, config.speaking_rate)
        
        segments.append(NarrationSegment(
            segment_id=f"intro_{uuid.uuid4().hex[:8]}",
            text=intro_text,
            start_time=current_time,
            duration=intro_duration,
            emotion=config.emotion,
            emphasis_words=self._extract_emphasis_words(intro_text),
            professor_name=professor_name,
            context="introduction"
        ))
        current_time += intro_duration + config.pause_duration
        
        # Step-by-step narration
        for i, step in enumerate(demonstration_data["steps"]):
            step_text = self._generate_step_narration(step, voice_profile, i+1)
            step_duration = self._estimate_duration(step_text, config.speaking_rate)
            
            segments.append(NarrationSegment(
                segment_id=f"step_{i+1}_{uuid.uuid4().hex[:8]}",
                text=step_text,
                start_time=current_time,
                duration=step_duration,
                emotion=self._determine_step_emotion(step, config.emotion),
                emphasis_words=self._extract_emphasis_words(step_text),
                professor_name=professor_name,
                context=f"step_{i+1}"
            ))
            current_time += step_duration + config.pause_duration
        
        # Conclusion segment
        conclusion_text = self._generate_conclusion(demonstration_data, voice_profile)
        conclusion_duration = self._estimate_duration(conclusion_text, config.speaking_rate)
        
        segments.append(NarrationSegment(
            segment_id=f"conclusion_{uuid.uuid4().hex[:8]}",
            text=conclusion_text,
            start_time=current_time,
            duration=conclusion_duration,
            emotion=SpeechEmotion.ENTHUSIASTIC,  # End on positive note
            emphasis_words=self._extract_emphasis_words(conclusion_text),
            professor_name=professor_name,
            context="conclusion"
        ))
        
        return segments
    
    def _generate_introduction(self, demo_data: Dict[str, Any], voice_profile: Dict[str, Any]) -> str:
        """Generate introduction based on professor's style"""
        title = demo_data["title"]
        topic = demo_data["topic"]
        professor_name = voice_profile["professor"]
        
        if voice_profile["professor"] == "Dr. Sarah Chen":
            return f"Welcome! I'm {professor_name}, and I'm absolutely thrilled to guide you through {title}! This is such an exciting topic in {topic}, and I can't wait to show you what we can accomplish together. Let's dive right in!"
        
        elif voice_profile["professor"] == "Dr. Marcus Rodriguez":
            return f"Hello, I'm {professor_name}. Today we'll be exploring {title} as part of our {topic} curriculum. We'll approach this systematically, examining each component carefully to build a comprehensive understanding."
        
        elif voice_profile["professor"] == "Dr. Aisha Patel":
            return f"Hi there! I'm {professor_name}, and I'm here to support you as we learn about {title}. This topic in {topic} might seem complex at first, but don't worry - we'll work through it step by step, and I'll be here to help every step of the way."
        
        elif voice_profile["professor"] == "Dr. James Kim":
            return f"Hey! I'm {professor_name}, and today we're going to explore {title}. You know what's really cool about {topic}? There's always something new to discover. Let me share what I've learned with you!"
        
        else:
            return f"Welcome! I'm {professor_name}, and today we'll be learning about {title} in our {topic} module."
    
    def _generate_step_narration(self, step: Dict[str, Any], voice_profile: Dict[str, Any], step_number: int) -> str:
        """Generate narration for individual step"""
        description = step.get("description", "")
        custom_narration = step.get("narration", "")
        
        if custom_narration:
            # Use custom narration but enhance with professor's style
            return self._enhance_with_professor_style(custom_narration, voice_profile)
        
        # Generate narration based on professor's style
        professor_name = voice_profile["professor"]
        
        if professor_name == "Dr. Sarah Chen":
            return f"Step {step_number}: {description} This is where the magic happens! Watch closely as we {description.lower()}."
        
        elif professor_name == "Dr. Marcus Rodriguez":
            return f"Step {step_number}: {description} Let's analyze this action carefully. Notice the systematic approach we're taking here."
        
        elif professor_name == "Dr. Aisha Patel":
            return f"Step {step_number}: {description} Don't worry if this seems complex - we'll take it slowly. I'm here to guide you through each part."
        
        elif professor_name == "Dr. James Kim":
            return f"Step {step_number}: {description} Here's something interesting about this step - it's actually pretty straightforward once you see how it works!"
        
        else:
            return f"Step {step_number}: {description}"
    
    def _generate_conclusion(self, demo_data: Dict[str, Any], voice_profile: Dict[str, Any]) -> str:
        """Generate conclusion based on professor's style"""
        title = demo_data["title"]
        professor_name = voice_profile["professor"]
        
        if professor_name == "Dr. Sarah Chen":
            return f"Fantastic work! We've successfully completed our exploration of {title}. I hope you're as excited as I am about what we've accomplished! Remember, the best way to learn is by doing, so try these steps yourself. Keep exploring, keep learning, and remember - you've got this!"
        
        elif professor_name == "Dr. Marcus Rodriguez":
            return f"Excellent. We've systematically worked through {title}, examining each component in detail. I encourage you to practice these techniques and consider how they apply to other problems in your studies. The analytical approach we've used here will serve you well in future projects."
        
        elif professor_name == "Dr. Aisha Patel":
            return f"Great job working through {title} with me today! Learning new concepts takes courage, and you've shown that courage. Remember, every expert was once a beginner, and you're well on your way. Take your time practicing these skills, and don't hesitate to reach out if you need support."
        
        elif professor_name == "Dr. James Kim":
            return f"Awesome! We've covered {title}, and I hope you found it as interesting as I do! The cool thing about what we've learned is that it opens up so many possibilities. Try experimenting with these concepts - you might discover something new that you can share with the rest of us!"
        
        else:
            return f"That concludes our demonstration of {title}. Thank you for your attention, and happy learning!"
    
    def _enhance_with_professor_style(self, text: str, voice_profile: Dict[str, Any]) -> str:
        """Enhance custom narration with professor's speaking style"""
        professor_name = voice_profile["professor"]
        
        if professor_name == "Dr. Sarah Chen":
            # Add enthusiasm
            if not any(word in text.lower() for word in ["exciting", "amazing", "fantastic", "wonderful"]):
                text = f"This is exciting - {text.lower()}"
        
        elif professor_name == "Dr. Marcus Rodriguez":
            # Add analytical tone
            if not any(word in text.lower() for word in ["analyze", "examine", "consider", "observe"]):
                text = f"Let's examine this: {text}"
        
        elif professor_name == "Dr. Aisha Patel":
            # Add supportive tone
            if not any(word in text.lower() for word in ["don't worry", "it's okay", "you're doing great"]):
                text = f"Don't worry, {text.lower()}"
        
        elif professor_name == "Dr. James Kim":
            # Add conversational tone
            if not any(word in text.lower() for word in ["you know", "here's the thing", "so"]):
                text = f"So, here's the thing - {text.lower()}"
        
        return text
    
    def _determine_step_emotion(self, step: Dict[str, Any], base_emotion: SpeechEmotion) -> SpeechEmotion:
        """Determine appropriate emotion for step"""
        action = step.get("action", "").lower()
        
        if action in ["click", "navigate", "start"]:
            return SpeechEmotion.ENTHUSIASTIC
        elif action in ["wait", "pause"]:
            return SpeechEmotion.THOUGHTFUL
        elif action in ["type", "select"]:
            return SpeechEmotion.ANALYTICAL
        else:
            return base_emotion
    
    def _extract_emphasis_words(self, text: str) -> List[str]:
        """Extract words that should be emphasized"""
        emphasis_keywords = [
            "important", "key", "critical", "essential", "crucial",
            "notice", "observe", "watch", "focus", "attention",
            "remember", "recall", "keep in mind", "don't forget"
        ]
        
        emphasized = []
        words = text.lower().split()
        
        for i, word in enumerate(words):
            if word in emphasis_keywords:
                # Include the word and next 1-2 words for context
                emphasized.append(" ".join(words[i:i+3]))
        
        return emphasized
    
    def _estimate_duration(self, text: str, speaking_rate: float) -> float:
        """Estimate duration of speech based on text length and rate"""
        # Average speaking rate: ~150 words per minute
        words = len(text.split())
        base_duration = (words / 150) * 60  # Convert to seconds
        return base_duration / speaking_rate
    
    async def generate_audio_narration(self, segments: List[NarrationSegment], config: NarrationConfig) -> str:
        """Generate audio narration from segments"""
        # This would integrate with TTS services like:
        # - Azure Cognitive Services Speech
        # - Google Cloud Text-to-Speech
        # - AWS Polly
        # - ElevenLabs (for more natural voices)
        
        audio_dir = self.output_dir / "audio"
        audio_dir.mkdir(exist_ok=True)
        
        # For now, create a placeholder audio file path
        audio_path = audio_dir / f"narration_{uuid.uuid4().hex[:8]}.wav"
        
        # In production, this would:
        # 1. Convert each segment to audio using TTS
        # 2. Apply voice settings (rate, pitch, emotion)
        # 3. Add pauses between segments
        # 4. Combine all segments into final audio
        # 5. Optionally add background music
        
        # Save narration script for reference
        script_path = audio_path.with_suffix('.txt')
        with open(script_path, 'w') as f:
            for segment in segments:
                f.write(f"[{segment.start_time:.2f}s] {segment.text}\n")
        
        return str(audio_path)
    
    def create_narration_config(self, professor_name: str, demo_type: str) -> NarrationConfig:
        """Create narration config based on professor and demo type"""
        # Map professor to voice profile
        professor_mapping = {
            "Dr. Sarah Chen": VoiceProfile.ENTHUSIASTIC_EXPERT,
            "Dr. Marcus Rodriguez": VoiceProfile.ANALYTICAL_GUIDE,
            "Dr. Aisha Patel": VoiceProfile.EMPATHETIC_MENTOR,
            "Dr. James Kim": VoiceProfile.CONVERSATIONAL_PEER
        }
        
        voice_profile = professor_mapping.get(professor_name, VoiceProfile.PROFESSIONAL_LECTURER)
        
        # Adjust settings based on demo type
        if demo_type == "tutorial":
            speaking_rate = 0.9  # Slower for tutorials
            emotion = SpeechEmotion.EMPATHETIC
        elif demo_type == "lecture_demo":
            speaking_rate = 1.0  # Normal rate
            emotion = SpeechEmotion.NEUTRAL
        elif demo_type == "hands_on_exercise":
            speaking_rate = 1.1  # Slightly faster
            emotion = SpeechEmotion.ENTHUSIASTIC
        else:
            speaking_rate = 1.0
            emotion = SpeechEmotion.NEUTRAL
        
        return NarrationConfig(
            voice_profile=voice_profile,
            speaking_rate=speaking_rate,
            emotion=emotion,
            pause_duration=0.5,
            background_music=False
        )
    
    def get_narration_preview(self, segments: List[NarrationSegment]) -> Dict[str, Any]:
        """Get preview of narration without generating audio"""
        total_duration = sum(segment.duration for segment in segments)
        
        return {
            "total_segments": len(segments),
            "total_duration_seconds": total_duration,
            "total_duration_minutes": total_duration / 60,
            "professor_name": segments[0].professor_name if segments else "Unknown",
            "segments_preview": [
                {
                    "segment_id": segment.segment_id,
                    "text_preview": segment.text[:100] + "..." if len(segment.text) > 100 else segment.text,
                    "start_time": segment.start_time,
                    "duration": segment.duration,
                    "emotion": segment.emotion.value,
                    "context": segment.context
                }
                for segment in segments[:5]  # Show first 5 segments
            ]
        }