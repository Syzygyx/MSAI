#!/usr/bin/env python3
"""
Create a working Google Form using alternative methods
"""

import json
import webbrowser
import os

def create_html_form():
    """Create an HTML form that mimics Google Forms"""
    print("🔧 Creating HTML form as alternative...")
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MS AI Program Application - AURNOVA University</title>
    <style>
        body {
            font-family: 'Google Sans', Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .form-container {
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .form-header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #4285f4;
            padding-bottom: 20px;
        }
        .form-title {
            color: #1a73e8;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .form-description {
            color: #5f6368;
            font-size: 16px;
            line-height: 1.5;
        }
        .section {
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            background-color: #fafafa;
        }
        .section-title {
            color: #1a73e8;
            font-size: 20px;
            margin-bottom: 15px;
            font-weight: 500;
        }
        .question {
            margin: 20px 0;
        }
        .question-title {
            font-weight: 500;
            margin-bottom: 8px;
            color: #202124;
        }
        .question-description {
            font-size: 14px;
            color: #5f6368;
            margin-bottom: 10px;
        }
        .required {
            color: #d93025;
        }
        input[type="text"], input[type="email"], input[type="tel"], input[type="date"], textarea, select {
            width: 100%;
            padding: 12px;
            border: 1px solid #dadce0;
            border-radius: 4px;
            font-size: 16px;
            margin-bottom: 10px;
        }
        textarea {
            min-height: 100px;
            resize: vertical;
        }
        .radio-group, .checkbox-group {
            margin: 10px 0;
        }
        .radio-item, .checkbox-item {
            margin: 8px 0;
            display: flex;
            align-items: center;
        }
        input[type="radio"], input[type="checkbox"] {
            margin-right: 10px;
        }
        .submit-btn {
            background-color: #1a73e8;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 20px;
        }
        .submit-btn:hover {
            background-color: #1557b0;
        }
        .word-count {
            font-size: 12px;
            color: #5f6368;
            text-align: right;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <div class="form-header">
            <h1 class="form-title">MS AI Program Application</h1>
            <p class="form-description">
                Thank you for your interest in the Master of Science in Artificial Intelligence program at AURNOVA University. 
                This application form will help us evaluate your qualifications and fit for our program.
                <br><br>
                For technical support, please contact: admissions@aurnova.edu
            </p>
        </div>

        <form id="applicationForm">
            <!-- Personal Information Section -->
            <div class="section">
                <h2 class="section-title">Personal Information</h2>
                
                <div class="question">
                    <div class="question-title">Full Name <span class="required">*</span></div>
                    <div class="question-description">Enter your full legal name as it appears on official documents.</div>
                    <input type="text" name="fullName" required>
                </div>

                <div class="question">
                    <div class="question-title">Email Address <span class="required">*</span></div>
                    <div class="question-description">We will use this email to communicate with you about your application.</div>
                    <input type="email" name="email" required>
                </div>

                <div class="question">
                    <div class="question-title">Phone Number <span class="required">*</span></div>
                    <div class="question-description">Include country code if outside the United States.</div>
                    <input type="tel" name="phone" required>
                </div>

                <div class="question">
                    <div class="question-title">Date of Birth <span class="required">*</span></div>
                    <div class="question-description">Enter your date of birth.</div>
                    <input type="date" name="dateOfBirth" required>
                </div>

                <div class="question">
                    <div class="question-title">Gender <span class="required">*</span></div>
                    <div class="question-description">Please select your gender identity.</div>
                    <div class="radio-group">
                        <div class="radio-item">
                            <input type="radio" name="gender" value="Male" id="gender-male" required>
                            <label for="gender-male">Male</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" name="gender" value="Female" id="gender-female" required>
                            <label for="gender-female">Female</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" name="gender" value="Non-binary" id="gender-nonbinary" required>
                            <label for="gender-nonbinary">Non-binary</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" name="gender" value="Prefer not to say" id="gender-prefer-not" required>
                            <label for="gender-prefer-not">Prefer not to say</label>
                        </div>
                    </div>
                </div>

                <div class="question">
                    <div class="question-title">Mailing Address <span class="required">*</span></div>
                    <div class="question-description">Please provide your complete mailing address including street, city, state, ZIP code, and country.</div>
                    <textarea name="mailingAddress" required></textarea>
                </div>
            </div>

            <!-- Academic Information Section -->
            <div class="section">
                <h2 class="section-title">Academic Information</h2>
                
                <div class="question">
                    <div class="question-title">Undergraduate Degree <span class="required">*</span></div>
                    <div class="question-description">Enter your undergraduate degree (e.g., Bachelor of Science in Computer Science).</div>
                    <input type="text" name="undergraduateDegree" required>
                </div>

                <div class="question">
                    <div class="question-title">Institution <span class="required">*</span></div>
                    <div class="question-description">Name of the institution where you earned your undergraduate degree.</div>
                    <input type="text" name="institution" required>
                </div>

                <div class="question">
                    <div class="question-title">GPA <span class="required">*</span></div>
                    <div class="question-description">Enter your undergraduate GPA on a 4.0 scale.</div>
                    <input type="text" name="gpa" required>
                </div>

                <div class="question">
                    <div class="question-title">Graduation Year <span class="required">*</span></div>
                    <div class="question-description">Year you graduated or expect to graduate from your undergraduate program.</div>
                    <input type="text" name="graduationYear" required>
                </div>

                <div class="question">
                    <div class="question-title">Relevant Coursework <span class="required">*</span></div>
                    <div class="question-description">List courses in mathematics, computer science, statistics, AI, machine learning, etc. Include course numbers and grades if available.</div>
                    <textarea name="relevantCoursework" required></textarea>
                </div>

                <div class="question">
                    <div class="question-title">Research Experience and Publications <span class="required">*</span></div>
                    <div class="question-description">Describe any research projects, publications, conference presentations, or academic work. Include details about your role, methodology, and outcomes.</div>
                    <textarea name="researchExperience" required></textarea>
                </div>
            </div>

            <!-- Essays Section -->
            <div class="section">
                <h2 class="section-title">Essays and Statements</h2>
                
                <div class="question">
                    <div class="question-title">Statement of Purpose (750-1000 words) <span class="required">*</span></div>
                    <div class="question-description">Please address your academic background, research interests, career goals, and why you chose AURNOVA University. Be specific and provide concrete examples.</div>
                    <textarea name="statementOfPurpose" required oninput="updateWordCount(this, 'sop-count')"></textarea>
                    <div class="word-count" id="sop-count">Word count: 0</div>
                </div>

                <div class="question">
                    <div class="question-title">Personal Statement (500-750 words) <span class="required">*</span></div>
                    <div class="question-description">Tell us about yourself beyond your academic achievements, including personal experiences, challenges overcome, and unique perspectives.</div>
                    <textarea name="personalStatement" required oninput="updateWordCount(this, 'ps-count')"></textarea>
                    <div class="word-count" id="ps-count">Word count: 0</div>
                </div>

                <div class="question">
                    <div class="question-title">Research Interests and Potential Thesis Topics (300-500 words) <span class="required">*</span></div>
                    <div class="question-description">Describe your research interests in AI and potential thesis topics. Be specific about current research and cite relevant papers if possible.</div>
                    <textarea name="researchInterests" required oninput="updateWordCount(this, 'ri-count')"></textarea>
                    <div class="word-count" id="ri-count">Word count: 0</div>
                </div>

                <div class="question">
                    <div class="question-title">Career Goals and Professional Development (300-500 words) <span class="required">*</span></div>
                    <div class="question-description">Describe your short-term and long-term career aspirations, specific roles/companies of interest, and how this program will help.</div>
                    <textarea name="careerGoals" required oninput="updateWordCount(this, 'cg-count')"></textarea>
                    <div class="word-count" id="cg-count">Word count: 0</div>
                </div>
            </div>

            <!-- References Section -->
            <div class="section">
                <h2 class="section-title">References</h2>
                <p>Please provide contact information for 2-3 individuals who can speak to your academic abilities, research potential, and character. At least one should be from an academic setting.</p>
                
                <h3>Reference 1</h3>
                <div class="question">
                    <div class="question-title">Name <span class="required">*</span></div>
                    <input type="text" name="ref1Name" required>
                </div>
                <div class="question">
                    <div class="question-title">Title/Position <span class="required">*</span></div>
                    <input type="text" name="ref1Title" required>
                </div>
                <div class="question">
                    <div class="question-title">Institution/Organization <span class="required">*</span></div>
                    <input type="text" name="ref1Institution" required>
                </div>
                <div class="question">
                    <div class="question-title">Email <span class="required">*</span></div>
                    <input type="email" name="ref1Email" required>
                </div>
                <div class="question">
                    <div class="question-title">Phone</div>
                    <input type="tel" name="ref1Phone">
                </div>
                <div class="question">
                    <div class="question-title">Relationship <span class="required">*</span></div>
                    <input type="text" name="ref1Relationship" required>
                </div>

                <h3>Reference 2</h3>
                <div class="question">
                    <div class="question-title">Name <span class="required">*</span></div>
                    <input type="text" name="ref2Name" required>
                </div>
                <div class="question">
                    <div class="question-title">Title/Position <span class="required">*</span></div>
                    <input type="text" name="ref2Title" required>
                </div>
                <div class="question">
                    <div class="question-title">Institution/Organization <span class="required">*</span></div>
                    <input type="text" name="ref2Institution" required>
                </div>
                <div class="question">
                    <div class="question-title">Email <span class="required">*</span></div>
                    <input type="email" name="ref2Email" required>
                </div>
                <div class="question">
                    <div class="question-title">Phone</div>
                    <input type="tel" name="ref2Phone">
                </div>
                <div class="question">
                    <div class="question-title">Relationship <span class="required">*</span></div>
                    <input type="text" name="ref2Relationship" required>
                </div>
            </div>

            <button type="submit" class="submit-btn">Submit Application</button>
        </form>
    </div>

    <script>
        function updateWordCount(textarea, countId) {
            const text = textarea.value;
            const wordCount = text.trim().split(/\s+/).filter(word => word.length > 0).length;
            document.getElementById(countId).textContent = `Word count: ${wordCount}`;
        }

        document.getElementById('applicationForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Form submitted! In a real implementation, this would be sent to a server for processing.');
        });
    </script>
</body>
</html>'''
    
    with open('msai_application_form.html', 'w') as f:
        f.write(html_content)
    
    print("✅ HTML form created: msai_application_form.html")
    return 'msai_application_form.html'

def open_form_in_browser():
    """Open the form in the browser"""
    html_file = create_html_form()
    file_path = os.path.abspath(html_file)
    webbrowser.open(f'file://{file_path}')
    print(f"🌐 Opening form in browser: {file_path}")

def main():
    """Main function"""
    print("🚀 Creating Working MS AI Application Form")
    print("=" * 50)
    
    # Create and open the HTML form
    open_form_in_browser()
    
    print("\n✅ Form created and opened in your browser!")
    print("\n📋 What you can do with this form:")
    print("1. Use it as a working application form")
    print("2. Copy the questions to create a Google Form manually")
    print("3. Use it as a template for the programmatic Google Form")
    print("4. Customize the styling and add more questions")
    
    print(f"\n🔗 Form file: {os.path.abspath('msai_application_form.html')}")

if __name__ == "__main__":
    main()