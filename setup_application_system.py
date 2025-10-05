#!/usr/bin/env python3
"""
Setup MSAI Application System
Configures the complete application system with Google Sheets integration
"""

import os
import json
from datetime import datetime
from google_sheets_integration import MSAIApplicationSheets

def setup_application_system():
    """Setup the complete MSAI application system"""
    print("🚀 Setting up MSAI Application System")
    print("=" * 50)
    
    # Initialize Google Sheets integration
    sheets_integration = MSAIApplicationSheets()
    
    # Authenticate
    print("\n🔑 Authenticating with Google Sheets...")
    if not sheets_integration.authenticate():
        print("❌ Authentication failed. Please check your credentials.")
        return False
    
    print("✅ Authentication successful")
    
    # Create spreadsheet
    print("\n📊 Creating Google Spreadsheet...")
    spreadsheet = sheets_integration.create_spreadsheet("MSAI Applications 2024")
    if not spreadsheet:
        print("❌ Failed to create spreadsheet")
        return False
    
    print(f"✅ Spreadsheet created: {spreadsheet.title}")
    print(f"🔗 Spreadsheet URL: https://docs.google.com/spreadsheets/d/{spreadsheet.id}")
    
    # Setup worksheet
    print("\n📋 Setting up worksheet...")
    if not sheets_integration.setup_worksheet("Applications"):
        print("❌ Failed to setup worksheet")
        return False
    
    print("✅ Worksheet setup complete")
    
    # Create additional worksheets
    print("\n📋 Creating additional worksheets...")
    try:
        # Create Statistics worksheet
        stats_worksheet = spreadsheet.add_worksheet(title="Statistics", rows=100, cols=10)
        stats_headers = [
            'Date', 'Total Applications', 'New Applications', 'Under Review', 
            'Accepted', 'Rejected', 'Waitlisted', 'Machine Learning', 
            'NLP', 'Computer Vision', 'General AI'
        ]
        stats_worksheet.update('A1:K1', [stats_headers])
        stats_worksheet.format('A1:K1', {
            'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 0.2},
            'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
        })
        print("✅ Statistics worksheet created")
        
        # Create Reviews worksheet
        reviews_worksheet = spreadsheet.add_worksheet(title="Reviews", rows=1000, cols=15)
        review_headers = [
            'Application ID', 'Applicant Name', 'Email', 'Reviewer', 
            'Review Date', 'Academic Score', 'Experience Score', 
            'Essay Score', 'Overall Score', 'Recommendation', 
            'Comments', 'Status', 'Next Steps', 'Follow-up Date', 'Notes'
        ]
        reviews_worksheet.update('A1:O1', [review_headers])
        reviews_worksheet.format('A1:O1', {
            'backgroundColor': {'red': 0.8, 'green': 0.4, 'blue': 0.2},
            'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
        })
        print("✅ Reviews worksheet created")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not create additional worksheets: {e}")
    
    # Save configuration
    config = {
        'spreadsheet_id': spreadsheet.id,
        'spreadsheet_url': f'https://docs.google.com/spreadsheets/d/{spreadsheet.id}',
        'worksheet_name': 'Applications',
        'service_account_email': 'msai-service-account@syzygyx-161202.iam.gserviceaccount.com',
        'service_account_file': 'msai-service-account-key.json',
        'created_at': datetime.now().isoformat(),
        'api_endpoints': {
            'submit_application': '/api/application',
            'upload_documents': '/api/application/upload',
            'get_applications': '/api/applications',
            'get_stats': '/api/applications/stats',
            'update_status': '/api/applications/{email}/status',
            'export_csv': '/api/applications/export'
        }
    }
    
    with open('msai_application_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n📄 Configuration saved to: msai_application_config.json")
    
    # Test the system
    print("\n🧪 Testing the application system...")
    
    # Test with sample data
    sample_application = {
        'firstName': 'Test',
        'lastName': 'User',
        'email': 'test@example.com',
        'phone': '+1-555-0123',
        'dateOfBirth': '1990-01-01',
        'gender': 'Other',
        'address': '123 Test St, Test City, TC 12345',
        'undergraduateDegree': 'Bachelor of Science in Computer Science',
        'undergraduateGPA': 3.5,
        'undergraduateInstitution': 'Test University',
        'graduationYear': 2015,
        'specialization': 'Machine Learning & Data Science',
        'startTerm': 'Fall 2024',
        'programFormat': 'Full-time',
        'interests': 'Machine Learning, Research',
        'statementOfPurpose': 'This is a test application for the MSAI program.',
        'reference1Name': 'Dr. Test Professor',
        'reference1Email': 'test.prof@university.edu',
        'reference1Relationship': 'Professor',
        'reference2Name': 'Ms. Test Manager',
        'reference2Email': 'test.manager@company.com',
        'reference2Relationship': 'Manager',
        'agreeTerms': True,
        'agreeMarketing': False
    }
    
    if sheets_integration.submit_application(sample_application):
        print("✅ Test application submitted successfully")
    else:
        print("❌ Test application failed")
        return False
    
    # Get statistics
    stats = sheets_integration.get_application_stats()
    print(f"\n📊 Current Statistics:")
    print(f"   Total Applications: {stats.get('total_applications', 0)}")
    print(f"   By Specialization: {stats.get('by_specialization', {})}")
    print(f"   By Status: {stats.get('by_status', {})}")
    
    print(f"\n✅ MSAI Application System setup complete!")
    print(f"🌐 Application Form: http://localhost:8000/")
    print(f"📊 Google Sheets: {config['spreadsheet_url']}")
    print(f"🔧 API Documentation: http://localhost:8000/docs")
    
    return True

def create_startup_script():
    """Create a startup script for the application system"""
    startup_script = """#!/bin/bash
# MSAI Application System Startup Script

echo "🚀 Starting MSAI Application System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install fastapi uvicorn python-multipart email-validator gspread google-auth google-auth-oauthlib google-auth-httplib2

# Start the application
echo "🌐 Starting application server..."
python msai_application_api.py
"""
    
    with open('start_application_system.sh', 'w') as f:
        f.write(startup_script)
    
    os.chmod('start_application_system.sh', 0o755)
    print("✅ Startup script created: start_application_system.sh")

def create_docker_setup():
    """Create Docker configuration for the application system"""
    dockerfile = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8000

# Start the application
CMD ["python", "msai_application_api.py"]
"""
    
    requirements = """fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
email-validator==2.1.0
gspread==5.12.0
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.2.0
pydantic==2.5.0
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile)
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("✅ Docker configuration created")

def main():
    """Main function"""
    print("🎓 MSAI Application System Setup")
    print("=" * 40)
    
    # Setup the application system
    if setup_application_system():
        print("\n🔧 Creating additional configuration files...")
        
        # Create startup script
        create_startup_script()
        
        # Create Docker setup
        create_docker_setup()
        
        print("\n🎉 Setup complete! You can now:")
        print("   1. Run: python msai_application_api.py")
        print("   2. Visit: http://localhost:8000/")
        print("   3. View API docs: http://localhost:8000/docs")
        print("   4. Check Google Sheets for submissions")
        
    else:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()