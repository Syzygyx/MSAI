#!/usr/bin/env python3
"""
Enhanced Google Form Creator Runner
Main script to run the enhanced Google Form creator with all features
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_google_form_creator import GoogleFormCreator
from form_validator import FormValidator
from form_analytics import FormAnalytics

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('google_form_creator.log'),
            logging.StreamHandler()
        ]
    )

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'google.oauth2',
        'googleapiclient',
        'pandas',
        'matplotlib',
        'seaborn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_credentials():
    """Check if authentication credentials are available"""
    service_account_file = "msai-service-key.json"
    oauth_credentials_file = "credentials.json"
    
    if os.path.exists(service_account_file):
        print(f"✅ Service account credentials found: {service_account_file}")
        return "service_account"
    elif os.path.exists(oauth_credentials_file):
        print(f"✅ OAuth credentials found: {oauth_credentials_file}")
        return "oauth"
    else:
        print("❌ No authentication credentials found")
        print("\n📋 Setup instructions:")
        print("1. For service account: Download JSON key from Google Cloud Console")
        print("2. For OAuth: Download OAuth client credentials from Google Cloud Console")
        print("3. Save as 'msai-service-key.json' or 'credentials.json'")
        return None

def create_sample_responses():
    """Create sample response data for testing"""
    sample_responses = [
        {
            "Timestamp": "2024-01-15 10:30:00",
            "Full Name": "John Doe",
            "Email Address": "john.doe@example.com",
            "Phone Number": "+1234567890",
            "Date of Birth": "1995-06-15",
            "Gender": "Male",
            "Mailing Address": "123 Main St, Anytown, ST 12345, USA",
            "Undergraduate Degree": "Bachelor of Science in Computer Science",
            "Institution": "State University",
            "GPA": "3.5",
            "Graduation Year": "2017",
            "Class Rank": "Top 15%",
            "Relevant Coursework": "Data Structures, Algorithms, Machine Learning, Statistics, Linear Algebra",
            "Research Experience and Publications": "Undergraduate research in computer vision, 2 conference papers",
            "Academic Honors and Awards": "Dean's List, Computer Science Honor Society",
            "Prerequisite Coursework Completed": "Calculus (I, II, III), Linear Algebra, Statistics and Probability, Programming (Python, Java, C++), Data Structures and Algorithms, Machine Learning or AI",
            "Programming Languages Proficiency": "Python (Advanced), Java (Intermediate), C++ (Intermediate), JavaScript (Beginner)",
            "Technical Skills and Tools": "TensorFlow, PyTorch, AWS, Git, Docker, Kubernetes",
            "GRE Verbal Score": "155",
            "GRE Quantitative Score": "165",
            "GRE Writing Score": "4.5",
            "English Proficiency": "Native Speaker",
            "Test Date": "2023-10-15",
            "Statement of Purpose (750-1000 words)": "I am passionate about artificial intelligence and machine learning. " * 100,
            "Personal Statement (500-750 words)": "My journey in computer science began in high school. " * 50,
            "Research Interests and Potential Thesis Topics (300-500 words)": "I am particularly interested in computer vision and natural language processing. " * 30,
            "Career Goals and Professional Development (300-500 words)": "My goal is to become a research scientist in AI. " * 30,
            "Current Employment Status": "Full-time employed",
            "Work Experience": "Software Engineer at Tech Corp for 3 years",
            "Notable Projects": "Open source contributions to TensorFlow, personal ML projects on GitHub",
            "Reference 1 - Name": "Dr. Jane Smith",
            "Reference 1 - Title/Position": "Professor of Computer Science",
            "Reference 1 - Institution/Organization": "State University",
            "Reference 1 - Email": "jane.smith@university.edu",
            "Reference 1 - Phone": "+1234567891",
            "Reference 1 - Relationship": "Academic Advisor",
            "Reference 2 - Name": "Mike Johnson",
            "Reference 2 - Title/Position": "Senior Software Engineer",
            "Reference 2 - Institution/Organization": "Tech Corp",
            "Reference 2 - Email": "mike.johnson@techcorp.com",
            "Reference 2 - Phone": "+1234567892",
            "Reference 2 - Relationship": "Direct Supervisor",
            "Honors, Awards, and Recognition": "Employee of the Year 2023, Hackathon Winner",
            "Extracurricular Activities and Leadership": "Volunteer coding instructor, Tech meetup organizer",
            "Additional Information": "Veteran, first-generation college graduate"
        },
        {
            "Timestamp": "2024-01-16 14:20:00",
            "Full Name": "Jane Smith",
            "Email Address": "jane.smith@example.com",
            "Phone Number": "+1987654321",
            "Date of Birth": "1998-03-22",
            "Gender": "Female",
            "Mailing Address": "456 Oak Ave, Another City, ST 54321, USA",
            "Undergraduate Degree": "Bachelor of Science in Mathematics",
            "Institution": "Private University",
            "GPA": "3.8",
            "Graduation Year": "2020",
            "Class Rank": "Top 10%",
            "Relevant Coursework": "Calculus I-III, Linear Algebra, Statistics, Probability, Numerical Analysis, Machine Learning",
            "Research Experience and Publications": "Undergraduate research in optimization algorithms, 1 journal paper",
            "Academic Honors and Awards": "Summa Cum Laude, Phi Beta Kappa, Mathematics Honor Society",
            "Prerequisite Coursework Completed": "Calculus (I, II, III), Linear Algebra, Statistics and Probability, Programming (Python, Java, C++), Data Structures and Algorithms, Machine Learning or AI, Computer Science Fundamentals",
            "Programming Languages Proficiency": "Python (Advanced), R (Advanced), MATLAB (Intermediate), Julia (Beginner)",
            "Technical Skills and Tools": "Scikit-learn, Pandas, NumPy, Jupyter, LaTeX, Git",
            "GRE Verbal Score": "160",
            "GRE Quantitative Score": "170",
            "GRE Writing Score": "5.0",
            "English Proficiency": "Native Speaker",
            "Test Date": "2023-09-20",
            "Statement of Purpose (750-1000 words)": "My mathematical background provides a strong foundation for AI research. " * 100,
            "Personal Statement (500-750 words)": "As a woman in STEM, I am passionate about diversity in AI. " * 50,
            "Research Interests and Potential Thesis Topics (300-500 words)": "I am interested in optimization methods for machine learning. " * 30,
            "Career Goals and Professional Development (300-500 words)": "I want to work on AI safety and ethics research. " * 30,
            "Diversity and Inclusion Statement (Optional, 200-400 words)": "I am committed to promoting diversity in AI and technology. " * 20,
            "Current Employment Status": "Student",
            "Work Experience": "Research Assistant at Private University for 2 years",
            "Notable Projects": "Open source optimization library, AI ethics blog",
            "Reference 1 - Name": "Dr. Robert Brown",
            "Reference 1 - Title/Position": "Professor of Mathematics",
            "Reference 1 - Institution/Organization": "Private University",
            "Reference 1 - Email": "robert.brown@university.edu",
            "Reference 1 - Phone": "+1987654322",
            "Reference 1 - Relationship": "Research Advisor",
            "Reference 2 - Name": "Dr. Sarah Wilson",
            "Reference 2 - Title/Position": "Assistant Professor of Computer Science",
            "Reference 2 - Institution/Organization": "Private University",
            "Reference 2 - Email": "sarah.wilson@university.edu",
            "Reference 2 - Phone": "+1987654323",
            "Reference 2 - Relationship": "Course Instructor",
            "Honors, Awards, and Recognition": "National Merit Scholar, Goldwater Scholarship",
            "Extracurricular Activities and Leadership": "Women in STEM President, Math Club Treasurer",
            "Additional Information": "International student, fluent in Spanish and French"
        }
    ]
    
    with open("form_responses.json", "w") as f:
        json.dump(sample_responses, f, indent=2)
    
    print("✅ Sample response data created: form_responses.json")

def run_form_creator():
    """Run the enhanced Google Form creator"""
    print("🚀 Starting Enhanced Google Form Creator")
    print("=" * 50)
    
    # Initialize creator
    creator = GoogleFormCreator()
    
    # Try authentication
    auth_method = check_credentials()
    if not auth_method:
        return False
    
    # Authenticate
    if auth_method == "service_account":
        if not creator.authenticate_service_account():
            print("❌ Service account authentication failed")
            return False
    else:
        if not creator.authenticate_oauth():
            print("❌ OAuth authentication failed")
            return False
    
    # Create the form
    print("\n📝 Creating Google Form...")
    form_data = creator.create_form()
    
    if form_data:
        print(f"\n🎉 Form created successfully!")
        print(f"📝 Form ID: {form_data['formId']}")
        print(f"🔗 Form URL: {form_data['responderUri']}")
        
        # Create linked sheet
        print("\n📊 Creating linked Google Sheet...")
        sheet_id = creator.create_linked_sheet()
        if sheet_id:
            print(f"📊 Linked Sheet ID: {sheet_id}")
            form_data['linkedSheetId'] = sheet_id
        
        # Save form details
        creator.save_form_details(form_data)
        
        return True
    else:
        print("\n❌ Form creation failed")
        return False

def run_validation_demo():
    """Run form validation demo"""
    print("\n🔍 Running Form Validation Demo")
    print("=" * 40)
    
    # Create sample data if it doesn't exist
    if not os.path.exists("form_responses.json"):
        create_sample_responses()
    
    # Load sample response
    with open("form_responses.json", "r") as f:
        responses = json.load(f)
    
    # Validate first response
    validator = FormValidator()
    result = validator.validate_response(responses[0])
    
    print(f"Validation Result:")
    print(f"Valid: {result.is_valid}")
    print(f"Score: {result.score}/100")
    print(f"Errors: {len(result.errors)}")
    print(f"Warnings: {len(result.warnings)}")
    
    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")
    
    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  - {warning}")

def run_analytics_demo():
    """Run analytics demo"""
    print("\n📊 Running Analytics Demo")
    print("=" * 30)
    
    # Create sample data if it doesn't exist
    if not os.path.exists("form_responses.json"):
        create_sample_responses()
    
    # Run analytics
    analytics = FormAnalytics()
    
    # Get summary stats
    stats = analytics.get_summary_stats()
    print(f"Total responses: {stats['total_responses']}")
    
    if stats.get("average_gpa"):
        print(f"Average GPA: {stats['average_gpa']:.2f}")
    
    # Get insights
    insights = analytics.generate_insights()
    print(f"\nInsights:")
    for insight in insights:
        print(f"  - {insight}")
    
    # Create visualizations
    print("\n📈 Creating visualizations...")
    analytics.create_visualizations()
    print("Visualizations saved to analytics_plots/")

def main():
    """Main function"""
    setup_logging()
    
    print("🎯 Enhanced Google Form Creator for MS AI Application")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check credentials
    auth_method = check_credentials()
    if not auth_method:
        print("\n💡 To get started:")
        print("1. Set up Google Cloud project and enable APIs")
        print("2. Create service account or OAuth credentials")
        print("3. Download credentials file")
        print("4. Run this script again")
        return
    
    # Menu
    while True:
        print("\n📋 Choose an option:")
        print("1. Create Google Form")
        print("2. Run Validation Demo")
        print("3. Run Analytics Demo")
        print("4. Run All (Form + Validation + Analytics)")
        print("5. Setup MCP Server")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            run_form_creator()
        elif choice == "2":
            run_validation_demo()
        elif choice == "3":
            run_analytics_demo()
        elif choice == "4":
            print("\n🚀 Running Complete Demo...")
            create_sample_responses()
            run_form_creator()
            run_validation_demo()
            run_analytics_demo()
        elif choice == "5":
            print("\n🔧 MCP Server Setup")
            print("Run: ./setup_mcp_server.sh")
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()