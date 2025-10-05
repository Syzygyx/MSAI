"""
MS AI Curriculum System - Pytest Validation Tests
Automated test suite using pytest for CI/CD integration
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

# Test configuration
BASE_URL = "https://msai.syzygyx.com"
TIMEOUT = 10
EXPECTED_PROFESSORS = 4
EXPECTED_TOTAL_CREDITS = 36
MAX_RESPONSE_TIME = 2.0

@pytest.fixture
def session():
    """Create a requests session for testing"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'MSAI-Pytest-Test/1.0',
        'Accept': 'application/json'
    })
    return session

@pytest.fixture
def base_url():
    """Base URL for testing"""
    return BASE_URL

class TestDomainAndSSL:
    """Test domain resolution and SSL configuration"""
    
    def test_domain_resolution(self):
        """Test that domain resolves to an IP address"""
        try:
            ip_address = socket.gethostbyname('msai.syzygyx.com')
            assert ip_address is not None, "Domain should resolve to an IP address"
            assert len(ip_address.split('.')) == 4, "Should be a valid IPv4 address"
        except socket.gaierror as e:
            pytest.fail(f"Domain resolution failed: {e}")
    
    def test_ssl_certificate_valid(self):
        """Test SSL certificate is valid and not expired"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection(('msai.syzygyx.com', 443), timeout=TIMEOUT) as sock:
                with context.wrap_socket(sock, server_hostname='msai.syzygyx.com') as ssock:
                    cert = ssock.getpeercert()
                    assert cert is not None, "SSL certificate should exist"
                    
                    # Check certificate expiration
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.now()).days
                    assert days_until_expiry > 0, f"Certificate expired {abs(days_until_expiry)} days ago"
                    assert days_until_expiry > 30, f"Certificate expires in {days_until_expiry} days (less than 30 days)"
        except Exception as e:
            pytest.fail(f"SSL certificate test failed: {e}")
    
    def test_https_redirect(self, session, base_url):
        """Test HTTP to HTTPS redirect"""
        http_url = base_url.replace('https://', 'http://')
        response = session.get(http_url, allow_redirects=False, timeout=TIMEOUT)
        
        assert response.status_code in [301, 302, 307, 308], f"Expected redirect status code, got {response.status_code}"
        
        redirect_location = response.headers.get('Location', '')
        assert 'https://' in redirect_location, f"Should redirect to HTTPS, got: {redirect_location}"

class TestBasicConnectivity:
    """Test basic connectivity and endpoints"""
    
    def test_root_endpoint_accessible(self, session, base_url):
        """Test root endpoint is accessible"""
        response = session.get(base_url, timeout=TIMEOUT)
        
        assert response.status_code == 200, f"Root endpoint should return 200, got {response.status_code}"
        
        data = response.json()
        assert 'message' in data, "Response should contain 'message' field"
        assert 'MS AI Curriculum System' in data['message'], "Message should mention MS AI Curriculum System"
        assert 'version' in data, "Response should contain 'version' field"
        assert 'status' in data, "Response should contain 'status' field"
    
    def test_health_endpoint(self, session, base_url):
        """Test health check endpoint"""
        health_url = urljoin(base_url, '/health')
        response = session.get(health_url, timeout=TIMEOUT)
        
        assert response.status_code == 200, f"Health endpoint should return 200, got {response.status_code}"
        
        data = response.json()
        assert data['status'] == 'healthy', f"Health status should be 'healthy', got {data['status']}"
        assert 'services' in data, "Health response should contain 'services' field"
        
        services = data['services']
        expected_services = ['professors', 'curriculum', 'students']
        for service in expected_services:
            assert service in services, f"Health check should include {service} service"
    
    def test_response_times(self, session, base_url):
        """Test that endpoints respond within acceptable time"""
        endpoints = ['/', '/health', '/api/professors', '/api/curriculum', '/api/students']
        
        for endpoint in endpoints:
            url = urljoin(base_url, endpoint)
            start_time = time.time()
            response = session.get(url, timeout=TIMEOUT)
            response_time = time.time() - start_time
            
            assert response.status_code == 200, f"{endpoint} should return 200"
            assert response_time <= MAX_RESPONSE_TIME, f"{endpoint} took {response_time:.2f}s (max: {MAX_RESPONSE_TIME}s)"

class TestAPIEndpoints:
    """Test API endpoints functionality"""
    
    def test_professors_api(self, session, base_url):
        """Test AI Professors API endpoint"""
        professors_url = urljoin(base_url, '/api/professors')
        response = session.get(professors_url, timeout=TIMEOUT)
        
        assert response.status_code == 200, f"Professors API should return 200, got {response.status_code}"
        
        data = response.json()
        assert 'professors' in data, "Response should contain 'professors' field"
        
        professors = data['professors']
        assert len(professors) >= EXPECTED_PROFESSORS, f"Should have at least {EXPECTED_PROFESSORS} professors, got {len(professors)}"
        
        # Validate professor data structure
        required_fields = ['id', 'name', 'specialization', 'expertise_level', 'h_index', 'total_citations']
        for professor in professors:
            for field in required_fields:
                assert field in professor, f"Professor should have {field} field"
                assert professor[field] is not None, f"Professor {field} should not be None"
        
        # Check for specific professors
        professor_names = [p['name'] for p in professors]
        expected_names = ['Dr. Sarah Chen', 'Dr. Marcus Rodriguez', 'Dr. Aisha Patel', 'Dr. James Kim']
        for name in expected_names:
            assert name in professor_names, f"Should have professor {name}"
    
    def test_curriculum_api(self, session, base_url):
        """Test curriculum API endpoint"""
        curriculum_url = urljoin(base_url, '/api/curriculum')
        response = session.get(curriculum_url, timeout=TIMEOUT)
        
        assert response.status_code == 200, f"Curriculum API should return 200, got {response.status_code}"
        
        data = response.json()
        required_fields = ['program_name', 'total_credits', 'core_courses', 'specialization_tracks', 'accreditation_body']
        
        for field in required_fields:
            assert field in data, f"Curriculum response should contain {field} field"
        
        assert data['total_credits'] == EXPECTED_TOTAL_CREDITS, f"Should have {EXPECTED_TOTAL_CREDITS} credits, got {data['total_credits']}"
        assert data['accreditation_body'] == 'SACSCOC', f"Should be SACSCOC accredited, got {data['accreditation_body']}"
        assert data['core_courses'] >= 3, f"Should have at least 3 core courses, got {data['core_courses']}"
        assert data['specialization_tracks'] >= 3, f"Should have at least 3 specialization tracks, got {data['specialization_tracks']}"
    
    def test_students_api(self, session, base_url):
        """Test simulated students API endpoint"""
        students_url = urljoin(base_url, '/api/students')
        response = session.get(students_url, timeout=TIMEOUT)
        
        assert response.status_code == 200, f"Students API should return 200, got {response.status_code}"
        
        data = response.json()
        assert 'students' in data, "Response should contain 'students' field"
        
        students = data['students']
        assert len(students) >= 1, f"Should have at least 1 student, got {len(students)}"
        
        # Validate student data structure
        required_fields = ['id', 'name', 'learning_style', 'current_level', 'enrolled_courses']
        for student in students:
            for field in required_fields:
                assert field in student, f"Student should have {field} field"
                assert student[field] is not None, f"Student {field} should not be None"

class TestSecurity:
    """Test security features"""
    
    def test_security_headers(self, session, base_url):
        """Test that security headers are present"""
        response = session.get(base_url, timeout=TIMEOUT)
        
        headers = response.headers
        security_headers = {
            'Strict-Transport-Security': 'HSTS header for HTTPS enforcement',
            'X-Content-Type-Options': 'Content type protection',
            'X-Frame-Options': 'Clickjacking protection',
            'X-XSS-Protection': 'XSS protection'
        }
        
        missing_headers = []
        for header, description in security_headers.items():
            if header not in headers:
                missing_headers.append(f"{header} ({description})")
        
        assert len(missing_headers) == 0, f"Missing security headers: {', '.join(missing_headers)}"
    
    def test_cors_configuration(self, session, base_url):
        """Test CORS configuration"""
        headers = {
            'Origin': 'https://msai.syzygyx.com',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = session.options(base_url, headers=headers, timeout=TIMEOUT)
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        
        for header, value in cors_headers.items():
            assert value is not None, f"CORS header {header} should be present"
    
    def test_rate_limiting(self, session, base_url):
        """Test rate limiting functionality"""
        # Make multiple rapid requests to test rate limiting
        rate_limited = False
        for i in range(15):  # Make 15 requests quickly
            response = session.get(urljoin(base_url, '/api/professors'), timeout=5)
            if response.status_code == 429:  # Too Many Requests
                rate_limited = True
                break
            time.sleep(0.1)  # Small delay between requests
        
        # Rate limiting is optional but good to have
        if not rate_limited:
            pytest.skip("Rate limiting not configured (this is optional)")
    
    def test_error_handling(self, session, base_url):
        """Test error handling for invalid endpoints"""
        response = session.get(urljoin(base_url, '/nonexistent-endpoint'), timeout=TIMEOUT)
        
        assert response.status_code == 404, f"Invalid endpoint should return 404, got {response.status_code}"

class TestDocumentation:
    """Test API documentation endpoints"""
    
    def test_api_docs_accessible(self, session, base_url):
        """Test that API documentation is accessible"""
        docs_url = urljoin(base_url, '/docs')
        response = session.get(docs_url, timeout=TIMEOUT)
        
        assert response.status_code == 200, f"API docs should be accessible, got {response.status_code}"
        assert 'text/html' in response.headers.get('Content-Type', ''), "API docs should return HTML"
    
    def test_redoc_accessible(self, session, base_url):
        """Test that ReDoc documentation is accessible"""
        redoc_url = urljoin(base_url, '/redoc')
        response = session.get(redoc_url, timeout=TIMEOUT)
        
        assert response.status_code == 200, f"ReDoc should be accessible, got {response.status_code}"
        assert 'text/html' in response.headers.get('Content-Type', ''), "ReDoc should return HTML"

class TestDataIntegrity:
    """Test data integrity and consistency"""
    
    def test_professor_data_consistency(self, session, base_url):
        """Test that professor data is consistent"""
        professors_url = urljoin(base_url, '/api/professors')
        response = session.get(professors_url, timeout=TIMEOUT)
        data = response.json()
        professors = data['professors']
        
        # Check that all professors have valid expertise levels
        for professor in professors:
            expertise_level = professor['expertise_level']
            assert isinstance(expertise_level, int), "Expertise level should be an integer"
            assert 1 <= expertise_level <= 10, f"Expertise level should be 1-10, got {expertise_level}"
            
            h_index = professor['h_index']
            assert isinstance(h_index, int), "H-index should be an integer"
            assert h_index >= 0, f"H-index should be non-negative, got {h_index}"
            
            citations = professor['total_citations']
            assert isinstance(citations, int), "Total citations should be an integer"
            assert citations >= 0, f"Total citations should be non-negative, got {citations}"
    
    def test_curriculum_data_consistency(self, session, base_url):
        """Test that curriculum data is consistent"""
        curriculum_url = urljoin(base_url, '/api/curriculum')
        response = session.get(curriculum_url, timeout=TIMEOUT)
        data = response.json()
        
        # Check that total credits is reasonable
        total_credits = data['total_credits']
        assert isinstance(total_credits, int), "Total credits should be an integer"
        assert 30 <= total_credits <= 60, f"Total credits should be 30-60, got {total_credits}"
        
        # Check that core courses count is reasonable
        core_courses = data['core_courses']
        assert isinstance(core_courses, int), "Core courses should be an integer"
        assert 3 <= core_courses <= 10, f"Core courses should be 3-10, got {core_courses}"
        
        # Check that specialization tracks count is reasonable
        specialization_tracks = data['specialization_tracks']
        assert isinstance(specialization_tracks, int), "Specialization tracks should be an integer"
        assert 2 <= specialization_tracks <= 8, f"Specialization tracks should be 2-8, got {specialization_tracks}"

# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers"""
    for item in items:
        # Mark tests that make network requests as integration tests
        if "session" in item.fixturenames:
            item.add_marker(pytest.mark.integration)

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])