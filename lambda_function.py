import json
from datetime import datetime

def lambda_handler(event, context):
    path = event.get('path', '/')
    
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    if path == '/health':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'services': {'professors': 'online', 'curriculum': 'online', 'students': 'online'},
                'deployment': 'AWS Lambda',
                'domain': 'msai.syzygyx.com'
            })
        }
    
    elif path == '/api/professors':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'professors': [
                    {'id': 'prof_001', 'name': 'Dr. Sarah Chen', 'specialization': 'Machine Learning', 'expertise_level': 'Expert'},
                    {'id': 'prof_002', 'name': 'Dr. Michael Rodriguez', 'specialization': 'Natural Language Processing', 'expertise_level': 'Expert'}
                ]
            })
        }
    
    elif path == '/api/curriculum':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'program_name': 'Master of Science in Artificial Intelligence',
                'total_credits': 36,
                'specializations': ['Machine Learning & Data Science', 'Natural Language Processing', 'Computer Vision & Robotics']
            })
        }
    
    elif path == '/api/students':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'students': [
                    {'id': 'student_001', 'name': 'Alex Johnson', 'learning_style': 'Visual', 'gpa': 3.7},
                    {'id': 'student_002', 'name': 'Maria Garcia', 'learning_style': 'Kinesthetic', 'gpa': 3.9}
                ]
            })
        }
    
    elif path == '/':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Welcome to MS AI Curriculum System',
                'version': '1.0.0',
                'status': 'online',
                'domain': 'msai.syzygyx.com',
                'timestamp': datetime.now().isoformat()
            })
        }
    
    else:
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'error': 'Not Found'})
        }
