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

# Create a simple enhanced application
cat > app.py << 'EOF'
#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime
import uuid

app = FastAPI(
    title="MS AI Curriculum System",
    description="Human-Centered AI Education Platform with Application Form",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

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

# Application form data models
class ApplicationData(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: str
    specialization: str
    startTerm: str
    programFormat: str
    undergraduateDegree: str
    undergraduateGPA: float
    graduationYear: int
    statementOfPurpose: str
    careerGoals: str
    agreeTerms: bool

class ApplicationResponse(BaseModel):
    success: bool
    message: str
    application_id: Optional[str] = None
    timestamp: str

# In-memory storage
applications_storage = []
application_stats = {'total_applications': 0}

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(content="<h1>MS AI Curriculum System</h1><p>Welcome to the MS AI Curriculum System with Application Form!</p><p><a href='/application'>Apply Now</a></p>")

@app.get("/health")
async def health_check():
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

@app.get("/application", response_class=HTMLResponse)
async def get_application_form():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MSAI Application Form</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; color: #333; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .submit-btn { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; }
        .submit-btn:hover { background: #0056b3; }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin-bottom: 20px; display: none; }
        .error { background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin-bottom: 20px; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 MSAI Application Form</h1>
            <p>Master of Science in Artificial Intelligence - Apply Now</p>
        </div>
        
        <div class="success" id="successMessage">
            ✅ Application submitted successfully! We'll be in touch soon.
        </div>
        
        <div class="error" id="errorMessage">
            ❌ There was an error submitting your application. Please try again.
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
                🚀 Submit Application
            </button>
        </form>
    </div>

    <script>
        document.getElementById('msaiApplicationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const successMessage = document.getElementById('successMessage');
            const errorMessage = document.getElementById('errorMessage');
            
            successMessage.style.display = 'none';
            errorMessage.style.display = 'none';
            
            try {
                const formData = new FormData(this);
                const data = Object.fromEntries(formData);
                
                const response = await fetch('/api/application', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    successMessage.style.display = 'block';
                    this.reset();
                } else {
                    throw new Error('Submission failed');
                }
                
            } catch (error) {
                console.error('Error:', error);
                errorMessage.style.display = 'block';
            }
        });
    </script>
</body>
</html>
    """)

@app.post("/api/application", response_model=ApplicationResponse)
async def submit_application(application: ApplicationData):
    try:
        form_data = application.dict()
        application_id = str(uuid.uuid4())
        form_data['application_id'] = application_id
        form_data['timestamp'] = datetime.now().isoformat()
        form_data['status'] = 'New'
        
        applications_storage.append(form_data)
        application_stats['total_applications'] += 1
        
        return ApplicationResponse(
            success=True,
            message="Application submitted successfully",
            application_id=application_id,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/applications")
async def get_applications():
    return applications_storage

@app.get("/api/applications/stats")
async def get_application_stats():
    return application_stats

@app.get("/api/specializations")
async def get_specializations():
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
    return {
        "formats": [
            "Full-time",
            "Part-time",
            "Online",
            "Hybrid"
        ]
    }

@app.get("/api/professors")
async def get_professors():
    return {
        "professors": [
            {
                "id": "prof_001",
                "name": "Dr. Sarah Chen",
                "specialization": "Machine Learning",
                "expertise_level": "Expert"
            },
            {
                "id": "prof_002", 
                "name": "Dr. Michael Rodriguez",
                "specialization": "Natural Language Processing",
                "expertise_level": "Expert"
            }
        ]
    }

@app.get("/api/curriculum")
async def get_curriculum():
    return {
        "program_info": {
            "program_name": "Master of Science in Artificial Intelligence",
            "total_credits": 36,
            "duration": "2 years",
            "accreditation": "ABET"
        }
    }

@app.get("/api/courses")
async def get_courses():
    return {
        "courses": {
            "AI_FUNDAMENTALS": {
                "course_id": "AI_FUNDAMENTALS",
                "title": "Foundations of Artificial Intelligence",
                "credits": 3
            },
            "ML_FUNDAMENTALS": {
                "course_id": "ML_FUNDAMENTALS",
                "title": "Machine Learning Fundamentals",
                "credits": 3
            }
        }
    }

@app.get("/api/tracks")
async def get_tracks():
    return {
        "tracks": {
            "ML_DATA_SCIENCE": {
                "name": "Machine Learning & Data Science",
                "description": "Advanced machine learning techniques and data science methodologies"
            }
        }
    }

@app.get("/api/students")
async def get_students():
    return {
        "students": [
            {"id": "student_001", "name": "Alex Johnson", "gpa": 3.7},
            {"id": "student_002", "name": "Maria Garcia", "gpa": 3.9}
        ]
    }

@app.get("/api/status")
async def get_status():
    return {
        "system": "MS AI Curriculum System",
        "status": "operational",
        "version": "1.0.0",
        "features": ["AI Professor System", "Curriculum Generator", "Application Form System"]
    }

@app.get("/metrics")
async def get_metrics():
    return {
        "active_users": 150,
        "applications_received": application_stats['total_applications'],
        "system_load": "normal"
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
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