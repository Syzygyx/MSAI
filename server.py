#!/usr/bin/env python3
import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

class MSAIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "healthy",
                "timestamp": "2024-01-01T00:00:00Z",
                "services": {
                    "professors": "online",
                    "curriculum": "online",
                    "students": "online",
                    "database": "online"
                }
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/api/professors':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
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
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/api/curriculum':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
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
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/api/students':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
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
            self.wfile.write(json.dumps(response).encode())
            
        else:
            super().do_GET()

if __name__ == "__main__":
    PORT = 8002
    with socketserver.TCPServer(("", PORT), MSAIHandler) as httpd:
        print(f"🚀 MS AI Curriculum System running on port {PORT}")
        print(f"🌐 Access at: http://localhost:{PORT}")
        httpd.serve_forever()
