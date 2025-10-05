const { test, expect } = require('@playwright/test');

// Test configuration
const BASE_URL = 'http://msai.syzygyx.com';
const TIMEOUT = 10000;

test.describe('MS AI Curriculum System - Playwright Validation', () => {
  
  test.beforeEach(async ({ page }) => {
    // Set longer timeout for all tests
    test.setTimeout(30000);
  });

  test.describe('Basic Connectivity', () => {
    test('should load the main page', async ({ page }) => {
      await page.goto(BASE_URL);
      
      // Check if page loads successfully
      await expect(page).toHaveTitle(/MS AI Curriculum System|FastAPI/);
      
      // Check for main content
      const response = await page.request.get(BASE_URL);
      expect(response.status()).toBe(200);
      
      const data = await response.json();
      expect(data.message).toContain('MS AI Curriculum System');
      expect(data.status).toBe('success');
      expect(data.domain).toBe('msai.syzygyx.com');
    });

    test('should have working health endpoint', async ({ page }) => {
      const response = await page.request.get(`${BASE_URL}/health`);
      expect(response.status()).toBe(200);
      
      const data = await response.json();
      expect(data.status).toBe('healthy');
      expect(data.services).toBeDefined();
      expect(data.services.professors).toBe('online');
      expect(data.services.curriculum).toBe('online');
      expect(data.services.students).toBe('online');
    });

    test('should respond within acceptable time', async ({ page }) => {
      const startTime = Date.now();
      await page.goto(BASE_URL);
      const loadTime = Date.now() - startTime;
      
      // Should load within 5 seconds
      expect(loadTime).toBeLessThan(5000);
    });
  });

  test.describe('API Endpoints', () => {
    test('should have working professors API', async ({ page }) => {
      const response = await page.request.get(`${BASE_URL}/api/professors`);
      expect(response.status()).toBe(200);
      
      const data = await response.json();
      expect(data.professors).toBeDefined();
      expect(Array.isArray(data.professors)).toBe(true);
      expect(data.professors.length).toBeGreaterThan(0);
      
      // Check professor data structure
      const professor = data.professors[0];
      expect(professor.id).toBeDefined();
      expect(professor.name).toBeDefined();
      expect(professor.specialization).toBeDefined();
      expect(professor.expertise_level).toBeDefined();
    });

    test('should have working curriculum API', async ({ page }) => {
      const response = await page.request.get(`${BASE_URL}/api/curriculum`);
      expect(response.status()).toBe(200);
      
      const data = await response.json();
      expect(data.program_name).toBeDefined();
      expect(data.total_credits).toBeDefined();
      expect(data.specializations).toBeDefined();
      expect(Array.isArray(data.specializations)).toBe(true);
      expect(data.specializations.length).toBeGreaterThan(0);
    });

    test('should have working students API', async ({ page }) => {
      const response = await page.request.get(`${BASE_URL}/api/students`);
      expect(response.status()).toBe(200);
      
      const data = await response.json();
      expect(data.students).toBeDefined();
      expect(Array.isArray(data.students)).toBe(true);
      expect(data.students.length).toBeGreaterThan(0);
      
      // Check student data structure
      const student = data.students[0];
      expect(student.id).toBeDefined();
      expect(student.name).toBeDefined();
      expect(student.learning_style).toBeDefined();
      expect(student.gpa).toBeDefined();
    });
  });

  test.describe('API Documentation', () => {
    test('should have accessible API docs', async ({ page }) => {
      const response = await page.request.get(`${BASE_URL}/docs`);
      expect(response.status()).toBe(200);
      
      const contentType = response.headers()['content-type'];
      expect(contentType).toContain('text/html');
    });

    test('should have accessible ReDoc', async ({ page }) => {
      const response = await page.request.get(`${BASE_URL}/redoc`);
      expect(response.status()).toBe(200);
      
      const contentType = response.headers()['content-type'];
      expect(contentType).toContain('text/html');
    });
  });

  test.describe('Error Handling', () => {
    test('should handle 404 errors gracefully', async ({ page }) => {
      const response = await page.request.get(`${BASE_URL}/nonexistent-endpoint`);
      expect(response.status()).toBe(404);
    });

    test('should handle invalid API endpoints', async ({ page }) => {
      const response = await page.request.get(`${BASE_URL}/api/invalid`);
      expect(response.status()).toBe(404);
    });
  });

  test.describe('Response Headers', () => {
    test('should have appropriate content type headers', async ({ page }) => {
      const response = await page.request.get(BASE_URL);
      const contentType = response.headers()['content-type'];
      expect(contentType).toContain('application/json');
    });

    test('should have server headers', async ({ page }) => {
      const response = await page.request.get(BASE_URL);
      const server = response.headers()['server'];
      expect(server).toBeDefined();
    });
  });

  test.describe('Performance Tests', () => {
    test('should handle multiple concurrent requests', async ({ page }) => {
      const promises = [];
      
      // Make 10 concurrent requests
      for (let i = 0; i < 10; i++) {
        promises.push(page.request.get(`${BASE_URL}/health`));
      }
      
      const responses = await Promise.all(promises);
      
      // All requests should succeed
      responses.forEach(response => {
        expect(response.status()).toBe(200);
      });
    });

    test('should maintain performance under load', async ({ page }) => {
      const startTime = Date.now();
      const requests = [];
      
      // Make 20 rapid requests
      for (let i = 0; i < 20; i++) {
        requests.push(page.request.get(`${BASE_URL}/api/professors`));
      }
      
      const responses = await Promise.all(requests);
      const totalTime = Date.now() - startTime;
      
      // All requests should succeed
      responses.forEach(response => {
        expect(response.status()).toBe(200);
      });
      
      // Should complete within reasonable time (10 seconds for 20 requests)
      expect(totalTime).toBeLessThan(10000);
    });
  });

  test.describe('Data Validation', () => {
    test('should return consistent professor data', async ({ page }) => {
      const response1 = await page.request.get(`${BASE_URL}/api/professors`);
      const response2 = await page.request.get(`${BASE_URL}/api/professors`);
      
      const data1 = await response1.json();
      const data2 = await response2.json();
      
      expect(data1.professors.length).toBe(data2.professors.length);
      
      // Check that professor IDs are consistent
      const ids1 = data1.professors.map(p => p.id).sort();
      const ids2 = data2.professors.map(p => p.id).sort();
      expect(ids1).toEqual(ids2);
    });

    test('should return valid JSON for all endpoints', async ({ page }) => {
      const endpoints = ['/', '/health', '/api/professors', '/api/curriculum', '/api/students'];
      
      for (const endpoint of endpoints) {
        const response = await page.request.get(`${BASE_URL}${endpoint}`);
        expect(response.status()).toBe(200);
        
        const data = await response.json();
        expect(data).toBeDefined();
        expect(typeof data).toBe('object');
      }
    });
  });

  test.describe('Cross-Browser Compatibility', () => {
    test('should work in different browsers', async ({ page, browserName }) => {
      await page.goto(BASE_URL);
      
      const response = await page.request.get(BASE_URL);
      expect(response.status()).toBe(200);
      
      const data = await response.json();
      expect(data.message).toContain('MS AI Curriculum System');
      
      console.log(`✅ Test passed in ${browserName}`);
    });
  });

  test.describe('Mobile Compatibility', () => {
    test('should work on mobile viewport', async ({ page }) => {
      // Set mobile viewport
      await page.setViewportSize({ width: 375, height: 667 });
      
      await page.goto(BASE_URL);
      
      const response = await page.request.get(BASE_URL);
      expect(response.status()).toBe(200);
      
      const data = await response.json();
      expect(data.message).toContain('MS AI Curriculum System');
    });
  });

  test.describe('Network Conditions', () => {
    test('should handle slow network conditions', async ({ page, context }) => {
      // Simulate slow 3G
      await context.route('**/*', route => {
        setTimeout(() => route.continue(), 1000);
      });
      
      const startTime = Date.now();
      await page.goto(BASE_URL);
      const loadTime = Date.now() - startTime;
      
      const response = await page.request.get(BASE_URL);
      expect(response.status()).toBe(200);
      
      // Should still work even with slow network
      expect(loadTime).toBeLessThan(15000);
    });
  });
});

test.describe('MS AI Curriculum System - Visual Tests', () => {
  test('should have proper page structure', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Check if page loads without errors
    const response = await page.request.get(BASE_URL);
    expect(response.status()).toBe(200);
    
    // Check for basic page elements (if it's an HTML page)
    const title = await page.title();
    expect(title).toBeDefined();
  });

  test('should handle API documentation pages', async ({ page }) => {
    await page.goto(`${BASE_URL}/docs`);
    
    // Check if docs page loads
    const response = await page.request.get(`${BASE_URL}/docs`);
    expect(response.status()).toBe(200);
    
    // Check for documentation content
    const content = await page.content();
    expect(content).toContain('FastAPI');
  });
});