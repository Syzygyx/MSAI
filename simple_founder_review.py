#!/usr/bin/env python3
"""
Simple founder pitch review of the MS AI program site
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def simple_founder_review():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        print("🎓 Conducting Founder Pitch Review...")
        
        # Review main site
        await page.goto('https://syzygyx.github.io/MSAI/')
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path='founder_review_main.png', full_page=True)
        
        # Get main page content
        main_content = await page.evaluate('''
            () => {
                return {
                    hero_title: document.querySelector('.hero h1')?.textContent || '',
                    hero_subtitle: document.querySelector('.hero h2')?.textContent || '',
                    hero_description: document.querySelector('.hero p')?.textContent || '',
                    cta_buttons: Array.from(document.querySelectorAll('.cta-buttons a')).map(a => a.textContent.trim()),
                    section_titles: Array.from(document.querySelectorAll('.section h2')).map(h2 => h2.textContent.trim()),
                    card_titles: Array.from(document.querySelectorAll('.card h3')).map(h3 => h3.textContent.trim()),
                    nav_links: Array.from(document.querySelectorAll('.nav-links a')).map(a => a.textContent.trim()),
                    has_white_paper: document.querySelector('a[href*="white-paper"]') !== null,
                    has_course_catalog: document.querySelector('a[href*="course-catalog"]') !== null,
                    has_application: document.querySelector('a[href*="application"]') !== null,
                    has_contact: document.querySelector('a[href*="mailto"]') !== null
                };
            }
        ''')
        
        # Review course catalog
        await page.goto('https://syzygyx.github.io/MSAI/course-catalog.html')
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path='founder_review_courses.png', full_page=True)
        
        course_content = await page.evaluate('''
            () => {
                return {
                    page_title: document.querySelector('.hero h1')?.textContent || '',
                    course_categories: Array.from(document.querySelectorAll('.category-title')).map(h3 => h3.textContent.trim()),
                    course_count: document.querySelectorAll('.course-card').length,
                    has_core_courses: document.querySelector('.category-title')?.textContent.includes('CORE') || false,
                    has_electives: Array.from(document.querySelectorAll('.category-title')).some(h3 => h3.textContent.includes('ELECTIVE')),
                    has_thesis: Array.from(document.querySelectorAll('.category-title')).some(h3 => h3.textContent.includes('THESIS'))
                };
            }
        ''')
        
        # Review white paper
        await page.goto('https://syzygyx.github.io/MSAI/white-paper.html')
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path='founder_review_whitepaper.png', full_page=True)
        
        whitepaper_content = await page.evaluate('''
            () => {
                return {
                    title: document.querySelector('.header h1')?.textContent || '',
                    subtitle: document.querySelector('.subtitle')?.textContent || '',
                    toc_sections: Array.from(document.querySelectorAll('.toc a')).map(a => a.textContent.trim()),
                    has_executive_summary: Array.from(document.querySelectorAll('.toc a')).some(a => a.textContent.includes('Executive Summary')),
                    has_curriculum: Array.from(document.querySelectorAll('.toc a')).some(a => a.textContent.includes('Curriculum')),
                    has_governance: Array.from(document.querySelectorAll('.toc a')).some(a => a.textContent.includes('Governance'))
                };
            }
        ''')
        
        # Generate assessment
        assessment = {
            'timestamp': datetime.now().isoformat(),
            'reviewer_perspective': 'University Founder Pitching MS AI Program',
            'main_site_analysis': main_content,
            'course_catalog_analysis': course_content,
            'whitepaper_analysis': whitepaper_content,
            'strengths': [],
            'weaknesses': [],
            'recommendations': [],
            'pitch_effectiveness_score': 0
        }
        
        # Analyze strengths
        strengths = []
        
        # Innovation and Vision
        if 'ARTIFICIAL INTELLIGENCE' in main_content.get('hero_title', ''):
            strengths.append("✅ Clear, bold program title that immediately communicates focus")
        
        if 'Revolutionary AI Education Program' in main_content.get('hero_description', ''):
            strengths.append("✅ Strong value proposition emphasizing innovation and accessibility")
        
        if 'AURNOVA UNIVERSITY' in main_content.get('hero_subtitle', ''):
            strengths.append("✅ Professional university branding and institutional identity")
        
        # Academic Rigor
        if main_content.get('has_white_paper', False):
            strengths.append("✅ Comprehensive white paper demonstrates academic depth and planning")
        
        if main_content.get('has_course_catalog', False):
            strengths.append("✅ Detailed course catalog shows structured curriculum and academic rigor")
        
        if course_content.get('course_count', 0) > 10:
            strengths.append("✅ Substantial course offering with comprehensive curriculum")
        
        if course_content.get('has_core_courses', False) and course_content.get('has_electives', False) and course_content.get('has_thesis', False):
            strengths.append("✅ Well-structured program with core, electives, and thesis components")
        
        # Professional Presentation
        if len(main_content.get('cta_buttons', [])) >= 2:
            strengths.append("✅ Multiple clear call-to-action buttons for different user intents")
        
        if len(main_content.get('section_titles', [])) >= 5:
            strengths.append("✅ Comprehensive site sections covering all key program aspects")
        
        # Accessibility
        if any('any academic background' in str(section).lower() for section in main_content.get('section_titles', [])):
            strengths.append("✅ Emphasizes accessibility to students from diverse backgrounds")
        
        # Analyze weaknesses
        weaknesses = []
        
        # Missing Critical Elements
        if not main_content.get('has_contact', False):
            weaknesses.append("❌ No clear contact information or admissions office details")
        
        # Faculty Information
        faculty_section = any('faculty' in section.lower() for section in main_content.get('section_titles', []))
        if not faculty_section:
            weaknesses.append("❌ Limited faculty information - critical for academic credibility")
        
        # Tuition and Financial Information
        if not any('tuition' in section.lower() or 'cost' in section.lower() or 'financial' in section.lower() for section in main_content.get('section_titles', [])):
            weaknesses.append("❌ No tuition or financial information - essential for student decision-making")
        
        # Accreditation Information
        if not any('accreditation' in section.lower() or 'accredited' in section.lower() for section in main_content.get('section_titles', [])):
            weaknesses.append("❌ Accreditation status not prominently displayed - critical for credibility")
        
        # Student Outcomes and Career Information
        if not any('career' in section.lower() or 'outcome' in section.lower() or 'job' in section.lower() for section in main_content.get('section_titles', [])):
            weaknesses.append("❌ Limited information about career outcomes and job prospects")
        
        # Application Process
        if not main_content.get('has_application', False):
            weaknesses.append("❌ No clear application process or admission requirements")
        
        # Generate recommendations
        recommendations = []
        
        # Immediate Critical Additions
        recommendations.append("🔥 Add prominent faculty profiles with credentials and research areas")
        recommendations.append("🔥 Include tuition costs, financial aid options, and payment plans")
        recommendations.append("🔥 Display accreditation status prominently (SACSCOC, ABET)")
        recommendations.append("🔥 Add contact information for admissions and program inquiries")
        recommendations.append("🔥 Include student testimonials and success stories")
        recommendations.append("🔥 Add career outcomes data and job placement statistics")
        
        # Strategic Enhancements
        recommendations.append("📈 Create faculty recruitment page to attract top AI researchers")
        recommendations.append("📈 Add industry partnership showcase and corporate sponsors")
        recommendations.append("📈 Include research highlights and faculty publications")
        recommendations.append("📈 Add virtual campus tour or program preview video")
        recommendations.append("📈 Create alumni network page and professional connections")
        
        # Marketing Improvements
        recommendations.append("🎯 Add social proof through industry endorsements and media coverage")
        recommendations.append("🎯 Include program comparison with other AI degrees")
        recommendations.append("🎯 Add application deadline and admission requirements timeline")
        recommendations.append("🎯 Create downloadable program brochure and fact sheet")
        recommendations.append("🎯 Add FAQ section addressing common concerns")
        
        # Calculate pitch effectiveness score
        score = 0
        score += len(strengths) * 8  # 8 points per strength
        score -= len(weaknesses) * 6  # -6 points per weakness
        score = max(0, min(100, score))  # Clamp between 0-100
        
        assessment.update({
            'strengths': strengths,
            'weaknesses': weaknesses,
            'recommendations': recommendations,
            'pitch_effectiveness_score': score
        })
        
        # Save detailed report
        with open('founder_pitch_assessment.json', 'w') as f:
            json.dump(assessment, f, indent=2)
        
        print(f"\n📊 FOUNDER PITCH ASSESSMENT")
        print(f"=" * 50)
        print(f"🎯 Pitch Effectiveness Score: {score}/100")
        print(f"✅ Strengths identified: {len(strengths)}")
        print(f"❌ Weaknesses identified: {len(weaknesses)}")
        print(f"💡 Recommendations: {len(recommendations)}")
        
        print(f"\n✅ KEY STRENGTHS:")
        for strength in strengths:
            print(f"   {strength}")
        
        print(f"\n❌ CRITICAL WEAKNESSES:")
        for weakness in weaknesses:
            print(f"   {weakness}")
        
        print(f"\n💡 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations[:8], 1):
            print(f"   {i}. {rec}")
        
        print(f"\n📁 Detailed report saved: founder_pitch_assessment.json")
        print(f"📸 Screenshots saved: founder_review_*.png")
        
        await browser.close()
        return assessment

if __name__ == "__main__":
    asyncio.run(simple_founder_review())