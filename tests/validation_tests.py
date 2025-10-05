"""
MS AI Curriculum System - Validation Tests
Comprehensive test suite for msai.syzygyx.com
"""

import pytest
import requests
import json
import time
from typing import Dict, List, Any
from datetime import datetime
import ssl
import socket
from urllib.parse import urljoin

class MSAIValidationSuite:
    """Comprehensive validation test suite for MS AI Curriculum System"""
    
    def __init__(self, base_url: str = "https://msai.syzygyx.com"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MSAI-Validation-Test/1.0',
            'Accept': 'application/json'
        })
        self.test_results = []
        
    def log_test(self, test_name: str, status: str, details: str = "", duration: float = 0):
        """Log test result"""
        result = {
            'test_name': test_name,
            'status': status,
            'details': details,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        if duration > 0:
            print(f"   Duration: {duration:.2f}s")
    
    def test_ssl_certificate(self) -> bool:
        """Test SSL certificate validity and configuration"""
        test_name = "SSL Certificate Validation"
        start_time = time.time()
        
        try:
            # Test SSL certificate
            context = ssl.create_default_context()
            with socket.create_connection(('msai.syzygyx.com', 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname='msai.syzygyx.com') as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check certificate validity
                    if not cert:
                        self.log_test(test_name, "FAIL", "No certificate found")
                        return False
                    
                    # Check certificate expiration
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.now()).days
                    
                    if days_until_expiry < 30:
                        self.log_test(test_name, "WARN", f"Certificate expires in {days_until_expiry} days")
                    else:
                        self.log_test(test_name, "PASS", f"Certificate valid for {days_until_expiry} days")
                    
                    duration = time.time() - start_time
                    self.log_test(test_name, "PASS", f"SSL certificate valid", duration)
                    return True
                    
        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, "FAIL", f"SSL error: {str(e)}", duration)
            return False
    
    def test_domain_resolution(self) -> bool:
        """Test domain DNS resolution"""
        test_name = "Domain DNS Resolution"
        start_time = time.time()
        
        try:
            import socket
            ip_address = socket.gethostbyname('msai.syzygyx.com')
            duration = time.time() - start_time
            
            if ip_address:
                self.log_test(test_name, "PASS", f"Domain resolves to {ip_address}", duration)
                return True
            else:
                self.log_test(test_name, "FAIL", "Domain does not resolve", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, "FAIL", f"DNS resolution error: {str(e)}", duration)
            return False
    
    def test_https_redirect(self) -> bool:
        """Test HTTP to HTTPS redirect"""
        test_name = "HTTP to HTTPS Redirect"
        start_time = time.time()
        
        try:
            http_url = self.base_url.replace('https://', 'http://')
            response = self.session.get(http_url, allow_redirects=False, timeout=10)
            duration = time.time() - start_time
            
            if response.status_code in [301, 302, 307, 308]:
                redirect_location = response.headers.get('Location', '')
                if 'https://' in redirect_location:
                    self.log_test(test_name, "PASS", f"Redirects to HTTPS", duration)
                    return True
                else:
                    self.log_test(test_name, "FAIL", f"Redirects to non-HTTPS: {redirect_location}", duration)
                    return False
            else:
                self.log_test(test_name, "FAIL", f"No redirect, status: {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, "FAIL", f"Redirect test error: {str(e)}", duration)
            return False
    
    def test_root_endpoint(self) -> bool:
        """Test root endpoint accessibility"""
        test_name = "Root Endpoint"
        start_time = time.time()
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'MS AI Curriculum System' in data['message']:
                    self.log_test(test_name, "PASS", f"Root endpoint accessible", duration)
                    return True
                else:
                    self.log_test(test_name, "FAIL", "Invalid response format", duration)
                    return False
            else:
                self.log_test(test_name, "FAIL", f"Status code: {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, "FAIL", f"Request error: {str(e)}", duration)
            return False
    
    def test_health_endpoint(self) -> bool:
        """Test health check endpoint"""
        test_name = "Health Check Endpoint"
        start_time = time.time()
        
        try:
            health_url = urljoin(self.base_url, '/health')
            response = self.session.get(health_url, timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    services = data.get('services', {})
                    self.log_test(test_name, "PASS", f"All services healthy: {list(services.keys())}", duration)
                    return True
                else:
                    self.log_test(test_name, "FAIL", f"Unhealthy status: {data.get('status')}", duration)
                    return False
            else:
                self.log_test(test_name, "FAIL", f"Status code: {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, "FAIL", f"Health check error: {str(e)}", duration)
            return False
    
    def test_api_professors(self) -> bool:
        """Test AI Professors API endpoint"""
        test_name = "AI Professors API"
        start_time = time.time()
        
        try:
            professors_url = urljoin(self.base_url, '/api/professors')
            response = self.session.get(professors_url, timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                professors = data.get('professors', [])
                
                if len(professors) >= 4:  # Expect at least 4 AI professors
                    # Validate professor data structure
                    required_fields = ['id', 'name', 'specialization', 'expertise_level', 'h_index']
                    valid_professors = 0
                    
                    for professor in professors:
                        if all(field in professor for field in required_fields):
                            valid_professors += 1
                    
                    if valid_professors == len(professors):
                        self.log_test(test_name, "PASS", f"Found {len(professors)} valid professors", duration)
                        return True
                    else:
                        self.log_test(test_name, "FAIL", f"Only {valid_professors}/{len(professors)} professors have valid data", duration)
                        return False
                else:
                    self.log_test(test_name, "FAIL", f"Expected at least 4 professors, found {len(professors)}", duration)
                    return False
            else:
                self.log_test(test_name, "FAIL", f"Status code: {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, "FAIL", f"Professors API error: {str(e)}", duration)
            return False
    
    def test_api_curriculum(self) -> bool:
        """Test curriculum API endpoint"""
        test_name = "Curriculum API"
        start_time = time.time()
        
        try:
            curriculum_url = urljoin(self.base_url, '/api/curriculum')
            response = self.session.get(curriculum_url, timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['program_name', 'total_credits', 'core_courses', 'specialization_tracks', 'accreditation_body']
                
                if all(field in data for field in required_fields):
                    if data['total_credits'] == 36 and data['accreditation_body'] == 'SACSCOC':
                        self.log_test(test_name, "PASS", f"Curriculum data valid: {data['total_credits']} credits", duration)
                        return True
                    else:
                        self.log_test(test_name, "FAIL", f"Invalid curriculum data: {data}", duration)
                        return False
                else:
                    self.log_test(test_name, "FAIL", f"Missing required fields: {required_fields}", duration)
                    return False
            else:
                self.log_test(test_name, "FAIL", f"Status code: {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, "FAIL", f"Curriculum API error: {str(e)}", duration)
            return False
    
    def test_api_students(self) -> bool:
        """Test simulated students API endpoint"""
        test_name = "Simulated Students API"
        start_time = time.time()
        
        try:
            students_url = urljoin(self.base_url, '/api/students')
            response = self.session.get(students_url, timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                students = data.get('students', [])
                
                if len(students) >= 1:  # Expect at least 1 simulated student
                    # Validate student data structure
                    required_fields = ['id', 'name', 'learning_style', 'current_level', 'enrolled_courses']
                    valid_students = 0
                    
                    for student in students:
                        if all(field in student for field in required_fields):
                            valid_students += 1
                    
                    if valid_students == len(students):
                        self.log_test(test_name, "PASS", f"Found {len(students)} valid students", duration)
                        return True
                    else:
                        self.log_test(test_name, "FAIL", f"Only {valid_students}/{len(students)} students have valid data", duration)
                        return False
                else:
                    self.log_test(test_name, "FAIL", f"Expected at least 1 student, found {len(students)}", duration)
                    return False
            else:
                self.log_test(test_name, "FAIL", f"Status code: {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, "FAIL", f"Students API error: {str(e)}", duration)
            return False
    
    def test_response_times(self) -> bool:
        """Test API response times"""
        test_name = "Response Time Performance"
        start_time = time.time()
        
        endpoints = [
            '/',
            '/health',
            '/api/professors',
            '/api/curriculum',
            '/api/students'
        ]
        
        slow_endpoints = []
        total_time = 0
        
        for endpoint in endpoints:
            try:
                url = urljoin(self.base_url, endpoint)
                response_start = time.time()
                response = self.session.get(url, timeout=10)
                response_time = time.time() - response_start
                total_time += response_time
                
                if response_time > 2.0:  # More than 2 seconds is slow
                    slow_endpoints.append(f"{endpoint}: {response_time:.2f}s")
                    
            except Exception as e:
                slow_endpoints.append(f"{endpoint}: ERROR")
        
        duration = time.time() - start_time
        avg_response_time = total_time / len(endpoints)
        
        if len(slow_endpoints) == 0:
            self.log_test(test_name, "PASS", f"All endpoints respond within 2s (avg: {avg_response_time:.2f}s)", duration)
            return True
        else:
            self.log_test(test_name, "WARN", f"Slow endpoints: {', '.join(slow_endpoints)}", duration)
            return False
    
    def test_security_headers(self) -> bool:
        """Test security headers"""
        test_name = "Security Headers"
        start_time = time.time()
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            duration = time.time() - start_time
            
            headers = response.headers
            security_headers = {
                'Strict-Transport-Security': 'HSTS header',
                'X-Content-Type-Options': 'Content type protection',
                'X-Frame-Options': 'Clickjacking protection',
                'X-XSS-Protection': 'XSS protection'
            }
            
            missing_headers = []
            present_headers = []
            
            for header, description in security_headers.items():
                if header in headers:
                    present_headers.append(f"{header}: {headers[header]}")
                else:
                    missing_headers.append(header)
            
            if len(missing_headers) == 0:
                self.log_test(test_name, "PASS", f"All security headers present", duration)
                return True
            else:
                self.log_test(test_name, "WARN", f"Missing headers: {', '.join(missing_headers)}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, "FAIL", f"Security headers test error: {str(e)}", duration)
            return False
    
    def test_cors_configuration(self) -> bool:
        """Test CORS configuration"""
        test_name = "CORS Configuration"
        start_time = time.time()
        
        try:
            # Test preflight request
            headers = {
                'Origin': 'https://msai.syzygyx.com',
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            response = self.session.options(self.base_url, headers=headers, timeout=10)
            duration = time.time() - start_time
            
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            if all(cors_headers.values()):
                self.log_test(test_name, "PASS", "CORS properly configured", duration)
                return True
            else:
                self.log_test(test_name, "WARN", f"CORS headers: {cors_headers}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, "FAIL", f"CORS test error: {str(e)}", duration)
            return False
    
    def test_rate_limiting(self) -> bool:
        """Test rate limiting functionality"""
        test_name = "Rate Limiting"
        start_time = time.time()
        
        try:
            # Make multiple rapid requests to test rate limiting
            rate_limited = False
            for i in range(15):  # Make 15 requests quickly
                response = self.session.get(urljoin(self.base_url, '/api/professors'), timeout=5)
                if response.status_code == 429:  # Too Many Requests
                    rate_limited = True
                    break
                time.sleep(0.1)  # Small delay between requests
            
            duration = time.time() - start_time
            
            if rate_limited:
                self.log_test(test_name, "PASS", "Rate limiting is working", duration)
                return True
            else:
                self.log_test(test_name, "WARN", "Rate limiting may not be configured", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, "FAIL", f"Rate limiting test error: {str(e)}", duration)
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling for invalid endpoints"""
        test_name = "Error Handling"
        start_time = time.time()
        
        try:
            # Test 404 error
            response = self.session.get(urljoin(self.base_url, '/nonexistent-endpoint'), timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 404:
                self.log_test(test_name, "PASS", "404 errors handled correctly", duration)
                return True
            else:
                self.log_test(test_name, "FAIL", f"Expected 404, got {response.status_code}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, "FAIL", f"Error handling test error: {str(e)}", duration)
            return False
    
    def test_documentation_endpoints(self) -> bool:
        """Test API documentation endpoints"""
        test_name = "API Documentation"
        start_time = time.time()
        
        doc_endpoints = ['/docs', '/redoc']
        accessible_docs = []
        
        for endpoint in doc_endpoints:
            try:
                url = urljoin(self.base_url, endpoint)
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    accessible_docs.append(endpoint)
            except:
                pass
        
        duration = time.time() - start_time
        
        if len(accessible_docs) > 0:
            self.log_test(test_name, "PASS", f"Documentation accessible: {', '.join(accessible_docs)}", duration)
            return True
        else:
            self.log_test(test_name, "FAIL", "No documentation endpoints accessible", duration)
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all validation tests"""
        print("🧪 MS AI Curriculum System - Validation Test Suite")
        print("=" * 60)
        print(f"Testing: {self.base_url}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Define test methods
        test_methods = [
            self.test_domain_resolution,
            self.test_ssl_certificate,
            self.test_https_redirect,
            self.test_root_endpoint,
            self.test_health_endpoint,
            self.test_api_professors,
            self.test_api_curriculum,
            self.test_api_students,
            self.test_response_times,
            self.test_security_headers,
            self.test_cors_configuration,
            self.test_rate_limiting,
            self.test_error_handling,
            self.test_documentation_endpoints
        ]
        
        # Run tests
        passed_tests = 0
        failed_tests = 0
        warning_tests = 0
        
        for test_method in test_methods:
            try:
                result = test_method()
                if result:
                    passed_tests += 1
                else:
                    failed_tests += 1
            except Exception as e:
                print(f"❌ {test_method.__name__}: ERROR - {str(e)}")
                failed_tests += 1
        
        # Count warnings
        for result in self.test_results:
            if result['status'] == 'WARN':
                warning_tests += 1
        
        # Generate summary
        total_tests = len(test_methods)
        print()
        print("📊 Test Summary")
        print("=" * 20)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️ Warnings: {warning_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Overall status
        if failed_tests == 0:
            overall_status = "PASS"
            status_emoji = "🎉"
        elif failed_tests <= 2:
            overall_status = "WARN"
            status_emoji = "⚠️"
        else:
            overall_status = "FAIL"
            status_emoji = "❌"
        
        print()
        print(f"{status_emoji} Overall Status: {overall_status}")
        
        # Generate detailed report
        report = {
            'base_url': self.base_url,
            'test_timestamp': datetime.now().isoformat(),
            'overall_status': overall_status,
            'summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'warnings': warning_tests,
                'success_rate': (passed_tests/total_tests)*100
            },
            'test_results': self.test_results
        }
        
        return report
    
    def save_report(self, report: Dict[str, Any], filename: str = None):
        """Save test report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"validation_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved to: {filename}")

def main():
    """Main function to run validation tests"""
    validator = MSAIValidationSuite()
    report = validator.run_all_tests()
    validator.save_report(report)
    
    # Exit with appropriate code
    if report['overall_status'] == 'FAIL':
        exit(1)
    elif report['overall_status'] == 'WARN':
        exit(2)
    else:
        exit(0)

if __name__ == "__main__":
    main()