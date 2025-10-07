#!/usr/bin/env python3
"""
Evaluate header improvements using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def evaluate_header():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        print("🔍 Evaluating header improvements...")
        
        # Navigate to the site
        await page.goto('https://syzygyx.github.io/MSAI/')
        await page.wait_for_load_state('networkidle')
        
        # Take full page screenshot
        await page.screenshot(path='header_evaluation_full.png', full_page=True)
        
        # Take header-specific screenshot
        header_element = await page.query_selector('.header')
        if header_element:
            await header_element.screenshot(path='header_evaluation_detail.png')
        
        # Check header animations and styling
        header_analysis = await page.evaluate('''
            () => {
                const header = document.querySelector('.header');
                const logo = document.querySelector('.logo');
                const navLinks = document.querySelectorAll('.nav-links a');
                const dynamicLines = document.querySelectorAll('.dynamic-line-1, .dynamic-line-2');
                
                if (!header) return { error: 'Header not found' };
                
                // Check header styles
                const headerStyles = {
                    background: getComputedStyle(header).background,
                    borderBottom: getComputedStyle(header).borderBottom,
                    boxShadow: getComputedStyle(header).boxShadow,
                    backdropFilter: getComputedStyle(header).backdropFilter
                };
                
                // Check logo styles
                const logoStyles = {
                    fontSize: getComputedStyle(logo).fontSize,
                    fontWeight: getComputedStyle(logo).fontWeight,
                    letterSpacing: getComputedStyle(logo).letterSpacing,
                    padding: getComputedStyle(logo).padding,
                    borderRadius: getComputedStyle(logo).borderRadius,
                    border: getComputedStyle(logo).border
                };
                
                // Check navigation styles
                const navStyles = {
                    display: getComputedStyle(document.querySelector('.nav')).display,
                    justifyContent: getComputedStyle(document.querySelector('.nav')).justifyContent,
                    alignItems: getComputedStyle(document.querySelector('.nav')).alignItems,
                    padding: getComputedStyle(document.querySelector('.nav')).padding,
                    maxWidth: getComputedStyle(document.querySelector('.nav')).maxWidth
                };
                
                // Check nav links
                const navLinkStyles = [];
                navLinks.forEach((link, index) => {
                    navLinkStyles.push({
                        index: index,
                        display: getComputedStyle(link).display,
                        fontSize: getComputedStyle(link).fontSize,
                        fontWeight: getComputedStyle(link).fontWeight,
                        padding: getComputedStyle(link).padding,
                        borderRadius: getComputedStyle(link).borderRadius,
                        background: getComputedStyle(link).background,
                        text: link.textContent.trim()
                    });
                });
                
                // Check dynamic lines
                const dynamicLineInfo = [];
                dynamicLines.forEach((line, index) => {
                    dynamicLineInfo.push({
                        index: index,
                        className: line.className,
                        position: getComputedStyle(line).position,
                        top: getComputedStyle(line).top,
                        height: getComputedStyle(line).height,
                        background: getComputedStyle(line).background,
                        animation: getComputedStyle(line).animation
                    });
                });
                
                // Check for CSS animations
                const animations = [];
                const styleSheets = document.styleSheets;
                for (let i = 0; i < styleSheets.length; i++) {
                    try {
                        const rules = styleSheets[i].cssRules;
                        for (let j = 0; j < rules.length; j++) {
                            if (rules[j].type === CSSRule.KEYFRAMES_RULE) {
                                animations.push({
                                    name: rules[j].name,
                                    type: 'keyframes'
                                });
                            }
                        }
                    } catch (e) {
                        // Cross-origin stylesheets may throw errors
                    }
                }
                
                return {
                    headerStyles,
                    logoStyles,
                    navStyles,
                    navLinkStyles,
                    dynamicLineInfo,
                    animations: animations.filter(a => a.name.includes('header-line')),
                    navLinksCount: navLinks.length,
                    dynamicLinesCount: dynamicLines.length
                };
            }
        ''')
        
        # Check title formatting
        title_analysis = await page.evaluate('''
            () => {
                const heroTitle = document.querySelector('.hero h1');
                if (!heroTitle) return { error: 'Hero title not found' };
                
                return {
                    textContent: heroTitle.textContent,
                    innerHTML: heroTitle.innerHTML,
                    fontSize: getComputedStyle(heroTitle).fontSize,
                    fontWeight: getComputedStyle(heroTitle).fontWeight,
                    lineHeight: getComputedStyle(heroTitle).lineHeight,
                    textAlign: getComputedStyle(heroTitle).textAlign
                };
            }
        ''')
        
        # Generate comprehensive report
        report = {
            'timestamp': datetime.now().isoformat(),
            'url': 'https://syzygyx.github.io/MSAI/',
            'header_analysis': header_analysis,
            'title_analysis': title_analysis,
            'screenshots': [
                'header_evaluation_full.png',
                'header_evaluation_detail.png'
            ],
            'evaluation_summary': {
                'dynamic_lines_present': header_analysis.get('dynamicLinesCount', 0) > 0,
                'animations_loaded': len(header_analysis.get('animations', [])) > 0,
                'professional_styling': header_analysis.get('logoStyles', {}).get('fontWeight') == '800',
                'title_properly_formatted': 'ARTIFICIAL INTELLIGENCE' in title_analysis.get('innerHTML', ''),
                'navigation_improved': header_analysis.get('navStyles', {}).get('maxWidth') != 'none'
            }
        }
        
        # Save detailed report
        with open('header_evaluation_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Header Evaluation Complete:")
        print(f"   Dynamic lines present: {report['evaluation_summary']['dynamic_lines_present']}")
        print(f"   Animations loaded: {report['evaluation_summary']['animations_loaded']}")
        print(f"   Professional styling: {report['evaluation_summary']['professional_styling']}")
        print(f"   Title properly formatted: {report['evaluation_summary']['title_properly_formatted']}")
        print(f"   Navigation improved: {report['evaluation_summary']['navigation_improved']}")
        print(f"   Nav links count: {header_analysis.get('navLinksCount', 0)}")
        print(f"   Dynamic lines count: {header_analysis.get('dynamicLinesCount', 0)}")
        print(f"   Animations found: {len(header_analysis.get('animations', []))}")
        print(f"   Screenshots saved: header_evaluation_full.png, header_evaluation_detail.png")
        print(f"   Report saved: header_evaluation_report.json")
        
        await browser.close()
        return report

if __name__ == "__main__":
    asyncio.run(evaluate_header())