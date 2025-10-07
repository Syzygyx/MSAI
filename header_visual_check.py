#!/usr/bin/env python3
"""
Visual check of header issues using Playwright
"""

import asyncio
from playwright.async_api import async_playwright

async def check_header_visual():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        print("🔍 Checking header visual issues...")
        
        # Navigate to the site
        await page.goto('https://syzygyx.github.io/MSAI/')
        await page.wait_for_load_state('networkidle')
        
        # Take header screenshot
        header_element = await page.query_selector('.header')
        if header_element:
            await header_element.screenshot(path='header_current_state.png')
            print("📸 Header screenshot saved: header_current_state.png")
        
        # Check header dimensions and layout
        header_info = await page.evaluate('''
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
                        top: header.offsetTop,
                        left: header.offsetLeft
                    },
                    nav: {
                        width: nav.offsetWidth,
                        height: nav.offsetHeight,
                        display: getComputedStyle(nav).display,
                        justifyContent: getComputedStyle(nav).justifyContent,
                        alignItems: getComputedStyle(nav).alignItems
                    },
                    logo: {
                        width: logo.offsetWidth,
                        height: logo.offsetHeight,
                        fontSize: getComputedStyle(logo).fontSize,
                        fontWeight: getComputedStyle(logo).fontWeight
                    },
                    navLinks: Array.from(navLinks).map(link => ({
                        text: link.textContent.trim(),
                        width: link.offsetWidth,
                        height: link.offsetHeight,
                        display: getComputedStyle(link).display
                    }))
                };
            }
        ''')
        
        print("📊 Header Analysis:")
        print(f"   Header dimensions: {header_info.get('header', {}).get('width', 0)}x{header_info.get('header', {}).get('height', 0)}")
        print(f"   Nav dimensions: {header_info.get('nav', {}).get('width', 0)}x{header_info.get('nav', {}).get('height', 0)}")
        print(f"   Logo dimensions: {header_info.get('logo', {}).get('width', 0)}x{header_info.get('logo', {}).get('height', 0)}")
        print(f"   Nav links count: {len(header_info.get('navLinks', []))}")
        
        # Check for layout issues
        issues = []
        
        # Check if nav is properly centered
        nav_width = header_info.get('nav', {}).get('width', 0)
        header_width = header_info.get('header', {}).get('width', 0)
        if nav_width < header_width * 0.8:
            issues.append("Navigation not utilizing full width")
        
        # Check logo size
        logo_font_size = header_info.get('logo', {}).get('fontSize', '0px')
        if 'px' in logo_font_size:
            logo_size = float(logo_font_size.replace('px', ''))
            if logo_size < 30:
                issues.append("Logo font size too small")
            elif logo_size > 50:
                issues.append("Logo font size too large")
        
        # Check nav links
        nav_links = header_info.get('navLinks', [])
        for i, link in enumerate(nav_links):
            if link.get('display') != 'inline-block':
                issues.append(f"Nav link {i} ({link.get('text')}) not using inline-block")
        
        if issues:
            print("\n⚠️  Issues found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("\n✅ No obvious layout issues detected")
        
        await browser.close()
        return header_info

if __name__ == "__main__":
    asyncio.run(check_header_visual())