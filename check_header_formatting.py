#!/usr/bin/env python3
"""
Check header formatting issues using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def check_header_formatting():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        print("🔍 Checking header formatting...")
        
        # Navigate to the site
        await page.goto('https://syzygyx.github.io/MSAI/')
        await page.wait_for_load_state('networkidle')
        
        # Take full page screenshot
        await page.screenshot(path='header_full_page.png', full_page=True)
        
        # Take header-specific screenshot
        header_element = await page.query_selector('.header')
        if header_element:
            await header_element.screenshot(path='header_element.png')
        
        # Check header styles
        header_styles = await page.evaluate('''
            () => {
                const header = document.querySelector('.header');
                const nav = document.querySelector('.nav');
                const logo = document.querySelector('.logo');
                const navLinks = document.querySelectorAll('.nav-links a');
                
                if (!header) return { error: 'Header not found' };
                
                const computedStyles = {
                    header: {
                        display: getComputedStyle(header).display,
                        flexDirection: getComputedStyle(header).flexDirection,
                        alignItems: getComputedStyle(header).alignItems,
                        justifyContent: getComputedStyle(header).justifyContent,
                        padding: getComputedStyle(header).padding,
                        margin: getComputedStyle(header).margin,
                        width: getComputedStyle(header).width,
                        height: getComputedStyle(header).height
                    },
                    nav: {
                        display: getComputedStyle(nav).display,
                        flexDirection: getComputedStyle(nav).flexDirection,
                        alignItems: getComputedStyle(nav).alignItems,
                        justifyContent: getComputedStyle(nav).justifyContent,
                        padding: getComputedStyle(nav).padding,
                        margin: getComputedStyle(nav).margin,
                        width: getComputedStyle(nav).width,
                        height: getComputedStyle(nav).height
                    },
                    logo: {
                        display: getComputedStyle(logo).display,
                        fontSize: getComputedStyle(logo).fontSize,
                        padding: getComputedStyle(logo).padding,
                        margin: getComputedStyle(logo).margin,
                        width: getComputedStyle(logo).width,
                        height: getComputedStyle(logo).height
                    }
                };
                
                // Check nav links
                const navLinkStyles = [];
                navLinks.forEach((link, index) => {
                    navLinkStyles.push({
                        index: index,
                        display: getComputedStyle(link).display,
                        fontSize: getComputedStyle(link).fontSize,
                        padding: getComputedStyle(link).padding,
                        margin: getComputedStyle(link).margin,
                        width: getComputedStyle(link).width,
                        height: getComputedStyle(link).height,
                        text: link.textContent.trim()
                    });
                });
                
                return {
                    computedStyles,
                    navLinkStyles,
                    navLinksCount: navLinks.length
                };
            }
        ''')
        
        # Check for layout issues
        layout_issues = []
        
        # Check if nav is flexbox
        if header_styles.get('computedStyles', {}).get('nav', {}).get('display') != 'flex':
            layout_issues.append('Nav is not using flexbox display')
        
        # Check if nav direction is row
        if header_styles.get('computedStyles', {}).get('nav', {}).get('flexDirection') != 'row':
            layout_issues.append('Nav flex-direction is not row')
        
        # Check nav links
        nav_links = header_styles.get('navLinkStyles', [])
        for link in nav_links:
            if link.get('display') != 'block' and link.get('display') != 'inline-block':
                layout_issues.append(f'Nav link {link.get("index")} has incorrect display: {link.get("display")}')
        
        # Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'url': 'https://syzygyx.github.io/MSAI/',
            'header_styles': header_styles,
            'layout_issues': layout_issues,
            'screenshots': [
                'header_full_page.png',
                'header_element.png'
            ]
        }
        
        # Save report
        with open('header_formatting_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Header Analysis Complete:")
        print(f"   Layout issues found: {len(layout_issues)}")
        if layout_issues:
            print("   Issues:")
            for issue in layout_issues:
                print(f"     - {issue}")
        
        print(f"   Nav links count: {header_styles.get('navLinksCount', 0)}")
        print(f"   Screenshots saved: header_full_page.png, header_element.png")
        print(f"   Report saved: header_formatting_report.json")
        
        await browser.close()
        return report

if __name__ == "__main__":
    asyncio.run(check_header_formatting())