#!/usr/bin/env python3
"""
Google Sheets Integration for MSAI Application Form
Handles form submissions and stores data in Google Sheets
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class MSAIApplicationSheets:
    """Handle MSAI application form submissions to Google Sheets"""
    
    def __init__(self, credentials_file: str = 'msai-service-account-key.json'):
        self.credentials_file = credentials_file
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        self.service = None
        self.sheet_id = None
        self.worksheet = None
        
    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            creds = Credentials.from_service_account_file(
                self.credentials_file, 
                scopes=self.scopes
            )
            
            self.service = gspread.authorize(creds)
            print("✅ Google Sheets authentication successful")
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def create_spreadsheet(self, title: str = "MSAI Applications"):
        """Create a new Google Spreadsheet for applications"""
        try:
            spreadsheet = self.service.create(title)
            self.sheet_id = spreadsheet.id
            
            # Share with service account email
            spreadsheet.share('msai-service-account@syzygyx-161202.iam.gserviceaccount.com', 
                            perm_type='user', role='writer')
            
            print(f"✅ Created spreadsheet: {title} (ID: {self.sheet_id})")
            return spreadsheet
            
        except Exception as e:
            print(f"❌ Error creating spreadsheet: {e}")
            return None
    
    def setup_worksheet(self, sheet_name: str = "Applications"):
        """Setup the worksheet with headers"""
        try:
            if not self.sheet_id:
                print("❌ No spreadsheet ID available")
                return False
            
            spreadsheet = self.service.open_by_key(self.sheet_id)
            worksheet = spreadsheet.worksheet(sheet_name)
            
            # Define headers
            headers = [
                'Timestamp',
                'First Name',
                'Last Name',
                'Email',
                'Phone',
                'Date of Birth',
                'Gender',
                'Address',
                'Undergraduate Degree',
                'Undergraduate GPA',
                'Undergraduate Institution',
                'Graduation Year',
                'Graduate Degree',
                'GRE Score',
                'TOEFL Score',
                'Specialization',
                'Start Term',
                'Program Format',
                'Areas of Interest',
                'Statement of Purpose',
                'Personal Statement',
                'Diversity Statement',
                'Research Experience',
                'Career Goals',
                'Additional Info',
                'Current Employer',
                'Current Position',
                'Work Experience',
                'Relevant Experience',
                # Reference 1
                'Reference 1 Name',
                'Reference 1 Title',
                'Reference 1 Email',
                'Reference 1 Phone',
                'Reference 1 Institution',
                'Reference 1 Relationship',
                'Reference 1 Years Known',
                # Reference 2
                'Reference 2 Name',
                'Reference 2 Title',
                'Reference 2 Email',
                'Reference 2 Phone',
                'Reference 2 Institution',
                'Reference 2 Relationship',
                'Reference 2 Years Known',
                # Reference 3
                'Reference 3 Name',
                'Reference 3 Title',
                'Reference 3 Email',
                'Reference 3 Phone',
                'Reference 3 Institution',
                'Reference 3 Relationship',
                'Reference 3 Years Known',
                'How Did You Hear',
                'Additional Comments',
                'Agree Terms',
                'Agree Marketing',
                'Status',
                'Notes'
            ]
            
            # Set headers
            worksheet.update('A1:AK1', [headers])
            
            # Format headers
            worksheet.format('A1:AK1', {
                'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
            })
            
            # Freeze header row
            worksheet.freeze(rows=1)
            
            # Auto-resize columns
            worksheet.columns_auto_resize(0, len(headers))
            
            self.worksheet = worksheet
            print(f"✅ Worksheet '{sheet_name}' setup complete")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up worksheet: {e}")
            return False
    
    def submit_application(self, form_data: Dict[str, Any]) -> bool:
        """Submit application data to Google Sheets"""
        try:
            if not self.worksheet:
                print("❌ Worksheet not initialized")
                return False
            
            # Prepare data row
            row_data = [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                form_data.get('firstName', ''),
                form_data.get('lastName', ''),
                form_data.get('email', ''),
                form_data.get('phone', ''),
                form_data.get('dateOfBirth', ''),
                form_data.get('gender', ''),
                form_data.get('address', ''),
                form_data.get('undergraduateDegree', ''),
                form_data.get('undergraduateGPA', ''),
                form_data.get('undergraduateInstitution', ''),
                form_data.get('graduationYear', ''),
                form_data.get('graduateDegree', ''),
                form_data.get('greScore', ''),
                form_data.get('toeflScore', ''),
                form_data.get('specialization', ''),
                form_data.get('startTerm', ''),
                form_data.get('programFormat', ''),
                form_data.get('interests', ''),
                form_data.get('statementOfPurpose', ''),
                form_data.get('diversityStatement', ''),
                form_data.get('researchExperience', ''),
                form_data.get('currentEmployer', ''),
                form_data.get('currentPosition', ''),
                form_data.get('workExperience', ''),
                form_data.get('relevantExperience', ''),
                form_data.get('reference1Name', ''),
                form_data.get('reference1Email', ''),
                form_data.get('reference1Relationship', ''),
                form_data.get('reference2Name', ''),
                form_data.get('reference2Email', ''),
                form_data.get('reference2Relationship', ''),
                form_data.get('howDidYouHear', ''),
                form_data.get('additionalComments', ''),
                'Yes' if form_data.get('agreeTerms') else 'No',
                'Yes' if form_data.get('agreeMarketing') else 'No',
                'New',  # Status
                ''  # Notes
            ]
            
            # Append row to worksheet
            self.worksheet.append_row(row_data)
            
            print(f"✅ Application submitted for {form_data.get('firstName')} {form_data.get('lastName')}")
            return True
            
        except Exception as e:
            print(f"❌ Error submitting application: {e}")
            return False
    
    def get_applications(self, status: str = None) -> List[Dict[str, Any]]:
        """Retrieve applications from Google Sheets"""
        try:
            if not self.worksheet:
                print("❌ Worksheet not initialized")
                return []
            
            # Get all records
            records = self.worksheet.get_all_records()
            
            if status:
                records = [record for record in records if record.get('Status') == status]
            
            return records
            
        except Exception as e:
            print(f"❌ Error retrieving applications: {e}")
            return []
    
    def update_application_status(self, email: str, status: str, notes: str = '') -> bool:
        """Update application status"""
        try:
            if not self.worksheet:
                print("❌ Worksheet not initialized")
                return False
            
            # Find the row with the email
            cell = self.worksheet.find(email)
            if not cell:
                print(f"❌ Application not found for email: {email}")
                return False
            
            # Update status and notes
            row = cell.row
            self.worksheet.update_cell(row, 36, status)  # Status column
            self.worksheet.update_cell(row, 37, notes)   # Notes column
            
            print(f"✅ Updated application status for {email} to {status}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating application status: {e}")
            return False
    
    def get_application_stats(self) -> Dict[str, Any]:
        """Get application statistics"""
        try:
            records = self.get_applications()
            
            stats = {
                'total_applications': len(records),
                'by_specialization': {},
                'by_status': {},
                'by_term': {},
                'by_format': {}
            }
            
            for record in records:
                # Count by specialization
                spec = record.get('Specialization', 'Unknown')
                stats['by_specialization'][spec] = stats['by_specialization'].get(spec, 0) + 1
                
                # Count by status
                status = record.get('Status', 'Unknown')
                stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
                
                # Count by term
                term = record.get('Start Term', 'Unknown')
                stats['by_term'][term] = stats['by_term'].get(term, 0) + 1
                
                # Count by format
                format_type = record.get('Program Format', 'Unknown')
                stats['by_format'][format_type] = stats['by_format'].get(format_type, 0) + 1
            
            return stats
            
        except Exception as e:
            print(f"❌ Error getting application stats: {e}")
            return {}
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export applications to CSV file"""
        try:
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'msai_applications_{timestamp}.csv'
            
            records = self.get_applications()
            
            if not records:
                print("❌ No applications to export")
                return None
            
            # Write to CSV
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = records[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)
            
            print(f"✅ Exported {len(records)} applications to {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error exporting to CSV: {e}")
            return None

def main():
    """Main function to test the Google Sheets integration"""
    print("🚀 MSAI Application Google Sheets Integration")
    print("=" * 50)
    
    # Initialize the integration
    sheets_integration = MSAIApplicationSheets()
    
    # Authenticate
    if not sheets_integration.authenticate():
        return
    
    # Create spreadsheet
    spreadsheet = sheets_integration.create_spreadsheet("MSAI Applications 2024")
    if not spreadsheet:
        return
    
    # Setup worksheet
    if not sheets_integration.setup_worksheet("Applications"):
        return
    
    # Test with sample data
    sample_application = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+1-555-0123',
        'dateOfBirth': '1995-06-15',
        'gender': 'Male',
        'address': '123 Main St, Anytown, ST 12345',
        'undergraduateDegree': 'Bachelor of Science in Computer Science',
        'undergraduateGPA': '3.75',
        'undergraduateInstitution': 'University of Example',
        'graduationYear': '2017',
        'specialization': 'Machine Learning & Data Science',
        'startTerm': 'Fall 2024',
        'programFormat': 'Full-time',
        'interests': 'Machine Learning, Natural Language Processing',
        'statementOfPurpose': 'I am passionate about AI and want to advance my career...',
        'reference1Name': 'Dr. Jane Smith',
        'reference1Email': 'jane.smith@university.edu',
        'reference1Relationship': 'Professor',
        'reference2Name': 'Mr. Bob Johnson',
        'reference2Email': 'bob.johnson@company.com',
        'reference2Relationship': 'Supervisor',
        'agreeTerms': True,
        'agreeMarketing': True
    }
    
    # Submit sample application
    if sheets_integration.submit_application(sample_application):
        print("✅ Sample application submitted successfully")
    
    # Get statistics
    stats = sheets_integration.get_application_stats()
    print(f"\n📊 Application Statistics:")
    print(f"   Total Applications: {stats.get('total_applications', 0)}")
    print(f"   By Specialization: {stats.get('by_specialization', {})}")
    print(f"   By Status: {stats.get('by_status', {})}")
    
    # Export to CSV
    csv_file = sheets_integration.export_to_csv()
    if csv_file:
        print(f"📄 Applications exported to: {csv_file}")
    
    print(f"\n🔗 Spreadsheet URL: https://docs.google.com/spreadsheets/d/{sheets_integration.sheet_id}")
    print("✅ Google Sheets integration setup complete!")

if __name__ == "__main__":
    main()