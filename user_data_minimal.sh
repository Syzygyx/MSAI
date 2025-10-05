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
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 pydantic==2.5.0

# Create a minimal application
cat > app.py << 'EOF'
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
from datetime import datetime
import uuid

app = FastAPI(title="MS AI Curriculum System", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

applications = []

class ApplicationData(BaseModel):
    firstName: str
    lastName: str
    email: str
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

@app.get("/")
async def root():
    return HTMLResponse(content="<h1>MS AI Curriculum System</h1><p>Welcome! <a href='/application'>Apply Now</a></p>")

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/application")
async def application_form():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html>
<head><title>MSAI Application</title></head>
<body style="font-family:Arial;max-width:800px;margin:0 auto;padding:20px;">
<h1>🎓 MSAI Application Form</h1>
<form id="form">
<div style="margin-bottom:15px;"><label>First Name: <input name="firstName" required></label></div>
<div style="margin-bottom:15px;"><label>Last Name: <input name="lastName" required></label></div>
<div style="margin-bottom:15px;"><label>Email: <input type="email" name="email" required></label></div>
<div style="margin-bottom:15px;"><label>Phone: <input name="phone" required></label></div>
<div style="margin-bottom:15px;"><label>Specialization: <select name="specialization" required><option value="">Select</option><option value="ML">Machine Learning</option><option value="NLP">NLP</option><option value="CV">Computer Vision</option></select></label></div>
<div style="margin-bottom:15px;"><label>Start Term: <select name="startTerm" required><option value="">Select</option><option value="Fall 2024">Fall 2024</option><option value="Spring 2025">Spring 2025</option></select></label></div>
<div style="margin-bottom:15px;"><label>Program Format: <select name="programFormat" required><option value="">Select</option><option value="Full-time">Full-time</option><option value="Part-time">Part-time</option><option value="Online">Online</option></select></label></div>
<div style="margin-bottom:15px;"><label>Undergraduate Degree: <input name="undergraduateDegree" required></label></div>
<div style="margin-bottom:15px;"><label>GPA: <input type="number" name="undergraduateGPA" step="0.01" min="0" max="4" required></label></div>
<div style="margin-bottom:15px;"><label>Graduation Year: <input type="number" name="graduationYear" required></label></div>
<div style="margin-bottom:15px;"><label>Statement of Purpose: <textarea name="statementOfPurpose" rows="4" required></textarea></label></div>
<div style="margin-bottom:15px;"><label>Career Goals: <textarea name="careerGoals" rows="3" required></textarea></label></div>
<div style="margin-bottom:15px;"><label><input type="checkbox" name="agreeTerms" required> I agree to terms *</label></div>
<button type="submit" style="background:#007bff;color:white;padding:15px 30px;border:none;border-radius:5px;cursor:pointer;">Submit Application</button>
</form>
<div id="message" style="margin-top:20px;padding:15px;border-radius:5px;display:none;"></div>
<script>
document.getElementById('form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);
    try {
        const response = await fetch('/api/application', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)});
        if (response.ok) {
            document.getElementById('message').style.display = 'block';
            document.getElementById('message').style.background = '#d4edda';
            document.getElementById('message').style.color = '#155724';
            document.getElementById('message').textContent = '✅ Application submitted successfully!';
            this.reset();
        } else {
            throw new Error('Failed');
        }
    } catch (error) {
        document.getElementById('message').style.display = 'block';
        document.getElementById('message').style.background = '#f8d7da';
        document.getElementById('message').style.color = '#721c24';
        document.getElementById('message').textContent = '❌ Error submitting application';
    }
});
</script>
</body>
</html>
    """)

@app.post("/api/application")
async def submit_application(application: ApplicationData):
    app_data = application.dict()
    app_data['id'] = str(uuid.uuid4())
    app_data['timestamp'] = datetime.now().isoformat()
    applications.append(app_data)
    return {"success": True, "message": "Application submitted successfully", "id": app_data['id']}

@app.get("/api/applications")
async def get_applications():
    return applications

@app.get("/api/specializations")
async def get_specializations():
    return {"specializations": ["Machine Learning", "NLP", "Computer Vision", "General AI"]}

@app.get("/api/start-terms")
async def get_start_terms():
    return {"terms": ["Fall 2024", "Spring 2025", "Fall 2025", "Spring 2026"]}

@app.get("/api/program-formats")
async def get_program_formats():
    return {"formats": ["Full-time", "Part-time", "Online", "Hybrid"]}

@app.get("/api/professors")
async def get_professors():
    return {"professors": [{"name": "Dr. Sarah Chen", "specialization": "ML"}, {"name": "Dr. Michael Rodriguez", "specialization": "NLP"}]}

@app.get("/api/curriculum")
async def get_curriculum():
    return {"program_name": "Master of Science in AI", "credits": 36}

@app.get("/api/courses")
async def get_courses():
    return {"courses": [{"title": "AI Fundamentals", "credits": 3}, {"title": "ML Fundamentals", "credits": 3}]}

@app.get("/api/tracks")
async def get_tracks():
    return {"tracks": [{"name": "ML & Data Science"}, {"name": "NLP"}, {"name": "Computer Vision"}]}

@app.get("/api/students")
async def get_students():
    return {"students": [{"name": "Alex Johnson", "gpa": 3.7}, {"name": "Maria Garcia", "gpa": 3.9}]}

@app.get("/api/status")
async def get_status():
    return {"system": "MS AI Curriculum System", "status": "operational", "version": "1.0.0"}

@app.get("/metrics")
async def get_metrics():
    return {"applications_received": len(applications), "system_load": "normal"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
EOF

# Create systemd service
cat > /etc/systemd/system/msai.service << 'EOF'
[Unit]
Description=MS AI Curriculum System
After=network.target
[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/msai
Environment=PATH=/opt/msai/venv/bin
ExecStart=/opt/msai/venv/bin/python app.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF

# Create nginx config
cat > /etc/nginx/sites-available/msai.syzygyx.com << 'EOF'
server {
    listen 80;
    server_name msai.syzygyx.com www.msai.syzygyx.com;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Enable nginx
ln -sf /etc/nginx/sites-available/msai.syzygyx.com /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t

# Start services
systemctl daemon-reload
systemctl enable msai
systemctl start msai
systemctl reload nginx

sleep 10

if curl -f http://localhost:8000/health; then
    echo "✅ MS AI Application deployed successfully!"
    echo "🌐 Application: http://msai.syzygyx.com"
    echo "📝 Application form: http://msai.syzygyx.com/application"
else
    echo "❌ Deployment failed"
    exit 1
fi