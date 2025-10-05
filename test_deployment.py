#!/usr/bin/env python3
"""
Test Deployment Script
Tests all endpoints after deployment to ensure everything is working
"""

import requests
import json
import time
from typing import Dict, List, Tuple

class DeploymentTester:
    def __init__(self, base_url: str = "http://msai.syzygyx.com"):
        self.base_url = base_url
        self.results = []
        
    def test_endpoint(self, endpoint: str, method: str = "GET", data: dict = None) -> Tuple[bool, str, int]:
        """Test a single endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)
            else:
                return False, f"Unsupported method: {method}", 0
            
            success = response.status_code < 400
            message = f"Status: {response.status_code}"
            
            if success:
                message += " ✅"
            else:
                message += f" ❌ - {response.text[:100]}"
            
            return success, message, response.status_code
            
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}", 0
        except Exception as e:
            return False, f"Error: {str(e)}", 0
    
    def run_all_tests(self) -> Dict[str, any]:
        """Run all deployment tests"""
        print("🧪 MS AI Deployment Test Suite")
        print("=" * 50)
        
        # Test endpoints
        endpoints_to_test = [
            ("/", "GET", "Main page"),
            ("/health", "GET", "Health check"),
            ("/api", "GET", "API root"),
            ("/api/professors", "GET", "Professors API"),
            ("/api/curriculum", "GET", "Curriculum API"),
            ("/api/courses", "GET", "Courses API"),
            ("/api/tracks", "GET", "Tracks API"),
            ("/api/students", "GET", "Students API"),
            ("/api/status", "GET", "Status API"),
            ("/metrics", "GET", "Metrics API"),
            ("/docs", "GET", "API documentation"),
            ("/application", "GET", "Application form"),
            ("/apply", "GET", "Apply redirect"),
            ("/api/specializations", "GET", "Specializations API"),
            ("/api/start-terms", "GET", "Start terms API"),
            ("/api/program-formats", "GET", "Program formats API"),
        ]
        
        results = {
            "total_tests": len(endpoints_to_test),
            "passed": 0,
            "failed": 0,
            "details": []
        }
        
        for endpoint, method, description in endpoints_to_test:
            print(f"\n🔍 Testing {description}...")
            success, message, status_code = self.test_endpoint(endpoint, method)
            
            result = {
                "endpoint": endpoint,
                "description": description,
                "method": method,
                "success": success,
                "message": message,
                "status_code": status_code
            }
            
            results["details"].append(result)
            
            if success:
                results["passed"] += 1
                print(f"   ✅ {message}")
            else:
                results["failed"] += 1
                print(f"   ❌ {message}")
        
        # Test application form submission
        print(f"\n📝 Testing application form submission...")
        test_application_data = {
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "phone": "+1-555-0123",
            "specialization": "Machine Learning & Data Science",
            "startTerm": "Fall 2024",
            "programFormat": "Full-time",
            "undergraduateDegree": "Computer Science",
            "undergraduateGPA": 3.5,
            "graduationYear": 2020,
            "statementOfPurpose": "Test statement",
            "careerGoals": "Test goals",
            "agreeTerms": True
        }
        
        success, message, status_code = self.test_endpoint("/api/application", "POST", test_application_data)
        
        app_result = {
            "endpoint": "/api/application",
            "description": "Application form submission",
            "method": "POST",
            "success": success,
            "message": message,
            "status_code": status_code
        }
        
        results["details"].append(app_result)
        results["total_tests"] += 1
        
        if success:
            results["passed"] += 1
            print(f"   ✅ {message}")
        else:
            results["failed"] += 1
            print(f"   ❌ {message}")
        
        return results
    
    def print_summary(self, results: Dict[str, any]):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("📊 DEPLOYMENT TEST SUMMARY")
        print("=" * 50)
        
        print(f"Total Tests: {results['total_tests']}")
        print(f"Passed: {results['passed']} ✅")
        print(f"Failed: {results['failed']} ❌")
        
        success_rate = (results['passed'] / results['total_tests']) * 100
        print(f"Success Rate: {success_rate:.1f}%")
        
        if results['failed'] > 0:
            print("\n❌ FAILED TESTS:")
            for test in results['details']:
                if not test['success']:
                    print(f"   - {test['description']}: {test['message']}")
        
        print(f"\n🌐 Live URLs:")
        print(f"   Main Site: {self.base_url}")
        print(f"   Application Form: {self.base_url}/application")
        print(f"   API Documentation: {self.base_url}/docs")
        print(f"   Health Check: {self.base_url}/health")
        
        if success_rate >= 90:
            print("\n🎉 DEPLOYMENT SUCCESSFUL!")
        elif success_rate >= 70:
            print("\n⚠️  DEPLOYMENT PARTIALLY SUCCESSFUL")
        else:
            print("\n❌ DEPLOYMENT FAILED - NEEDS ATTENTION")
        
        return success_rate >= 90

def main():
    """Main test function"""
    print("🚀 Starting MS AI Deployment Tests...")
    
    # Wait a moment for any recent deployment to complete
    print("⏳ Waiting for deployment to stabilize...")
    time.sleep(30)
    
    tester = DeploymentTester()
    results = tester.run_all_tests()
    success = tester.print_summary(results)
    
    # Save results to file
    with open('deployment_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: deployment_test_results.json")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)