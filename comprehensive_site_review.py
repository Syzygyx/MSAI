#!/usr/bin/env python3
"""
Comprehensive site review using Playwright to check all links and functionality
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime
from urllib.parse import urljoin, urlparse

async def review_site():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        print("🔍 Starting comprehensive site review...")
        
        # Navigate to the main site
        base_url = 'https://syzygyx.github.io/MSAI/'
        await page.goto(base_url)
        await page.wait_for_load_state('networkidle')
        
        # Take full page screenshot
        await page.screenshot(path='site_review_full.png', full_page=True)
        
        # Find all links on the page
        links = await page.evaluate('''
            () => {
                const links = [];
                const allLinks = document.querySelectorAll('a[href]');
                
                allLinks.forEach((link, index) => {
                    const href = link.getAttribute('href');
                    const text = link.textContent.trim();
                    const classes = link.className;
                    const isExternal = href.startsWith('http') || href.startsWith('//');
                    const isAnchor = href.startsWith('#');
                    const isFile = href.includes('.pdf') || href.includes('.html');
                    
                    links.push({
                        index: index,
                        href: href,
                        text: text,
                        classes: classes,
                        isExternal: isExternal,
                        isAnchor: isAnchor,
                        isFile: isFile,
                        visible: link.offsetParent !== null
                    });
                });
                
                return links;
            }
        ''')
        
        print(f"📊 Found {len(links)} links on the page")
        
        # Test each link
        broken_links = []
        working_links = []
        
        for link_info in links:
            href = link_info['href']
            text = link_info['text']
            
            print(f"🔗 Testing link: '{text}' -> {href}")
            
            try:
                if link_info['isAnchor']:
                    # Test anchor links by checking if target exists
                    anchor_id = href[1:]  # Remove the #
                    target_exists = await page.evaluate(f'''
                        () => {{
                            const element = document.getElementById('{anchor_id}');
                            return element !== null;
                        }}
                    ''')
                    
                    if target_exists:
                        working_links.append({
                            'href': href,
                            'text': text,
                            'status': 'anchor_working',
                            'type': 'anchor'
                        })
                    else:
                        broken_links.append({
                            'href': href,
                            'text': text,
                            'status': 'anchor_broken',
                            'type': 'anchor',
                            'error': f'Anchor #{anchor_id} not found'
                        })
                
                elif link_info['isExternal']:
                    # Test external links
                    try:
                        response = await page.goto(href, wait_until='networkidle', timeout=10000)
                        if response.status < 400:
                            working_links.append({
                                'href': href,
                                'text': text,
                                'status': 'external_working',
                                'type': 'external',
                                'status_code': response.status
                            })
                        else:
                            broken_links.append({
                                'href': href,
                                'text': text,
                                'status': 'external_broken',
                                'type': 'external',
                                'status_code': response.status,
                                'error': f'HTTP {response.status}'
                            })
                    except Exception as e:
                        broken_links.append({
                            'href': href,
                            'text': text,
                            'status': 'external_broken',
                            'type': 'external',
                            'error': str(e)
                        })
                
                elif link_info['isFile']:
                    # Test file links
                    file_url = urljoin(base_url, href)
                    try:
                        response = await page.goto(file_url, wait_until='networkidle', timeout=10000)
                        if response.status < 400:
                            working_links.append({
                                'href': href,
                                'text': text,
                                'status': 'file_working',
                                'type': 'file',
                                'status_code': response.status,
                                'full_url': file_url
                            })
                        else:
                            broken_links.append({
                                'href': href,
                                'text': text,
                                'status': 'file_broken',
                                'type': 'file',
                                'status_code': response.status,
                                'full_url': file_url,
                                'error': f'HTTP {response.status}'
                            })
                    except Exception as e:
                        broken_links.append({
                            'href': href,
                            'text': text,
                            'status': 'file_broken',
                            'type': 'file',
                            'full_url': file_url,
                            'error': str(e)
                        })
                
                else:
                    # Test internal page links
                    internal_url = urljoin(base_url, href)
                    try:
                        response = await page.goto(internal_url, wait_until='networkidle', timeout=10000)
                        if response.status < 400:
                            working_links.append({
                                'href': href,
                                'text': text,
                                'status': 'internal_working',
                                'type': 'internal',
                                'status_code': response.status,
                                'full_url': internal_url
                            })
                        else:
                            broken_links.append({
                                'href': href,
                                'text': text,
                                'status': 'internal_broken',
                                'type': 'internal',
                                'status_code': response.status,
                                'full_url': internal_url,
                                'error': f'HTTP {response.status}'
                            })
                    except Exception as e:
                        broken_links.append({
                            'href': href,
                            'text': text,
                            'status': 'internal_broken',
                            'type': 'internal',
                            'full_url': internal_url,
                            'error': str(e)
                        })
                
                # Navigate back to main page for next test
                await page.goto(base_url)
                await page.wait_for_load_state('networkidle')
                
            except Exception as e:
                broken_links.append({
                    'href': href,
                    'text': text,
                    'status': 'test_failed',
                    'type': 'unknown',
                    'error': str(e)
                })
        
        # Check for missing sections that links point to
        missing_sections = []
        for link in links:
            if link['isAnchor']:
                section_id = link['href'][1:]
                section_exists = await page.evaluate(f'''
                    () => {{
                        const element = document.getElementById('{section_id}');
                        return element !== null;
                    }}
                ''')
                if not section_exists:
                    missing_sections.append(section_id)
        
        # Generate comprehensive report
        report = {
            'timestamp': datetime.now().isoformat(),
            'base_url': base_url,
            'total_links': len(links),
            'working_links': len(working_links),
            'broken_links': len(broken_links),
            'missing_sections': missing_sections,
            'broken_links_details': broken_links,
            'working_links_details': working_links,
            'screenshots': ['site_review_full.png']
        }
        
        # Save detailed report
        with open('site_review_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Site Review Complete:")
        print(f"   Total links found: {len(links)}")
        print(f"   Working links: {len(working_links)}")
        print(f"   Broken links: {len(broken_links)}")
        print(f"   Missing sections: {len(missing_sections)}")
        
        if broken_links:
            print(f"\n❌ Broken Links Found:")
            for link in broken_links:
                print(f"   - '{link['text']}' -> {link['href']} ({link['status']})")
                if 'error' in link:
                    print(f"     Error: {link['error']}")
        
        if missing_sections:
            print(f"\n⚠️  Missing Sections:")
            for section in missing_sections:
                print(f"   - #{section}")
        
        print(f"\n📁 Report saved: site_review_report.json")
        print(f"📸 Screenshot saved: site_review_full.png")
        
        await browser.close()
        return report

if __name__ == "__main__":
    asyncio.run(review_site())