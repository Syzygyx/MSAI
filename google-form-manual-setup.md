# MS AI Google Form - Manual Setup Guide

Since the Google Forms API requires special permissions, here's a step-by-step manual setup guide:

## 🚀 Quick Setup (5 minutes)

### Step 1: Create the Google Form
1. Go to [forms.google.com](https://forms.google.com)
2. Click **"+ Blank"** to create a new form
3. Title: **"MS AI Program Application - AURNOVA University"**
4. Description: **"Thank you for your interest in the Master of Science in Artificial Intelligence program at AURNOVA University. This application form will help us evaluate your qualifications and fit for our program."**

### Step 2: Add Form Sections

#### Section 1: Personal Information
- **Full Name** (Short answer, Required)
- **Email Address** (Short answer, Required, Email validation)
- **Phone Number** (Short answer, Required)
- **Date of Birth** (Date, Required)
- **Gender** (Multiple choice, Required)
  - Male, Female, Non-binary, Prefer not to say
- **Mailing Address** (Paragraph, Required)

#### Section 2: Academic Information
- **Undergraduate Degree** (Short answer, Required)
- **Institution** (Short answer, Required)
- **GPA** (Short answer, Required)
- **Graduation Year** (Short answer, Required)
- **Class Rank** (Short answer, Optional)
- **Relevant Coursework** (Paragraph, Required)
- **Research Experience and Publications** (Paragraph, Required)
- **Academic Honors and Awards** (Paragraph, Optional)

#### Section 3: Prerequisites
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

#### Section 4: Test Scores
- **GRE Verbal Score** (Short answer, Optional)
- **GRE Quantitative Score** (Short answer, Optional)
- **GRE Writing Score** (Short answer, Optional)
- **TOEFL Total Score** (Short answer, Optional)
- **IELTS Overall Score** (Short answer, Optional)
- **English Proficiency** (Multiple choice, Required)
  - Native Speaker, TOEFL Score, IELTS Score, Duolingo English Test, Other
- **Test Date** (Date, Optional)

#### Section 5: Essays
- **Statement of Purpose** (Paragraph, Required)
  - Description: "Please address your academic background, research interests, career goals, and why you chose AURNOVA University (750-1000 words)"
- **Personal Statement** (Paragraph, Required)
  - Description: "Tell us about yourself beyond academic achievements (500-750 words)"
- **Research Interests** (Paragraph, Required)
  - Description: "Describe your research interests in AI and potential thesis topics (300-500 words)"
- **Career Goals** (Paragraph, Required)
  - Description: "Describe your short-term and long-term career aspirations (300-500 words)"
- **Diversity Statement** (Paragraph, Optional)
  - Description: "How will you contribute to diversity and inclusion in our program? (200-400 words)"

#### Section 6: Professional Experience
- **Current Employment Status** (Multiple choice, Required)
  - Full-time employed, Part-time employed, Student, Unemployed, Other
- **Work Experience** (Paragraph, Required)
- **Notable Projects** (Paragraph, Optional)

#### Section 7: References
- **Reference 1 - Name** (Short answer, Required)
- **Reference 1 - Title/Position** (Short answer, Required)
- **Reference 1 - Institution** (Short answer, Required)
- **Reference 1 - Email** (Short answer, Required, Email validation)
- **Reference 1 - Phone** (Short answer, Optional)
- **Reference 1 - Relationship** (Short answer, Required)
- **Reference 2 - Name** (Short answer, Required)
- **Reference 2 - Title/Position** (Short answer, Required)
- **Reference 2 - Institution** (Short answer, Required)
- **Reference 2 - Email** (Short answer, Required, Email validation)
- **Reference 2 - Phone** (Short answer, Optional)
- **Reference 2 - Relationship** (Short answer, Required)
- **Reference 3 - Name** (Short answer, Optional)
- **Reference 3 - Title/Position** (Short answer, Optional)
- **Reference 3 - Institution** (Short answer, Optional)
- **Reference 3 - Email** (Short answer, Optional, Email validation)
- **Reference 3 - Phone** (Short answer, Optional)
- **Reference 3 - Relationship** (Short answer, Optional)

#### Section 8: Additional Information
- **Honors and Awards** (Paragraph, Optional)
- **Extracurricular Activities** (Paragraph, Optional)
- **Additional Information** (Paragraph, Optional)

### Step 3: Form Settings
1. Click the **Settings** gear icon
2. **General** tab:
   - ✅ Collect email addresses
   - ✅ Limit to 1 response per person
   - ✅ Show progress bar
   - ❌ Shuffle question order
3. **Presentation** tab:
   - ✅ Show link to submit another response
   - ✅ Confirmation message: "Thank you for your application to the MS AI program! We will review your application and contact you within 2-3 weeks."

### Step 4: Customize Appearance
1. Click the **Palette** icon
2. Choose colors that match your university branding
3. Add a header image if desired

### Step 5: Test the Form
1. Click **Preview** to test the form
2. Fill out a test submission
3. Check that all validations work correctly

### Step 6: Publish and Get Links
1. Click **Send** button
2. Copy the **Form URL** (this is what you'll use on your website)
3. Click **Responses** tab to see the linked Google Sheet

### Step 7: Google Sheet Setup
1. The responses will automatically go to a Google Sheet
2. **Freeze the header row** (View > Freeze > 1 row)
3. **Auto-resize columns** (Format > Auto-fit column width)
4. **Add filters** for easy sorting (Data > Create a filter)

## 🔗 Update Your Website

Once you have the Google Form URL, update your website:

1. Replace `https://forms.google.com` in your website files with your actual form URL
2. Test the complete flow from your website to the form
3. Verify that responses are being collected in the Google Sheet

## 📊 Form URL Format

Your Google Form URL will look like:
```
https://docs.google.com/forms/d/e/[FORM_ID]/viewform
```

## ✅ Benefits of This Approach

- **No API permissions needed** - Uses standard Google Forms interface
- **Full control** - You can customize everything manually
- **Easy maintenance** - Simple to update and manage
- **Automatic data collection** - Responses go directly to Google Sheets
- **Mobile optimized** - Works perfectly on all devices
- **Email notifications** - Automatic confirmations and receipts

## 🎯 Next Steps

1. Create the form using this guide
2. Test it thoroughly
3. Update your website with the form URL
4. Monitor responses in the Google Sheet
5. Set up any additional automation as needed

This approach gives you all the benefits of Google Forms without the complexity of API setup!