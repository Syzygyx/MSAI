# Google Form Creation Solution

## 🚨 Issue Identified: Drive Storage Quota Exceeded

The service account's Google Drive storage quota has been exceeded, which is preventing the creation of new Google Forms. Here are the solutions:

## Solution 1: Fix Service Account Quota (Recommended)

### Step 1: Check and Clean Up Drive Storage
```bash
# Run this to check current usage and clean up
source venv/bin/activate && python -c "
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file(
    'msai-service-key.json', 
    scopes=['https://www.googleapis.com/auth/drive.file']
)

drive_service = build('drive', 'v3', credentials=credentials)

# List all files
results = drive_service.files().list(pageSize=100, fields='files(id,name,mimeType,size)').execute()
files = results.get('files', [])

print(f'Total files: {len(files)}')
for file in files:
    print(f'- {file[\"name\"]} ({file[\"mimeType\"]}) - ID: {file[\"id\"]}')

# Delete old files if needed
# Uncomment the lines below to delete files (BE CAREFUL!)
# for file in files:
#     if 'test' in file['name'].lower() or 'old' in file['name'].lower():
#         drive_service.files().delete(fileId=file['id']).execute()
#         print(f'Deleted: {file[\"name\"]}')
"
```

### Step 2: Increase Drive Quota
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to IAM & Admin > Quotas
3. Search for "Drive API"
4. Request quota increase if needed

### Step 3: Use Different Service Account
Create a new service account with fresh quota:
1. Go to IAM & Admin > Service Accounts
2. Create new service account
3. Download new key file
4. Update the script to use the new key

## Solution 2: Use OAuth Authentication

### Step 1: Create OAuth Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to APIs & Services > Credentials
3. Click "Create Credentials" > "OAuth 2.0 Client ID"
4. Choose "Desktop Application"
5. Download the JSON file as `credentials.json`

### Step 2: Run OAuth Form Creator
```bash
source venv/bin/activate && python create_form_oauth.py
```

## Solution 3: Manual Google Form Creation (Immediate Solution)

Since you need the Google Form now, here's how to create it manually:

### Step 1: Create the Form
1. Go to [Google Forms](https://forms.google.com)
2. Click "Blank" to create a new form
3. Set title: "MS AI Program Application - AURNOVA University"

### Step 2: Add Description
```
Thank you for your interest in the Master of Science in Artificial Intelligence program at AURNOVA University. This application form will help us evaluate your qualifications and fit for our program.

For technical support, please contact: admissions@aurnova.edu
```

### Step 3: Add Questions (Use this structure)

#### Section 1: Personal Information
- **Full Name** (Short answer, Required)
- **Email Address** (Short answer, Required, Email validation)
- **Phone Number** (Short answer, Required)
- **Date of Birth** (Date, Required)
- **Gender** (Multiple choice, Required)
  - Male
  - Female
  - Non-binary
  - Prefer not to say
- **Mailing Address** (Paragraph, Required)

#### Section 2: Academic Information
- **Undergraduate Degree** (Short answer, Required)
- **Institution** (Short answer, Required)
- **GPA** (Short answer, Required, Number validation 0-4)
- **Graduation Year** (Short answer, Required, Number validation)
- **Class Rank** (Short answer, Optional)
- **Relevant Coursework** (Paragraph, Required)
- **Research Experience and Publications** (Paragraph, Required)
- **Academic Honors and Awards** (Paragraph, Optional)

#### Section 3: Graduate School Preparation
- **Prerequisite Coursework Completed** (Checkboxes, Required)
  - Calculus (I, II, III)
  - Linear Algebra
  - Statistics and Probability
  - Programming (Python, Java, C++)
  - Data Structures and Algorithms
  - Machine Learning or AI
  - Database Systems
  - Computer Science Fundamentals
- **Programming Languages Proficiency** (Paragraph, Required)
- **Technical Skills and Tools** (Paragraph, Required)

#### Section 4: Standardized Test Scores
- **GRE Verbal Score** (Short answer, Optional, Number validation 130-170)
- **GRE Quantitative Score** (Short answer, Optional, Number validation 130-170)
- **GRE Writing Score** (Short answer, Optional, Number validation 0-6)
- **TOEFL Total Score** (Short answer, Optional, Number validation 0-120)
- **IELTS Overall Score** (Short answer, Optional, Number validation 0-9)
- **English Proficiency** (Multiple choice, Required)
  - Native Speaker
  - TOEFL Score
  - IELTS Score
  - Duolingo English Test
  - Other
- **Test Date** (Date, Optional)

#### Section 5: Essays and Statements
- **Statement of Purpose (750-1000 words)** (Paragraph, Required)
- **Personal Statement (500-750 words)** (Paragraph, Required)
- **Research Interests and Potential Thesis Topics (300-500 words)** (Paragraph, Required)
- **Career Goals and Professional Development (300-500 words)** (Paragraph, Required)
- **Diversity and Inclusion Statement (Optional, 200-400 words)** (Paragraph, Optional)

#### Section 6: Professional Experience
- **Current Employment Status** (Multiple choice, Required)
  - Full-time employed
  - Part-time employed
  - Student
  - Unemployed
  - Other
- **Work Experience** (Paragraph, Required)
- **Notable Projects** (Paragraph, Optional)

#### Section 7: References
- **Reference 1 - Name** (Short answer, Required)
- **Reference 1 - Title/Position** (Short answer, Required)
- **Reference 1 - Institution/Organization** (Short answer, Required)
- **Reference 1 - Email** (Short answer, Required, Email validation)
- **Reference 1 - Phone** (Short answer, Optional)
- **Reference 1 - Relationship** (Short answer, Required)
- **Reference 2 - Name** (Short answer, Required)
- **Reference 2 - Title/Position** (Short answer, Required)
- **Reference 2 - Institution/Organization** (Short answer, Required)
- **Reference 2 - Email** (Short answer, Required, Email validation)
- **Reference 2 - Phone** (Short answer, Optional)
- **Reference 2 - Relationship** (Short answer, Required)
- **Reference 3 - Name** (Short answer, Optional)
- **Reference 3 - Title/Position** (Short answer, Optional)
- **Reference 3 - Institution/Organization** (Short answer, Optional)
- **Reference 3 - Email** (Short answer, Optional, Email validation)
- **Reference 3 - Phone** (Short answer, Optional)
- **Reference 3 - Relationship** (Short answer, Optional)

#### Section 8: Additional Information
- **Honors, Awards, and Recognition** (Paragraph, Optional)
- **Extracurricular Activities and Leadership** (Paragraph, Optional)
- **Additional Information** (Paragraph, Optional)

### Step 4: Configure Form Settings
1. Click the Settings gear icon
2. Enable "Collect email addresses"
3. Enable "Limit to 1 response per person"
4. Enable "Show progress bar"
5. Set confirmation message: "Thank you for your application to the MS AI program! We will review your application and contact you within 2-3 weeks."

### Step 5: Set Up Response Collection
1. Click "Responses" tab
2. Click "Create Spreadsheet" to link a Google Sheet
3. This will automatically collect all responses

## Solution 4: Use Google Apps Script (Advanced)

If you want to automate the form creation, you can use Google Apps Script:

1. Go to [Google Apps Script](https://script.google.com)
2. Create a new project
3. Use the Forms API to create the form programmatically
4. This bypasses the service account quota issues

## Recommended Immediate Action

**I recommend using Solution 3 (Manual Creation)** because:
1. ✅ **Immediate** - You can create the form right now
2. ✅ **No technical issues** - No API or quota problems
3. ✅ **Full control** - You can customize everything
4. ✅ **Reliable** - No dependency on external services

Once you have the manual form created, you can always come back to automate it later when the quota issues are resolved.

## Next Steps

1. **Create the form manually** using the structure above
2. **Test the form** with sample data
3. **Customize the appearance** to match your branding
4. **Set up response collection** with Google Sheets
5. **Deploy to your website** and start accepting applications

Would you like me to help you with any of these steps?