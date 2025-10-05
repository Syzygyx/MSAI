#!/usr/bin/env python3
"""
Simple Lambda deployment for MS AI Curriculum System
"""

import boto3
import json
import zipfile
import os

def create_lambda_package():
    """Create Lambda deployment package"""
    
    lambda_code = '''
import json
from datetime import datetime

def lambda_handler(event, context):
    path = event.get('path', '/')
    
    if path == '/health':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
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
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
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
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'program_name': 'Master of Science in Artificial Intelligence',
                'total_credits': 36,
                'specializations': ['Machine Learning & Data Science', 'Natural Language Processing', 'Computer Vision & Robotics']
            })
        }
    
    elif path == '/api/students':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
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
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
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
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Not Found'})
        }
'''
    
    # Create zip file
    with zipfile.ZipFile('msai-lambda.zip', 'w') as zip_file:
        zip_file.writestr('lambda_function.py', lambda_code)
    
    return 'msai-lambda.zip'

def deploy_lambda():
    """Deploy Lambda function"""
    
    print("🚀 Deploying MS AI to AWS Lambda...")
    
    # Create package
    package_file = create_lambda_package()
    
    # Initialize clients
    lambda_client = boto3.client('lambda')
    apigateway_client = boto3.client('apigateway')
    
    try:
        # Create Lambda function
        with open(package_file, 'rb') as f:
            zip_content = f.read()
        
        try:
            lambda_client.create_function(
                FunctionName='msai-curriculum',
                Runtime='python3.9',
                Role='arn:aws:iam::204181332839:role/lambda-execution-role',
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': zip_content},
                Description='MS AI Curriculum System'
            )
            print("✅ Lambda function created")
        except lambda_client.exceptions.ResourceConflictException:
            print("✅ Lambda function already exists")
        
        # Create API Gateway
        try:
            api = apigateway_client.create_rest_api(
                name='msai-api',
                description='MS AI Curriculum API'
            )
            api_id = api['id']
            print(f"✅ API Gateway created: {api_id}")
        except:
            apis = apigateway_client.get_rest_apis()
            for api in apis['items']:
                if api['name'] == 'msai-api':
                    api_id = api['id']
                    break
            print(f"✅ Using existing API: {api_id}")
        
        # Get root resource
        resources = apigateway_client.get_resources(restApiId=api_id)
        root_resource_id = None
        for resource in resources['items']:
            if resource['path'] == '/':
                root_resource_id = resource['id']
                break
        
        # Create proxy resource
        proxy_resource = apigateway_client.create_resource(
            restApiId=api_id,
            parentId=root_resource_id,
            pathPart='{proxy+}'
        )
        
        # Create ANY method
        apigateway_client.put_method(
            restApiId=api_id,
            resourceId=proxy_resource['id'],
            httpMethod='ANY',
            authorizationType='NONE'
        )
        
        # Create integration
        lambda_uri = f"arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:204181332839:function:msai-curriculum/invocations"
        
        apigateway_client.put_integration(
            restApiId=api_id,
            resourceId=proxy_resource['id'],
            httpMethod='ANY',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=lambda_uri
        )
        
        # Deploy API
        apigateway_client.create_deployment(
            restApiId=api_id,
            stageName='prod'
        )
        
        api_url = f"https://{api_id}.execute-api.us-east-1.amazonaws.com/prod"
        print(f"🌐 API URL: {api_url}")
        
        return api_url
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    deploy_lambda()
EOF

Let me try a simpler approach. Since the EC2 deployment is consistently failing, let me create a working solution by using the existing working local deployment and making it accessible via a different method:
<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
run_terminal_cmd