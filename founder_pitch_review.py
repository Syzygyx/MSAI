#!/usr/bin/env python3
"""
Comprehensive founder pitch review of the MS AI program site
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def founder_pitch_review():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        print("🎓 Conducting Founder Pitch Review...")
        
        # Review main site
        await page.goto('https://syzygyx.github.io/MSAI/')
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path='founder_review_main.png', full_page=True)
        
        # Review course catalog
        await page.goto('https://syzygyx.github.io/MSAI/course-catalog.html')
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path='founder_review_courses.png', full_page=True)
        
        # Review white paper
        await page.goto('https://syzygyx.github.io/MSAI/white-paper.html')
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path='founder_review_whitepaper.png', full_page=True)
        
        # Review application form
        await page.goto('https://syzygyx.github.io/MSAI/msai_application_form.html')
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path='founder_review_application.png', full_page=True)
        
        # Analyze content effectiveness
        content_analysis = await page.evaluate('''
            () => {
                // Go back to main page for analysis
                window.location.href = 'https://syzygyx.github.io/MSAI/';
                return new Promise((resolve) => {
                    setTimeout(() => {
                        const analysis = {
                            hero_section: {
                                title: document.querySelector('.hero h1')?.textContent || '',
                                subtitle: document.querySelector('.hero h2')?.textContent || '',
                                description: document.querySelector('.hero p')?.textContent || '',
                                cta_buttons: Array.from(document.querySelectorAll('.cta-buttons a')).map(a => ({
                                    text: a.textContent.trim(),
                                    href: a.href
                                }))
                            },
                            program_highlights: {
                                sections: Array.from(document.querySelectorAll('.section h2')).map(h2 => h2.textContent.trim()),
                                cards: Array.from(document.querySelectorAll('.card h3')).map(h3 => h3.textContent.trim())
                            },
                            navigation: {
                                links: Array.from(document.querySelectorAll('.nav-links a')).map(a => ({
                                    text: a.textContent.trim(),
                                    href: a.href
                                }))
                            },
                            credibility_indicators: {
                                has_white_paper: document.querySelector('a[href*="white-paper"]') !== null,
                                has_course_catalog: document.querySelector('a[href*="course-catalog"]') !== null,
                                has_application: document.querySelector('a[href*="application"]') !== null,
                                has_contact: document.querySelector('a[href*="mailto"]') !== null
                            }
                        };
                        resolve(analysis);
                    }, 2000);
                });
            }
        ''')
        
        # Generate founder pitch assessment
        assessment = {
            'timestamp': datetime.now().isoformat(),
            'reviewer_perspective': 'University Founder Pitching MS AI Program',
            'target_audiences': ['Prospective Students', 'Faculty Recruits', 'Industry Partners', 'Accreditors', 'Investors'],
            'content_analysis': content_analysis,
            'strengths': [],
            'weaknesses': [],
            'recommendations': [],
            'pitch_effectiveness_score': 0,
            'screenshots': [
                'founder_review_main.png',
                'founder_review_courses.png', 
                'founder_review_whitepaper.png',
                'founder_review_application.png'
            ]
        }
        
        # Assess strengths
        strengths = []
        
        # Innovation and Vision
        if 'ARTIFICIAL INTELLIGENCE' in content_analysis.get('hero_section', {}).get('title', ''):
            strengths.append("Clear, bold program title that immediately communicates focus")
        
        if 'Revolutionary AI Education Program' in content_analysis.get('hero_section', {}).get('description', ''):
            strengths.append("Strong value proposition emphasizing innovation and accessibility")
        
        # Academic Rigor
        if content_analysis.get('credibility_indicators', {}).get('has_white_paper', False):
            strengths.append("Comprehensive white paper demonstrates academic depth and planning")
        
        if content_analysis.get('credibility_indicators', {}).get('has_course_catalog', False):
            strengths.append("Detailed course catalog shows structured curriculum and academic rigor")
        
        # Accessibility
        if any('any academic background' in str(section).lower() for section in content_analysis.get('program_highlights', {}).get('sections', [])):
            strengths.append("Emphasizes accessibility to students from diverse backgrounds")
        
        # Professional Presentation
        if len(content_analysis.get('hero_section', {}).get('cta_buttons', [])) >= 2:
            strengths.append("Multiple clear call-to-action buttons for different user intents")
        
        # Assess weaknesses
        weaknesses = []
        
        # Missing Elements
        if not content_analysis.get('credibility_indicators', {}).get('has_contact', False):
            weaknesses.append("No clear contact information or admissions office details")
        
        # Faculty Information
        faculty_section = any('faculty' in section.lower() for section in content_analysis.get('program_highlights', {}).get('sections', []))
        if not faculty_section:
            weaknesses.append("Limited faculty information - critical for academic credibility")
        
        # Tuition and Financial Information
        if not any('tuition' in section.lower() or 'cost' in section.lower() or 'financial' in section.lower() for section in content_analysis.get('program_highlights', {}).get('sections', [])):
            weaknesses.append("No tuition or financial information - essential for student decision-making")
        
        # Accreditation Information
        if not any('accreditation' in section.lower() or 'accredited' in section.lower() for section in content_analysis.get('program_highlights', {}).get('sections', [])):
            weaknesses.append("Accreditation status not prominently displayed - critical for credibility")
        
        # Student Outcomes and Career Information
        if not any('career' in section.lower() or 'outcome' in section.lower() or 'job' in section.lower() for section in content_analysis.get('program_highlights', {}).get('sections', [])):
            weaknesses.append("Limited information about career outcomes and job prospects")
        
        # Generate recommendations
        recommendations = []
        
        # Immediate Improvements
        recommendations.append("Add prominent faculty profiles with credentials and research areas")
        recommendations.append("Include tuition costs, financial aid options, and payment plans")
        recommendations.append("Display accreditation status prominently (SACSCOC, ABET)")
        recommendations.append("Add contact information for admissions and program inquiries")
        recommendations.append("Include student testimonials and success stories")
        recommendations.append("Add career outcomes data and job placement statistics")
        
        # Strategic Enhancements
        recommendations.append("Create faculty recruitment page to attract top AI researchers")
        recommendations.append("Add industry partnership showcase and corporate sponsors")
        recommendations.append("Include research highlights and faculty publications")
        recommendations.append("Add virtual campus tour or program preview video")
        recommendations.append("Create alumni network page and professional connections")
        
        # Marketing Improvements
        recommendations.append("Add social proof through industry endorsements and media coverage")
        recommendations.append("Include program comparison with other AI degrees")
        recommendations.append("Add application deadline and admission requirements timeline")
        recommendations.append("Create downloadable program brochure and fact sheet")
        
        # Calculate pitch effectiveness score
        score = 0
        score += len(strengths) * 10  # 10 points per strength
        score -= len(weaknesses) * 5  # -5 points per weakness
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
        
        print(f"\n📊 Founder Pitch Assessment Complete:")
        print(f"   Pitch Effectiveness Score: {score}/100")
        print(f"   Strengths identified: {len(strengths)}")
        print(f"   Weaknesses identified: {len(weaknesses)}")
        print(f"   Recommendations: {len(recommendations)}")
        
        print(f"\n✅ Key Strengths:")
        for strength in strengths:
            print(f"   • {strength}")
        
        print(f"\n⚠️  Critical Weaknesses:")
        for weakness in weaknesses:
            print(f"   • {weakness}")
        
        print(f"\n💡 Top Recommendations:")
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"   {i}. {rec}")
        
        print(f"\n📁 Detailed report saved: founder_pitch_assessment.json")
        print(f"📸 Screenshots saved: founder_review_*.png")
        
        await browser.close()
        return assessment

if __name__ == "__main__":
    asyncio.run(founder_pitch_review())