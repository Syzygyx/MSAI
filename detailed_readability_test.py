#!/usr/bin/env python3
"""
Detailed readability test for Tron-styled site
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def detailed_readability_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        print("🔍 Running detailed readability analysis...")
        
        # Navigate to both pages
        pages_to_test = [
            ('https://syzygyx.github.io/MSAI/', 'main_page'),
            ('https://syzygyx.github.io/MSAI/msai_application_form.html', 'application_form')
        ]
        
        all_issues = []
        
        for url, page_name in pages_to_test:
            print(f"📄 Testing {page_name}...")
            await page.goto(url)
            await page.wait_for_load_state('networkidle')
            
            # Take screenshots
            await page.screenshot(path=f'{page_name}_full.png', full_page=True)
            await page.screenshot(path=f'{page_name}_viewport.png')
            
            # Analyze text elements
            text_elements = await page.query_selector_all('h1, h2, h3, h4, h5, h6, p, li, span, label, input, textarea, button')
            
            for i, element in enumerate(text_elements):
                try:
                    text = await element.inner_text()
                    if not text.strip():
                        continue
                        
                    # Get computed styles
                    styles = await element.evaluate('''
                        (element) => {
                            const computed = window.getComputedStyle(element);
                            return {
                                color: computed.color,
                                textShadow: computed.textShadow,
                                fontSize: computed.fontSize,
                                fontWeight: computed.fontWeight,
                                opacity: computed.opacity,
                                backgroundColor: computed.backgroundColor,
                                borderColor: computed.borderColor,
                                boxShadow: computed.boxShadow,
                                fontFamily: computed.fontFamily
                            };
                        }
                    ''')
                    
                    # Analyze text shadow intensity
                    text_shadow = styles['textShadow']
                    if text_shadow and text_shadow != 'none':
                        # Parse text shadow values
                        shadow_parts = text_shadow.split(',')
                        max_blur = 0
                        glow_count = 0
                        
                        for shadow in shadow_parts:
                            parts = shadow.strip().split(' ')
                            if len(parts) >= 3:
                                try:
                                    blur = int(parts[2].replace('px', ''))
                                    max_blur = max(max_blur, blur)
                                    if blur > 10:
                                        glow_count += 1
                                except:
                                    pass
                        
                        # Check for excessive glow
                        if max_blur > 25:
                            all_issues.append({
                                'page': page_name,
                                'element_type': element.tag_name.lower(),
                                'text_preview': text[:100] + '...' if len(text) > 100 else text,
                                'issue_type': 'excessive_glow',
                                'blur_radius': max_blur,
                                'glow_count': glow_count,
                                'styles': styles
                            })
                        
                        # Check for multiple overlapping glows
                        if glow_count > 2:
                            all_issues.append({
                                'page': page_name,
                                'element_type': element.tag_name.lower(),
                                'text_preview': text[:100] + '...' if len(text) > 100 else text,
                                'issue_type': 'multiple_glows',
                                'blur_radius': max_blur,
                                'glow_count': glow_count,
                                'styles': styles
                            })
                    
                    # Check font size vs glow ratio
                    try:
                        font_size = int(styles['fontSize'].replace('px', ''))
                        if max_blur > 0 and font_size > 0:
                            glow_ratio = max_blur / font_size
                            if glow_ratio > 0.5:  # Glow is more than half the font size
                                all_issues.append({
                                    'page': page_name,
                                    'element_type': element.tag_name.lower(),
                                    'text_preview': text[:100] + '...' if len(text) > 100 else text,
                                    'issue_type': 'high_glow_ratio',
                                    'glow_ratio': round(glow_ratio, 2),
                                    'font_size': font_size,
                                    'blur_radius': max_blur,
                                    'styles': styles
                                })
                    except:
                        pass
                        
                except Exception as e:
                    print(f"Error analyzing element {i}: {e}")
                    continue
        
        # Generate detailed report
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_issues': len(all_issues),
            'issues_by_type': {},
            'issues_by_page': {},
            'recommendations': [
                'Reduce text-shadow blur radius to 10-15px maximum',
                'Limit glow effects to headings only, not body text',
                'Use subtle glow (5-10px blur) for better readability',
                'Consider removing glow from form elements',
                'Test on different screen sizes and zoom levels'
            ],
            'detailed_issues': all_issues
        }
        
        # Categorize issues
        for issue in all_issues:
            issue_type = issue['issue_type']
            page = issue['page']
            
            if issue_type not in report['issues_by_type']:
                report['issues_by_type'][issue_type] = 0
            report['issues_by_type'][issue_type] += 1
            
            if page not in report['issues_by_page']:
                report['issues_by_page'][page] = 0
            report['issues_by_page'][page] += 1
        
        # Save report
        with open('detailed_readability_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Detailed Analysis Complete:")
        print(f"   Total issues found: {len(all_issues)}")
        print(f"   Issues by type: {report['issues_by_type']}")
        print(f"   Issues by page: {report['issues_by_page']}")
        
        # Show top issues
        if all_issues:
            print(f"\n🚨 Top Readability Issues:")
            for i, issue in enumerate(all_issues[:10]):
                print(f"   {i+1}. {issue['page']} - {issue['element_type']}: {issue['issue_type']}")
                print(f"      Text: {issue['text_preview']}")
                if 'blur_radius' in issue:
                    print(f"      Blur: {issue['blur_radius']}px")
                if 'glow_ratio' in issue:
                    print(f"      Glow ratio: {issue['glow_ratio']}")
                print()
        
        await browser.close()
        return report

if __name__ == "__main__":
    asyncio.run(detailed_readability_test())