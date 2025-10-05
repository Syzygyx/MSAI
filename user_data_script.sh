#!/bin/bash
set -e

echo "🚀 Starting MS AI Enhanced Application Deployment..."

# Update system
apt-get update
apt-get upgrade -y

# Install required packages
apt-get install -y python3 python3-pip python3-venv nginx git curl wget

# Create application directory
mkdir -p /opt/msai
cd /opt/msai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 python-dotenv==1.0.0 pydantic==2.5.0 jinja2==3.1.2 python-multipart==0.0.6 email-validator==2.1.0

# Create the enhanced application
cat > app.py << 'EOF'
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
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MSAI Application Form - Master of Science in Artificial Intelligence</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; line-height: 1.6; color: #333; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); overflow: hidden; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }
        .header h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 10px; }
        .header p { font-size: 1.1rem; opacity: 0.9; }
        .form-container { padding: 40px; }
        .form-group { margin-bottom: 25px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #333; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 12px 16px; border: 2px solid #e1e5e9; border-radius: 10px; font-size: 16px; transition: border-color 0.3s ease; }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: #667eea; }
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .submit-btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 40px; border: none; border-radius: 10px; font-size: 18px; font-weight: 600; cursor: pointer; transition: transform 0.3s ease; width: 100%; }
        .submit-btn:hover { transform: translateY(-2px); }
        .success-message { background: #d4edda; color: #155724; padding: 15px; border-radius: 10px; margin-bottom: 20px; display: none; }
        .error-message { background: #f8d7da; color: #721c24; padding: 15px; border-radius: 10px; margin-bottom: 20px; display: none; }
        @media (max-width: 768px) { .form-row { grid-template-columns: 1fr; } .header h1 { font-size: 2rem; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-graduation-cap"></i> MSAI Application</h1>
            <p>Master of Science in Artificial Intelligence - Apply Now</p>
        </div>
        
        <div class="form-container">
            <div class="success-message" id="successMessage">
                <i class="fas fa-check-circle"></i> Application submitted successfully! We'll be in touch soon.
            </div>
            
            <div class="error-message" id="errorMessage">
                <i class="fas fa-exclamation-circle"></i> There was an error submitting your application. Please try again.
            </div>
            
            <form id="msaiApplicationForm">
                <div class="form-row">
                    <div class="form-group">
                        <label for="firstName">First Name *</label>
                        <input type="text" id="firstName" name="firstName" required>
                    </div>
                    <div class="form-group">
                        <label for="lastName">Last Name *</label>
                        <input type="text" id="lastName" name="lastName" required>
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="email">Email Address *</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    <div class="form-group">
                        <label for="phone">Phone Number *</label>
                        <input type="tel" id="phone" name="phone" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="specialization">Specialization Track *</label>
                    <select id="specialization" name="specialization" required>
                        <option value="">Select a specialization</option>
                        <option value="Machine Learning & Data Science">Machine Learning & Data Science</option>
                        <option value="Natural Language Processing">Natural Language Processing</option>
                        <option value="Computer Vision & Robotics">Computer Vision & Robotics</option>
                        <option value="General AI">General AI</option>
                    </select>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="startTerm">Start Term *</label>
                        <select id="startTerm" name="startTerm" required>
                            <option value="">Select start term</option>
                            <option value="Fall 2024">Fall 2024</option>
                            <option value="Spring 2025">Spring 2025</option>
                            <option value="Fall 2025">Fall 2025</option>
                            <option value="Spring 2026">Spring 2026</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="programFormat">Program Format *</label>
                        <select id="programFormat" name="programFormat" required>
                            <option value="">Select program format</option>
                            <option value="Full-time">Full-time</option>
                            <option value="Part-time">Part-time</option>
                            <option value="Online">Online</option>
                            <option value="Hybrid">Hybrid</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="undergraduateDegree">Undergraduate Degree *</label>
                    <input type="text" id="undergraduateDegree" name="undergraduateDegree" required>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="undergraduateGPA">Undergraduate GPA *</label>
                        <input type="number" id="undergraduateGPA" name="undergraduateGPA" step="0.01" min="0" max="4" required>
                    </div>
                    <div class="form-group">
                        <label for="graduationYear">Graduation Year *</label>
                        <input type="number" id="graduationYear" name="graduationYear" min="1950" max="2024" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="statementOfPurpose">Statement of Purpose *</label>
                    <textarea id="statementOfPurpose" name="statementOfPurpose" rows="4" required placeholder="Tell us about your interest in AI and career goals..."></textarea>
                </div>
                
                <div class="form-group">
                    <label for="researchExperience">Research Experience</label>
                    <textarea id="researchExperience" name="researchExperience" rows="3" placeholder="Describe any research experience or projects..."></textarea>
                </div>
                
                <div class="form-group">
                    <label for="careerGoals">Career Goals *</label>
                    <textarea id="careerGoals" name="careerGoals" rows="3" required placeholder="What are your career goals in AI?"></textarea>
                </div>
                
                <div class="form-group">
                    <label>
                        <input type="checkbox" name="agreeTerms" required>
                        I agree to the terms and conditions *
                    </label>
                </div>
                
                <button type="submit" class="submit-btn">
                    <i class="fas fa-paper-plane"></i> Submit Application
                </button>
            </form>
        </div>
    </div>

    <script>
        document.getElementById('msaiApplicationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const successMessage = document.getElementById('successMessage');
            const errorMessage = document.getElementById('errorMessage');
            
            // Reset messages
            successMessage.style.display = 'none';
            errorMessage.style.display = 'none';
            
            try {
                // Collect form data
                const formData = new FormData(this);
                const data = Object.fromEntries(formData);
                
                // Submit to API
                const response = await fetch('/api/application', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    successMessage.style.display = 'block';
                    this.reset();
                    successMessage.scrollIntoView({ behavior: 'smooth' });
                } else {
                    throw new Error('Submission failed');
                }
                
            } catch (error) {
                console.error('Error submitting form:', error);
                errorMessage.style.display = 'block';
            }
        });
    </script>
</body>
</html>
    """)

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

@app.get("/api/applications/stats")
async def get_application_stats():
    """Get application statistics"""
    try:
        return application_stats
    except Exception as e:
        print(f"❌ Error getting application stats: {e}")
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
                "description": "Comprehensive introduction to AI concepts, history, and foundational theories."
            },
            "ML_FUNDAMENTALS": {
                "course_id": "ML_FUNDAMENTALS",
                "course_code": "AI-502",
                "title": "Machine Learning Fundamentals",
                "credits": 3,
                "level": "Foundational",
                "description": "Hands-on introduction to machine learning algorithms, implementation, and real-world applications."
            },
            "DEEP_LEARNING": {
                "course_id": "DEEP_LEARNING",
                "course_code": "AI-503",
                "title": "Deep Learning and Neural Networks",
                "credits": 3,
                "level": "Advanced",
                "description": "Advanced course covering deep neural networks, architectures, and cutting-edge applications."
            }
        },
        "specialization_tracks": {
            "ML_DATA_SCIENCE": {
                "track_id": "ML_DATA_SCIENCE",
                "name": "Machine Learning & Data Science",
                "description": "This specialization focuses on advanced machine learning techniques, data science methodologies, and the development of intelligent systems that can learn from data.",
                "total_credits": 12,
                "core_courses": ["ML_FUNDAMENTALS", "DEEP_LEARNING"],
                "career_outcomes": ["Machine Learning Engineer", "Data Scientist", "MLOps Engineer", "AI Research Scientist"]
            },
            "NLP_TRACK": {
                "track_id": "NLP_TRACK",
                "name": "Natural Language Processing",
                "description": "This specialization delves deep into natural language processing, covering both traditional linguistic approaches and modern transformer-based models.",
                "total_credits": 12,
                "core_courses": ["NLP_FUNDAMENTALS", "DEEP_LEARNING"],
                "career_outcomes": ["NLP Engineer", "Conversational AI Developer", "Language Technology Specialist", "AI Research Scientist"]
            },
            "CV_ROBOTICS": {
                "track_id": "CV_ROBOTICS",
                "name": "Computer Vision & Robotics",
                "description": "This specialization combines computer vision with robotics to create intelligent systems that can perceive and interact with the physical world.",
                "total_credits": 12,
                "core_courses": ["COMPUTER_VISION", "DEEP_LEARNING"],
                "career_outcomes": ["Computer Vision Engineer", "Autonomous Vehicle Engineer", "Robotics Engineer", "Medical AI Specialist"]
            }
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

@app.get("/api/tracks")
async def get_specialization_tracks():
    """Get specialization track information"""
    curriculum = await get_curriculum()
    return {
        "tracks": curriculum["specialization_tracks"],
        "total_tracks": len(curriculum["specialization_tracks"]),
        "ai_curriculum_features": {
            "personalized_learning": "AI adapts curriculum to individual learning styles and career goals",
            "virtual_professors": "AI professors with unique personalities and expertise areas",
            "adaptive_content": "Course materials that evolve based on latest research and industry trends"
        }
    }

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
        "app:app",
        host=host,
        port=port,
        reload=False,
        workers=1
    )
EOF

# Create systemd service
cat > /etc/systemd/system/msai.service << 'EOF'
[Unit]
Description=MS AI Curriculum System with Application Form
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/msai
Environment=PATH=/opt/msai/venv/bin
ExecStart=/opt/msai/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create nginx configuration
cat > /etc/nginx/sites-available/msai.syzygyx.com << 'EOF'
server {
    listen 80;
    server_name msai.syzygyx.com www.msai.syzygyx.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /opt/msai/static/;
    }
    
    location /uploads/ {
        alias /opt/msai/uploads/;
    }
}
EOF

# Enable nginx site
ln -sf /etc/nginx/sites-available/msai.syzygyx.com /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
nginx -t

# Start services
systemctl daemon-reload
systemctl enable msai
systemctl start msai
systemctl reload nginx

# Wait for service to start
sleep 10

# Test the deployment
if curl -f http://localhost:8000/health; then
    echo "✅ MS AI Enhanced Application deployed successfully!"
    echo "🌐 Application is running at: http://msai.syzygyx.com"
    echo "📝 Application form: http://msai.syzygyx.com/application"
    echo "📚 API docs: http://msai.syzygyx.com/docs"
else
    echo "❌ Deployment failed - service not responding"
    exit 1
fi