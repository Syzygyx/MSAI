#!/usr/bin/env python3
"""
Fix header issues using Playwright analysis
"""

import asyncio
from playwright.async_api import async_playwright

async def fix_header():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        print("🔧 Analyzing header issues...")
        
        # Navigate to the site
        await page.goto('https://syzygyx.github.io/MSAI/')
        await page.wait_for_load_state('networkidle')
        
        # Take header screenshot
        header_element = await page.query_selector('.header')
        if header_element:
            await header_element.screenshot(path='header_before_fix.png')
        
        # Analyze header layout issues
        header_analysis = await page.evaluate('''
            () => {
                const header = document.querySelector('.header');
                const nav = document.querySelector('.nav');
                const logo = document.querySelector('.logo');
                const navLinks = document.querySelectorAll('.nav-links a');
                
                if (!header) return { error: 'Header not found' };
                
                return {
                    header: {
                        width: header.offsetWidth,
                        height: header.offsetHeight,
                        display: getComputedStyle(header).display,
                        position: getComputedStyle(header).position
                    },
                    nav: {
                        width: nav.offsetWidth,
                        height: nav.offsetHeight,
                        display: getComputedStyle(nav).display,
                        flexDirection: getComputedStyle(nav).flexDirection,
                        justifyContent: getComputedStyle(nav).justifyContent,
                        alignItems: getComputedStyle(nav).alignItems,
                        maxWidth: getComputedStyle(nav).maxWidth,
                        margin: getComputedStyle(nav).margin
                    },
                    logo: {
                        width: logo.offsetWidth,
                        height: logo.offsetHeight,
                        fontSize: getComputedStyle(logo).fontSize,
                        margin: getComputedStyle(logo).margin
                    },
                    navLinks: {
                        count: navLinks.length,
                        containerWidth: document.querySelector('.nav-links').offsetWidth,
                        containerDisplay: getComputedStyle(document.querySelector('.nav-links')).display,
                        containerJustifyContent: getComputedStyle(document.querySelector('.nav-links')).justifyContent,
                        containerGap: getComputedStyle(document.querySelector('.nav-links')).gap,
                        links: Array.from(navLinks).map(link => ({
                            text: link.textContent.trim(),
                            width: link.offsetWidth,
                            height: link.offsetHeight,
                            display: getComputedStyle(link).display,
                            fontSize: getComputedStyle(link).fontSize,
                            padding: getComputedStyle(link).padding
                        }))
                    }
                };
            }
        ''')
        
        print("📊 Header Analysis:")
        print(f"   Header: {header_analysis.get('header', {}).get('width', 0)}x{header_analysis.get('header', {}).get('height', 0)}")
        print(f"   Nav: {header_analysis.get('nav', {}).get('width', 0)}x{header_analysis.get('nav', {}).get('height', 0)}")
        print(f"   Logo: {header_analysis.get('logo', {}).get('width', 0)}x{header_analysis.get('logo', {}).get('height', 0)}")
        print(f"   Nav Links: {header_analysis.get('navLinks', {}).get('count', 0)}")
        print(f"   Nav Container Width: {header_analysis.get('navLinks', {}).get('containerWidth', 0)}")
        
        # Identify issues
        issues = []
        
        # Check if nav is using full width
        nav_width = header_analysis.get('nav', {}).get('width', 0)
        header_width = header_analysis.get('header', {}).get('width', 0)
        if nav_width < header_width * 0.9:
            issues.append("Navigation not using full header width")
        
        # Check nav links container
        nav_links_container_width = header_analysis.get('navLinks', {}).get('containerWidth', 0)
        if nav_links_container_width < nav_width * 0.6:
            issues.append("Nav links container too narrow")
        
        # Check logo size
        logo_width = header_analysis.get('logo', {}).get('width', 0)
        if logo_width > nav_width * 0.3:
            issues.append("Logo taking too much space")
        
        # Check nav links spacing
        nav_links = header_analysis.get('navLinks', {}).get('links', [])
        total_links_width = sum(link.get('width', 0) for link in nav_links)
        if total_links_width > nav_links_container_width * 1.1:
            issues.append("Nav links overflowing container")
        
        print(f"\n⚠️  Issues found: {len(issues)}")
        for issue in issues:
            print(f"   - {issue}")
        
        await browser.close()
        return header_analysis

if __name__ == "__main__":
    asyncio.run(fix_header())