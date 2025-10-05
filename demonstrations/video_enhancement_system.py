"""
MS AI Curriculum System - Video Enhancement System
Advanced video processing with AI-generated annotations and effects
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
import json
import uuid
import subprocess
from pathlib import Path
import cv2
import numpy as np

class AnnotationType(Enum):
    HIGHLIGHT_BOX = "highlight_box"
    ARROW_POINTER = "arrow_pointer"
    TEXT_CALLOUT = "text_callout"
    CIRCLE_HIGHLIGHT = "circle_highlight"
    PROGRESS_BAR = "progress_bar"
    STEP_NUMBER = "step_number"
    PROFESSOR_AVATAR = "professor_avatar"

class AnimationStyle(Enum):
    FADE_IN = "fade_in"
    SLIDE_IN = "slide_in"
    BOUNCE = "bounce"
    GLOW = "glow"
    PULSE = "pulse"
    TYPEWRITER = "typewriter"

@dataclass
class VideoAnnotation:
    """Individual annotation for video enhancement"""
    annotation_id: str
    annotation_type: AnnotationType
    start_time: float
    end_time: float
    position: Tuple[int, int]  # (x, y)
    size: Tuple[int, int]  # (width, height)
    text: str = ""
    color: str = "#ff6b6b"
    animation_style: AnimationStyle = AnimationStyle.FADE_IN
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VideoEnhancementConfig:
    """Configuration for video enhancement"""
    add_professor_avatar: bool = True
    add_step_numbers: bool = True
    add_progress_bar: bool = True
    add_highlight_effects: bool = True
    add_text_callouts: bool = True
    background_music: bool = False
    music_volume: float = 0.3
    transition_effects: bool = True
    color_scheme: str = "professional"  # professional, vibrant, minimal

class VideoEnhancementSystem:
    """Advanced video enhancement system for demonstrations"""
    
    def __init__(self):
        self.output_dir = Path("demonstrations/enhanced_videos")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = Path("demonstrations/temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Color schemes
        self.color_schemes = {
            "professional": {
                "primary": "#2c3e50",
                "secondary": "#3498db", 
                "accent": "#e74c3c",
                "text": "#2c3e50",
                "background": "#ecf0f1"
            },
            "vibrant": {
                "primary": "#ff6b6b",
                "secondary": "#4ecdc4",
                "accent": "#45b7d1",
                "text": "#2c3e50",
                "background": "#f8f9fa"
            },
            "minimal": {
                "primary": "#000000",
                "secondary": "#666666",
                "accent": "#999999",
                "text": "#333333",
                "background": "#ffffff"
            }
        }
    
    def enhance_demonstration_video(self, 
                                  video_path: str, 
                                  audio_path: str,
                                  demonstration_data: Dict[str, Any],
                                  narration_segments: List[Any],
                                  config: VideoEnhancementConfig) -> Dict[str, Any]:
        """Enhance demonstration video with AI-generated effects"""
        
        try:
            # Step 1: Extract video information
            video_info = self._get_video_info(video_path)
            
            # Step 2: Generate annotations based on demonstration steps
            annotations = self._generate_annotations(demonstration_data, narration_segments, video_info)
            
            # Step 3: Create enhanced video with annotations
            enhanced_video_path = self._apply_video_enhancements(
                video_path, annotations, config, video_info
            )
            
            # Step 4: Combine video and audio
            final_video_path = self._combine_video_audio(
                enhanced_video_path, audio_path, config
            )
            
            # Step 5: Add final touches (transitions, effects)
            polished_video_path = self._add_final_effects(
                final_video_path, config, video_info
            )
            
            return {
                "success": True,
                "enhanced_video_path": polished_video_path,
                "annotations_count": len(annotations),
                "duration_seconds": video_info["duration"],
                "resolution": f"{video_info['width']}x{video_info['height']}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Video enhancement failed: {str(e)}"
            }
    
    def _get_video_info(self, video_path: str) -> Dict[str, Any]:
        """Get video information using FFprobe"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            
            video_stream = next(s for s in data['streams'] if s['codec_type'] == 'video')
            
            return {
                "duration": float(data['format']['duration']),
                "width": int(video_stream['width']),
                "height": int(video_stream['height']),
                "fps": eval(video_stream['r_frame_rate']),
                "codec": video_stream['codec_name']
            }
        except Exception:
            # Fallback values if FFprobe fails
            return {
                "duration": 60.0,
                "width": 1920,
                "height": 1080,
                "fps": 30.0,
                "codec": "h264"
            }
    
    def _generate_annotations(self, 
                            demonstration_data: Dict[str, Any], 
                            narration_segments: List[Any],
                            video_info: Dict[str, Any]) -> List[VideoAnnotation]:
        """Generate AI-powered annotations for video"""
        annotations = []
        colors = self.color_schemes["professional"]
        
        # Add step number annotations
        for i, step in enumerate(demonstration_data["steps"]):
            step_start_time = i * 5.0  # Assume 5 seconds per step
            step_end_time = step_start_time + 4.0
            
            # Step number annotation
            annotations.append(VideoAnnotation(
                annotation_id=f"step_number_{i+1}",
                annotation_type=AnnotationType.STEP_NUMBER,
                start_time=step_start_time,
                end_time=step_end_time,
                position=(50, 50),
                size=(100, 60),
                text=f"Step {i+1}",
                color=colors["primary"],
                animation_style=AnimationStyle.BOUNCE
            ))
            
            # Highlight element if specified
            if step.get("highlight_element") and step.get("target"):
                annotations.append(VideoAnnotation(
                    annotation_id=f"highlight_{i+1}",
                    annotation_type=AnnotationType.HIGHLIGHT_BOX,
                    start_time=step_start_time + 1.0,
                    end_time=step_end_time,
                    position=(100, 100),  # Would be calculated from element position
                    size=(200, 50),
                    text="",
                    color=colors["accent"],
                    animation_style=AnimationStyle.GLOW,
                    metadata={"element_selector": step["target"]}
                ))
            
            # Text callout for step description
            annotations.append(VideoAnnotation(
                annotation_id=f"callout_{i+1}",
                annotation_type=AnnotationType.TEXT_CALLOUT,
                start_time=step_start_time + 0.5,
                end_time=step_end_time,
                position=(video_info["width"] - 300, 100),
                size=(250, 100),
                text=step.get("description", ""),
                color=colors["secondary"],
                animation_style=AnimationStyle.SLIDE_IN
            ))
        
        # Add progress bar
        annotations.append(VideoAnnotation(
            annotation_id="progress_bar",
            annotation_type=AnnotationType.PROGRESS_BAR,
            start_time=0,
            end_time=video_info["duration"],
            position=(50, video_info["height"] - 50),
            size=(video_info["width"] - 100, 20),
            text="",
            color=colors["primary"],
            animation_style=AnimationStyle.PULSE
        ))
        
        # Add professor avatar (if enabled)
        annotations.append(VideoAnnotation(
            annotation_id="professor_avatar",
            annotation_type=AnnotationType.PROFESSOR_AVATAR,
            start_time=0,
            end_time=video_info["duration"],
            position=(video_info["width"] - 150, 50),
            size=(100, 100),
            text="Dr. Sarah Chen",  # Would come from narration
            color=colors["secondary"],
            animation_style=AnimationStyle.FADE_IN
        ))
        
        return annotations
    
    def _apply_video_enhancements(self, 
                                video_path: str, 
                                annotations: List[VideoAnnotation],
                                config: VideoEnhancementConfig,
                                video_info: Dict[str, Any]) -> str:
        """Apply video enhancements using FFmpeg"""
        
        enhanced_path = self.temp_dir / f"enhanced_{uuid.uuid4().hex[:8]}.mp4"
        
        # Create FFmpeg filter complex for annotations
        filter_complex = self._create_ffmpeg_filter(annotations, video_info, config)
        
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-filter_complex', filter_complex,
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-c:a', 'copy',
                '-y',  # Overwrite output file
                str(enhanced_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return str(enhanced_path)
            
        except subprocess.CalledProcessError as e:
            # Fallback: just copy original video
            import shutil
            shutil.copy2(video_path, enhanced_path)
            return str(enhanced_path)
    
    def _create_ffmpeg_filter(self, 
                            annotations: List[VideoAnnotation],
                            video_info: Dict[str, Any],
                            config: VideoEnhancementConfig) -> str:
        """Create FFmpeg filter complex for annotations"""
        
        filters = []
        colors = self.color_schemes.get(config.color_scheme, self.color_schemes["professional"])
        
        # Add background for annotations
        filters.append(f"color=c={colors['background']}:size={video_info['width']}x{video_info['height']}:duration={video_info['duration']}[bg]")
        
        # Add video input
        filters.append("[0:v][bg]overlay=0:0[base]")
        
        current_input = "base"
        input_count = 1
        
        # Add each annotation
        for annotation in annotations:
            if annotation.annotation_type == AnnotationType.TEXT_CALLOUT:
                # Add text overlay
                text_filter = f"[{current_input}]drawtext=text='{annotation.text}':x={annotation.position[0]}:y={annotation.position[1]}:fontsize=24:fontcolor={colors['text']}:box=1:boxcolor={colors['background']}:boxborderw=5[text{input_count}]"
                filters.append(text_filter)
                current_input = f"text{input_count}"
                input_count += 1
            
            elif annotation.annotation_type == AnnotationType.HIGHLIGHT_BOX:
                # Add rectangle overlay
                rect_filter = f"[{current_input}]drawbox=x={annotation.position[0]}:y={annotation.position[1]}:w={annotation.size[0]}:h={annotation.size[1]}:color={colors['accent']}:t=3[rect{input_count}]"
                filters.append(rect_filter)
                current_input = f"rect{input_count}"
                input_count += 1
            
            elif annotation.annotation_type == AnnotationType.STEP_NUMBER:
                # Add step number
                step_filter = f"[{current_input}]drawtext=text='{annotation.text}':x={annotation.position[0]}:y={annotation.position[1]}:fontsize=36:fontcolor={colors['primary']}:box=1:boxcolor={colors['accent']}:boxborderw=3[step{input_count}]"
                filters.append(step_filter)
                current_input = f"step{input_count}"
                input_count += 1
        
        return ";".join(filters)
    
    def _combine_video_audio(self, 
                           video_path: str, 
                           audio_path: str, 
                           config: VideoEnhancementConfig) -> str:
        """Combine enhanced video with audio narration"""
        
        combined_path = self.temp_dir / f"combined_{uuid.uuid4().hex[:8]}.mp4"
        
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                '-y',
                str(combined_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return str(combined_path)
            
        except subprocess.CalledProcessError:
            # Fallback: return video without audio
            return video_path
    
    def _add_final_effects(self, 
                         video_path: str, 
                         config: VideoEnhancementConfig,
                         video_info: Dict[str, Any]) -> str:
        """Add final effects and polish to video"""
        
        final_path = self.output_dir / f"final_{uuid.uuid4().hex[:8]}.mp4"
        
        try:
            # Add fade in/out effects
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f'fade=in:0:30,fade=out:{int(video_info["duration"]-30)}:30',
                '-c:a', 'copy',
                '-y',
                str(final_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return str(final_path)
            
        except subprocess.CalledProcessError:
            # Fallback: copy video as-is
            import shutil
            shutil.copy2(video_path, final_path)
            return str(final_path)
    
    def create_thumbnail(self, video_path: str, timestamp: float = 5.0) -> str:
        """Create thumbnail from video"""
        
        thumbnail_dir = self.output_dir / "thumbnails"
        thumbnail_dir.mkdir(exist_ok=True)
        
        thumbnail_path = thumbnail_dir / f"thumb_{uuid.uuid4().hex[:8]}.jpg"
        
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-ss', str(timestamp),
                '-vframes', '1',
                '-q:v', '2',
                '-y',
                str(thumbnail_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return str(thumbnail_path)
            
        except subprocess.CalledProcessError:
            # Create placeholder thumbnail
            return self._create_placeholder_thumbnail(str(thumbnail_path))
    
    def _create_placeholder_thumbnail(self, thumbnail_path: str) -> str:
        """Create placeholder thumbnail"""
        # Create a simple colored rectangle as placeholder
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        img[:] = [52, 73, 94]  # Professional blue color
        
        cv2.putText(img, "MS AI Demo", (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv2.imwrite(thumbnail_path, img)
        
        return thumbnail_path
    
    def get_enhancement_preview(self, annotations: List[VideoAnnotation]) -> Dict[str, Any]:
        """Get preview of video enhancements"""
        
        annotation_types = {}
        for annotation in annotations:
            annotation_type = annotation.annotation_type.value
            if annotation_type not in annotation_types:
                annotation_types[annotation_type] = 0
            annotation_types[annotation_type] += 1
        
        return {
            "total_annotations": len(annotations),
            "annotation_types": annotation_types,
            "duration_coverage": self._calculate_duration_coverage(annotations),
            "enhancement_summary": {
                "text_callouts": annotation_types.get("text_callout", 0),
                "highlights": annotation_types.get("highlight_box", 0),
                "step_numbers": annotation_types.get("step_number", 0),
                "progress_indicators": annotation_types.get("progress_bar", 0)
            }
        }
    
    def _calculate_duration_coverage(self, annotations: List[VideoAnnotation]) -> float:
        """Calculate what percentage of video duration has annotations"""
        if not annotations:
            return 0.0
        
        # Find total duration
        max_end_time = max(annotation.end_time for annotation in annotations)
        
        # Calculate covered time (simplified)
        covered_time = sum(annotation.end_time - annotation.start_time for annotation in annotations)
        
        return min(100.0, (covered_time / max_end_time) * 100)
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            self.temp_dir.mkdir(exist_ok=True)