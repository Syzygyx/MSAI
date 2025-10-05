#!/usr/bin/env python3
"""
AI Site Walker - Comprehensive Website Analysis Tool
Uses Playwright for browser automation and AI analysis
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
import re
import requests
from dataclasses import dataclass, asdict

# Try to import Playwright
try:
    from playwright.async_api import async_playwright, Page, Browser, BrowserContext
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = Any
    Browser = Any
    BrowserContext = Any

# Configuration
SITE_URL = "http://msai.syzygyx.com"
MAX_PAGES = 20
MAX_DEPTH = 3
TIMEOUT = 30000

@dataclass
class SiteAnalysis:
    """Comprehensive site analysis result"""
    url: str
    title: str
    status_code: int
    load_time: float
    content_length: int
    has_errors: bool
    error_messages: List[str]
    scores: Dict[str, int]  # accessibility, performance, seo, content, technical
    content_analysis: Dict[str, Any]
    technical_analysis: Dict[str, Any]
    ux_analysis: Dict[str, Any]
    visual_analysis: Dict[str, Any]
    ai_insights: List[str]
    priority_level: str  # low, medium, high, critical
    recommendations: List[str]
    timestamp: str

class AISiteWalker:
    """AI-powered site walker with comprehensive analysis"""
    
    def __init__(self, site_url: str, use_playwright: bool = True):
        self.site_url = site_url
        self.visited_urls = set()
        self.analysis_results = []
        self.use_playwright = use_playwright and PLAYWRIGHT_AVAILABLE
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        print(f"🤖 AI Site Walker initialized")
        print(f"🔧 Analysis method: {'Playwright' if self.use_playwright else 'Requests'}")
        print(f"🌐 Target site: {site_url}")
    
    async def walk_site(self) -> List[SiteAnalysis]:
        """Main method to walk and analyze the entire site"""
        print(f"\n🚀 Starting AI-powered site walk...")
        print("=" * 60)
        
        if self.use_playwright:
            await self._walk_with_playwright()
        else:
            self._walk_with_requests()
        
        # Generate comprehensive AI insights
        self._generate_comprehensive_insights()
        
        return self.analysis_results
    
    async def _walk_with_playwright(self):
        """Walk site using Playwright for comprehensive browser testing"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            
            try:
                await self._analyze_page_playwright(context, self.site_url, depth=0)
            finally:
                await browser.close()
    
    def _walk_with_requests(self):
        """Walk site using requests (fallback method)"""
        self._analyze_page_requests(self.site_url)
    
    async def _analyze_page_playwright(self, context: BrowserContext, url: str, depth: int = 0):
        """Analyze a single page using Playwright"""
        if depth > MAX_DEPTH or len(self.visited_urls) >= MAX_PAGES or url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        print(f"🔍 Walking: {url} (depth: {depth})")
        
        try:
            page = await context.new_page()
            start_time = time.time()
            
            # Navigate and measure performance
            response = await page.goto(url, timeout=TIMEOUT, wait_until='networkidle')
            load_time = time.time() - start_time
            
            # Basic page information
            title = await page.title()
            status_code = response.status if response else 0
            content = await page.content()
            content_length = len(content)
            
            # Comprehensive analysis
            has_errors, error_messages = await self._check_errors_playwright(page)
            content_analysis = await self._analyze_content_playwright(page, content)
            technical_analysis = await self._analyze_technical_playwright(page)
            ux_analysis = await self._analyze_ux_playwright(page)
            visual_analysis = await self._analyze_visual_playwright(page)
            
            # Calculate comprehensive scores
            scores = await self._calculate_scores_playwright(page, load_time, content)
            
            # Generate AI insights and recommendations
            ai_insights = await self._generate_ai_insights_playwright(
                content_analysis, technical_analysis, ux_analysis, visual_analysis, page
            )
            recommendations = await self._generate_recommendations_playwright(
                scores, has_errors, content_analysis, technical_analysis, ux_analysis
            )
            
            # Determine priority level
            priority_level = self._determine_priority_level(scores, has_errors, load_time)
            
            # Create comprehensive analysis result
            analysis = SiteAnalysis(
                url=url,
                title=title,
                status_code=status_code,
                load_time=load_time,
                content_length=content_length,
                has_errors=has_errors,
                error_messages=error_messages,
                scores=scores,
                content_analysis=content_analysis,
                technical_analysis=technical_analysis,
                ux_analysis=ux_analysis,
                visual_analysis=visual_analysis,
                ai_insights=ai_insights,
                priority_level=priority_level,
                recommendations=recommendations,
                timestamp=datetime.now().isoformat()
            )
            
            self.analysis_results.append(analysis)
            
            # Continue walking to linked pages
            if depth < MAX_DEPTH:
                links = await self._extract_links_playwright(page, url)
                for link in links[:3]:  # Limit to 3 links per page
                    if link not in self.visited_urls:
                        await self._analyze_page_playwright(context, link, depth + 1)
            
            await page.close()
            
        except Exception as e:
            print(f"❌ Error analyzing {url}: {str(e)}")
            self._create_error_analysis(url, str(e))
    
    def _analyze_page_requests(self, url: str):
        """Analyze a single page using requests (fallback)"""
        if len(self.visited_urls) >= MAX_PAGES or url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        print(f"🔍 Walking: {url}")
        
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=10)
            load_time = time.time() - start_time
            
            # Basic page information
            title = self._extract_title(response.text)
            status_code = response.status_code
            content_length = len(response.text)
            
            # Comprehensive analysis
            has_errors, error_messages = self._check_errors_requests(response)
            content_analysis = self._analyze_content_requests(response.text, url)
            technical_analysis = self._analyze_technical_requests(response, url)
            ux_analysis = self._analyze_ux_requests(response.text)
            visual_analysis = self._analyze_visual_requests(response.text)
            
            # Calculate comprehensive scores
            scores = self._calculate_scores_requests(response, load_time)
            
            # Generate AI insights and recommendations
            ai_insights = self._generate_ai_insights_requests(
                content_analysis, technical_analysis, ux_analysis, visual_analysis
            )
            recommendations = self._generate_recommendations_requests(
                scores, has_errors, content_analysis, technical_analysis, ux_analysis
            )
            
            # Determine priority level
            priority_level = self._determine_priority_level(scores, has_errors, load_time)
            
            # Create comprehensive analysis result
            analysis = SiteAnalysis(
                url=url,
                title=title,
                status_code=status_code,
                load_time=load_time,
                content_length=content_length,
                has_errors=has_errors,
                error_messages=error_messages,
                scores=scores,
                content_analysis=content_analysis,
                technical_analysis=technical_analysis,
                ux_analysis=ux_analysis,
                visual_analysis=visual_analysis,
                ai_insights=ai_insights,
                priority_level=priority_level,
                recommendations=recommendations,
                timestamp=datetime.now().isoformat()
            )
            
            self.analysis_results.append(analysis)
            
            # Continue walking to linked pages
            if len(self.visited_urls) < MAX_PAGES:
                links = self._extract_links_requests(response.text, url)
                for link in links[:3]:  # Limit to 3 links per page
                    if link not in self.visited_urls:
                        self._analyze_page_requests(link)
            
        except Exception as e:
            print(f"❌ Error analyzing {url}: {str(e)}")
            self._create_error_analysis(url, str(e))
    
    def _create_error_analysis(self, url: str, error: str):
        """Create error analysis result"""
        error_analysis = SiteAnalysis(
            url=url,
            title="Error",
            status_code=0,
            load_time=0,
            content_length=0,
            has_errors=True,
            error_messages=[error],
            scores={'accessibility': 0, 'performance': 0, 'seo': 0, 'content': 0, 'technical': 0},
            content_analysis={},
            technical_analysis={},
            ux_analysis={},
            visual_analysis={},
            ai_insights=[f"Critical error detected: {error}"],
            priority_level="critical",
            recommendations=[f"Fix critical error: {error}"],
            timestamp=datetime.now().isoformat()
        )
        self.analysis_results.append(error_analysis)
    
    # Playwright analysis methods
    async def _check_errors_playwright(self, page: Page) -> tuple[bool, List[str]]:
        """Check for errors using Playwright"""
        errors = []
        
        def handle_console(msg):
            if msg.type in ['error', 'warning']:
                errors.append(f"{msg.type.upper()}: {msg.text}")
        
        page.on("console", handle_console)
        
        def handle_response(response):
            if response.status >= 400:
                errors.append(f"HTTP {response.status}: {response.url}")
        
        page.on("response", handle_response)
        
        return len(errors) > 0, errors
    
    async def _analyze_content_playwright(self, page: Page, content: str) -> Dict[str, Any]:
        """Analyze content using Playwright"""
        text_content = await page.evaluate("""
            () => {
                const scripts = document.querySelectorAll('script, style');
                scripts.forEach(el => el.remove());
                return document.body.innerText || document.body.textContent || '';
            }
        """)
        
        heading_count = await page.locator('h1, h2, h3, h4, h5, h6').count()
        link_count = await page.locator('a').count()
        image_count = await page.locator('img').count()
        button_count = await page.locator('button').count()
        form_count = await page.locator('form').count()
        
        has_ai_content = any(word in content.lower() for word in ['ai', 'artificial intelligence', 'machine learning'])
        has_api_content = 'api' in content.lower()
        
        return {
            'word_count': len(text_content.split()),
            'heading_count': heading_count,
            'link_count': link_count,
            'image_count': image_count,
            'button_count': button_count,
            'form_count': form_count,
            'has_ai_content': has_ai_content,
            'has_api_content': has_api_content,
            'content_quality': 'high' if len(text_content.split()) > 200 else 'medium' if len(text_content.split()) > 100 else 'low'
        }
    
    async def _analyze_technical_playwright(self, page: Page) -> Dict[str, Any]:
        """Analyze technical aspects using Playwright"""
        has_https = page.url.startswith('https://')
        has_viewport_meta = await page.locator('meta[name="viewport"]').count() > 0
        has_alt_text = await page.locator('img[alt]').count() > 0
        has_aria_labels = await page.locator('[aria-label]').count() > 0
        has_semantic_html = await page.locator('main, article, section, nav, header, footer').count() > 0
        has_javascript = await page.locator('script').count() > 0
        
        return {
            'has_https': has_https,
            'has_viewport_meta': has_viewport_meta,
            'has_alt_text': has_alt_text,
            'has_aria_labels': has_aria_labels,
            'has_semantic_html': has_semantic_html,
            'has_javascript': has_javascript,
            'modern_web_score': sum([
                has_https, has_viewport_meta, has_alt_text, has_aria_labels, has_semantic_html
            ]) / 5 * 100
        }
    
    async def _analyze_ux_playwright(self, page: Page) -> Dict[str, Any]:
        """Analyze user experience using Playwright"""
        has_navigation = await page.locator('nav, .nav, .navigation').count() > 0
        has_search = await page.locator('input[type="search"], .search').count() > 0
        has_loading_indicators = await page.locator('.loading, .spinner, .loader').count() > 0
        
        return {
            'has_navigation': has_navigation,
            'has_search': has_search,
            'has_loading_indicators': has_loading_indicators,
            'interactivity_score': sum([has_navigation, has_search]) / 2 * 100
        }
    
    async def _analyze_visual_playwright(self, page: Page) -> Dict[str, Any]:
        """Analyze visual aspects using Playwright"""
        has_flexbox = await page.locator('[style*="flex"], [class*="flex"]').count() > 0
        has_grid = await page.locator('[style*="grid"], [class*="grid"]').count() > 0
        has_transitions = await page.locator('[style*="transition"], [class*="transition"]').count() > 0
        has_animations = await page.locator('[style*="animation"], [class*="animate"]').count() > 0
        
        return {
            'has_flexbox': has_flexbox,
            'has_grid': has_grid,
            'has_transitions': has_transitions,
            'has_animations': has_animations,
            'modern_css_score': sum([has_flexbox, has_grid, has_transitions, has_animations]) / 4 * 100
        }
    
    async def _calculate_scores_playwright(self, page: Page, load_time: float, content: str) -> Dict[str, int]:
        """Calculate comprehensive scores using Playwright"""
        # Accessibility score
        accessibility = 0
        if await page.locator('img[alt]').count() > 0:
            accessibility += 20
        if await page.locator('[aria-label]').count() > 0:
            accessibility += 20
        if await page.locator('h1').count() > 0:
            accessibility += 20
        if await page.locator('main, article, section').count() > 0:
            accessibility += 20
        if await page.locator('button, a').count() > 0:
            accessibility += 20
        
        # Performance score
        performance = 100 if load_time < 1.0 else 80 if load_time < 2.0 else 60 if load_time < 3.0 else 40 if load_time < 5.0 else 20
        
        # SEO score
        seo = 0
        title = await page.title()
        if title and len(title) > 10:
            seo += 20
        meta_desc = await page.locator('meta[name="description"]').get_attribute('content')
        if meta_desc and len(meta_desc) > 50:
            seo += 20
        if await page.locator('h1').count() > 0:
            seo += 20
        if await page.locator('a[href]').count() > 0:
            seo += 20
        if await page.locator('img[alt]').count() > 0:
            seo += 20
        
        # Content score
        text_content = await page.evaluate("() => document.body.innerText || ''")
        word_count = len(text_content.split())
        content_score = min(100, word_count * 2)  # 2 points per word, max 100
        
        # Technical score
        technical = 0
        if page.url.startswith('https://'):
            technical += 20
        if await page.locator('meta[name="viewport"]').count() > 0:
            technical += 20
        if await page.locator('img[alt]').count() > 0:
            technical += 20
        if await page.locator('[aria-label]').count() > 0:
            technical += 20
        if await page.locator('main, article, section').count() > 0:
            technical += 20
        
        return {
            'accessibility': min(accessibility, 100),
            'performance': performance,
            'seo': min(seo, 100),
            'content': content_score,
            'technical': technical
        }
    
    async def _generate_ai_insights_playwright(self, content_analysis: Dict, technical_analysis: Dict, 
                                             ux_analysis: Dict, visual_analysis: Dict, page: Page) -> List[str]:
        """Generate AI insights using Playwright analysis"""
        insights = []
        
        if content_analysis['has_ai_content']:
            insights.append("🤖 AI content detected - excellent for AI-focused applications")
        
        if content_analysis['has_api_content']:
            insights.append("🔗 API integration found - good developer experience")
        
        if content_analysis['content_quality'] == 'high':
            insights.append("📝 High-quality content with good word count")
        
        if technical_analysis['modern_web_score'] > 80:
            insights.append("⚡ Modern web standards well implemented")
        
        if ux_analysis['interactivity_score'] > 70:
            insights.append("🎯 Good user interactivity and navigation")
        
        if visual_analysis['modern_css_score'] > 70:
            insights.append("🎨 Modern CSS features well utilized")
        
        return insights
    
    async def _generate_recommendations_playwright(self, scores: Dict[str, int], has_errors: bool, 
                                                 content_analysis: Dict, technical_analysis: Dict, 
                                                 ux_analysis: Dict) -> List[str]:
        """Generate recommendations using Playwright analysis"""
        recommendations = []
        
        if has_errors:
            recommendations.append("🚨 Fix critical errors immediately")
        
        if scores['accessibility'] < 60:
            recommendations.append("♿ Improve accessibility with alt text, ARIA labels, and semantic HTML")
        
        if scores['performance'] < 70:
            recommendations.append("⚡ Optimize page load time and performance")
        
        if scores['seo'] < 60:
            recommendations.append("🔍 Improve SEO with better titles, meta descriptions, and heading structure")
        
        if scores['content'] < 50:
            recommendations.append("📝 Add more high-quality content")
        
        if scores['technical'] < 60:
            recommendations.append("🔧 Implement modern web standards and best practices")
        
        if not technical_analysis['has_https']:
            recommendations.append("🔒 Implement HTTPS for security and SEO")
        
        if not technical_analysis['has_viewport_meta']:
            recommendations.append("📱 Add viewport meta tag for mobile responsiveness")
        
        return recommendations
    
    async def _extract_links_playwright(self, page: Page, base_url: str) -> List[str]:
        """Extract internal links using Playwright"""
        links = await page.evaluate("""
            () => {
                const links = Array.from(document.querySelectorAll('a[href]'));
                return links.map(link => link.href).filter(href => href);
            }
        """)
        
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
        
        return list(set(internal_links))
    
    # Requests-based analysis methods (fallback)
    def _extract_title(self, html_content: str) -> str:
        """Extract page title from HTML"""
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        if title_match:
            return title_match.group(1).strip()
        return "No Title"
    
    def _check_errors_requests(self, response: requests.Response) -> tuple[bool, List[str]]:
        """Check for errors using requests"""
        errors = []
        
        if response.status_code >= 400:
            errors.append(f"HTTP {response.status_code}: {response.reason}")
        
        content = response.text.lower()
        if 'error' in content and any(word in content for word in ['not found', '404', '500', 'server error']):
            errors.append("Error indicators found in content")
        
        return len(errors) > 0, errors
    
    def _analyze_content_requests(self, html_content: str, url: str) -> Dict[str, Any]:
        """Analyze content using requests"""
        text_content = re.sub(r'<[^>]+>', ' ', html_content)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        has_headings = bool(re.search(r'<h[1-6][^>]*>', html_content, re.IGNORECASE))
        has_images = bool(re.search(r'<img[^>]*>', html_content, re.IGNORECASE))
        has_links = bool(re.search(r'<a[^>]*href', html_content, re.IGNORECASE))
        has_forms = bool(re.search(r'<form[^>]*>', html_content, re.IGNORECASE))
        has_buttons = bool(re.search(r'<button[^>]*>', html_content, re.IGNORECASE))
        
        has_ai_content = any(word in html_content.lower() for word in ['ai', 'artificial intelligence', 'machine learning'])
        has_api_content = 'api' in html_content.lower()
        
        return {
            'word_count': len(text_content.split()),
            'has_headings': has_headings,
            'has_images': has_images,
            'has_links': has_links,
            'has_forms': has_forms,
            'has_buttons': has_buttons,
            'has_ai_content': has_ai_content,
            'has_api_content': has_api_content,
            'content_quality': 'high' if len(text_content.split()) > 200 else 'medium' if len(text_content.split()) > 100 else 'low'
        }
    
    def _analyze_technical_requests(self, response: requests.Response, url: str) -> Dict[str, Any]:
        """Analyze technical aspects using requests"""
        has_https = url.startswith('https://')
        content_type = response.headers.get('content-type', '').lower()
        has_html_content = 'text/html' in content_type
        has_compression = 'gzip' in response.headers.get('content-encoding', '').lower()
        
        content = response.text.lower()
        has_viewport_meta = 'viewport' in content and 'meta' in content
        has_alt_text = 'alt=' in content
        has_aria_labels = 'aria-' in content
        has_semantic_html = any(word in content for word in ['<main', '<article', '<section', '<nav', '<header', '<footer'])
        
        return {
            'has_https': has_https,
            'has_html_content': has_html_content,
            'has_compression': has_compression,
            'has_viewport_meta': has_viewport_meta,
            'has_alt_text': has_alt_text,
            'has_aria_labels': has_aria_labels,
            'has_semantic_html': has_semantic_html,
            'response_size': len(response.content),
            'modern_web_score': sum([
                has_https, has_viewport_meta, has_alt_text, has_aria_labels, has_semantic_html
            ]) / 5 * 100
        }
    
    def _analyze_ux_requests(self, html_content: str) -> Dict[str, Any]:
        """Analyze user experience using requests"""
        content = html_content.lower()
        has_navigation = any(word in content for word in ['<nav', 'navigation', 'menu'])
        has_search = any(word in content for word in ['search', 'input type="search"'])
        has_loading_indicators = any(word in content for word in ['loading', 'spinner', 'loader'])
        
        return {
            'has_navigation': has_navigation,
            'has_search': has_search,
            'has_loading_indicators': has_loading_indicators,
            'interactivity_score': sum([has_navigation, has_search]) / 2 * 100
        }
    
    def _analyze_visual_requests(self, html_content: str) -> Dict[str, Any]:
        """Analyze visual aspects using requests"""
        content = html_content.lower()
        has_flexbox = any(word in content for word in ['flexbox', 'display: flex', 'flex-'])
        has_grid = any(word in content for word in ['grid', 'display: grid', 'grid-'])
        has_transitions = any(word in content for word in ['transition', 'transform'])
        has_animations = any(word in content for word in ['animation', 'keyframes', 'animate'])
        
        return {
            'has_flexbox': has_flexbox,
            'has_grid': has_grid,
            'has_transitions': has_transitions,
            'has_animations': has_animations,
            'modern_css_score': sum([has_flexbox, has_grid, has_transitions, has_animations]) / 4 * 100
        }
    
    def _calculate_scores_requests(self, response: requests.Response, load_time: float) -> Dict[str, int]:
        """Calculate comprehensive scores using requests"""
        content = response.text.lower()
        
        # Accessibility score
        accessibility = 0
        if 'alt=' in content:
            accessibility += 20
        if 'aria-' in content:
            accessibility += 20
        if '<h1' in content:
            accessibility += 20
        if any(word in content for word in ['<main', '<article', '<section']):
            accessibility += 20
        if any(word in content for word in ['<button', '<a']):
            accessibility += 20
        
        # Performance score
        performance = 100 if load_time < 1.0 else 80 if load_time < 2.0 else 60 if load_time < 3.0 else 40 if load_time < 5.0 else 20
        
        # SEO score
        seo = 0
        if '<title>' in content:
            seo += 20
        if 'meta name="description"' in content:
            seo += 20
        if '<h1' in content:
            seo += 20
        if '<a' in content:
            seo += 20
        if 'alt=' in content:
            seo += 20
        
        # Content score
        text_content = re.sub(r'<[^>]+>', ' ', response.text)
        word_count = len(text_content.split())
        content_score = min(100, word_count * 2)
        
        # Technical score
        technical = 0
        if response.url.startswith('https://'):
            technical += 20
        if 'viewport' in content and 'meta' in content:
            technical += 20
        if 'alt=' in content:
            technical += 20
        if 'aria-' in content:
            technical += 20
        if any(word in content for word in ['<main', '<article', '<section']):
            technical += 20
        
        return {
            'accessibility': min(accessibility, 100),
            'performance': performance,
            'seo': min(seo, 100),
            'content': content_score,
            'technical': technical
        }
    
    def _generate_ai_insights_requests(self, content_analysis: Dict, technical_analysis: Dict, 
                                     ux_analysis: Dict, visual_analysis: Dict) -> List[str]:
        """Generate AI insights using requests analysis"""
        insights = []
        
        if content_analysis['has_ai_content']:
            insights.append("🤖 AI content detected - excellent for AI-focused applications")
        
        if content_analysis['has_api_content']:
            insights.append("🔗 API integration found - good developer experience")
        
        if content_analysis['content_quality'] == 'high':
            insights.append("📝 High-quality content with good word count")
        
        if technical_analysis['modern_web_score'] > 80:
            insights.append("⚡ Modern web standards well implemented")
        
        if ux_analysis['interactivity_score'] > 70:
            insights.append("🎯 Good user interactivity and navigation")
        
        if visual_analysis['modern_css_score'] > 70:
            insights.append("🎨 Modern CSS features well utilized")
        
        return insights
    
    def _generate_recommendations_requests(self, scores: Dict[str, int], has_errors: bool, 
                                         content_analysis: Dict, technical_analysis: Dict, 
                                         ux_analysis: Dict) -> List[str]:
        """Generate recommendations using requests analysis"""
        recommendations = []
        
        if has_errors:
            recommendations.append("🚨 Fix critical errors immediately")
        
        if scores['accessibility'] < 60:
            recommendations.append("♿ Improve accessibility with alt text, ARIA labels, and semantic HTML")
        
        if scores['performance'] < 70:
            recommendations.append("⚡ Optimize page load time and performance")
        
        if scores['seo'] < 60:
            recommendations.append("🔍 Improve SEO with better titles, meta descriptions, and heading structure")
        
        if scores['content'] < 50:
            recommendations.append("📝 Add more high-quality content")
        
        if scores['technical'] < 60:
            recommendations.append("🔧 Implement modern web standards and best practices")
        
        if not technical_analysis['has_https']:
            recommendations.append("🔒 Implement HTTPS for security and SEO")
        
        if not technical_analysis['has_viewport_meta']:
            recommendations.append("📱 Add viewport meta tag for mobile responsiveness")
        
        return recommendations
    
    def _extract_links_requests(self, html_content: str, base_url: str) -> List[str]:
        """Extract internal links using requests"""
        href_pattern = r'href=["\']([^"\']+)["\']'
        matches = re.findall(href_pattern, html_content, re.IGNORECASE)
        
        base_domain = urlparse(base_url).netloc
        internal_links = []
        
        for link in matches:
            try:
                if link.startswith('/'):
                    full_url = urljoin(base_url, link)
                elif link.startswith('http'):
                    parsed = urlparse(link)
                    if parsed.netloc == base_domain:
                        full_url = link
                    else:
                        continue
                else:
                    full_url = urljoin(base_url, link)
                
                if full_url not in internal_links and '#' not in full_url:
                    internal_links.append(full_url)
            except:
                continue
        
        return internal_links[:5]
    
    def _determine_priority_level(self, scores: Dict[str, int], has_errors: bool, load_time: float) -> str:
        """Determine priority level for the page"""
        if has_errors:
            return "critical"
        
        avg_score = sum(scores.values()) / len(scores)
        
        if avg_score < 30 or load_time > 5.0:
            return "high"
        elif avg_score < 60 or load_time > 3.0:
            return "medium"
        else:
            return "low"
    
    def _generate_comprehensive_insights(self):
        """Generate comprehensive AI insights across all analyzed pages"""
        if not self.analysis_results:
            return
        
        print(f"\n🤖 Generating Comprehensive AI Insights...")
        print("=" * 50)
        
        # Calculate overall statistics
        total_pages = len(self.analysis_results)
        avg_scores = {
            'accessibility': sum(p.scores['accessibility'] for p in self.analysis_results) / total_pages,
            'performance': sum(p.scores['performance'] for p in self.analysis_results) / total_pages,
            'seo': sum(p.scores['seo'] for p in self.analysis_results) / total_pages,
            'content': sum(p.scores['content'] for p in self.analysis_results) / total_pages,
            'technical': sum(p.scores['technical'] for p in self.analysis_results) / total_pages
        }
        
        pages_by_priority = {
            'critical': sum(1 for p in self.analysis_results if p.priority_level == 'critical'),
            'high': sum(1 for p in self.analysis_results if p.priority_level == 'high'),
            'medium': sum(1 for p in self.analysis_results if p.priority_level == 'medium'),
            'low': sum(1 for p in self.analysis_results if p.priority_level == 'low')
        }
        
        pages_with_ai_content = sum(1 for p in self.analysis_results if p.content_analysis.get('has_ai_content', False))
        pages_with_api_content = sum(1 for p in self.analysis_results if p.content_analysis.get('has_api_content', False))
        
        print(f"📊 Comprehensive Site Analysis Results:")
        print(f"   • Total Pages Analyzed: {total_pages}")
        print(f"   • Average Accessibility Score: {avg_scores['accessibility']:.1f}/100")
        print(f"   • Average Performance Score: {avg_scores['performance']:.1f}/100")
        print(f"   • Average SEO Score: {avg_scores['seo']:.1f}/100")
        print(f"   • Average Content Score: {avg_scores['content']:.1f}/100")
        print(f"   • Average Technical Score: {avg_scores['technical']:.1f}/100")
        print(f"   • Pages with AI Content: {pages_with_ai_content}")
        print(f"   • Pages with API Content: {pages_with_api_content}")
        print(f"   • Priority Distribution: {pages_by_priority}")
        
        # AI insights
        if pages_with_ai_content > 0:
            print(f"\n🤖 AI Content Analysis:")
            print(f"   • AI content detected on {pages_with_ai_content} pages")
            print(f"   • This is excellent for an AI-focused application!")
        
        if pages_with_api_content > 0:
            print(f"\n🔗 API Integration Analysis:")
            print(f"   • API content found on {pages_with_api_content} pages")
            print(f"   • Good developer experience and API documentation!")
        
        # Priority insights
        if pages_by_priority['critical'] > 0:
            print(f"\n🚨 Critical Issues Found:")
            print(f"   • {pages_by_priority['critical']} pages need immediate attention")
            print(f"   • Focus on fixing critical errors first")
        
        if pages_by_priority['high'] > 0:
            print(f"\n⚠️  High Priority Issues:")
            print(f"   • {pages_by_priority['high']} pages need significant improvements")
            print(f"   • Address these after critical issues")
        
        # Overall assessment
        overall_score = sum(avg_scores.values()) / len(avg_scores)
        if overall_score >= 80:
            print(f"\n✅ Overall Assessment: EXCELLENT ({overall_score:.1f}/100)")
            print(f"   • Site is performing very well across all metrics")
        elif overall_score >= 60:
            print(f"\n⚠️  Overall Assessment: GOOD ({overall_score:.1f}/100)")
            print(f"   • Site is performing well with room for improvement")
        elif overall_score >= 40:
            print(f"\n⚠️  Overall Assessment: FAIR ({overall_score:.1f}/100)")
            print(f"   • Site needs significant improvements")
        else:
            print(f"\n❌ Overall Assessment: POOR ({overall_score:.1f}/100)")
            print(f"   • Site needs major improvements across all areas")
    
    def save_comprehensive_report(self, filename: str = None):
        """Save comprehensive analysis report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"comprehensive_ai_analysis_{timestamp}.json"
        
        # Calculate summary statistics
        total_pages = len(self.analysis_results)
        avg_scores = {
            'accessibility': sum(p.scores['accessibility'] for p in self.analysis_results) / total_pages if total_pages > 0 else 0,
            'performance': sum(p.scores['performance'] for p in self.analysis_results) / total_pages if total_pages > 0 else 0,
            'seo': sum(p.scores['seo'] for p in self.analysis_results) / total_pages if total_pages > 0 else 0,
            'content': sum(p.scores['content'] for p in self.analysis_results) / total_pages if total_pages > 0 else 0,
            'technical': sum(p.scores['technical'] for p in self.analysis_results) / total_pages if total_pages > 0 else 0
        }
        
        pages_by_priority = {
            'critical': sum(1 for p in self.analysis_results if p.priority_level == 'critical'),
            'high': sum(1 for p in self.analysis_results if p.priority_level == 'high'),
            'medium': sum(1 for p in self.analysis_results if p.priority_level == 'medium'),
            'low': sum(1 for p in self.analysis_results if p.priority_level == 'low')
        }
        
        report_data = {
            'site_url': self.site_url,
            'analysis_timestamp': datetime.now().isoformat(),
            'analysis_method': 'Playwright' if self.use_playwright else 'Requests',
            'summary': {
                'total_pages': total_pages,
                'average_scores': avg_scores,
                'priority_distribution': pages_by_priority,
                'overall_score': sum(avg_scores.values()) / len(avg_scores) if avg_scores else 0
            },
            'pages': [asdict(page) for page in self.analysis_results]
        }
        
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"📄 Comprehensive analysis report saved to: {filename}")
        return filename

async def main():
    """Main function to run the AI site walker"""
    print("🚀 AI Site Walker - Comprehensive Website Analysis")
    print("=" * 60)
    
    # Initialize walker
    walker = AISiteWalker(SITE_URL, use_playwright=PLAYWRIGHT_AVAILABLE)
    
    # Walk and analyze the site
    start_time = time.time()
    results = await walker.walk_site()
    analysis_time = time.time() - start_time
    
    # Print summary
    print(f"\n✅ AI Site Walk Complete!")
    print(f"⏱️  Total Time: {analysis_time:.2f} seconds")
    print(f"📄 Pages Analyzed: {len(results)}")
    
    # Save comprehensive report
    report_file = walker.save_comprehensive_report()
    
    # Print detailed results sorted by priority
    print(f"\n📋 Detailed Results (sorted by priority):")
    priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    sorted_results = sorted(results, key=lambda x: priority_order.get(x.priority_level, 4))
    
    for i, page in enumerate(sorted_results, 1):
        priority_icon = {
            'critical': '🚨',
            'high': '⚠️',
            'medium': '🔶',
            'low': '✅'
        }.get(page.priority_level, '❓')
        
        print(f"\n{i}. {priority_icon} {page.url} ({page.priority_level.upper()} priority)")
        print(f"   Title: {page.title}")
        print(f"   Status: {page.status_code}")
        print(f"   Load Time: {page.load_time:.2f}s")
        print(f"   Scores: A:{page.scores['accessibility']}/100 P:{page.scores['performance']}/100 S:{page.scores['seo']}/100 C:{page.scores['content']}/100 T:{page.scores['technical']}/100")
        print(f"   Content Quality: {page.content_analysis.get('content_quality', 'unknown')}")
        
        if page.ai_insights:
            print(f"   AI Insights: {', '.join(page.ai_insights[:2])}")
        
        if page.recommendations:
            print(f"   Top Recommendations:")
            for rec in page.recommendations[:3]:
                print(f"     {rec}")
        
        if page.has_errors:
            print(f"   ⚠️  Errors: {', '.join(page.error_messages)}")

if __name__ == "__main__":
    asyncio.run(main())