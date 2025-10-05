#!/usr/bin/env python3
"""
AI-Powered Site Analyzer using Playwright
Intelligently walks through websites and analyzes each page
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
import re

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
import openai
from dataclasses import dataclass, asdict

# Configuration
SITE_URL = "http://msai.syzygyx.com"
MAX_PAGES = 20
MAX_DEPTH = 3
TIMEOUT = 30000  # 30 seconds per page

@dataclass
class PageAnalysis:
    """Data structure for page analysis results"""
    url: str
    title: str
    status_code: int
    load_time: float
    content_length: int
    has_errors: bool
    error_messages: List[str]
    accessibility_score: int
    performance_score: int
    seo_score: int
    content_analysis: Dict[str, Any]
    technical_analysis: Dict[str, Any]
    user_experience_analysis: Dict[str, Any]
    ai_recommendations: List[str]
    timestamp: str

class AISiteAnalyzer:
    """AI-powered website analyzer using Playwright"""
    
    def __init__(self, site_url: str, openai_api_key: Optional[str] = None):
        self.site_url = site_url
        self.visited_urls = set()
        self.analysis_results = []
        self.openai_api_key = openai_api_key
        
        if openai_api_key:
            openai.api_key = openai_api_key
    
    async def analyze_site(self) -> List[PageAnalysis]:
        """Main method to analyze the entire site"""
        print(f"🤖 AI Site Analyzer starting analysis of {self.site_url}")
        print("=" * 60)
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=False)  # Set to True for headless
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            
            try:
                # Start analysis from the main page
                await self._analyze_page_recursive(context, self.site_url, depth=0)
                
                # Generate AI insights across all pages
                await self._generate_ai_insights()
                
            finally:
                await browser.close()
        
        return self.analysis_results
    
    async def _analyze_page_recursive(self, context: BrowserContext, url: str, depth: int = 0):
        """Recursively analyze pages starting from the given URL"""
        if depth > MAX_DEPTH or len(self.visited_urls) >= MAX_PAGES or url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        print(f"🔍 Analyzing: {url} (depth: {depth})")
        
        try:
            page = await context.new_page()
            start_time = time.time()
            
            # Navigate to page
            response = await page.goto(url, timeout=TIMEOUT, wait_until='networkidle')
            load_time = time.time() - start_time
            
            # Basic page info
            title = await page.title()
            status_code = response.status if response else 0
            
            # Get page content
            content = await page.content()
            content_length = len(content)
            
            # Check for errors
            has_errors, error_messages = await self._check_page_errors(page)
            
            # Analyze page content
            content_analysis = await self._analyze_content(page, content)
            
            # Technical analysis
            technical_analysis = await self._analyze_technical_aspects(page)
            
            # User experience analysis
            ux_analysis = await self._analyze_user_experience(page)
            
            # Calculate scores
            accessibility_score = await self._calculate_accessibility_score(page)
            performance_score = await self._calculate_performance_score(page, load_time)
            seo_score = await self._calculate_seo_score(page, content)
            
            # Generate AI recommendations
            ai_recommendations = await self._generate_ai_recommendations(
                content_analysis, technical_analysis, ux_analysis
            )
            
            # Create analysis result
            analysis = PageAnalysis(
                url=url,
                title=title,
                status_code=status_code,
                load_time=load_time,
                content_length=content_length,
                has_errors=has_errors,
                error_messages=error_messages,
                accessibility_score=accessibility_score,
                performance_score=performance_score,
                seo_score=seo_score,
                content_analysis=content_analysis,
                technical_analysis=technical_analysis,
                user_experience_analysis=ux_analysis,
                ai_recommendations=ai_recommendations,
                timestamp=datetime.now().isoformat()
            )
            
            self.analysis_results.append(analysis)
            
            # Find and analyze linked pages
            if depth < MAX_DEPTH:
                links = await self._extract_internal_links(page, url)
                for link in links[:5]:  # Limit to 5 links per page
                    if link not in self.visited_urls:
                        await self._analyze_page_recursive(context, link, depth + 1)
            
            await page.close()
            
        except Exception as e:
            print(f"❌ Error analyzing {url}: {str(e)}")
            # Create error analysis
            error_analysis = PageAnalysis(
                url=url,
                title="Error",
                status_code=0,
                load_time=0,
                content_length=0,
                has_errors=True,
                error_messages=[str(e)],
                accessibility_score=0,
                performance_score=0,
                seo_score=0,
                content_analysis={},
                technical_analysis={},
                user_experience_analysis={},
                ai_recommendations=[f"Fix critical error: {str(e)}"],
                timestamp=datetime.now().isoformat()
            )
            self.analysis_results.append(error_analysis)
    
    async def _check_page_errors(self, page: Page) -> tuple[bool, List[str]]:
        """Check for JavaScript errors and console messages"""
        errors = []
        
        # Listen for console messages
        def handle_console(msg):
            if msg.type in ['error', 'warning']:
                errors.append(f"{msg.type.upper()}: {msg.text}")
        
        page.on("console", handle_console)
        
        # Check for network errors
        def handle_response(response):
            if response.status >= 400:
                errors.append(f"HTTP {response.status}: {response.url}")
        
        page.on("response", handle_response)
        
        return len(errors) > 0, errors
    
    async def _analyze_content(self, page: Page, content: str) -> Dict[str, Any]:
        """Analyze page content for quality and relevance"""
        # Extract text content
        text_content = await page.evaluate("""
            () => {
                // Remove script and style elements
                const scripts = document.querySelectorAll('script, style');
                scripts.forEach(el => el.remove());
                
                // Get text content
                return document.body.innerText || document.body.textContent || '';
            }
        """)
        
        # Basic content metrics
        word_count = len(text_content.split())
        paragraph_count = len(re.findall(r'\n\s*\n', text_content))
        
        # Check for key elements
        has_headings = await page.locator('h1, h2, h3, h4, h5, h6').count() > 0
        has_images = await page.locator('img').count() > 0
        has_links = await page.locator('a').count() > 0
        has_forms = await page.locator('form').count() > 0
        
        # Check for specific content types
        has_api_links = 'api' in content.lower()
        has_documentation = any(word in content.lower() for word in ['docs', 'documentation', 'guide', 'tutorial'])
        
        return {
            'word_count': word_count,
            'paragraph_count': paragraph_count,
            'has_headings': has_headings,
            'has_images': has_images,
            'has_links': has_links,
            'has_forms': has_forms,
            'has_api_links': has_api_links,
            'has_documentation': has_documentation,
            'content_quality': 'high' if word_count > 100 and has_headings else 'medium' if word_count > 50 else 'low'
        }
    
    async def _analyze_technical_aspects(self, page: Page) -> Dict[str, Any]:
        """Analyze technical aspects of the page"""
        # Check for modern web technologies
        has_https = page.url.startswith('https://')
        
        # Check for responsive design
        viewport_meta = await page.locator('meta[name="viewport"]').count() > 0
        
        # Check for performance optimizations
        has_gzip = False  # Would need to check response headers
        has_minified_css = await page.locator('link[rel="stylesheet"]').count() > 0
        has_minified_js = await page.locator('script[src]').count() > 0
        
        # Check for accessibility features
        has_alt_text = await page.locator('img[alt]').count() > 0
        has_aria_labels = await page.locator('[aria-label]').count() > 0
        has_semantic_html = await page.locator('main, article, section, nav, header, footer').count() > 0
        
        return {
            'has_https': has_https,
            'has_viewport_meta': viewport_meta,
            'has_gzip': has_gzip,
            'has_minified_css': has_minified_css,
            'has_minified_js': has_minified_js,
            'has_alt_text': has_alt_text,
            'has_aria_labels': has_aria_labels,
            'has_semantic_html': has_semantic_html,
            'modern_web_score': sum([
                has_https, viewport_meta, has_alt_text, has_aria_labels, has_semantic_html
            ]) / 5 * 100
        }
    
    async def _analyze_user_experience(self, page: Page) -> Dict[str, Any]:
        """Analyze user experience aspects"""
        # Check for interactive elements
        has_buttons = await page.locator('button, input[type="button"], input[type="submit"]').count() > 0
        has_navigation = await page.locator('nav, .nav, .navigation').count() > 0
        has_search = await page.locator('input[type="search"], .search').count() > 0
        
        # Check for loading states
        has_loading_indicators = await page.locator('.loading, .spinner, .loader').count() > 0
        
        # Check for error handling
        has_error_messages = await page.locator('.error, .alert, .warning').count() > 0
        
        # Check for feedback mechanisms
        has_success_messages = await page.locator('.success, .alert-success').count() > 0
        
        return {
            'has_buttons': has_buttons,
            'has_navigation': has_navigation,
            'has_search': has_search,
            'has_loading_indicators': has_loading_indicators,
            'has_error_messages': has_error_messages,
            'has_success_messages': has_success_messages,
            'interactivity_score': sum([
                has_buttons, has_navigation, has_search
            ]) / 3 * 100
        }
    
    async def _calculate_accessibility_score(self, page: Page) -> int:
        """Calculate accessibility score (0-100)"""
        score = 0
        
        # Check for basic accessibility features
        if await page.locator('img[alt]').count() > 0:
            score += 20
        if await page.locator('[aria-label]').count() > 0:
            score += 20
        if await page.locator('h1').count() > 0:
            score += 20
        if await page.locator('main, article, section').count() > 0:
            score += 20
        if await page.locator('button, a').count() > 0:
            score += 20
        
        return min(score, 100)
    
    async def _calculate_performance_score(self, page: Page, load_time: float) -> int:
        """Calculate performance score (0-100)"""
        # Base score on load time
        if load_time < 1.0:
            return 100
        elif load_time < 2.0:
            return 80
        elif load_time < 3.0:
            return 60
        elif load_time < 5.0:
            return 40
        else:
            return 20
    
    async def _calculate_seo_score(self, page: Page, content: str) -> int:
        """Calculate SEO score (0-100)"""
        score = 0
        
        # Check for title tag
        title = await page.title()
        if title and len(title) > 10:
            score += 20
        
        # Check for meta description
        meta_desc = await page.locator('meta[name="description"]').get_attribute('content')
        if meta_desc and len(meta_desc) > 50:
            score += 20
        
        # Check for headings
        if await page.locator('h1').count() > 0:
            score += 20
        
        # Check for internal links
        if await page.locator('a[href]').count() > 0:
            score += 20
        
        # Check for images with alt text
        if await page.locator('img[alt]').count() > 0:
            score += 20
        
        return min(score, 100)
    
    async def _extract_internal_links(self, page: Page, base_url: str) -> List[str]:
        """Extract internal links from the page"""
        links = await page.evaluate("""
            () => {
                const links = Array.from(document.querySelectorAll('a[href]'));
                return links.map(link => link.href).filter(href => href);
            }
        """)
        
        # Filter for internal links
        base_domain = urlparse(base_url).netloc
        internal_links = []
        
        for link in links:
            try:
                parsed = urlparse(link)
                if parsed.netloc == base_domain or parsed.netloc == '':
                    full_url = urljoin(base_url, link)
                    internal_links.append(full_url)
            except:
                continue
        
        return list(set(internal_links))  # Remove duplicates
    
    async def _generate_ai_recommendations(self, content_analysis: Dict, technical_analysis: Dict, ux_analysis: Dict) -> List[str]:
        """Generate AI-powered recommendations for the page"""
        recommendations = []
        
        # Content recommendations
        if content_analysis['word_count'] < 100:
            recommendations.append("Consider adding more content to improve SEO and user engagement")
        
        if not content_analysis['has_headings']:
            recommendations.append("Add proper heading structure (H1, H2, H3) for better content organization")
        
        if not content_analysis['has_images']:
            recommendations.append("Consider adding relevant images to enhance visual appeal")
        
        # Technical recommendations
        if not technical_analysis['has_https']:
            recommendations.append("Implement HTTPS for better security and SEO")
        
        if not technical_analysis['has_viewport_meta']:
            recommendations.append("Add viewport meta tag for mobile responsiveness")
        
        if technical_analysis['modern_web_score'] < 60:
            recommendations.append("Improve modern web standards compliance")
        
        # UX recommendations
        if not ux_analysis['has_navigation']:
            recommendations.append("Add clear navigation to help users find content")
        
        if ux_analysis['interactivity_score'] < 50:
            recommendations.append("Increase interactivity with buttons, forms, or interactive elements")
        
        return recommendations
    
    async def _generate_ai_insights(self):
        """Generate AI insights across all analyzed pages"""
        if not self.analysis_results:
            return
        
        print("\n🤖 Generating AI insights across all pages...")
        
        # Calculate overall statistics
        total_pages = len(self.analysis_results)
        avg_load_time = sum(p.load_time for p in self.analysis_results) / total_pages
        avg_accessibility = sum(p.accessibility_score for p in self.analysis_results) / total_pages
        avg_performance = sum(p.performance_score for p in self.analysis_results) / total_pages
        avg_seo = sum(p.seo_score for p in self.analysis_results) / total_pages
        
        pages_with_errors = sum(1 for p in self.analysis_results if p.has_errors)
        
        print(f"📊 Overall Site Statistics:")
        print(f"   • Total Pages Analyzed: {total_pages}")
        print(f"   • Average Load Time: {avg_load_time:.2f}s")
        print(f"   • Average Accessibility Score: {avg_accessibility:.1f}/100")
        print(f"   • Average Performance Score: {avg_performance:.1f}/100")
        print(f"   • Average SEO Score: {avg_seo:.1f}/100")
        print(f"   • Pages with Errors: {pages_with_errors}")
    
    def save_analysis_report(self, filename: str = None):
        """Save analysis results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_site_analysis_{timestamp}.json"
        
        # Convert dataclass instances to dictionaries
        report_data = {
            'site_url': self.site_url,
            'analysis_timestamp': datetime.now().isoformat(),
            'total_pages': len(self.analysis_results),
            'pages': [asdict(page) for page in self.analysis_results]
        }
        
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"📄 Analysis report saved to: {filename}")
        return filename

async def main():
    """Main function to run the AI site analyzer"""
    print("🚀 AI-Powered Site Analyzer")
    print("=" * 40)
    
    # Initialize analyzer
    analyzer = AISiteAnalyzer(SITE_URL)
    
    # Run analysis
    start_time = time.time()
    results = await analyzer.analyze_site()
    analysis_time = time.time() - start_time
    
    # Print summary
    print(f"\n✅ Analysis Complete!")
    print(f"⏱️  Total Time: {analysis_time:.2f} seconds")
    print(f"📄 Pages Analyzed: {len(results)}")
    
    # Save report
    report_file = analyzer.save_analysis_report()
    
    # Print detailed results
    print(f"\n📋 Detailed Results:")
    for i, page in enumerate(results, 1):
        print(f"\n{i}. {page.url}")
        print(f"   Title: {page.title}")
        print(f"   Status: {page.status_code}")
        print(f"   Load Time: {page.load_time:.2f}s")
        print(f"   Accessibility: {page.accessibility_score}/100")
        print(f"   Performance: {page.performance_score}/100")
        print(f"   SEO: {page.seo_score}/100")
        if page.ai_recommendations:
            print(f"   AI Recommendations: {len(page.ai_recommendations)}")
            for rec in page.ai_recommendations[:2]:  # Show first 2
                print(f"     • {rec}")

if __name__ == "__main__":
    asyncio.run(main())