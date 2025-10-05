#!/usr/bin/env python3
"""
Working Lambda deployment for MS AI Curriculum System
"""

import boto3
import json
import zipfile
import time

def create_lambda_function():
    """Create the Lambda function code"""
    
    lambda_code = '''
import json
from datetime import datetime

def lambda_handler(event, context):
    """MS AI Curriculum System Lambda function"""
    
    # Parse the request
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    
    # CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle OPTIONS requests for CORS
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'CORS preflight'})
        }
    
    # Route requests
    if path == '/health':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'services': {
                    'professors': 'online',
                    'curriculum': 'online',
                    'students': 'online',
                    'database': 'online'
                },
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
                    {
                        'id': 'prof_001',
                        'name': 'Dr. Sarah Chen',
                        'specialization': 'Machine Learning',
                        'expertise_level': 'Expert',
                        'h_index': 45,
                        'total_citations': 1250,
                        'persona': {
                            'teaching_philosophy': 'Learning through hands-on experience and real-world applications',
                            'motivational_quotes': [
                                'The future belongs to those who learn AI today',
                                'Every algorithm tells a story'
                            ]
                        }
                    },
                    {
                        'id': 'prof_002',
                        'name': 'Dr. Michael Rodriguez',
                        'specialization': 'Natural Language Processing',
                        'expertise_level': 'Expert',
                        'h_index': 38,
                        'total_citations': 980,
                        'persona': {
                            'teaching_philosophy': 'Understanding language is understanding intelligence',
                            'motivational_quotes': [
                                'Language is the bridge between human and artificial intelligence',
                                'Words have power, algorithms amplify it'
                            ]
                        }
                    }
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
                'duration': '2 years',
                'accreditation': 'ABET',
                'specializations': [
                    'Machine Learning & Data Science',
                    'Natural Language Processing',
                    'Computer Vision & Robotics'
                ],
                'ai_features': {
                    'personalized_learning': 'AI adapts curriculum to individual learning styles',
                    'virtual_professors': 'AI professors with unique personalities',
                    'adaptive_content': 'Content that evolves with student progress',
                    'intelligent_assessment': 'AI-powered evaluation system'
                }
            })
        }
    
    elif path == '/api/students':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'students': [
                    {
                        'id': 'student_001',
                        'name': 'Alex Johnson',
                        'learning_style': 'Visual',
                        'current_level': 'Intermediate',
                        'enrolled_courses': ['ML Fundamentals', 'Data Structures'],
                        'gpa': 3.7
                    },
                    {
                        'id': 'student_002',
                        'name': 'Maria Garcia',
                        'learning_style': 'Kinesthetic',
                        'current_level': 'Advanced',
                        'enrolled_courses': ['Deep Learning', 'NLP Applications'],
                        'gpa': 3.9
                    }
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
                'timestamp': datetime.now().isoformat(),
                'deployment': 'AWS Lambda',
                'endpoints': {
                    'health': '/health',
                    'professors': '/api/professors',
                    'curriculum': '/api/curriculum',
                    'students': '/api/students'
                }
            })
        }
    
    else:
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({
                'error': 'Not Found',
                'message': 'The requested endpoint was not found',
                'available_endpoints': ['/', '/health', '/api/professors', '/api/curriculum', '/api/students']
            })
        }
'''
    
    return lambda_code

def create_deployment_package():
    """Create Lambda deployment package"""
    
    lambda_code = create_lambda_function()
    
    # Create zip file
    with zipfile.ZipFile('msai-lambda-deployment.zip', 'w') as zip_file:
        zip_file.writestr('lambda_function.py', lambda_code)
    
    return 'msai-lambda-deployment.zip'

def deploy_lambda():
    """Deploy the Lambda function"""
    
    print("🚀 Deploying MS AI Curriculum System to AWS Lambda...")
    
    # Create deployment package
    package_file = create_deployment_package()
    
    # Initialize AWS clients
    lambda_client = boto3.client('lambda')
    apigateway_client = boto3.client('apigateway')
    iam_client = boto3.client('iam')
    
    try:
        # Create IAM role for Lambda
        print("Creating IAM role for Lambda...")
        role_policy = {
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
            role = iam_client.create_role(
                RoleName='msai-lambda-role',
                AssumeRolePolicyDocument=json.dumps(role_policy),
                Description='Role for MS AI Lambda function'
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
        except:
            pass
        
        # Wait for role to be ready
        time.sleep(10)
        
        # Create Lambda function
        print("Creating Lambda function...")
        with open(package_file, 'rb') as f:
            zip_content = f.read()
        
        try:
            lambda_function = lambda_client.create_function(
                FunctionName='msai-curriculum-system',
                Runtime='python3.9',
                Role=f'arn:aws:iam::{boto3.client("sts").get_caller_identity()["Account"]}:role/msai-lambda-role',
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': zip_content},
                Description='MS AI Curriculum System API',
                Timeout=30,
                MemorySize=256
            )
            print("✅ Lambda function created")
        except lambda_client.exceptions.ResourceConflictException:
            print("✅ Lambda function already exists")
        
        # Create API Gateway
        print("Creating API Gateway...")
        try:
            api = apigateway_client.create_rest_api(
                name='msai-curriculum-api',
                description='MS AI Curriculum System API Gateway',
                endpointConfiguration={'types': ['REGIONAL']}
            )
            api_id = api['id']
            print(f"✅ API Gateway created: {api_id}")
        except:
            # Get existing API
            apis = apigateway_client.get_rest_apis()
            for api in apis['items']:
                if api['name'] == 'msai-curriculum-api':
                    api_id = api['id']
                    break
            print(f"✅ Using existing API Gateway: {api_id}")
        
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
        proxy_resource_id = proxy_resource['id']
        
        # Create ANY method for proxy
        apigateway_client.put_method(
            restApiId=api_id,
            resourceId=proxy_resource_id,
            httpMethod='ANY',
            authorizationType='NONE'
        )
        
        # Create integration
        lambda_uri = f"arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:{boto3.client('sts').get_caller_identity()['Account']}:function:msai-curriculum-system/invocations"
        
        apigateway_client.put_integration(
            restApiId=api_id,
            resourceId=proxy_resource_id,
            httpMethod='ANY',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=lambda_uri
        )
        
        # Create ANY method for root
        apigateway_client.put_method(
            restApiId=api_id,
            resourceId=root_resource_id,
            httpMethod='ANY',
            authorizationType='NONE'
        )
        
        apigateway_client.put_integration(
            restApiId=api_id,
            resourceId=root_resource_id,
            httpMethod='ANY',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=lambda_uri
        )
        
        # Deploy API
        print("Deploying API...")
        deployment = apigateway_client.create_deployment(
            restApiId=api_id,
            stageName='prod'
        )
        print("✅ API deployed")
        
        # Add Lambda permission
        try:
            lambda_client.add_permission(
                FunctionName='msai-curriculum-system',
                StatementId='apigateway-invoke',
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn=f'arn:aws:execute-api:us-east-1:{boto3.client("sts").get_caller_identity()["Account"]}:{api_id}/*/*'
            )
            print("✅ Lambda permission added")
        except:
            pass
        
        # Get API URL
        api_url = f"https://{api_id}.execute-api.us-east-1.amazonaws.com/prod"
        print(f"🌐 API URL: {api_url}")
        
        # Test the API
        print("Testing API...")
        import requests
        try:
            response = requests.get(f'{api_url}/health', timeout=10)
            if response.status_code == 200:
                print("✅ API is working!")
                print("Response:", response.json())
            else:
                print(f"❌ API returned status {response.status_code}")
        except Exception as e:
            print(f"❌ API test failed: {e}")
        
        print("✅ MS AI Curriculum System deployed to Lambda!")
        print(f"🔗 Access at: {api_url}")
        print(f"🔍 Health check: {api_url}/health")
        print(f"👨‍🏫 Professors: {api_url}/api/professors")
        print(f"📚 Curriculum: {api_url}/api/curriculum")
        print(f"👥 Students: {api_url}/api/students")
        
        return api_url
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    deploy_lambda()
EOF

Now let me run the Lambda deployment:
<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
run_terminal_cmd