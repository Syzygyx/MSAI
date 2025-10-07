#!/usr/bin/env python3
"""
Try alternative approaches to create Google Forms
"""

import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def try_oauth_approach():
    """Try using OAuth instead of service account"""
    print('🔍 Trying OAuth approach...')
    
    # Check if we have OAuth credentials
    if not os.path.exists('credentials.json'):
        print('❌ No OAuth credentials found. Need to create them.')
        print('\nTo create OAuth credentials:')
        print('1. Go to https://console.developers.google.com/')
        print('2. Navigate to APIs & Services > Credentials')
        print('3. Click "Create Credentials" > "OAuth 2.0 Client ID"')
        print('4. Choose "Desktop Application"')
        print('5. Download the JSON file as "credentials.json"')
        return False
    
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.oauth2.credentials import Credentials
        
        SCOPES = ['https://www.googleapis.com/auth/forms.body']
        
        creds = None
        token_file = 'token.json'
        
        # Load existing token
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                from google.auth.transport.requests import Request
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        # Try to create form with OAuth
        service = build('forms', 'v1', credentials=creds)
        form_info = {'info': {'title': 'MS AI Application - OAuth Test'}}
        form = service.forms().create(body=form_info).execute()
        
        print('✅ OAuth approach worked!')
        print(f'Form ID: {form["formId"]}')
        print(f'Form URL: {form["responderUri"]}')
        return form
        
    except Exception as e:
        print(f'❌ OAuth approach failed: {e}')
        return False

def try_different_service_account():
    """Try with different service account configuration"""
    print('\n🔍 Trying different service account configuration...')
    
    try:
        # Try with more permissive scopes
        credentials = service_account.Credentials.from_service_account_file(
            'msai-service-key.json', 
            scopes=[
                'https://www.googleapis.com/auth/forms.body',
                'https://www.googleapis.com/auth/drive.file',
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/cloud-platform'
            ]
        )
        
        service = build('forms', 'v1', credentials=credentials)
        
        # Try different request formats
        test_cases = [
            {'info': {'title': 'Test 1'}},
            {'info': {'title': 'Test 2', 'description': ''}},
            {'info': {'title': 'Test 3'}, 'settings': {}},
        ]
        
        for i, test_case in enumerate(test_cases):
            try:
                print(f'  Trying test case {i+1}...')
                form = service.forms().create(body=test_case).execute()
                print(f'✅ Test case {i+1} worked!')
                print(f'Form ID: {form["formId"]}')
                return form
            except HttpError as e:
                print(f'  ❌ Test case {i+1} failed: {e.resp.status}')
                continue
        
        print('❌ All test cases failed')
        return False
        
    except Exception as e:
        print(f'❌ Service account approach failed: {e}')
        return False

def try_google_apps_script():
    """Try using Google Apps Script API"""
    print('\n🔍 Trying Google Apps Script approach...')
    
    try:
        credentials = service_account.Credentials.from_service_account_file(
            'msai-service-key.json', 
            scopes=['https://www.googleapis.com/auth/script.projects']
        )
        
        service = build('script', 'v1', credentials=credentials)
        
        # Create a script that creates a form
        script_code = '''
function createForm() {
  var form = FormApp.create('MS AI Program Application - AURNOVA University');
  form.setDescription('Thank you for your interest in the Master of Science in Artificial Intelligence program at AURNOVA University.');
  
  // Add basic questions
  form.addTextItem()
    .setTitle('Full Name')
    .setRequired(true);
    
  form.addTextItem()
    .setTitle('Email Address')
    .setRequired(true);
    
  form.addTextItem()
    .setTitle('Phone Number')
    .setRequired(true);
    
  form.addDateItem()
    .setTitle('Date of Birth')
    .setRequired(true);
    
  var genderItem = form.addMultipleChoiceItem();
  genderItem.setTitle('Gender')
    .setRequired(true)
    .setChoices([
      genderItem.createChoice('Male'),
      genderItem.createChoice('Female'),
      genderItem.createChoice('Non-binary'),
      genderItem.createChoice('Prefer not to say')
    ]);
  
  form.addParagraphTextItem()
    .setTitle('Mailing Address')
    .setRequired(true);
  
  return form.getPublishedUrl();
}
'''
        
        # Create a new script project
        project = {
            'title': 'MS AI Form Creator'
        }
        
        created_project = service.projects().create(body=project).execute()
        project_id = created_project['scriptId']
        
        print(f'✅ Created Apps Script project: {project_id}')
        
        # Add the code
        content = {
            'files': [{
                'name': 'Code',
                'type': 'SERVER_JS',
                'source': script_code
            }]
        }
        
        service.projects().updateContent(
            scriptId=project_id,
            body=content
        ).execute()
        
        print('✅ Added form creation code to Apps Script')
        print('You can now run this script in Google Apps Script to create the form')
        
        return {
            'project_id': project_id,
            'script_url': f'https://script.google.com/d/{project_id}/edit'
        }
        
    except Exception as e:
        print(f'❌ Apps Script approach failed: {e}')
        return False

def try_direct_api_call():
    """Try making a direct API call with proper authentication"""
    print('\n🔍 Trying direct API call...')
    
    try:
        import requests
        
        credentials = service_account.Credentials.from_service_account_file(
            'msai-service-key.json', 
            scopes=['https://www.googleapis.com/auth/forms.body']
        )
        
        # Get access token
        from google.auth.transport.requests import Request
        credentials.refresh(Request())
        access_token = credentials.token
        
        # Make direct API call
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'info': {
                'title': 'MS AI Program Application - Direct API'
            }
        }
        
        response = requests.post(
            'https://forms.googleapis.com/v1/forms',
            headers=headers,
            json=data
        )
        
        print(f'Direct API call status: {response.status_code}')
        print(f'Response: {response.text[:500]}')
        
        if response.status_code == 200:
            form_data = response.json()
            print('✅ Direct API call succeeded!')
            print(f'Form ID: {form_data["formId"]}')
            return form_data
        else:
            print(f'❌ Direct API call failed: {response.status_code}')
            return False
            
    except Exception as e:
        print(f'❌ Direct API call failed: {e}')
        return False

def main():
    """Try all alternative approaches"""
    print('🚀 Trying Alternative Approaches to Create Google Form')
    print('=' * 60)
    
    approaches = [
        ('OAuth', try_oauth_approach),
        ('Different Service Account Config', try_different_service_account),
        ('Google Apps Script', try_google_apps_script),
        ('Direct API Call', try_direct_api_call)
    ]
    
    for name, approach_func in approaches:
        print(f'\n--- Trying {name} ---')
        result = approach_func()
        if result:
            print(f'\n🎉 SUCCESS with {name}!')
            return result
    
    print('\n❌ All approaches failed')
    print('\nThis suggests there might be a fundamental issue with:')
    print('1. The Google Forms API service itself')
    print('2. Your Google Cloud project configuration')
    print('3. Billing or quota issues')
    print('4. Regional restrictions')
    
    print('\nNext steps:')
    print('1. Check Google Cloud Console for any alerts or issues')
    print('2. Verify billing is enabled for your project')
    print('3. Try creating a form manually to test if the API works at all')
    print('4. Contact Google support if the issue persists')

if __name__ == "__main__":
    main()