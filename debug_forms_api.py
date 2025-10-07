#!/usr/bin/env python3
"""
Debug Google Forms API Issues
"""

import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def debug_forms_api():
    """Debug the Google Forms API issue step by step"""
    print('🔍 Debugging Google Forms API Issue')
    print('=' * 50)
    
    # 1. Check service account details
    with open('msai-service-key.json', 'r') as f:
        key_data = json.load(f)
        print('Service Account Details:')
        print(f'  Email: {key_data.get("client_email")}')
        print(f'  Project ID: {key_data.get("project_id")}')
        print(f'  Private Key ID: {key_data.get("private_key_id")}')
        print(f'  Auth URI: {key_data.get("auth_uri")}')
        print(f'  Token URI: {key_data.get("token_uri")}')
    
    # 2. Test authentication
    try:
        credentials = service_account.Credentials.from_service_account_file(
            'msai-service-key.json', 
            scopes=['https://www.googleapis.com/auth/forms.body']
        )
        print('\n✅ Service account credentials loaded')
        
        # 3. Test API service creation
        service = build('forms', 'v1', credentials=credentials)
        print('✅ Forms API service created')
        
        # 4. Test different request formats
        print('\n🔍 Testing different request formats...')
        
        # Test 1: Minimal request
        try:
            print('Test 1: Minimal request...')
            form_info = {'info': {'title': 'Test Form Debug'}}
            form = service.forms().create(body=form_info).execute()
            print('✅ Minimal form created successfully!')
            print(f'Form ID: {form["formId"]}')
            return form
        except HttpError as e:
            print(f'❌ Minimal request failed: {e}')
            print(f'Status: {e.resp.status}')
            print(f'Reason: {e.resp.reason}')
            
        # Test 2: With explicit alt parameter
        try:
            print('\nTest 2: With alt=json parameter...')
            form_info = {'info': {'title': 'Test Form Debug 2'}}
            form = service.forms().create(body=form_info, alt='json').execute()
            print('✅ Form created with alt=json!')
            print(f'Form ID: {form["formId"]}')
            return form
        except HttpError as e:
            print(f'❌ Alt=json failed: {e}')
            
        # Test 3: Check if it's a quota issue by testing other APIs
        print('\nTest 3: Testing other APIs...')
        try:
            # Test Drive API
            drive_service = build('drive', 'v3', credentials=credentials)
            about = drive_service.about().get(fields='user').execute()
            print('✅ Drive API works - not a general auth issue')
        except Exception as e:
            print(f'❌ Drive API also fails: {e}')
            
        # Test 4: Try with different scopes
        print('\nTest 4: Testing with different scopes...')
        try:
            credentials_wide = service_account.Credentials.from_service_account_file(
                'msai-service-key.json', 
                scopes=[
                    'https://www.googleapis.com/auth/forms.body',
                    'https://www.googleapis.com/auth/drive.file',
                    'https://www.googleapis.com/auth/spreadsheets'
                ]
            )
            service_wide = build('forms', 'v1', credentials=credentials_wide)
            form_info = {'info': {'title': 'Test Form Wide Scopes'}}
            form = service_wide.forms().create(body=form_info).execute()
            print('✅ Form created with wide scopes!')
            print(f'Form ID: {form["formId"]}')
            return form
        except HttpError as e:
            print(f'❌ Wide scopes failed: {e}')
            
        # Test 5: Check if it's a project-specific issue
        print('\nTest 5: Checking project configuration...')
        try:
            # Try to make a raw request to see the exact error
            auth_req = requests.Request()
            credentials.refresh(auth_req)
            access_token = credentials.token
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            data = {'info': {'title': 'Test Form Raw'}}
            
            response = requests.post(
                'https://forms.googleapis.com/v1/forms',
                headers=headers,
                json=data
            )
            
            print(f'Raw request status: {response.status_code}')
            print(f'Raw request response: {response.text[:500]}')
            
            if response.status_code == 200:
                form_data = response.json()
                print('✅ Raw request succeeded!')
                print(f'Form ID: {form_data["formId"]}')
                return form_data
            else:
                print(f'❌ Raw request failed: {response.status_code}')
                print(f'Response: {response.text}')
                
        except Exception as e:
            print(f'❌ Raw request error: {e}')
            
    except Exception as e:
        print(f'❌ General error: {e}')
        print(f'Error type: {type(e).__name__}')
    
    return None

def check_api_enabled():
    """Check if the Forms API is enabled"""
    print('\n🔍 Checking if Forms API is enabled...')
    
    try:
        credentials = service_account.Credentials.from_service_account_file(
            'msai-service-key.json', 
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        # Try to access the API management endpoint
        service = build('serviceusage', 'v1', credentials=credentials)
        project_id = 'syzygyx-161202'  # From your service account
        
        # Check if Forms API is enabled
        service_name = f'projects/{project_id}/services/forms.googleapis.com'
        
        try:
            service_info = service.services().get(name=service_name).execute()
            state = service_info.get('state', 'UNKNOWN')
            print(f'Forms API state: {state}')
            
            if state == 'ENABLED':
                print('✅ Forms API is enabled')
            else:
                print('❌ Forms API is not enabled')
                print('You need to enable it in Google Cloud Console')
                
        except HttpError as e:
            if e.resp.status == 403:
                print('❌ No permission to check API status')
            else:
                print(f'❌ Error checking API status: {e}')
                
    except Exception as e:
        print(f'❌ Error checking API: {e}')

if __name__ == "__main__":
    # Check if API is enabled
    check_api_enabled()
    
    # Debug the API issue
    result = debug_forms_api()
    
    if result:
        print('\n🎉 SUCCESS! We found a working approach!')
        print(f'Form ID: {result["formId"]}')
        print(f'Form URL: {result["responderUri"]}')
    else:
        print('\n❌ All approaches failed. Need to investigate further.')
        print('\nNext steps:')
        print('1. Check if Forms API is enabled in Google Cloud Console')
        print('2. Verify service account has correct permissions')
        print('3. Try creating a form manually to test API access')
        print('4. Contact Google support if issue persists')