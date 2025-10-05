#!/bin/bash
set -e

echo "🎓 Setting up MS AI Curriculum System on EC2..."

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker ubuntu
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Install Python and pip
sudo apt-get install -y python3 python3-pip git

# Create application directory
sudo mkdir -p /opt/msai
cd /opt/msai

# Create the application files
sudo tee app.py > /dev/null << 'APP_EOF'
#!/usr/bin/env python3
"""
MS AI Curriculum System - Main Application
Production entry point for msai.syzygyx.com
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn

# Create FastAPI application
app = FastAPI(
    title="MS AI Curriculum System",
    description="Human-Centered AI Education Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://msai.syzygyx.com", "https://www.msai.syzygyx.com", "http://44.220.164.13"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["msai.syzygyx.com", "www.msai.syzygyx.com", "44.220.164.13"]
)

# Setup templates
templates = Jinja2Templates(directory="templates")

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
        "description": "Human-Centered AI Education Platform",
        "endpoints": {
            "professors": "/api/professors",
            "curriculum": "/api/curriculum", 
            "students": "/api/students",
            "status": "/api/status",
            "health": "/health",
            "metrics": "/metrics",
            "docs": "/docs"
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
            "database": "online"
        }
    }

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
    """Get curriculum information"""
    return {
        "program_name": "Master of Science in Artificial Intelligence",
        "total_credits": 36,
        "core_courses": 6,
        "specialization_tracks": 3,
        "accreditation_body": "ABET",
        "duration": "2 years",
        "specializations": [
            "Machine Learning & Data Science",
            "Natural Language Processing",
            "Computer Vision & Robotics"
        ]
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
            "Real-time Assessment"
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
APP_EOF

# Create requirements.txt
sudo tee requirements.txt > /dev/null << 'REQ_EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
pydantic==2.5.0
jinja2==3.1.2
REQ_EOF

# Create templates directory and index.html
sudo mkdir -p templates
sudo tee templates/index.html > /dev/null << 'HTML_EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MS AI Curriculum System - Revolutionary AI-Powered Education</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Header */
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
        }

        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: #667eea;
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: #333;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        .nav-links a:hover {
            color: #667eea;
        }

        /* Hero Section */
        .hero {
            padding: 120px 0 80px;
            text-align: center;
            color: white;
        }

        .hero h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            background: linear-gradient(45deg, #fff, #f0f8ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero .subtitle {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            opacity: 0.9;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }

        .cta-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }

        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }

        .btn-primary {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }

        /* Features Section */
        .features {
            padding: 80px 0;
            background: white;
        }

        .section-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 3rem;
            color: #333;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }

        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #f0f0f0;
        }

        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }

        .feature-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
            color: white;
            font-size: 1.5rem;
        }

        .feature-card h3 {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #333;
        }

        .feature-card p {
            color: #666;
            line-height: 1.6;
        }

        /* Demo Section */
        .demo {
            padding: 80px 0;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            text-align: center;
        }

        .demo-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
            flex-wrap: wrap;
        }

        .demo-btn {
            padding: 12px 25px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 25px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .demo-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }

        /* Footer */
        .footer {
            background: #333;
            color: white;
            padding: 40px 0;
            text-align: center;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2.5rem;
            }

            .hero .subtitle {
                font-size: 1.1rem;
            }

            .cta-buttons {
                flex-direction: column;
                align-items: center;
            }

            .nav-links {
                display: none;
            }

            .features-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .fade-in-up {
            animation: fadeInUp 0.6s ease-out;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <nav class="nav container">
            <div class="logo">🎓 MS AI Curriculum</div>
            <ul class="nav-links">
                <li><a href="#features">Features</a></li>
                <li><a href="#demo">Demo</a></li>
                <li><a href="/docs">API Docs</a></li>
            </ul>
        </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h1 class="fade-in-up">Revolutionary AI-Powered Education</h1>
            <p class="subtitle fade-in-up">
                Experience the future of learning with AI-generated curriculum, personalized instructors, 
                and adaptive content that evolves with every student.
            </p>
            <div class="cta-buttons fade-in-up">
                <a href="#demo" class="btn btn-primary">
                    <i class="fas fa-play"></i> See It In Action
                </a>
                <a href="/docs" class="btn btn-secondary">
                    <i class="fas fa-code"></i> Explore API
                </a>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features">
        <div class="container">
            <h2 class="section-title">Powered by Advanced AI Technology</h2>
            <div class="features-grid">
                <div class="feature-card fade-in-up">
                    <div class="feature-icon">
                        <i class="fas fa-brain"></i>
                    </div>
                    <h3>AI-Generated Curriculum</h3>
                    <p>Our advanced AI algorithms create personalized learning paths that adapt to each student's learning style, pace, and goals. No two curricula are ever the same.</p>
                </div>
                <div class="feature-card fade-in-up">
                    <div class="feature-icon">
                        <i class="fas fa-user-graduate"></i>
                    </div>
                    <h3>Virtual AI Professors</h3>
                    <p>Meet our AI professors with unique personalities, teaching philosophies, and expertise. Each professor is designed to provide personalized mentorship and guidance.</p>
                </div>
                <div class="feature-card fade-in-up">
                    <div class="feature-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3>Adaptive Learning</h3>
                    <p>Content automatically adjusts based on student performance, learning patterns, and engagement levels. The system learns and improves with every interaction.</p>
                </div>
                <div class="feature-card fade-in-up">
                    <div class="feature-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h3>Intelligent Assessment</h3>
                    <p>AI-powered evaluation that goes beyond traditional testing, analyzing comprehension, creativity, and practical application of knowledge.</p>
                </div>
                <div class="feature-card fade-in-up">
                    <div class="feature-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <h3>Collaborative Learning</h3>
                    <p>AI facilitates peer-to-peer learning, group projects, and collaborative problem-solving with intelligent matching and guidance.</p>
                </div>
                <div class="feature-card fade-in-up">
                    <div class="feature-icon">
                        <i class="fas fa-graduation-cap"></i>
                    </div>
                    <h3>Industry-Ready Skills</h3>
                    <p>Curriculum designed with industry experts and AI analysis of job market trends to ensure graduates are ready for real-world challenges.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Demo Section -->
    <section id="demo" class="demo">
        <div class="container">
            <h2 class="section-title">Experience the Future</h2>
            <p style="font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;">
                Try our interactive demos and see how AI transforms education
            </p>
            <div class="demo-buttons">
                <a href="/api/professors" class="demo-btn">
                    <i class="fas fa-user-graduate"></i> Meet AI Professors
                </a>
                <a href="/api/curriculum" class="demo-btn">
                    <i class="fas fa-book"></i> Explore Curriculum
                </a>
                <a href="/api/students" class="demo-btn">
                    <i class="fas fa-users"></i> Student Simulator
                </a>
                <a href="/health" class="demo-btn">
                    <i class="fas fa-heartbeat"></i> System Status
                </a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 MS AI Curriculum System. Powered by advanced AI technology.</p>
            <p style="margin-top: 1rem; opacity: 0.8;">🌐 Now live at msai.syzygyx.com</p>
        </div>
    </footer>

    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Add loading states to demo buttons
        document.querySelectorAll('.demo-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                const originalText = this.innerHTML;
                this.innerHTML = '<span class="loading"></span> Loading...';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            });
        });

        // Initialize page
        document.addEventListener('DOMContentLoaded', function() {
            // Add fade-in animation to elements as they come into view
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in-up');
                    }
                });
            }, observerOptions);

            document.querySelectorAll('.feature-card').forEach(el => {
                observer.observe(el);
            });
        });
    </script>
</body>
</html>
HTML_EOF

# Install Python dependencies
sudo pip3 install -r requirements.txt

# Create systemd service
sudo tee /etc/systemd/system/msai.service > /dev/null << 'EOF'
[Unit]
Description=MS AI Curriculum System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/msai
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10
Environment=PORT=8000
Environment=HOST=0.0.0.0

[Install]
WantedBy=multi-user.target
