#!/usr/bin/env python3
"""
Deploy MS AI Curriculum System using AWS Lambda and API Gateway
"""

import json
import boto3
import zipfile
import os
from pathlib import Path

def create_lambda_function():
    """Create Lambda function for MS AI Curriculum System"""
    
    # Create Lambda client
    lambda_client = boto3.client('lambda')
    
    # Create the Lambda function code
    lambda_code = '''
import json
from mangum import Mangum
from fastapi import FastAPI

app = FastAPI(title="MS AI Curriculum System")

@app.get("/")
def read_root():
    return {
        "message": "MS AI Curriculum System is live!", 
        "status": "success", 
        "domain": "msai.syzygyx.com"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "services": {
            "professors": "online", 
            "curriculum": "online", 
            "students": "online"
        }
    }

@app.get("/api/professors")
def get_professors():
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
def get_curriculum():
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
def get_students():
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

# Create Mangum handler
handler = Mangum(app)
'''
    
    # Create requirements.txt
    requirements = '''
fastapi==0.104.1
mangum==0.17.0
'''
    
    # Create deployment package
    with zipfile.ZipFile('lambda_deployment.zip', 'w') as zip_file:
        zip_file.writestr('lambda_function.py', lambda_code)
        zip_file.writestr('requirements.txt', requirements)
    
    print("✅ Lambda deployment package created")
    
    # Create IAM role for Lambda
    iam_client = boto3.client('iam')
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        role_response = iam_client.create_role(
            RoleName='msai-lambda-role',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role for MS AI Curriculum System Lambda function'
        )
        print("✅ IAM role created")
    except iam_client.exceptions.EntityAlreadyExistsException:
        print("✅ IAM role already exists")
    
    # Attach basic execution policy
    try:
        iam_client.attach_role_policy(
            RoleName='msai-lambda-role',
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        print("✅ Basic execution policy attached")
    except Exception as e:
        print(f"Policy attachment: {e}")
    
    # Wait for role to be ready
    import time
    time.sleep(10)
    
    # Create Lambda function
    try:
        with open('lambda_deployment.zip', 'rb') as zip_file:
            response = lambda_client.create_function(
                FunctionName='msai-curriculum-system',
                Runtime='python3.9',
                Role=f'arn:aws:iam::{boto3.client("sts").get_caller_identity()["Account"]}:role/msai-lambda-role',
                Handler='lambda_function.handler',
                Code={'ZipFile': zip_file.read()},
                Description='MS AI Curriculum System API',
                Timeout=30,
                MemorySize=512
            )
        print("✅ Lambda function created successfully")
        print(f"Function ARN: {response['FunctionArn']}")
        return response['FunctionArn']
    except Exception as e:
        print(f"❌ Error creating Lambda function: {e}")
        return None

def create_api_gateway():
    """Create API Gateway for the Lambda function"""
    
    api_client = boto3.client('apigateway')
    
    try:
        # Create REST API
        api_response = api_client.create_rest_api(
            name='msai-curriculum-api',
            description='MS AI Curriculum System API Gateway',
            endpointConfiguration={'types': ['REGIONAL']}
        )
        
        api_id = api_response['id']
        print(f"✅ API Gateway created: {api_id}")
        
        # Get root resource
        resources = api_client.get_resources(restApiId=api_id)
        root_resource_id = resources['items'][0]['id']
        
        # Create proxy resource
        proxy_resource = api_client.create_resource(
            restApiId=api_id,
            parentId=root_resource_id,
            pathPart='{proxy+}'
        )
        
        proxy_resource_id = proxy_resource['id']
        
        # Create ANY method
        api_client.put_method(
            restApiId=api_id,
            resourceId=proxy_resource_id,
            httpMethod='ANY',
            authorizationType='NONE'
        )
        
        # Create integration
        api_client.put_integration(
            restApiId=api_id,
            resourceId=proxy_resource_id,
            httpMethod='ANY',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:lambda:us-east-1:{boto3.client("sts").get_caller_identity()["Account"]}:function:msai-curriculum-system'
        )
        
        # Create root method
        api_client.put_method(
            restApiId=api_id,
            resourceId=root_resource_id,
            httpMethod='ANY',
            authorizationType='NONE'
        )
        
        # Create root integration
        api_client.put_integration(
            restApiId=api_id,
            resourceId=root_resource_id,
            httpMethod='ANY',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:lambda:us-east-1:{boto3.client("sts").get_caller_identity()["Account"]}:function:msai-curriculum-system'
        )
        
        # Deploy API
        deployment = api_client.create_deployment(
            restApiId=api_id,
            stageName='prod'
        )
        
        print(f"✅ API Gateway deployed: https://{api_id}.execute-api.us-east-1.amazonaws.com/prod")
        return f"https://{api_id}.execute-api.us-east-1.amazonaws.com/prod"
        
    except Exception as e:
        print(f"❌ Error creating API Gateway: {e}")
        return None

def main():
    """Main deployment function"""
    print("🎓 MS AI Curriculum System - Lambda Deployment")
    print("=" * 50)
    
    # Create Lambda function
    function_arn = create_lambda_function()
    if not function_arn:
        print("❌ Failed to create Lambda function")
        return False
    
    # Create API Gateway
    api_url = create_api_gateway()
    if not api_url:
        print("❌ Failed to create API Gateway")
        return False
    
    print("\n🎉 Deployment completed successfully!")
    print("=" * 40)
    print(f"🌐 API URL: {api_url}")
    print(f"📊 Test endpoints:")
    print(f"   - Health: {api_url}/health")
    print(f"   - Professors: {api_url}/api/professors")
    print(f"   - Curriculum: {api_url}/api/curriculum")
    print(f"   - Students: {api_url}/api/students")
    
    return True

if __name__ == "__main__":
    main()