#!/usr/bin/env python3
"""
Comprehensive Site Testing with Playwright
Tests the entire MS AI website for user-friendliness, navigation, and functionality
"""

import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright

class ComprehensiveSiteTester:
    def __init__(self):
        self.results = []
        self.base_url = "http://msai.syzygyx.com"
        self.pages_to_test = [
            {"url": "/", "name": "Home Page (Python App)"},
            {"url": "/apply", "name": "Application Form"},
            {"url": "/courses", "name": "Course Catalog"},
            {"url": "/white-paper", "name": "White Paper"}
        ]
        
    async def test_page_load(self, page, page_info):
        """Test basic page loading and responsiveness"""
        try:
            print(f"🔍 Testing {page_info['name']}...")
            
            # Navigate to page
            response = await page.goto(f"{self.base_url}{page_info['url']}", 
                                     wait_until="networkidle", timeout=30000)
            
            # Check response status
            if response.status != 200:
                self.results.append({
                    "test": f"Page Load - {page_info['name']}",
                    "status": "FAIL",
                    "message": f"HTTP {response.status} - Page failed to load"
                })
                return False
            
            # Check page title
            title = await page.title()
            if not title or "404" in title.lower():
                self.results.append({
                    "test": f"Page Title - {page_info['name']}",
                    "status": "FAIL",
                    "message": f"Invalid title: {title}"
                })
                return False
            
            # Check for basic content
            content = await page.content()
            if len(content) < 1000:  # Minimum content length
                self.results.append({
                    "test": f"Content Check - {page_info['name']}",
                    "status": "FAIL",
                    "message": "Page appears to have insufficient content"
                })
                return False
            
            self.results.append({
                "test": f"Page Load - {page_info['name']}",
                "status": "PASS",
                "message": f"Page loaded successfully (Title: {title[:50]}...)"
            })
            return True
            
        except Exception as e:
            self.results.append({
                "test": f"Page Load - {page_info['name']}",
                "status": "FAIL",
                "message": f"Exception: {str(e)}"
            })
            return False

    async def test_navigation(self, page, page_info):
        """Test navigation elements and links"""
        try:
            print(f"🧭 Testing navigation on {page_info['name']}...")
            
            # Test main navigation links
            nav_links = [
                {"selector": "a[href='http://msai.syzygyx.com'], a[href='/']", "name": "Home link"},
                {"selector": "a[href*='/apply']", "name": "Apply link"},
                {"selector": "a[href*='/courses']", "name": "Courses link"},
                {"selector": "a[href*='/white-paper']", "name": "White Paper link"}
            ]
            
            for link in nav_links:
                try:
                    elements = await page.query_selector_all(link["selector"])
                    if elements:
                        # Test first link
                        href = await elements[0].get_attribute("href")
                        if href and not href.startswith("http"):
                            href = f"{self.base_url}{href}"
                        
                        # Click and test navigation
                        await elements[0].click()
                        await page.wait_for_load_state("networkidle", timeout=10000)
                        
                        # Check if we're on a valid page
                        current_url = page.url
                        if "msai.syzygyx.com" in current_url:
                            self.results.append({
                                "test": f"Navigation - {link['name']}",
                                "status": "PASS",
                                "message": f"Successfully navigated to {current_url}"
                            })
                        else:
                            self.results.append({
                                "test": f"Navigation - {link['name']}",
                                "status": "FAIL",
                                "message": f"Navigation failed - ended up at {current_url}"
                            })
                        
                        # Go back to original page
                        await page.go_back()
                        await page.wait_for_load_state("networkidle")
                    else:
                        self.results.append({
                            "test": f"Navigation - {link['name']}",
                            "status": "WARN",
                            "message": f"No {link['name']} found on page"
                        })
                except Exception as e:
                    self.results.append({
                        "test": f"Navigation - {link['name']}",
                        "status": "FAIL",
                        "message": f"Navigation error: {str(e)}"
                    })
            
        except Exception as e:
            self.results.append({
                "test": f"Navigation - {page_info['name']}",
                "status": "FAIL",
                "message": f"Navigation test failed: {str(e)}"
            })

    async def test_application_form(self, page):
        """Test the application form functionality"""
        try:
            print("📝 Testing Application Form...")
            
            # Test form elements
            form_elements = [
                {"selector": "input[name='firstName']", "name": "First Name field"},
                {"selector": "input[name='lastName']", "name": "Last Name field"},
                {"selector": "input[name='email']", "name": "Email field"},
                {"selector": "select[name='degreeLevel']", "name": "Degree Level dropdown"},
                {"selector": "select[name='specialization']", "name": "Specialization dropdown"},
                {"selector": "textarea[name='statementOfPurpose']", "name": "Statement of Purpose"},
                {"selector": "textarea[name='personalStatement']", "name": "Personal Statement"},
                {"selector": "button[type='submit']", "name": "Submit button"}
            ]
            
            # Wait for page to fully load
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(5000)
            
            # Scroll to bottom to ensure all content is loaded
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            
            # Scroll back to top
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(1000)
            
            # Take a screenshot for debugging
            await page.screenshot(path="debug_apply_page.png")
            
            # Debug: Check page content
            content = await page.content()
            input_count = content.count('input')
            form_count = content.count('form')
            
            # Log a sample of the content to see what's actually there
            sample_content = content[content.find('<body>'):content.find('<body>') + 2000] if '<body>' in content else content[:2000]
            
            # Check for JavaScript errors
            console_messages = []
            page.on("console", lambda msg: console_messages.append(f"{msg.type}: {msg.text}") if msg.type == "error" else None)
            
            self.results.append({
                "test": "Form Debug Info",
                "status": "INFO",
                "message": f"Found {input_count} input elements and {form_count} form elements on page"
            })
            
            self.results.append({
                "test": "Page Content Sample",
                "status": "INFO",
                "message": f"Page content sample: {sample_content[:200]}..."
            })
            
            if console_messages:
                self.results.append({
                    "test": "JavaScript Errors",
                    "status": "WARN",
                    "message": f"Found {len(console_messages)} JavaScript errors: {console_messages[:3]}"
                })
            
            # Check if form is visible
            form_element = await page.query_selector("form")
            if form_element:
                is_form_visible = await form_element.is_visible()
                self.results.append({
                    "test": "Form Visibility",
                    "status": "INFO",
                    "message": f"Form element found and visible: {is_form_visible}"
                })
            else:
                self.results.append({
                    "test": "Form Visibility",
                    "status": "FAIL",
                    "message": "No form element found on page"
                })
            
            for element in form_elements:
                try:
                    # Try multiple selectors
                    selectors_to_try = [
                        element["selector"],
                        f"input[name='{element['name'].split()[0].lower()}']",
                        f"#{element['name'].split()[0].lower()}",
                        f"input[id='{element['name'].split()[0].lower()}']"
                    ]
                    
                    el = None
                    for selector in selectors_to_try:
                        el = await page.query_selector(selector)
                        if el:
                            break
                    
                    if el:
                        is_visible = await el.is_visible()
                        is_enabled = await el.is_enabled()
                        
                        if is_visible and is_enabled:
                            self.results.append({
                                "test": f"Form Element - {element['name']}",
                                "status": "PASS",
                                "message": "Element is visible and enabled"
                            })
                        else:
                            self.results.append({
                                "test": f"Form Element - {element['name']}",
                                "status": "FAIL",
                                "message": f"Element not visible or enabled (visible: {is_visible}, enabled: {is_enabled})"
                            })
                    else:
                        self.results.append({
                            "test": f"Form Element - {element['name']}",
                            "status": "FAIL",
                            "message": f"Element not found with any selector: {selectors_to_try}"
                        })
                except Exception as e:
                    self.results.append({
                        "test": f"Form Element - {element['name']}",
                        "status": "FAIL",
                        "message": f"Error testing element: {str(e)}"
                    })
            
            # Test form validation
            try:
                submit_btn = await page.query_selector("button[type='submit']")
                if submit_btn:
                    await submit_btn.click()
                    await page.wait_for_timeout(2000)  # Wait for validation
                    
                    # Check for validation messages
                    error_messages = await page.query_selector_all(".error-message")
                    if error_messages:
                        self.results.append({
                            "test": "Form Validation",
                            "status": "PASS",
                            "message": "Form validation is working (error messages displayed)"
                        })
                    else:
                        self.results.append({
                            "test": "Form Validation",
                            "status": "WARN",
                            "message": "No validation messages found - may need testing"
                        })
            except Exception as e:
                self.results.append({
                    "test": "Form Validation",
                    "status": "FAIL",
                    "message": f"Form validation test failed: {str(e)}"
                })
                
        except Exception as e:
            self.results.append({
                "test": "Application Form Test",
                "status": "FAIL",
                "message": f"Application form test failed: {str(e)}"
            })

    async def test_course_catalog(self, page):
        """Test the course catalog functionality"""
        try:
            print("📚 Testing Course Catalog...")
            
            # Test course cards
            course_cards = await page.query_selector_all(".course-card")
            if course_cards:
                self.results.append({
                    "test": "Course Cards",
                    "status": "PASS",
                    "message": f"Found {len(course_cards)} course cards"
                })
                
                # Test syllabus toggles
                syllabus_buttons = await page.query_selector_all(".syllabus-toggle")
                if syllabus_buttons:
                    try:
                        # Click first syllabus button
                        await syllabus_buttons[0].click()
                        await page.wait_for_timeout(1000)
                        
                        # Check if syllabus content appeared
                        syllabus_content = await page.query_selector(".syllabus-content")
                        if syllabus_content and await syllabus_content.is_visible():
                            self.results.append({
                                "test": "Syllabus Toggle",
                                "status": "PASS",
                                "message": "Syllabus toggle functionality works"
                            })
                        else:
                            self.results.append({
                                "test": "Syllabus Toggle",
                                "status": "FAIL",
                                "message": "Syllabus content not visible after toggle"
                            })
                    except Exception as e:
                        self.results.append({
                            "test": "Syllabus Toggle",
                            "status": "FAIL",
                            "message": f"Syllabus toggle test failed: {str(e)}"
                        })
                else:
                    self.results.append({
                        "test": "Syllabus Toggle",
                        "status": "WARN",
                        "message": "No syllabus toggle buttons found"
                    })
            else:
                self.results.append({
                    "test": "Course Cards",
                    "status": "FAIL",
                    "message": "No course cards found"
                })
                
        except Exception as e:
            self.results.append({
                "test": "Course Catalog Test",
                "status": "FAIL",
                "message": f"Course catalog test failed: {str(e)}"
            })

    async def test_white_paper(self, page):
        """Test the white paper page"""
        try:
            print("📄 Testing White Paper...")
            
            # Test table of contents
            toc_links = await page.query_selector_all(".toc a")
            if toc_links:
                self.results.append({
                    "test": "Table of Contents",
                    "status": "PASS",
                    "message": f"Found {len(toc_links)} TOC links"
                })
                
                # Test TOC navigation
                try:
                    first_link = toc_links[0]
                    href = await first_link.get_attribute("href")
                    if href and href.startswith("#"):
                        await first_link.click()
                        await page.wait_for_timeout(1000)
                        
                        # Check if we scrolled to the section
                        current_url = page.url
                        if href in current_url:
                            self.results.append({
                                "test": "TOC Navigation",
                                "status": "PASS",
                                "message": "TOC navigation works correctly"
                            })
                        else:
                            self.results.append({
                                "test": "TOC Navigation",
                                "status": "WARN",
                                "message": "TOC navigation may not be working properly"
                            })
                except Exception as e:
                    self.results.append({
                        "test": "TOC Navigation",
                        "status": "FAIL",
                        "message": f"TOC navigation test failed: {str(e)}"
                    })
            else:
                self.results.append({
                    "test": "Table of Contents",
                    "status": "FAIL",
                    "message": "No TOC links found"
                })
            
            # Test sections
            sections = await page.query_selector_all(".section")
            if sections:
                self.results.append({
                    "test": "Content Sections",
                    "status": "PASS",
                    "message": f"Found {len(sections)} content sections"
                })
            else:
                self.results.append({
                    "test": "Content Sections",
                    "status": "FAIL",
                    "message": "No content sections found"
                })
                
        except Exception as e:
            self.results.append({
                "test": "White Paper Test",
                "status": "FAIL",
                "message": f"White paper test failed: {str(e)}"
            })

    async def test_responsive_design(self, page):
        """Test responsive design on different screen sizes"""
        try:
            print("📱 Testing Responsive Design...")
            
            screen_sizes = [
                {"width": 1920, "height": 1080, "name": "Desktop"},
                {"width": 1024, "height": 768, "name": "Tablet"},
                {"width": 375, "height": 667, "name": "Mobile"}
            ]
            
            for size in screen_sizes:
                try:
                    await page.set_viewport_size({"width": size["width"], "height": size["height"]})
                    await page.wait_for_timeout(1000)
                    
                    # Check if main content is visible
                    main_content = await page.query_selector(".container, .content, main")
                    if main_content:
                        is_visible = await main_content.is_visible()
                        if is_visible:
                            self.results.append({
                                "test": f"Responsive - {size['name']}",
                                "status": "PASS",
                                "message": f"Content visible on {size['name']} ({size['width']}x{size['height']})"
                            })
                        else:
                            self.results.append({
                                "test": f"Responsive - {size['name']}",
                                "status": "FAIL",
                                "message": f"Content not visible on {size['name']}"
                            })
                    else:
                        self.results.append({
                            "test": f"Responsive - {size['name']}",
                            "status": "WARN",
                            "message": f"No main content found on {size['name']}"
                        })
                        
                except Exception as e:
                    self.results.append({
                        "test": f"Responsive - {size['name']}",
                        "status": "FAIL",
                        "message": f"Responsive test failed for {size['name']}: {str(e)}"
                    })
            
            # Reset to desktop
            await page.set_viewport_size({"width": 1920, "height": 1080})
            
        except Exception as e:
            self.results.append({
                "test": "Responsive Design",
                "status": "FAIL",
                "message": f"Responsive design test failed: {str(e)}"
            })

    async def test_accessibility(self, page):
        """Test basic accessibility features"""
        try:
            print("♿ Testing Accessibility...")
            
            # Test for alt text on images
            images = await page.query_selector_all("img")
            images_with_alt = 0
            for img in images:
                alt_text = await img.get_attribute("alt")
                if alt_text:
                    images_with_alt += 1
            
            if images:
                alt_percentage = (images_with_alt / len(images)) * 100
                if alt_percentage >= 80:
                    self.results.append({
                        "test": "Image Alt Text",
                        "status": "PASS",
                        "message": f"{alt_percentage:.1f}% of images have alt text"
                    })
                else:
                    self.results.append({
                        "test": "Image Alt Text",
                        "status": "WARN",
                        "message": f"Only {alt_percentage:.1f}% of images have alt text"
                    })
            else:
                self.results.append({
                    "test": "Image Alt Text",
                    "status": "PASS",
                    "message": "No images found to test"
                })
            
            # Test for heading hierarchy
            headings = await page.query_selector_all("h1, h2, h3, h4, h5, h6")
            if headings:
                h1_count = len(await page.query_selector_all("h1"))
                if h1_count == 1:
                    self.results.append({
                        "test": "Heading Hierarchy",
                        "status": "PASS",
                        "message": "Found exactly one H1 heading"
                    })
                elif h1_count > 1:
                    self.results.append({
                        "test": "Heading Hierarchy",
                        "status": "WARN",
                        "message": f"Found {h1_count} H1 headings (should be 1)"
                    })
                else:
                    self.results.append({
                        "test": "Heading Hierarchy",
                        "status": "FAIL",
                        "message": "No H1 heading found"
                    })
            else:
                self.results.append({
                    "test": "Heading Hierarchy",
                    "status": "WARN",
                    "message": "No headings found"
                })
            
            # Test for form labels
            form_inputs = await page.query_selector_all("input, select, textarea")
            labeled_inputs = 0
            for input_el in form_inputs:
                # Check for associated label
                input_id = await input_el.get_attribute("id")
                if input_id:
                    label = await page.query_selector(f"label[for='{input_id}']")
                    if label:
                        labeled_inputs += 1
                    else:
                        # Check for wrapping label
                        parent_label = await input_el.query_selector("xpath=ancestor::label")
                        if parent_label:
                            labeled_inputs += 1
            
            if form_inputs:
                label_percentage = (labeled_inputs / len(form_inputs)) * 100
                if label_percentage >= 80:
                    self.results.append({
                        "test": "Form Labels",
                        "status": "PASS",
                        "message": f"{label_percentage:.1f}% of form inputs have labels"
                    })
                else:
                    self.results.append({
                        "test": "Form Labels",
                        "status": "WARN",
                        "message": f"Only {label_percentage:.1f}% of form inputs have labels"
                    })
            else:
                self.results.append({
                    "test": "Form Labels",
                    "status": "PASS",
                    "message": "No form inputs found to test"
                })
                
        except Exception as e:
            self.results.append({
                "test": "Accessibility",
                "status": "FAIL",
                "message": f"Accessibility test failed: {str(e)}"
            })

    async def test_performance(self, page):
        """Test basic performance metrics"""
        try:
            print("⚡ Testing Performance...")
            
            # Measure page load time
            start_time = datetime.now()
            await page.goto(f"{self.base_url}/apply", wait_until="networkidle")
            load_time = (datetime.now() - start_time).total_seconds()
            
            if load_time < 3:
                self.results.append({
                    "test": "Page Load Time",
                    "status": "PASS",
                    "message": f"Page loaded in {load_time:.2f} seconds"
                })
            elif load_time < 5:
                self.results.append({
                    "test": "Page Load Time",
                    "status": "WARN",
                    "message": f"Page loaded in {load_time:.2f} seconds (acceptable but slow)"
                })
            else:
                self.results.append({
                    "test": "Page Load Time",
                    "status": "FAIL",
                    "message": f"Page loaded in {load_time:.2f} seconds (too slow)"
                })
            
            # Check for console errors
            console_errors = []
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            
            # Wait a bit to catch any console errors
            await page.wait_for_timeout(2000)
            
            if not console_errors:
                self.results.append({
                    "test": "Console Errors",
                    "status": "PASS",
                    "message": "No console errors detected"
                })
            else:
                self.results.append({
                    "test": "Console Errors",
                    "status": "WARN",
                    "message": f"Found {len(console_errors)} console errors"
                })
                
        except Exception as e:
            self.results.append({
                "test": "Performance",
                "status": "FAIL",
                "message": f"Performance test failed: {str(e)}"
            })

    async def run_all_tests(self):
        """Run all tests across all pages"""
        print("🚀 Starting Comprehensive Site Testing...")
        print(f"Testing site: {self.base_url}")
        print("=" * 60)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Test each page
                for page_info in self.pages_to_test:
                    print(f"\n📍 Testing {page_info['name']} ({self.base_url}{page_info['url']})")
                    print("-" * 40)
                    
                    # Basic page load test
                    success = await self.test_page_load(page, page_info)
                    
                    if success:
                        # Navigation test
                        await self.test_navigation(page, page_info)
                        
                        # Page-specific tests
                        if page_info['url'] == '/apply':
                            await self.test_application_form(page)
                        elif page_info['url'] == '/courses':
                            await self.test_course_catalog(page)
                        elif page_info['url'] == '/white-paper':
                            await self.test_white_paper(page)
                        
                        # Responsive design test (on one page)
                        if page_info['url'] == '/apply':
                            await self.test_responsive_design(page)
                        
                        # Accessibility test (on one page)
                        if page_info['url'] == '/apply':
                            await self.test_accessibility(page)
                        
                        # Performance test (on one page)
                        if page_info['url'] == '/apply':
                            await self.test_performance(page)
                
                print("\n" + "=" * 60)
                print("✅ All tests completed!")
                
            except Exception as e:
                self.results.append({
                    "test": "Test Suite",
                    "status": "FAIL",
                    "message": f"Test suite failed: {str(e)}"
                })
                print(f"❌ Test suite failed: {str(e)}")
            
            finally:
                await browser.close()

    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        # Count results by status
        status_counts = {"PASS": 0, "WARN": 0, "FAIL": 0, "INFO": 0}
        for result in self.results:
            if result["status"] in status_counts:
                status_counts[result["status"]] += 1
        
        total_tests = len(self.results)
        pass_rate = (status_counts["PASS"] / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {status_counts['PASS']}")
        print(f"⚠️  Warnings: {status_counts['WARN']}")
        print(f"❌ Failed: {status_counts['FAIL']}")
        print(f"📈 Pass Rate: {pass_rate:.1f}%")
        
        print("\n" + "-" * 60)
        print("📋 DETAILED RESULTS")
        print("-" * 60)
        
        for result in self.results:
            status_icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}
            icon = status_icon.get(result["status"], "❓")
            print(f"{icon} {result['test']}: {result['message']}")
        
        # Overall assessment
        print("\n" + "=" * 60)
        print("🎯 OVERALL ASSESSMENT")
        print("=" * 60)
        
        if pass_rate >= 90:
            print("🌟 EXCELLENT: Site is highly user-friendly and functional!")
        elif pass_rate >= 75:
            print("👍 GOOD: Site is mostly user-friendly with minor issues.")
        elif pass_rate >= 60:
            print("⚠️  FAIR: Site has some user-friendliness issues that should be addressed.")
        else:
            print("❌ POOR: Site has significant user-friendliness issues that need immediate attention.")
        
        print(f"\nPass Rate: {pass_rate:.1f}%")
        
        # Save results to file
        results_data = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "total_tests": total_tests,
            "pass_rate": pass_rate,
            "status_counts": status_counts,
            "results": self.results
        }
        
        with open("comprehensive_test_results.json", "w") as f:
            json.dump(results_data, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: comprehensive_test_results.json")

async def main():
    tester = ComprehensiveSiteTester()
    await tester.run_all_tests()
    tester.print_summary()

if __name__ == "__main__":
    asyncio.run(main())