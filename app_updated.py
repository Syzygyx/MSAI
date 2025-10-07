#!/usr/bin/env python3
"""
MS AI Program - AURNOVA University
Updated to serve our HTML content
"""

import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

# Create FastAPI application
app = FastAPI(
    title="MS AI Program - AURNOVA University",
    description="Master of Science in Artificial Intelligence Program",
    version="2.0.0"
)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Serve the main index page"""
    return HTMLResponse(content="""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MS AI Program - AURNOVA University</title>
    <style>
        body {
            font-family: 'Times New Roman', 'Georgia', serif;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            line-height: 1.6;
        }
        .header {
            background-color: #000000;
            color: white;
            padding: 40px 0;
            text-align: center;
        }
        .header h1 {
            font-size: 48px;
            margin: 0;
            font-weight: bold;
            letter-spacing: 2px;
        }
        .header h2 {
            font-size: 24px;
            margin: 10px 0 0 0;
            font-weight: normal;
            color: #cccccc;
        }
        .nav {
            background-color: #333333;
            padding: 15px 0;
            text-align: center;
        }
        .nav a {
            color: white;
            text-decoration: none;
            margin: 0 30px;
            font-size: 16px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .nav a:hover {
            color: #cccccc;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        .hero {
            background-color: #f8f9fa;
            padding: 80px 0;
            text-align: center;
        }
        .hero h2 {
            font-size: 36px;
            color: #000000;
            margin-bottom: 20px;
            font-weight: bold;
        }
        .hero p {
            font-size: 20px;
            color: #333333;
            max-width: 800px;
            margin: 0 auto 40px auto;
        }
        .cta-button {
            display: inline-block;
            background-color: #000000;
            color: white;
            padding: 20px 40px;
            text-decoration: none;
            font-size: 18px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            border: 2px solid #000000;
            margin: 0 10px;
        }
        .cta-button:hover {
            background-color: #333333;
            border-color: #333333;
        }
        .cta-button.secondary {
            background-color: transparent;
            color: #000000;
        }
        .cta-button.secondary:hover {
            background-color: #000000;
            color: white;
        }
        .content {
            padding: 80px 0;
        }
        .section {
            margin-bottom: 80px;
        }
        .section h3 {
            font-size: 32px;
            color: #000000;
            margin-bottom: 40px;
            text-align: center;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .section h4 {
            font-size: 24px;
            color: #000000;
            margin-bottom: 20px;
            font-weight: bold;
        }
        .section h5 {
            font-size: 20px;
            color: #000000;
            margin-bottom: 15px;
            font-weight: bold;
        }
        .two-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-bottom: 40px;
        }
        .three-column {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        .four-column {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 40px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
            margin: 40px 0;
        }
        .stat-item {
            text-align: center;
            padding: 20px;
            border: 2px solid #333333;
        }
        .stat-number {
            font-size: 36px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 10px;
        }
        .stat-label {
            font-size: 14px;
            color: #333333;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .card {
            background-color: #ffffff;
            border: 2px solid #333333;
            padding: 30px;
        }
        .card h4 {
            font-size: 20px;
            color: #000000;
            margin-bottom: 15px;
            font-weight: bold;
        }
        .card p {
            color: #333333;
            margin-bottom: 15px;
        }
        .card ul {
            color: #333333;
            padding-left: 20px;
        }
        .card li {
            margin-bottom: 8px;
        }
        .timeline {
            position: relative;
            padding: 20px 0;
        }
        .timeline-item {
            display: flex;
            margin-bottom: 30px;
            align-items: flex-start;
        }
        .timeline-marker {
            width: 20px;
            height: 20px;
            background-color: #000000;
            border-radius: 50%;
            margin-right: 20px;
            margin-top: 5px;
            flex-shrink: 0;
        }
        .timeline-content {
            flex: 1;
        }
        .timeline-content h5 {
            margin-bottom: 10px;
            color: #000000;
        }
        .timeline-content p {
            color: #333333;
            margin-bottom: 5px;
        }
        .faculty-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }
        .faculty-card {
            background-color: #ffffff;
            border: 2px solid #333333;
            padding: 25px;
            text-align: center;
        }
        .faculty-card h5 {
            color: #000000;
            margin-bottom: 10px;
        }
        .faculty-card .title {
            color: #666666;
            font-style: italic;
            margin-bottom: 15px;
        }
        .faculty-card p {
            color: #333333;
            font-size: 14px;
        }
        .requirements {
            background-color: #f8f9fa;
            padding: 40px;
            border: 2px solid #333333;
        }
        .requirements h4 {
            font-size: 22px;
            color: #000000;
            margin-bottom: 20px;
            font-weight: bold;
        }
        .requirements-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        .requirements-column h5 {
            font-size: 18px;
            color: #000000;
            margin-bottom: 15px;
            font-weight: bold;
        }
        .requirements-column ul {
            color: #333333;
            padding-left: 20px;
        }
        .requirements-column li {
            margin-bottom: 8px;
        }
        .footer {
            background-color: #000000;
            color: white;
            padding: 40px 0;
            text-align: center;
        }
        .footer p {
            margin: 10px 0;
        }
        .footer a {
            color: #cccccc;
            text-decoration: none;
        }
        .footer a:hover {
            color: white;
        }
        @media (max-width: 768px) {
            .two-column, .requirements-grid, .three-column, .four-column {
                grid-template-columns: 1fr;
            }
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .faculty-grid {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 36px;
            }
            .hero h2 {
                font-size: 28px;
            }
            .hero p {
                font-size: 18px;
            }
            .section h3 {
                font-size: 28px;
            }
            .nav a {
                margin: 0 15px;
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <h1>Master of Science in Artificial Intelligence</h1>
            <h2>AURNOVA University</h2>
        </div>
    </header>

    <nav class="nav">
        <div class="container">
            <a href="#program">Program</a>
            <a href="#admissions">Admissions</a>
            <a href="#curriculum">Curriculum</a>
            <a href="#faculty">Faculty</a>
            <a href="#research">Research</a>
            <a href="#careers">Careers</a>
            <a href="#whitepaper">White Paper</a>
            <a href="#apply">Apply Now</a>
        </div>
    </nav>

    <section class="hero">
        <div class="container">
            <h2>Advance Your Career in Artificial Intelligence</h2>
            <p>Join the next generation of AI professionals with our comprehensive Master of Science program. Gain deep technical expertise, hands-on experience, and the skills needed to lead in the rapidly evolving field of artificial intelligence.</p>
            <a href="msai_application_form.html" class="cta-button">Apply Now</a>
            <a href="#whitepaper" class="cta-button secondary">Read White Paper</a>
        </div>
    </section>

    <section class="content">
        <div class="container">
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">95%</div>
                    <div class="stat-label">Employment Rate</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">$120K</div>
                    <div class="stat-label">Average Starting Salary</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">24</div>
                    <div class="stat-label">Months to Complete</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">15:1</div>
                    <div class="stat-label">Student-Faculty Ratio</div>
                </div>
            </div>
        </div>
    </section>

    <main class="content">
        <div class="container">
            <section id="program" class="section">
                <h3>Program Overview</h3>
                
                <div class="two-column">
                    <div class="card">
                        <h4>Program Duration & Format</h4>
                        <p><strong>Full-time:</strong> 24 months (4 semesters)</p>
                        <p><strong>Part-time:</strong> 36 months (6 semesters)</p>
                        <p><strong>Credit Hours:</strong> 36 total credits</p>
                        <p><strong>Delivery:</strong> Hybrid (70% on-campus, 30% online)</p>
                        <p><strong>Start Dates:</strong> Fall (September) and Spring (January)</p>
                    </div>
                    <div class="card">
                        <h4>Program Highlights</h4>
                        <ul>
                            <li>Hands-on research opportunities</li>
                            <li>Industry partnerships and internships</li>
                            <li>State-of-the-art AI laboratories</li>
                            <li>Small class sizes (max 20 students)</li>
                            <li>Thesis or capstone project options</li>
                            <li>Professional development workshops</li>
                        </ul>
                    </div>
                </div>

                <div class="two-column">
                    <div class="card">
                        <h4>Core Competencies</h4>
                        <ul>
                            <li>Machine Learning & Deep Learning</li>
                            <li>Natural Language Processing</li>
                            <li>Computer Vision & Image Processing</li>
                            <li>AI Ethics & Responsible AI</li>
                            <li>AI Systems Engineering</li>
                            <li>Data Science & Analytics</li>
                            <li>Robotics & Autonomous Systems</li>
                            <li>AI in Healthcare & Medicine</li>
                        </ul>
                    </div>
                    <div class="card">
                        <h4>Career Outcomes</h4>
                        <ul>
                            <li>AI Research Scientist</li>
                            <li>Machine Learning Engineer</li>
                            <li>AI Product Manager</li>
                            <li>Data Science Director</li>
                            <li>AI Consultant</li>
                            <li>Robotics Engineer</li>
                            <li>AI Ethics Specialist</li>
                            <li>Technical Lead/Architect</li>
                        </ul>
                    </div>
                </div>

                <div class="card">
                    <h4>Program Mission</h4>
                    <p>The Master of Science in Artificial Intelligence program at AURNOVA University prepares students to become leaders in the rapidly evolving field of AI. Our program combines rigorous theoretical foundations with practical, hands-on experience, ensuring graduates are equipped with both the technical expertise and ethical awareness needed to shape the future of artificial intelligence.</p>
                    
                    <h5>Learning Objectives</h5>
                    <div class="two-column">
                        <ul>
                            <li>Master advanced machine learning algorithms and deep learning architectures</li>
                            <li>Develop expertise in natural language processing and computer vision</li>
                            <li>Understand ethical implications and responsible AI development</li>
                            <li>Gain hands-on experience with industry-standard tools and frameworks</li>
                        </ul>
                        <ul>
                            <li>Conduct independent research and contribute to AI knowledge</li>
                            <li>Apply AI solutions to real-world problems across industries</li>
                            <li>Communicate complex AI concepts to diverse audiences</li>
                            <li>Lead AI projects and teams in professional settings</li>
                        </ul>
                    </div>
                </div>
            </section>

            <section id="admissions" class="section">
                <h3>Admission Requirements</h3>
                
                <div class="requirements">
                    <h4>Academic Prerequisites</h4>
                    <div class="requirements-grid">
                        <div class="requirements-column">
                            <h5>Required Background</h5>
                            <ul>
                                <li>Bachelor's degree in Computer Science, Engineering, Mathematics, Physics, or related field</li>
                                <li>Minimum GPA of 3.0 on a 4.0 scale (3.5+ preferred)</li>
                                <li>Strong foundation in programming (Python, Java, C++, or R)</li>
                                <li>Mathematics: Calculus I & II, Linear Algebra, Statistics/Probability</li>
                                <li>Basic knowledge of data structures and algorithms</li>
                            </ul>
                        </div>
                        <div class="requirements-column">
                            <h5>Application Materials</h5>
                            <ul>
                                <li>Completed online application form</li>
                                <li>Official transcripts from all institutions</li>
                                <li>Statement of Purpose (750-1000 words)</li>
                                <li>Personal Statement (500-750 words)</li>
                                <li>Three letters of recommendation</li>
                                <li>Current resume/CV</li>
                                <li>GRE scores (optional but recommended)</li>
                                <li>TOEFL/IELTS (international students)</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div class="two-column">
                    <div class="card">
                        <h4>Prerequisite Coursework</h4>
                        <p><strong>Required Courses (or equivalent):</strong></p>
                        <ul>
                            <li>Calculus I & II</li>
                            <li>Linear Algebra</li>
                            <li>Statistics and Probability</li>
                            <li>Data Structures and Algorithms</li>
                            <li>Programming Fundamentals</li>
                        </ul>
                        <p><strong>Recommended Courses:</strong></p>
                        <ul>
                            <li>Machine Learning (introductory)</li>
                            <li>Database Systems</li>
                            <li>Discrete Mathematics</li>
                            <li>Computer Organization</li>
                        </ul>
                    </div>
                    <div class="card">
                        <h4>Application Timeline</h4>
                        <div class="timeline">
                            <div class="timeline-item">
                                <div class="timeline-marker"></div>
                                <div class="timeline-content">
                                    <h5>September 1</h5>
                                    <p>Application opens for Fall 2025</p>
                                </div>
                            </div>
                            <div class="timeline-item">
                                <div class="timeline-marker"></div>
                                <div class="timeline-content">
                                    <h5>March 15</h5>
                                    <p>Application deadline</p>
                                </div>
                            </div>
                            <div class="timeline-item">
                                <div class="timeline-marker"></div>
                                <div class="timeline-content">
                                    <h5>April 15</h5>
                                    <p>Admission decisions released</p>
                                </div>
                            </div>
                            <div class="timeline-item">
                                <div class="timeline-marker"></div>
                                <div class="timeline-content">
                                    <h5>May 1</h5>
                                    <p>Enrollment deposit deadline</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <h4>Selection Criteria</h4>
                    <p>Admission to the MS AI program is competitive and based on a holistic review of each application. The admissions committee considers:</p>
                    <div class="two-column">
                        <ul>
                            <li>Academic performance and GPA</li>
                            <li>Relevance of undergraduate coursework</li>
                            <li>Quality of statement of purpose</li>
                            <li>Letters of recommendation</li>
                        </ul>
                        <ul>
                            <li>Research experience and publications</li>
                            <li>Professional experience in related fields</li>
                            <li>Programming and technical skills</li>
                            <li>Potential for success in graduate study</li>
                        </ul>
                    </div>
                </div>
            </section>

            <section id="curriculum" class="section">
                <h3>Curriculum</h3>
                
                <div class="card">
                    <h4>Program Structure</h4>
                    <p>The MS AI program consists of 36 credit hours distributed across core courses, electives, and a culminating experience. Students can choose between a thesis track (6 credits) or a capstone project track (3 credits).</p>
                    
                    <div class="two-column">
                        <div>
                            <h5>Core Courses (18 credits)</h5>
                            <ul>
                                <li>AI-501: Advanced Machine Learning (3)</li>
                                <li>AI-502: Deep Learning & Neural Networks (3)</li>
                                <li>AI-503: Natural Language Processing (3)</li>
                                <li>AI-504: Computer Vision (3)</li>
                                <li>AI-505: AI Ethics & Society (3)</li>
                                <li>AI-506: Research Methods in AI (3)</li>
                            </ul>
                        </div>
                        <div>
                            <h5>Elective Courses (12 credits)</h5>
                            <ul>
                                <li>AI-601: Reinforcement Learning (3)</li>
                                <li>AI-602: Robotics & Autonomous Systems (3)</li>
                                <li>AI-603: AI for Healthcare (3)</li>
                                <li>AI-604: AI in Business Applications (3)</li>
                                <li>AI-605: Advanced Statistics for AI (3)</li>
                                <li>AI-606: AI Systems Architecture (3)</li>
                                <li>AI-607: Quantum Machine Learning (3)</li>
                                <li>AI-608: AI for Climate Science (3)</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div class="two-column">
                    <div class="card">
                        <h4>Year 1 - Foundation</h4>
                        <h5>Fall Semester</h5>
                        <ul>
                            <li>AI-501: Advanced Machine Learning</li>
                            <li>AI-503: Natural Language Processing</li>
                            <li>AI-505: AI Ethics & Society</li>
                            <li>Elective Course</li>
                        </ul>
                        <h5>Spring Semester</h5>
                        <ul>
                            <li>AI-502: Deep Learning & Neural Networks</li>
                            <li>AI-504: Computer Vision</li>
                            <li>AI-506: Research Methods in AI</li>
                            <li>Elective Course</li>
                        </ul>
                    </div>
                    <div class="card">
                        <h4>Year 2 - Specialization</h4>
                        <h5>Fall Semester</h5>
                        <ul>
                            <li>Two Elective Courses</li>
                            <li>Thesis/Capstone Preparation</li>
                            <li>Professional Development Workshop</li>
                        </ul>
                        <h5>Spring Semester</h5>
                        <ul>
                            <li>Two Elective Courses</li>
                            <li>AI-699: Thesis (6) or AI-698: Capstone (3)</li>
                            <li>Industry Internship (optional)</li>
                        </ul>
                    </div>
                </div>

                <div class="card">
                    <h4>Specialization Tracks</h4>
                    <p>Students can focus their studies in one of four specialization tracks:</p>
                    <div class="four-column">
                        <div>
                            <h5>Research Track</h5>
                            <ul>
                                <li>Advanced Research Methods</li>
                                <li>Publication Workshop</li>
                                <li>Thesis Defense</li>
                            </ul>
                        </div>
                        <div>
                            <h5>Industry Track</h5>
                            <ul>
                                <li>AI Product Development</li>
                                <li>Industry Internship</li>
                                <li>Capstone Project</li>
                            </ul>
                        </div>
                        <div>
                            <h5>Healthcare AI</h5>
                            <ul>
                                <li>Medical AI Applications</li>
                                <li>Healthcare Data Science</li>
                                <li>Regulatory Compliance</li>
                            </ul>
                        </div>
                        <div>
                            <h5>Ethics & Policy</h5>
                            <ul>
                                <li>AI Governance</li>
                                <li>Policy Analysis</li>
                                <li>Ethical AI Design</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <section id="faculty" class="section">
                <h3>Faculty</h3>
                <p>Our distinguished faculty members are leading researchers and practitioners in artificial intelligence, bringing both academic excellence and real-world experience to the classroom.</p>
                
                <div class="faculty-grid">
                    <div class="faculty-card">
                        <h5>Dr. Sarah Chen</h5>
                        <div class="title">Professor & Program Director</div>
                        <p>Expertise: Machine Learning, Computer Vision. Former Google AI researcher with 50+ publications in top-tier conferences.</p>
                    </div>
                    <div class="faculty-card">
                        <h5>Dr. Michael Rodriguez</h5>
                        <div class="title">Associate Professor</div>
                        <p>Expertise: Natural Language Processing, Deep Learning. NSF CAREER Award recipient and industry consultant.</p>
                    </div>
                    <div class="faculty-card">
                        <h5>Dr. Aisha Patel</h5>
                        <div class="title">Assistant Professor</div>
                        <p>Expertise: AI Ethics, Responsible AI. Leading researcher in algorithmic fairness and bias mitigation.</p>
                    </div>
                    <div class="faculty-card">
                        <h5>Dr. James Wilson</h5>
                        <div class="title">Professor</div>
                        <p>Expertise: Robotics, Autonomous Systems. Former Tesla Autopilot engineer with extensive industry experience.</p>
                    </div>
                    <div class="faculty-card">
                        <h5>Dr. Maria Gonzalez</h5>
                        <div class="title">Associate Professor</div>
                        <p>Expertise: Healthcare AI, Medical Imaging. Collaborates with major hospitals on AI diagnostic systems.</p>
                    </div>
                    <div class="faculty-card">
                        <h5>Dr. David Kim</h5>
                        <div class="title">Assistant Professor</div>
                        <p>Expertise: Reinforcement Learning, Game Theory. Former OpenAI researcher specializing in multi-agent systems.</p>
                    </div>
                </div>
            </section>

            <section id="research" class="section">
                <h3>Research Opportunities</h3>
                
                <div class="two-column">
                    <div class="card">
                        <h4>Research Areas</h4>
                        <ul>
                            <li>Machine Learning & Deep Learning</li>
                            <li>Natural Language Processing</li>
                            <li>Computer Vision & Image Processing</li>
                            <li>Robotics & Autonomous Systems</li>
                            <li>AI Ethics & Fairness</li>
                            <li>Healthcare AI Applications</li>
                            <li>AI for Climate Science</li>
                            <li>Quantum Machine Learning</li>
                        </ul>
                    </div>
                    <div class="card">
                        <h4>Research Centers</h4>
                        <ul>
                            <li>Center for AI Research (CAIR)</li>
                            <li>Institute for Ethical AI</li>
                            <li>Healthcare AI Laboratory</li>
                            <li>Robotics Innovation Center</li>
                            <li>Data Science Institute</li>
                        </ul>
                    </div>
                </div>

                <div class="card">
                    <h4>Research Opportunities for Students</h4>
                    <div class="two-column">
                        <ul>
                            <li>Faculty-mentored research projects</li>
                            <li>Industry collaboration projects</li>
                            <li>Conference presentation opportunities</li>
                            <li>Publication in top-tier journals</li>
                        </ul>
                        <ul>
                            <li>Summer research internships</li>
                            <li>Graduate research assistantships</li>
                            <li>Travel funding for conferences</li>
                            <li>Research equipment access</li>
                        </ul>
                    </div>
                </div>
            </section>

            <section id="careers" class="section">
                <h3>Career Services & Outcomes</h3>
                
                <div class="card">
                    <h4>Career Services</h4>
                    <div class="two-column">
                        <ul>
                            <li>Individual career counseling</li>
                            <li>Resume and portfolio review</li>
                            <li>Mock interview sessions</li>
                            <li>Industry networking events</li>
                        </ul>
                        <ul>
                            <li>Job placement assistance</li>
                            <li>Alumni mentorship program</li>
                            <li>Company recruitment visits</li>
                            <li>Professional development workshops</li>
                        </ul>
                    </div>
                </div>

                <div class="two-column">
                    <div class="card">
                        <h4>Employment Statistics</h4>
                        <ul>
                            <li><strong>95%</strong> employment rate within 6 months</li>
                            <li><strong>$120,000</strong> average starting salary</li>
                            <li><strong>$150,000+</strong> median salary after 3 years</li>
                            <li><strong>85%</strong> work in AI/ML roles</li>
                            <li><strong>15%</strong> pursue PhD programs</li>
                        </ul>
                    </div>
                    <div class="card">
                        <h4>Top Employers</h4>
                        <ul>
                            <li>Google, Microsoft, Amazon</li>
                            <li>Meta, Apple, Tesla</li>
                            <li>OpenAI, Anthropic, DeepMind</li>
                            <li>Healthcare companies</li>
                            <li>Financial services firms</li>
                            <li>Government agencies</li>
                        </ul>
                    </div>
                </div>
            </section>

            <section id="whitepaper" class="section">
                <h3>Program White Paper</h3>
                
                <div class="card">
                    <h4>Download Our Comprehensive Program White Paper</h4>
                    <p>Get detailed insights into our Master of Science in Artificial Intelligence program, including curriculum design philosophy, industry partnerships, research opportunities, and career outcomes. This comprehensive document provides in-depth information for prospective students, academic advisors, and industry professionals.</p>
                    
                    <div class="two-column">
                        <div>
                            <h5>White Paper Contents:</h5>
                            <ul>
                                <li>Program Philosophy & Learning Objectives</li>
                                <li>Detailed Curriculum Analysis</li>
                                <li>Industry Partnership Case Studies</li>
                                <li>Research Impact & Publications</li>
                                <li>Student Success Stories</li>
                                <li>Faculty Research Profiles</li>
                            </ul>
                        </div>
                        <div>
                            <h5>Additional Resources:</h5>
                            <ul>
                                <li>Alumni Career Trajectories</li>
                                <li>Industry Advisory Board Insights</li>
                                <li>Technology Infrastructure Details</li>
                                <li>International Collaboration Programs</li>
                                <li>Funding & Scholarship Opportunities</li>
                                <li>Future Program Developments</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="#whitepaper" class="cta-button">View White Paper Online</a>
                        <a href="MS_AI_Program_White_Paper.pdf" class="cta-button secondary" target="_blank" style="margin-left: 15px;">Download PDF</a>
                        <p style="margin-top: 15px; color: #666666; font-size: 14px;">
                            <strong>File Size:</strong> 2.3 MB | <strong>Pages:</strong> 45 | <strong>Last Updated:</strong> January 2025
                        </p>
                    </div>
                </div>

                <div class="two-column">
                    <div class="card">
                        <h4>Executive Summary</h4>
                        <p>The MS AI program at AURNOVA University represents a cutting-edge approach to graduate education in artificial intelligence. Our program combines rigorous theoretical foundations with practical, hands-on experience, preparing students for leadership roles in the rapidly evolving AI landscape.</p>
                        <p><strong>Key Highlights:</strong></p>
                        <ul>
                            <li>Industry-aligned curriculum with real-world applications</li>
                            <li>World-class faculty with industry and research expertise</li>
                            <li>State-of-the-art laboratories and computing resources</li>
                            <li>Strong industry partnerships and internship opportunities</li>
                        </ul>
                    </div>
                    <div class="card">
                        <h4>Research Impact</h4>
                        <p>Our faculty and students have contributed significantly to the field of artificial intelligence, with over 200 publications in top-tier conferences and journals, including NeurIPS, ICML, ICLR, and AAAI.</p>
                        <p><strong>Recent Achievements:</strong></p>
                        <ul>
                            <li>15 patents filed in AI technologies</li>
                            <li>$5M in research funding secured</li>
                            <li>3 startup companies launched by alumni</li>
                            <li>50+ industry partnerships established</li>
                        </ul>
                    </div>
                </div>
            </section>

            <section id="apply" class="section">
                <h3>Ready to Apply?</h3>
                <div style="text-align: center; padding: 40px;">
                    <p style="font-size: 20px; margin-bottom: 30px; color: #333333;">
                        Take the first step toward your future in artificial intelligence. Our application process is designed to be straightforward and comprehensive.
                    </p>
                    <a href="msai_application_form.html" class="cta-button">Start Your Application</a>
                    <p style="margin-top: 20px; color: #666666;">
                        <strong>Application Deadline:</strong> March 15, 2025<br>
                        <strong>Program Start:</strong> Fall 2025
                    </p>
                </div>
            </section>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p><strong>AURNOVA University</strong></p>
            <p>Master of Science in Artificial Intelligence Program</p>
            <p>Email: <a href="mailto:admissions@aurnova.edu">admissions@aurnova.edu</a> | Phone: (555) 123-4567</p>
            <p>&copy; 2025 AURNOVA University. All rights reserved.</p>
        </div>
    </footer>
</body>
</html><!-- Updated Mon Oct  6 23:08:46 EDT 2025 -->
""")

@app.get("/application", response_class=HTMLResponse)
async def read_application():
    """Serve the application form"""
    return HTMLResponse(content="""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MS AI Program Application - AURNOVA University</title>
    <style>
        body {
            font-family: 'Times New Roman', 'Georgia', serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #ffffff;
            line-height: 1.6;
        }
        .form-container {
            background: white;
            border: 1px solid #333333;
            padding: 50px;
            box-shadow: none;
        }
        .form-header {
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 3px solid #000000;
            padding-bottom: 30px;
        }
        .form-title {
            color: #000000;
            font-size: 32px;
            margin-bottom: 15px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        .university-name {
            color: #333333;
            font-size: 24px;
            margin-bottom: 20px;
            font-weight: normal;
        }
        .form-description {
            color: #333333;
            font-size: 16px;
            line-height: 1.8;
            text-align: left;
            max-width: 700px;
            margin: 0 auto;
        }
        .section {
            margin: 40px 0;
            padding: 30px;
            border: 2px solid #000000;
            background-color: #ffffff;
        }
        .section-title {
            color: #000000;
            font-size: 22px;
            margin-bottom: 25px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid #333333;
            padding-bottom: 10px;
        }
        .question {
            margin: 25px 0;
        }
        .question-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #000000;
            font-size: 16px;
        }
        .question-description {
            font-size: 14px;
            color: #333333;
            margin-bottom: 12px;
            font-style: italic;
        }
        .required {
            color: #000000;
            font-weight: bold;
        }
        input[type="text"], input[type="email"], input[type="tel"], input[type="date"], textarea, select {
            width: 100%;
            padding: 15px;
            border: 2px solid #333333;
            border-radius: 0;
            font-size: 16px;
            margin-bottom: 15px;
            font-family: 'Times New Roman', 'Georgia', serif;
            background-color: #ffffff;
        }
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #000000;
            box-shadow: 0 0 0 2px rgba(0,0,0,0.1);
        }
        textarea {
            min-height: 120px;
            resize: vertical;
        }
        .radio-group, .checkbox-group {
            margin: 15px 0;
        }
        .radio-item, .checkbox-item {
            margin: 12px 0;
            display: flex;
            align-items: center;
        }
        input[type="radio"], input[type="checkbox"] {
            margin-right: 15px;
            transform: scale(1.2);
        }
        .submit-btn {
            background-color: #000000;
            color: white;
            padding: 20px 40px;
            border: 2px solid #000000;
            font-size: 18px;
            cursor: pointer;
            margin-top: 40px;
            font-family: 'Times New Roman', 'Georgia', serif;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .submit-btn:hover {
            background-color: #333333;
            border-color: #333333;
        }
        .word-count {
            font-size: 12px;
            color: #666666;
            text-align: right;
            font-style: italic;
            margin-top: 5px;
        }
        h3 {
            color: #000000;
            font-size: 18px;
            margin: 30px 0 20px 0;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <div class="form-header">
            <h1 class="form-title">Master of Science in Artificial Intelligence</h1>
            <div class="university-name">AURNOVA University</div>
            <p class="form-description">
                <strong>Application for Admission</strong><br><br>
                Thank you for your interest in the Master of Science in Artificial Intelligence program at AURNOVA University. 
                This application form will help us evaluate your qualifications and fit for our program. Please complete all sections thoroughly and accurately.
                <br><br>
                <strong>Application Deadline:</strong> March 15, 2025<br>
                <strong>For technical support:</strong> admissions@aurnova.edu
            </p>
        </div>

        <form id="applicationForm">
            <!-- Personal Information Section -->
            <div class="section">
                <h2 class="section-title">Personal Information</h2>
                
                <div class="question">
                    <div class="question-title">Full Name <span class="required">*</span></div>
                    <div class="question-description">Enter your full legal name as it appears on official documents.</div>
                    <input type="text" name="fullName" required>
                </div>

                <div class="question">
                    <div class="question-title">Email Address <span class="required">*</span></div>
                    <div class="question-description">We will use this email to communicate with you about your application.</div>
                    <input type="email" name="email" required>
                </div>

                <div class="question">
                    <div class="question-title">Phone Number <span class="required">*</span></div>
                    <div class="question-description">Include country code if outside the United States.</div>
                    <input type="tel" name="phone" required>
                </div>

                <div class="question">
                    <div class="question-title">Date of Birth <span class="required">*</span></div>
                    <div class="question-description">Enter your date of birth.</div>
                    <input type="date" name="dateOfBirth" required>
                </div>

                <div class="question">
                    <div class="question-title">Gender <span class="required">*</span></div>
                    <div class="question-description">Please select your gender identity.</div>
                    <div class="radio-group">
                        <div class="radio-item">
                            <input type="radio" name="gender" value="Male" id="gender-male" required>
                            <label for="gender-male">Male</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" name="gender" value="Female" id="gender-female" required>
                            <label for="gender-female">Female</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" name="gender" value="Non-binary" id="gender-nonbinary" required>
                            <label for="gender-nonbinary">Non-binary</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" name="gender" value="Prefer not to say" id="gender-prefer-not" required>
                            <label for="gender-prefer-not">Prefer not to say</label>
                        </div>
                    </div>
                </div>

                <div class="question">
                    <div class="question-title">Mailing Address <span class="required">*</span></div>
                    <div class="question-description">Please provide your complete mailing address including street, city, state, ZIP code, and country.</div>
                    <textarea name="mailingAddress" required></textarea>
                </div>
            </div>

            <!-- Academic Information Section -->
            <div class="section">
                <h2 class="section-title">Academic Information</h2>
                
                <div class="question">
                    <div class="question-title">Undergraduate Degree <span class="required">*</span></div>
                    <div class="question-description">Enter your undergraduate degree (e.g., Bachelor of Science in Computer Science).</div>
                    <input type="text" name="undergraduateDegree" required>
                </div>

                <div class="question">
                    <div class="question-title">Institution <span class="required">*</span></div>
                    <div class="question-description">Name of the institution where you earned your undergraduate degree.</div>
                    <input type="text" name="institution" required>
                </div>

                <div class="question">
                    <div class="question-title">GPA <span class="required">*</span></div>
                    <div class="question-description">Enter your undergraduate GPA on a 4.0 scale.</div>
                    <input type="text" name="gpa" required>
                </div>

                <div class="question">
                    <div class="question-title">Graduation Year <span class="required">*</span></div>
                    <div class="question-description">Year you graduated or expect to graduate from your undergraduate program.</div>
                    <input type="text" name="graduationYear" required>
                </div>

                <div class="question">
                    <div class="question-title">Relevant Coursework <span class="required">*</span></div>
                    <div class="question-description">List courses in mathematics, computer science, statistics, AI, machine learning, etc. Include course numbers and grades if available.</div>
                    <textarea name="relevantCoursework" required></textarea>
                </div>

                <div class="question">
                    <div class="question-title">Research Experience and Publications <span class="required">*</span></div>
                    <div class="question-description">Describe any research projects, publications, conference presentations, or academic work. Include details about your role, methodology, and outcomes.</div>
                    <textarea name="researchExperience" required></textarea>
                </div>
            </div>

            <!-- Essays Section -->
            <div class="section">
                <h2 class="section-title">Essays and Statements</h2>
                
                <div class="question">
                    <div class="question-title">Statement of Purpose (750-1000 words) <span class="required">*</span></div>
                    <div class="question-description">Please address your academic background, research interests, career goals, and why you chose AURNOVA University. Be specific and provide concrete examples.</div>
                    <textarea name="statementOfPurpose" required oninput="updateWordCount(this, 'sop-count')"></textarea>
                    <div class="word-count" id="sop-count">Word count: 0</div>
                </div>

                <div class="question">
                    <div class="question-title">Personal Statement (500-750 words) <span class="required">*</span></div>
                    <div class="question-description">Tell us about yourself beyond your academic achievements, including personal experiences, challenges overcome, and unique perspectives.</div>
                    <textarea name="personalStatement" required oninput="updateWordCount(this, 'ps-count')"></textarea>
                    <div class="word-count" id="ps-count">Word count: 0</div>
                </div>

                <div class="question">
                    <div class="question-title">Research Interests and Potential Thesis Topics (300-500 words) <span class="required">*</span></div>
                    <div class="question-description">Describe your research interests in AI and potential thesis topics. Be specific about current research and cite relevant papers if possible.</div>
                    <textarea name="researchInterests" required oninput="updateWordCount(this, 'ri-count')"></textarea>
                    <div class="word-count" id="ri-count">Word count: 0</div>
                </div>

                <div class="question">
                    <div class="question-title">Career Goals and Professional Development (300-500 words) <span class="required">*</span></div>
                    <div class="question-description">Describe your short-term and long-term career aspirations, specific roles/companies of interest, and how this program will help.</div>
                    <textarea name="careerGoals" required oninput="updateWordCount(this, 'cg-count')"></textarea>
                    <div class="word-count" id="cg-count">Word count: 0</div>
                </div>
            </div>

            <!-- References Section -->
            <div class="section">
                <h2 class="section-title">References</h2>
                <p>Please provide contact information for 2-3 individuals who can speak to your academic abilities, research potential, and character. At least one should be from an academic setting.</p>
                
                <h3>Reference 1</h3>
                <div class="question">
                    <div class="question-title">Name <span class="required">*</span></div>
                    <input type="text" name="ref1Name" required>
                </div>
                <div class="question">
                    <div class="question-title">Title/Position <span class="required">*</span></div>
                    <input type="text" name="ref1Title" required>
                </div>
                <div class="question">
                    <div class="question-title">Institution/Organization <span class="required">*</span></div>
                    <input type="text" name="ref1Institution" required>
                </div>
                <div class="question">
                    <div class="question-title">Email <span class="required">*</span></div>
                    <input type="email" name="ref1Email" required>
                </div>
                <div class="question">
                    <div class="question-title">Phone</div>
                    <input type="tel" name="ref1Phone">
                </div>
                <div class="question">
                    <div class="question-title">Relationship <span class="required">*</span></div>
                    <input type="text" name="ref1Relationship" required>
                </div>

                <h3>Reference 2</h3>
                <div class="question">
                    <div class="question-title">Name <span class="required">*</span></div>
                    <input type="text" name="ref2Name" required>
                </div>
                <div class="question">
                    <div class="question-title">Title/Position <span class="required">*</span></div>
                    <input type="text" name="ref2Title" required>
                </div>
                <div class="question">
                    <div class="question-title">Institution/Organization <span class="required">*</span></div>
                    <input type="text" name="ref2Institution" required>
                </div>
                <div class="question">
                    <div class="question-title">Email <span class="required">*</span></div>
                    <input type="email" name="ref2Email" required>
                </div>
                <div class="question">
                    <div class="question-title">Phone</div>
                    <input type="tel" name="ref2Phone">
                </div>
                <div class="question">
                    <div class="question-title">Relationship <span class="required">*</span></div>
                    <input type="text" name="ref2Relationship" required>
                </div>
            </div>

            <button type="submit" class="submit-btn">Submit Application</button>
        </form>
    </div>

    <script>
        function updateWordCount(textarea, countId) {
            const text = textarea.value;
            const wordCount = text.trim().split(/\s+/).filter(word => word.length > 0).length;
            document.getElementById(countId).textContent = `Word count: ${wordCount}`;
        }

        document.getElementById('applicationForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Form submitted! In a real implementation, this would be sent to a server for processing.');
        });
    </script>
</body>
</html>""")

@app.get("/apply", response_class=HTMLResponse)
async def read_apply():
    """Alias for application form"""
    return await read_application()

@app.get("/form", response_class=HTMLResponse)
async def read_form():
    """Alias for application form"""
    return await read_application()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "MS AI Program Site", "version": "2.0.0"}

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "status": "operational",
        "service": "MS AI Program Site",
        "version": "2.0.0",
        "endpoints": {
            "main": "/",
            "application": "/application",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
