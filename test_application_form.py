#!/usr/bin/env python3
"""
Playwright Test Suite for MS AI Application Form
This script validates the application form functionality
"""

import asyncio
from playwright.async_api import async_playwright
import json
import time

class ApplicationFormTester:
    def __init__(self):
        self.results = []
        self.base_url = "https://dcmcshan.github.io/MSAI"
        
    async def test_page_load(self, page):
        """Test if the application form page loads correctly"""
        try:
            print("🔍 Testing page load...")
            await page.goto(self.base_url)
            
            # Check if the page title is correct
            title = await page.title()
            if "MSAI Application Form" in title:
                self.results.append({"test": "Page Load", "status": "✅ PASS", "details": f"Title: {title}"})
                print("✅ Page loads correctly")
            else:
                self.results.append({"test": "Page Load", "status": "❌ FAIL", "details": f"Unexpected title: {title}"})
                print(f"❌ Page title issue: {title}")
                
        except Exception as e:
            self.results.append({"test": "Page Load", "status": "❌ FAIL", "details": f"Error: {str(e)}"})
            print(f"❌ Page load failed: {e}")
    
    async def test_form_elements(self, page):
        """Test if all form elements are present and functional"""
        try:
            print("🔍 Testing form elements...")
            
            # Check required form fields
            required_fields = [
                "firstName", "lastName", "email", "phone", 
                "specialization", "startTerm", "programFormat",
                "undergraduateDegree", "undergraduateGPA", "graduationYear",
                "statementOfPurpose", "careerGoals", "agreeTerms"
            ]
            
            missing_fields = []
            for field in required_fields:
                element = await page.query_selector(f"#{field}")
                if not element:
                    missing_fields.append(field)
            
            if not missing_fields:
                self.results.append({"test": "Form Elements", "status": "✅ PASS", "details": "All required fields present"})
                print("✅ All form elements present")
            else:
                self.results.append({"test": "Form Elements", "status": "❌ FAIL", "details": f"Missing fields: {missing_fields}"})
                print(f"❌ Missing fields: {missing_fields}")
                
        except Exception as e:
            self.results.append({"test": "Form Elements", "status": "❌ FAIL", "details": f"Error: {str(e)}"})
            print(f"❌ Form elements test failed: {e}")
    
    async def test_form_validation(self, page):
        """Test form validation functionality"""
        try:
            print("🔍 Testing form validation...")
            
            # Try to submit empty form
            submit_button = await page.query_selector("button[type='submit']")
            if submit_button:
                await submit_button.click()
                
                # Check if validation messages appear
                await page.wait_for_timeout(1000)
                
                # Check if form shows validation errors
                error_elements = await page.query_selector_all("input:invalid, select:invalid, textarea:invalid")
                
                if len(error_elements) > 0:
                    self.results.append({"test": "Form Validation", "status": "✅ PASS", "details": f"Validation working - {len(error_elements)} invalid fields"})
                    print("✅ Form validation working")
                else:
                    self.results.append({"test": "Form Validation", "status": "❌ FAIL", "details": "No validation errors shown"})
                    print("❌ Form validation not working")
            else:
                self.results.append({"test": "Form Validation", "status": "❌ FAIL", "details": "Submit button not found"})
                print("❌ Submit button not found")
                
        except Exception as e:
            self.results.append({"test": "Form Validation", "status": "❌ FAIL", "details": f"Error: {str(e)}"})
            print(f"❌ Form validation test failed: {e}")
    
    async def test_form_submission(self, page):
        """Test form submission with valid data"""
        try:
            print("🔍 Testing form submission...")
            
            # Fill out the form with valid data
            await page.fill("#firstName", "John")
            await page.fill("#lastName", "Doe")
            await page.fill("#email", "john.doe@example.com")
            await page.fill("#phone", "555-123-4567")
            await page.select_option("#specialization", "Machine Learning & Data Science")
            await page.select_option("#startTerm", "Fall 2024")
            await page.select_option("#programFormat", "Full-time")
            await page.fill("#undergraduateDegree", "Computer Science")
            await page.fill("#undergraduateGPA", "3.5")
            await page.fill("#graduationYear", "2020")
            await page.fill("#statementOfPurpose", "I am passionate about AI and want to advance my career in machine learning.")
            await page.fill("#careerGoals", "I want to become a machine learning engineer and work on cutting-edge AI projects.")
            await page.check("#agreeTerms")
            
            # Submit the form
            submit_button = await page.query_selector("button[type='submit']")
            if submit_button:
                await submit_button.click()
                
                # Wait for response
                await page.wait_for_timeout(2000)
                
                # Check for success message
                success_message = await page.query_selector("#successMessage")
                if success_message:
                    is_visible = await success_message.is_visible()
                    if is_visible:
                        self.results.append({"test": "Form Submission", "status": "✅ PASS", "details": "Form submitted successfully"})
                        print("✅ Form submission working")
                    else:
                        self.results.append({"test": "Form Submission", "status": "❌ FAIL", "details": "Success message not visible"})
                        print("❌ Success message not visible")
                else:
                    self.results.append({"test": "Form Submission", "status": "❌ FAIL", "details": "Success message element not found"})
                    print("❌ Success message element not found")
            else:
                self.results.append({"test": "Form Submission", "status": "❌ FAIL", "details": "Submit button not found"})
                print("❌ Submit button not found")
                
        except Exception as e:
            self.results.append({"test": "Form Submission", "status": "❌ FAIL", "details": f"Error: {str(e)}"})
            print(f"❌ Form submission test failed: {e}")
    
    async def test_responsive_design(self, page):
        """Test responsive design on different screen sizes"""
        try:
            print("🔍 Testing responsive design...")
            
            # Test mobile viewport
            await page.set_viewport_size({"width": 375, "height": 667})
            await page.goto(self.base_url)
            
            # Check if form is still usable on mobile
            form_container = await page.query_selector(".container")
            if form_container:
                is_visible = await form_container.is_visible()
                if is_visible:
                    self.results.append({"test": "Responsive Design", "status": "✅ PASS", "details": "Form works on mobile viewport"})
                    print("✅ Responsive design working")
                else:
                    self.results.append({"test": "Responsive Design", "status": "❌ FAIL", "details": "Form not visible on mobile"})
                    print("❌ Form not visible on mobile")
            else:
                self.results.append({"test": "Responsive Design", "status": "❌ FAIL", "details": "Form container not found"})
                print("❌ Form container not found")
                
        except Exception as e:
            self.results.append({"test": "Responsive Design", "status": "❌ FAIL", "details": f"Error: {str(e)}"})
            print(f"❌ Responsive design test failed: {e}")
    
    async def test_accessibility(self, page):
        """Test basic accessibility features"""
        try:
            print("🔍 Testing accessibility...")
            
            # Check for proper labels
            labels = await page.query_selector_all("label")
            inputs = await page.query_selector_all("input, select, textarea")
            
            if len(labels) >= len(inputs):
                self.results.append({"test": "Accessibility", "status": "✅ PASS", "details": f"Good label coverage: {len(labels)} labels for {len(inputs)} inputs"})
                print("✅ Accessibility features present")
            else:
                self.results.append({"test": "Accessibility", "status": "⚠️ WARN", "details": f"Some inputs may lack labels: {len(labels)} labels for {len(inputs)} inputs"})
                print("⚠️ Some inputs may lack labels")
                
        except Exception as e:
            self.results.append({"test": "Accessibility", "status": "❌ FAIL", "details": f"Error: {str(e)}"})
            print(f"❌ Accessibility test failed: {e}")
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting MS AI Application Form Validation")
        print("=" * 60)
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Run all tests
                await self.test_page_load(page)
                await self.test_form_elements(page)
                await self.test_form_validation(page)
                await self.test_form_submission(page)
                await self.test_responsive_design(page)
                await self.test_accessibility(page)
                
            finally:
                await browser.close()
            
            # Print results summary
            self.print_summary()
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.results if "✅ PASS" in result["status"])
        failed = sum(1 for result in self.results if "❌ FAIL" in result["status"])
        warnings = sum(1 for result in self.results if "⚠️ WARN" in result["status"])
        
        print(f"Total Tests: {len(self.results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️ Warnings: {warnings}")
        
        print("\n📋 Detailed Results:")
        for result in self.results:
            print(f"  {result['status']} {result['test']}: {result['details']}")
        
        if failed == 0:
            print("\n🎉 All tests passed! Application form is working correctly.")
        else:
            print(f"\n⚠️ {failed} test(s) failed. Please review the issues above.")
        
        # Save results to file
        with open("test_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📄 Detailed results saved to: test_results.json")

async def main():
    """Main function"""
    tester = ApplicationFormTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())