#!/usr/bin/env python3
"""
Create OAuth credentials for Google Forms API
"""

import json
import webbrowser
from urllib.parse import urlencode

def create_oauth_credentials():
    """Guide user through creating OAuth credentials"""
    print('🔧 Creating OAuth Credentials for Google Forms API')
    print('=' * 50)
    
    print('Step 1: Go to Google Cloud Console')
    print('Opening: https://console.developers.google.com/')
    
    # Open the Google Cloud Console
    webbrowser.open('https://console.developers.google.com/')
    
    print('\nStep 2: Navigate to your project')
    print('1. Select project: syzygyx-161202')
    print('2. Go to APIs & Services > Credentials')
    
    print('\nStep 3: Create OAuth 2.0 Client ID')
    print('1. Click "Create Credentials"')
    print('2. Select "OAuth 2.0 Client ID"')
    print('3. If prompted, configure OAuth consent screen first')
    print('4. Choose "Desktop Application"')
    print('5. Name it: "MS AI Form Creator"')
    print('6. Click "Create"')
    
    print('\nStep 4: Download credentials')
    print('1. Click the download button (⬇️) next to your new client ID')
    print('2. Save the file as "credentials.json" in this directory')
    print('3. The file should contain client_id, client_secret, etc.')
    
    print('\nStep 5: Enable required APIs')
    print('Make sure these APIs are enabled:')
    print('- Google Forms API')
    print('- Google Drive API')
    print('- Google Sheets API')
    
    print('\nAfter completing these steps, run:')
    print('python create_form_with_oauth.py')
    
    return True

def check_credentials():
    """Check if OAuth credentials exist"""
    if os.path.exists('credentials.json'):
        print('✅ OAuth credentials found!')
        try:
            with open('credentials.json', 'r') as f:
                creds = json.load(f)
                if 'client_id' in creds and 'client_secret' in creds:
                    print('✅ Credentials file looks valid')
                    return True
                else:
                    print('❌ Credentials file is missing required fields')
                    return False
        except json.JSONDecodeError:
            print('❌ Credentials file is not valid JSON')
            return False
    else:
        print('❌ OAuth credentials not found')
        return False

if __name__ == "__main__":
    import os
    
    if check_credentials():
        print('\n🎉 OAuth credentials are ready!')
        print('You can now run: python create_form_with_oauth.py')
    else:
        create_oauth_credentials()