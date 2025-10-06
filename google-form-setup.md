# MS AI Google Form Setup Guide

## Step 1: Create Google Form

### Form Title
**MS AI Program Application - AURNOVA University**

### Form Settings
- **Collect email addresses**: Yes
- **Limit to 1 response**: Yes
- **Show progress bar**: Yes
- **Shuffle question order**: No
- **Confirmation message**: "Thank you for your application to the MS AI program! We will review your application and contact you within 2-3 weeks."

## Step 2: Form Sections and Questions

### Section 1: Personal Information
1. **Full Name** (Short answer, Required)
2. **Email Address** (Short answer, Required, Email validation)
3. **Phone Number** (Short answer, Required)
4. **Date of Birth** (Date, Required)
5. **Gender** (Multiple choice, Required)
   - Male
   - Female
   - Non-binary
   - Prefer not to say
6. **Mailing Address** (Paragraph, Required)

### Section 2: Academic Information
7. **Undergraduate Degree** (Short answer, Required)
8. **Institution** (Short answer, Required)
9. **GPA** (Short answer, Required, Number validation 0-4)
10. **Graduation Year** (Short answer, Required, Number validation)
11. **Class Rank** (Short answer, Optional)
12. **Relevant Coursework** (Paragraph, Required)
13. **Research Experience and Publications** (Paragraph, Required)
14. **Academic Honors and Awards** (Paragraph, Optional)

### Section 3: Graduate School Preparation
15. **Prerequisite Coursework Completed** (Checkboxes, Required)
    - Calculus (I, II, III)
    - Linear Algebra
    - Statistics and Probability
    - Programming (Python, Java, C++)
    - Data Structures and Algorithms
    - Machine Learning or AI
    - Database Systems
    - Computer Science Fundamentals
16. **Programming Languages Proficiency** (Paragraph, Required)
17. **Technical Skills and Tools** (Paragraph, Required)

### Section 4: Standardized Test Scores
18. **GRE Verbal Score** (Short answer, Optional, Number validation 130-170)
19. **GRE Quantitative Score** (Short answer, Optional, Number validation 130-170)
20. **GRE Writing Score** (Short answer, Optional, Number validation 0-6)
21. **TOEFL Total Score** (Short answer, Optional, Number validation 0-120)
22. **IELTS Overall Score** (Short answer, Optional, Number validation 0-9)
23. **English Proficiency** (Multiple choice, Required)
    - Native Speaker
    - TOEFL Score
    - IELTS Score
    - Duolingo English Test
    - Other
24. **Test Date** (Date, Optional)

### Section 5: Essays and Statements
25. **Statement of Purpose** (Paragraph, Required)
    - Description: "Please address your academic background, research interests, career goals, and why you chose AURNOVA University (750-1000 words)"
26. **Personal Statement** (Paragraph, Required)
    - Description: "Tell us about yourself beyond academic achievements, including personal experiences, challenges overcome, and unique perspectives (500-750 words)"
27. **Research Interests and Potential Thesis Topics** (Paragraph, Required)
    - Description: "Describe specific AI subfields that interest you, current research trends, and potential thesis topics (300-500 words)"
28. **Career Goals and Professional Development** (Paragraph, Required)
    - Description: "Describe your short-term and long-term career aspirations, specific roles/companies of interest, and how this program will help (300-500 words)"
29. **Diversity and Inclusion Statement** (Paragraph, Optional)
    - Description: "How will you contribute to diversity and inclusion in our program and the broader AI community? (200-400 words)"

### Section 6: Professional Experience
30. **Current Employment Status** (Multiple choice, Required)
    - Full-time employed
    - Part-time employed
    - Student
    - Unemployed
    - Other
31. **Work Experience** (Paragraph, Required)
32. **Notable Projects** (Paragraph, Optional)

### Section 7: References
33. **Reference 1 - Name** (Short answer, Required)
34. **Reference 1 - Title/Position** (Short answer, Required)
35. **Reference 1 - Institution/Organization** (Short answer, Required)
36. **Reference 1 - Email** (Short answer, Required, Email validation)
37. **Reference 1 - Phone** (Short answer, Optional)
38. **Reference 1 - Relationship** (Short answer, Required)
39. **Reference 2 - Name** (Short answer, Required)
40. **Reference 2 - Title/Position** (Short answer, Required)
41. **Reference 2 - Institution/Organization** (Short answer, Required)
42. **Reference 2 - Email** (Short answer, Required, Email validation)
43. **Reference 2 - Phone** (Short answer, Optional)
44. **Reference 2 - Relationship** (Short answer, Required)
45. **Reference 3 - Name** (Short answer, Optional)
46. **Reference 3 - Title/Position** (Short answer, Optional)
47. **Reference 3 - Institution/Organization** (Short answer, Optional)
48. **Reference 3 - Email** (Short answer, Optional, Email validation)
49. **Reference 3 - Phone** (Short answer, Optional)
50. **Reference 3 - Relationship** (Short answer, Optional)

### Section 8: Additional Information
51. **Honors, Awards, and Recognition** (Paragraph, Optional)
52. **Extracurricular Activities and Leadership** (Paragraph, Optional)
53. **Additional Information** (Paragraph, Optional)

## Step 3: Google Sheet Setup

### Sheet Columns (Auto-generated from form responses)
The Google Sheet will automatically create columns for each form question. Here are the key columns to expect:

**Personal Info:**
- Timestamp
- Full Name
- Email Address
- Phone Number
- Date of Birth
- Gender
- Mailing Address

**Academic Info:**
- Undergraduate Degree
- Institution
- GPA
- Graduation Year
- Class Rank
- Relevant Coursework
- Research Experience and Publications
- Academic Honors and Awards

**Prerequisites:**
- Prerequisite Coursework Completed (comma-separated list)

**Test Scores:**
- GRE Verbal Score
- GRE Quantitative Score
- GRE Writing Score
- TOEFL Total Score
- IELTS Overall Score
- English Proficiency
- Test Date

**Essays:**
- Statement of Purpose
- Personal Statement
- Research Interests and Potential Thesis Topics
- Career Goals and Professional Development
- Diversity and Inclusion Statement

**Professional:**
- Current Employment Status
- Work Experience
- Notable Projects

**References:**
- Reference 1 - Name through Reference 3 - Relationship

**Additional:**
- Honors, Awards, and Recognition
- Extracurricular Activities and Leadership
- Additional Information

### Sheet Formatting Recommendations
1. **Freeze header row** (View > Freeze > 1 row)
2. **Auto-resize columns** (Format > Auto-fit column width)
3. **Add data validation** for key fields
4. **Create filters** for easy sorting and searching
5. **Add conditional formatting** for status tracking

## Step 4: Form Customization

### Theme and Branding
- **Header image**: Upload MS AI program logo
- **Color scheme**: Blue and white to match university branding
- **Font**: Default Google Fonts

### Response Settings
- **Collect email addresses**: Yes
- **Send confirmation email**: Yes
- **Response receipts**: Yes
- **Edit after submit**: No
- **View summary charts**: Yes

## Step 5: Testing and Launch

### Pre-Launch Checklist
- [ ] Test form with sample data
- [ ] Verify all required fields work
- [ ] Check email notifications
- [ ] Test Google Sheet data collection
- [ ] Verify mobile responsiveness
- [ ] Update website links

### Launch Steps
1. Publish the form
2. Copy the form URL
3. Update website to redirect to Google Form
4. Test the complete flow
5. Monitor initial submissions

## Step 6: Maintenance

### Regular Tasks
- Monitor form responses
- Check for spam submissions
- Update form questions as needed
- Backup Google Sheet data
- Review and improve form based on user feedback

### Data Management
- Export data regularly
- Create backup copies
- Set up automated reports
- Implement data validation rules