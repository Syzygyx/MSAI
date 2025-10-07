#!/usr/bin/env python3
"""
Evaluate readability of the Tron-styled site using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def evaluate_readability():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        print("🔍 Evaluating readability of Tron-styled site...")
        
        # Navigate to the site
        await page.goto('https://syzygyx.github.io/MSAI/')
        await page.wait_for_load_state('networkidle')
        
        # Take screenshots
        await page.screenshot(path='tron_site_full.png', full_page=True)
        await page.screenshot(path='tron_site_viewport.png')
        
        # Evaluate text readability
        readability_issues = []
        
        # Check main headings
        headings = await page.query_selector_all('h1, h2, h3, h4, h5, h6')
        for i, heading in enumerate(headings):
            text = await heading.inner_text()
            styles = await heading.evaluate('''
                (element) => {
                    const computed = window.getComputedStyle(element);
                    return {
                        color: computed.color,
                        textShadow: computed.textShadow,
                        fontSize: computed.fontSize,
                        fontWeight: computed.fontWeight,
                        opacity: computed.opacity
                    };
                }
            ''')
            
            # Check if text has excessive glow
            if '0 0' in styles['textShadow'] and 'px' in styles['textShadow']:
                shadow_parts = styles['textShadow'].split(' ')
                if len(shadow_parts) >= 3:
                    try:
                        blur_radius = int(shadow_parts[2].replace('px', ''))
                        if blur_radius > 20:
                            readability_issues.append({
                                'element': f'Heading {i+1}',
                                'text': text[:50] + '...' if len(text) > 50 else text,
                                'issue': f'Excessive glow (blur: {blur_radius}px)',
                                'styles': styles
                            })
                    except:
                        pass
        
        # Check paragraphs and body text
        paragraphs = await page.query_selector_all('p, li, span')
        for i, para in enumerate(paragraphs[:10]):  # Check first 10 paragraphs
            text = await para.inner_text()
            if text.strip():
                styles = await para.evaluate('''
                    (element) => {
                        const computed = window.getComputedStyle(element);
                        return {
                            color: computed.color,
                            textShadow: computed.textShadow,
                            fontSize: computed.fontSize,
                            fontWeight: computed.fontWeight,
                            opacity: computed.opacity,
                            backgroundColor: computed.backgroundColor
                        };
                    }
                ''')
                
                # Check contrast and readability
                if '0 0' in styles['textShadow'] and 'px' in styles['textShadow']:
                    shadow_parts = styles['textShadow'].split(' ')
                    if len(shadow_parts) >= 3:
                        try:
                            blur_radius = int(shadow_parts[2].replace('px', ''))
                            if blur_radius > 15:
                                readability_issues.append({
                                    'element': f'Paragraph {i+1}',
                                    'text': text[:50] + '...' if len(text) > 50 else text,
                                    'issue': f'Excessive glow (blur: {blur_radius}px)',
                                    'styles': styles
                                })
                        except:
                            pass
        
        # Check form elements
        form_elements = await page.query_selector_all('input, textarea, select, label')
        for i, element in enumerate(form_elements[:10]):
            text = await element.inner_text()
            if text.strip():
                styles = await element.evaluate('''
                    (element) => {
                        const computed = window.getComputedStyle(element);
                        return {
                            color: computed.color,
                            textShadow: computed.textShadow,
                            fontSize: computed.fontSize,
                            fontWeight: computed.fontWeight,
                            opacity: computed.opacity,
                            borderColor: computed.borderColor,
                            boxShadow: computed.boxShadow
                        };
                    }
                ''')
                
                # Check if form elements are readable
                if '0 0' in styles['textShadow'] and 'px' in styles['textShadow']:
                    shadow_parts = styles['textShadow'].split(' ')
                    if len(shadow_parts) >= 3:
                        try:
                            blur_radius = int(shadow_parts[2].replace('px', ''))
                            if blur_radius > 10:
                                readability_issues.append({
                                    'element': f'Form element {i+1}',
                                    'text': text[:50] + '...' if len(text) > 50 else text,
                                    'issue': f'Excessive glow (blur: {blur_radius}px)',
                                    'styles': styles
                                })
                        except:
                            pass
        
        # Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'url': 'https://syzygyx.github.io/MSAI/',
            'total_issues': len(readability_issues),
            'issues': readability_issues,
            'recommendations': [
                'Reduce text-shadow blur radius for better readability',
                'Consider using subtle glow effects instead of strong ones',
                'Ensure sufficient contrast between text and background',
                'Test readability on different screen sizes and devices'
            ]
        }
        
        # Save report
        with open('readability_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Found {len(readability_issues)} readability issues")
        print("📄 Report saved to readability_report.json")
        print("📸 Screenshots saved: tron_site_full.png, tron_site_viewport.png")
        
        # Print summary
        if readability_issues:
            print("\n🚨 Readability Issues Found:")
            for issue in readability_issues[:5]:  # Show first 5 issues
                print(f"  - {issue['element']}: {issue['issue']}")
                print(f"    Text: {issue['text']}")
                print()
        
        await browser.close()
        return report

if __name__ == "__main__":
    asyncio.run(evaluate_readability())