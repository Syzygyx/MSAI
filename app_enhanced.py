#!/usr/bin/env python3
"""
MS AI Curriculum System - Enhanced Application with Application Form
Production entry point for msai.syzygyx.com
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import json
import uvicorn
from datetime import datetime
import uuid

# Create FastAPI application
app = FastAPI(
    title="MS AI Curriculum System",
    description="Human-Centered AI Education Platform with Application Form",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://msai.syzygyx.com", "https://www.msai.syzygyx.com", "http://msai.syzygyx.com", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["msai.syzygyx.com", "www.msai.syzygyx.com", "localhost"]
)

# Setup templates
templates = Jinja2Templates(directory="templates")

# Mount static files if directory exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models for application form
class ApplicationData(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: str
    dateOfBirth: str
    gender: Optional[str] = None
    address: str
    undergraduateDegree: str
    undergraduateGPA: float
    undergraduateInstitution: str
    graduationYear: int
    graduateDegree: Optional[str] = None
    greScore: Optional[int] = None
    toeflScore: Optional[int] = None
    specialization: str
    startTerm: str
    programFormat: str
    interests: List[str] = []
    statementOfPurpose: str
    personalStatement: str
    diversityStatement: str
    researchExperience: str
    careerGoals: str
    additionalInfo: Optional[str] = None
    currentEmployer: Optional[str] = None
    currentPosition: Optional[str] = None
    workExperience: Optional[str] = None
    relevantExperience: Optional[str] = None
    # Reference 1
    reference1Name: str
    reference1Title: str
    reference1Email: EmailStr
    reference1Phone: Optional[str] = None
    reference1Institution: str
    reference1Relationship: str
    reference1YearsKnown: str
    # Reference 2
    reference2Name: str
    reference2Title: str
    reference2Email: EmailStr
    reference2Phone: Optional[str] = None
    reference2Institution: str
    reference2Relationship: str
    reference2YearsKnown: str
    # Reference 3
    reference3Name: str
    reference3Title: str
    reference3Email: EmailStr
    reference3Phone: Optional[str] = None
    reference3Institution: str
    reference3Relationship: str
    reference3YearsKnown: str
    howDidYouHear: Optional[str] = None
    additionalComments: Optional[str] = None
    agreeTerms: bool
    agreeMarketing: bool = False

class ApplicationResponse(BaseModel):
    success: bool
    message: str
    application_id: Optional[str] = None
    timestamp: str

class ApplicationStats(BaseModel):
    total_applications: int
    by_specialization: Dict[str, int]
    by_status: Dict[str, int]
    by_term: Dict[str, int]
    by_format: Dict[str, int]

# In-memory storage for applications (replace with database in production)
applications_storage = []
application_stats = {
    'total_applications': 0,
    'by_specialization': {},
    'by_status': {'New': 0, 'Under Review': 0, 'Accepted': 0, 'Rejected': 0},
    'by_term': {},
    'by_format': {}
}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main landing page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "message": "Welcome to MS AI Curriculum System API",
        "version": "1.0.0",
        "status": "online",
        "domain": "msai.syzygyx.com",
        "description": "Human-Centered AI Education Platform with Application Form",
        "endpoints": {
            "professors": "/api/professors",
            "curriculum": "/api/curriculum", 
            "students": "/api/students",
            "status": "/api/status",
            "health": "/health",
            "metrics": "/metrics",
            "docs": "/docs",
            "application_form": "/application",
            "application_api": "/api/application"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "services": {
            "professors": "online",
            "curriculum": "online",
            "students": "online",
            "database": "online",
            "application_form": "online"
        }
    }

# Application Form Routes
@app.get("/application", response_class=HTMLResponse)
async def get_application_form():
    """Serve the application form"""
    try:
        with open("msai_application_form.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Application form not found</h1>", status_code=404)

@app.post("/api/application", response_model=ApplicationResponse)
async def submit_application(application: ApplicationData):
    """Submit a new application"""
    try:
        # Convert Pydantic model to dict
        form_data = application.dict()
        
        # Generate application ID
        application_id = str(uuid.uuid4())
        form_data['application_id'] = application_id
        form_data['timestamp'] = datetime.now().isoformat()
        form_data['status'] = 'New'
        
        # Store application (in production, save to database)
        applications_storage.append(form_data)
        
        # Update statistics
        application_stats['total_applications'] += 1
        
        # Update specialization stats
        spec = form_data.get('specialization', 'Unknown')
        application_stats['by_specialization'][spec] = application_stats['by_specialization'].get(spec, 0) + 1
        
        # Update term stats
        term = form_data.get('startTerm', 'Unknown')
        application_stats['by_term'][term] = application_stats['by_term'].get(term, 0) + 1
        
        # Update format stats
        format_type = form_data.get('programFormat', 'Unknown')
        application_stats['by_format'][format_type] = application_stats['by_format'].get(format_type, 0) + 1
        
        # Update status stats
        application_stats['by_status']['New'] += 1
        
        return ApplicationResponse(
            success=True,
            message="Application submitted successfully",
            application_id=application_id,
            timestamp=datetime.now().isoformat()
        )
            
    except Exception as e:
        print(f"❌ Error submitting application: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/application/upload")
async def upload_documents(
    application_id: str = Form(...),
    transcript: UploadFile = File(...),
    resume: UploadFile = File(...),
    additional_docs: List[UploadFile] = File([])
):
    """Upload application documents"""
    try:
        # Create upload directory for this application
        upload_dir = Path(f"uploads/{application_id}")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        uploaded_files = {}
        
        # Save transcript
        if transcript:
            transcript_path = upload_dir / f"transcript_{transcript.filename}"
            with open(transcript_path, "wb") as f:
                content = await transcript.read()
                f.write(content)
            uploaded_files['transcript'] = str(transcript_path)
        
        # Save resume
        if resume:
            resume_path = upload_dir / f"resume_{resume.filename}"
            with open(resume_path, "wb") as f:
                content = await resume.read()
                f.write(content)
            uploaded_files['resume'] = str(resume_path)
        
        # Save additional documents
        additional_paths = []
        for i, doc in enumerate(additional_docs):
            doc_path = upload_dir / f"additional_{i}_{doc.filename}"
            with open(doc_path, "wb") as f:
                content = await doc.read()
                f.write(content)
            additional_paths.append(str(doc_path))
        
        uploaded_files['additional_docs'] = additional_paths
        
        return {
            "success": True,
            "message": "Documents uploaded successfully",
            "files": uploaded_files
        }
        
    except Exception as e:
        print(f"❌ Error uploading documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/applications", response_model=List[Dict[str, Any]])
async def get_applications(status: Optional[str] = None):
    """Get all applications or filter by status"""
    try:
        if status:
            filtered_apps = [app for app in applications_storage if app.get('status') == status]
            return filtered_apps
        return applications_storage
    except Exception as e:
        print(f"❌ Error retrieving applications: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/applications/stats", response_model=ApplicationStats)
async def get_application_stats():
    """Get application statistics"""
    try:
        return ApplicationStats(**application_stats)
    except Exception as e:
        print(f"❌ Error getting application stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/applications/{email}/status")
async def update_application_status(
    email: str,
    status: str,
    notes: Optional[str] = None
):
    """Update application status"""
    try:
        # Find application by email
        app_found = False
        for app in applications_storage:
            if app.get('email') == email:
                old_status = app.get('status', 'New')
                app['status'] = status
                app['notes'] = notes or ""
                app_found = True
                
                # Update stats
                application_stats['by_status'][old_status] = max(0, application_stats['by_status'].get(old_status, 0) - 1)
                application_stats['by_status'][status] = application_stats['by_status'].get(status, 0) + 1
                break
        
        if app_found:
            return {"success": True, "message": f"Application status updated to {status}"}
        else:
            raise HTTPException(status_code=404, detail="Application not found")
            
    except Exception as e:
        print(f"❌ Error updating application status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/specializations")
async def get_specializations():
    """Get available specializations"""
    return {
        "specializations": [
            "Machine Learning & Data Science",
            "Natural Language Processing",
            "Computer Vision & Robotics",
            "General AI"
        ]
    }

@app.get("/api/start-terms")
async def get_start_terms():
    """Get available start terms"""
    return {
        "terms": [
            "Fall 2024",
            "Spring 2025",
            "Fall 2025",
            "Spring 2026"
        ]
    }

@app.get("/api/program-formats")
async def get_program_formats():
    """Get available program formats"""
    return {
        "formats": [
            "Full-time",
            "Part-time",
            "Online",
            "Hybrid"
        ]
    }

# Existing Curriculum System Routes
@app.get("/api/professors")
async def get_professors():
    """Get AI professors information"""
    return {
        "professors": [
            {
                "id": "prof_001",
                "name": "Dr. Sarah Chen",
                "specialization": "Machine Learning",
                "expertise_level": "Expert",
                "h_index": 45,
                "total_citations": 1250,
                "persona": {
                    "teaching_philosophy": "Learning through hands-on experience and real-world applications",
                    "motivational_quotes": ["The future belongs to those who learn AI today", "Every algorithm tells a story"]
                }
            },
            {
                "id": "prof_002", 
                "name": "Dr. Michael Rodriguez",
                "specialization": "Natural Language Processing",
                "expertise_level": "Expert",
                "h_index": 38,
                "total_citations": 980,
                "persona": {
                    "teaching_philosophy": "Understanding language is understanding intelligence",
                    "motivational_quotes": ["Language is the bridge between human and artificial intelligence", "Words have power, algorithms amplify it"]
                }
            }
        ]
    }

@app.get("/api/curriculum")
async def get_curriculum():
    """Get comprehensive curriculum information"""
    return {
        "program_info": {
            "program_name": "Master of Science in Artificial Intelligence",
            "total_credits": 36,
            "duration": "2 years",
            "accreditation": "ABET",
            "ai_curriculum_description": "Every course is dynamically generated and personalized using advanced AI algorithms"
        },
        "core_courses": {
            "AI_FUNDAMENTALS": {
                "course_id": "AI_FUNDAMENTALS",
                "course_code": "AI-501",
                "title": "Foundations of Artificial Intelligence",
                "credits": 3,
                "level": "Foundational",
                "description": "Comprehensive introduction to AI concepts, history, and foundational theories.",
                "detailed_description": "This foundational course provides students with a comprehensive understanding of artificial intelligence, covering its historical development, core theoretical frameworks, and fundamental concepts. Students will explore the philosophical foundations of AI, understand different approaches to machine intelligence, and examine the ethical implications of AI development.",
                "learning_outcomes": [
                    "Define and explain core AI concepts and terminology",
                    "Analyze historical development of AI and key milestones",
                    "Evaluate different AI approaches and their applications",
                    "Discuss ethical implications of AI development"
                ],
                "modules": [
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
                    }
                ],
                "ai_generated_content": {
                    "adaptive_learning_paths": "Personalized curriculum based on student background",
                    "ai_tutors": ["Dr. Sarah Chen (ML Specialist)", "Dr. Michael Rodriguez (NLP Expert)"],
                    "content_generation": "Dynamic course materials based on current AI research"
                },
                "career_pathways": ["AI Researcher", "Machine Learning Engineer", "AI Product Manager", "AI Consultant"]
            },
            "ML_FUNDAMENTALS": {
                "course_id": "ML_FUNDAMENTALS",
                "course_code": "AI-502",
                "title": "Machine Learning Fundamentals",
                "credits": 3,
                "level": "Foundational",
                "description": "Hands-on introduction to machine learning algorithms, implementation, and real-world applications.",
                "detailed_description": "This course provides a comprehensive, hands-on introduction to machine learning algorithms and their practical implementation. Students will learn to build, train, and evaluate machine learning models using modern tools and frameworks. The course emphasizes practical application through AI-generated projects that adapt to student interests and career goals.",
                "learning_outcomes": [
                    "Implement supervised learning algorithms",
                    "Apply unsupervised learning techniques",
                    "Evaluate model performance using appropriate metrics",
                    "Optimize models for real-world deployment"
                ],
                "modules": [
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
                    }
                ],
                "ai_generated_content": {
                    "personalized_datasets": "Custom datasets based on student interests",
                    "adaptive_projects": "Projects that scale with student skill level",
                    "ai_code_review": "Automated feedback on code quality and ML best practices"
                },
                "career_pathways": ["Data Scientist", "Machine Learning Engineer", "AI Research Scientist", "MLOps Engineer"]
            },
            "DEEP_LEARNING": {
                "course_id": "DEEP_LEARNING",
                "course_code": "AI-503",
                "title": "Deep Learning and Neural Networks",
                "credits": 3,
                "level": "Advanced",
                "description": "Advanced course covering deep neural networks, architectures, and cutting-edge applications.",
                "detailed_description": "This advanced course delves into deep learning architectures, from basic neural networks to state-of-the-art models like Transformers and GANs. Students will build and train complex neural networks for various applications including computer vision, natural language processing, and generative AI.",
                "learning_outcomes": [
                    "Design and implement deep neural networks",
                    "Apply CNNs for computer vision tasks",
                    "Implement RNNs and Transformers for NLP",
                    "Develop generative models (GANs, VAEs)"
                ],
                "modules": [
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
                    }
                ],
                "ai_generated_content": {
                    "research_integration": "Latest papers automatically integrated into curriculum",
                    "architecture_exploration": "AI suggests novel network architectures",
                    "performance_optimization": "AI helps optimize model performance"
                },
                "career_pathways": ["Deep Learning Engineer", "AI Research Scientist", "Computer Vision Engineer", "NLP Engineer"]
            }
        },
        "specialization_tracks": {
            "ML_DATA_SCIENCE": {
                "track_id": "ML_DATA_SCIENCE",
                "name": "Machine Learning & Data Science",
                "description": "This specialization focuses on advanced machine learning techniques, data science methodologies, and the development of intelligent systems that can learn from data. Students will master both theoretical foundations and practical implementation of ML algorithms, statistical modeling, and data-driven decision making.",
                "total_credits": 12,
                "core_courses": ["ML_FUNDAMENTALS", "DEEP_LEARNING"],
                "elective_courses": [
                    "Advanced Statistical Learning",
                    "Big Data Analytics",
                    "MLOps and Model Deployment",
                    "Reinforcement Learning",
                    "Time Series Analysis",
                    "Ensemble Methods"
                ],
                "capstone_project": "Develop a comprehensive machine learning system that addresses a real-world problem. Students will work with industry partners or research labs to identify a meaningful challenge, collect and preprocess data, develop and optimize ML models, and deploy the solution.",
                "industry_partnerships": ["Google AI Research", "Microsoft Azure ML", "Amazon ML Solutions", "Data Science Consulting Firms"],
                "career_outcomes": ["Machine Learning Engineer", "Data Scientist", "MLOps Engineer", "AI Research Scientist"],
                "ai_curriculum_focus": "AI-generated personalized learning paths based on student interests and career goals. Virtual AI professors provide mentorship in specialized ML domains."
            },
            "NLP_TRACK": {
                "track_id": "NLP_TRACK",
                "name": "Natural Language Processing",
                "description": "This specialization delves deep into natural language processing, covering both traditional linguistic approaches and modern transformer-based models. Students will learn to build systems that can understand, process, and generate human language across multiple domains and languages.",
                "total_credits": 12,
                "core_courses": ["NLP_FUNDAMENTALS", "DEEP_LEARNING"],
                "elective_courses": [
                    "Advanced Language Models",
                    "Multilingual NLP",
                    "Conversational AI",
                    "Information Retrieval",
                    "Text Mining and Analytics",
                    "Speech Processing"
                ],
                "capstone_project": "Build a comprehensive NLP system that demonstrates mastery of multiple NLP techniques. Projects may include multilingual chatbots, document analysis systems, language translation tools, or specialized NLP applications for specific industries.",
                "industry_partnerships": ["OpenAI", "Hugging Face", "Google Research", "Facebook AI Research"],
                "career_outcomes": ["NLP Engineer", "Conversational AI Developer", "Language Technology Specialist", "AI Research Scientist"],
                "ai_curriculum_focus": "AI-generated multilingual curriculum that adapts to student language backgrounds. Virtual AI professors fluent in multiple languages provide specialized guidance."
            },
            "CV_ROBOTICS": {
                "track_id": "CV_ROBOTICS",
                "name": "Computer Vision & Robotics",
                "description": "This specialization combines computer vision with robotics to create intelligent systems that can perceive and interact with the physical world. Students will learn to develop vision systems for autonomous vehicles, robotics, medical imaging, and augmented reality applications.",
                "total_credits": 12,
                "core_courses": ["COMPUTER_VISION", "DEEP_LEARNING"],
                "elective_courses": [
                    "Autonomous Vehicle Systems",
                    "Medical Image Analysis",
                    "Robotic Perception",
                    "Augmented Reality",
                    "3D Computer Vision",
                    "Real-time Vision Systems"
                ],
                "capstone_project": "Develop a complete computer vision system for a robotics or autonomous system application. Students will work with industry partners to identify real-world challenges in autonomous vehicles, medical imaging, robotics, or AR/VR.",
                "industry_partnerships": ["Tesla", "Waymo", "Boston Dynamics", "Medical Imaging Companies"],
                "career_outcomes": ["Computer Vision Engineer", "Autonomous Vehicle Engineer", "Robotics Engineer", "Medical AI Specialist"],
                "ai_curriculum_focus": "AI-generated projects that adapt to different hardware platforms and application domains. Virtual AI professors with expertise in specific vision and robotics domains."
            }
        },
        "ai_features": {
            "personalized_learning": "AI adapts curriculum to individual learning styles and career goals",
            "virtual_professors": "AI professors with unique personalities and expertise areas",
            "adaptive_content": "Course materials that evolve based on latest research and industry trends",
            "intelligent_assessment": "AI-powered evaluation that goes beyond traditional testing",
            "real_world_projects": "Industry-relevant projects generated based on current market needs"
        }
    }

@app.get("/api/courses")
async def get_courses():
    """Get detailed course information"""
    curriculum = await get_curriculum()
    return {
        "courses": curriculum["core_courses"],
        "total_courses": len(curriculum["core_courses"]),
        "ai_generated": True,
        "personalization": "Each course adapts to individual learning styles and career goals"
    }

@app.get("/api/courses/{course_id}")
async def get_course_detail(course_id: str):
    """Get detailed information for a specific course"""
    curriculum = await get_curriculum()
    
    if course_id in curriculum["core_courses"]:
        return curriculum["core_courses"][course_id]
    else:
        raise HTTPException(status_code=404, detail="Course not found")

@app.get("/api/tracks")
async def get_specialization_tracks():
    """Get specialization track information"""
    curriculum = await get_curriculum()
    return {
        "tracks": curriculum["specialization_tracks"],
        "total_tracks": len(curriculum["specialization_tracks"]),
        "ai_curriculum_features": curriculum["ai_features"]
    }

@app.get("/api/tracks/{track_id}")
async def get_track_detail(track_id: str):
    """Get detailed information for a specific specialization track"""
    curriculum = await get_curriculum()
    
    if track_id in curriculum["specialization_tracks"]:
        return curriculum["specialization_tracks"][track_id]
    else:
        raise HTTPException(status_code=404, detail="Track not found")

@app.get("/api/students")
async def get_students():
    """Get simulated students"""
    return {
        "students": [
            {
                "id": "student_001",
                "name": "Alex Johnson",
                "learning_style": "Visual",
                "current_level": "Intermediate",
                "enrolled_courses": ["ML Fundamentals", "Data Structures"],
                "gpa": 3.7
            },
            {
                "id": "student_002",
                "name": "Maria Garcia",
                "learning_style": "Kinesthetic", 
                "current_level": "Advanced",
                "enrolled_courses": ["Deep Learning", "NLP Applications"],
                "gpa": 3.9
            }
        ]
    }

@app.get("/api/status")
async def get_status():
    """Get system status"""
    return {
        "system": "MS AI Curriculum System",
        "status": "operational",
        "version": "1.0.0",
        "uptime": "100%",
        "features": [
            "AI Professor System",
            "Curriculum Generator", 
            "Student Simulator",
            "Interactive Learning",
            "Real-time Assessment",
            "Application Form System"
        ]
    }

@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return {
        "active_users": 150,
        "courses_available": 12,
        "professors_online": 8,
        "students_enrolled": 45,
        "applications_received": application_stats['total_applications'],
        "system_load": "normal",
        "response_time": "120ms"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "app_enhanced:app",
        host=host,
        port=port,
        reload=False,
        workers=1
    )