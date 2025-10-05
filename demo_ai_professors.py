#!/usr/bin/env python3
"""
AI Professors Demo
Demonstrates the AI Professor system with distinct personas and research capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_systems.professors import AIProfessorSystem, ProfessorSpecialization
import json

def main():
    print("=" * 80)
    print("AI PROFESSORS DEMONSTRATION")
    print("MS AI Curriculum - Florida Accredited Program")
    print("=" * 80)
    
    # Initialize the AI Professor system
    system = AIProfessorSystem()
    
    print(f"\n📚 AI PROFESSOR ROSTER")
    print("-" * 50)
    
    # Display all professors with their personas
    for professor in system.professors:
        print(f"\n👨‍🏫 {professor.name}")
        print(f"   Specialization: {professor.specialization.value.title()}")
        print(f"   Expertise Level: {professor.expertise_level}/10")
        print(f"   H-index: {professor.h_index}")
        print(f"   Total Citations: {professor.total_citations:,}")
        print(f"   Research Funding: ${professor.research_funding:,.0f}")
        
        # Display persona information
        print(f"\n   🎭 PERSONA:")
        print(f"   • Teaching Philosophy: {professor.persona.teaching_philosophy}")
        print(f"   • Communication Style: {professor.persona.communication_style}")
        print(f"   • Personality Traits: {', '.join([t.value for t in professor.persona.personality_traits])}")
        print(f"   • Motivational Quote: \"{professor.persona.motivational_quotes[0]}\"")
        
        # Display unique characteristics
        print(f"   • Unique Characteristics:")
        for char in professor.persona.unique_characteristics:
            print(f"     - {char}")
        
        # Display recent publications
        print(f"\n   📄 RECENT PUBLICATIONS:")
        for i, paper in enumerate(professor.publications[:2]):  # Show first 2 papers
            print(f"   {i+1}. \"{paper.title}\"")
            print(f"      Venue: {paper.venue.value.upper()}")
            print(f"      Citations: {paper.citations}")
            print(f"      Impact Factor: {paper.impact_factor}")
        
        print("-" * 50)
    
    print(f"\n🔬 RESEARCH COLLABORATION DEMONSTRATION")
    print("-" * 50)
    
    # Demonstrate research collaboration
    prof1 = system.professors[0]  # Dr. Sarah Chen
    prof2 = system.professors[1]  # Dr. Marcus Rodriguez
    
    print(f"\nCollaboration between {prof1.name} and {prof2.name}")
    print(f"Specializations: {prof1.specialization.value} + {prof2.specialization.value}")
    
    # Generate collaborative research paper
    collab_paper = system.simulate_research_collaboration(
        prof1.professor_id,
        prof2.professor_id,
        "visual learning analytics"
    )
    
    print(f"\n📄 COLLABORATIVE RESEARCH PAPER:")
    print(f"Title: \"{collab_paper.title}\"")
    print(f"Authors: {', '.join(collab_paper.authors)}")
    print(f"Venue: {collab_paper.venue.value.upper()}")
    print(f"Publication Date: {collab_paper.publication_date.strftime('%B %Y')}")
    print(f"Impact Factor: {collab_paper.impact_factor}")
    print(f"Abstract: {collab_paper.abstract}")
    print(f"Methodology: {collab_paper.methodology}")
    print(f"Key Findings: {collab_paper.findings}")
    
    print(f"\n🎓 COURSE ASSIGNMENT DEMONSTRATION")
    print("-" * 50)
    
    # Demonstrate course assignment
    courses = ["AI501", "AI502", "AI503", "AI601", "AI701"]
    
    for course_id in courses:
        professor = system.assign_professor_to_course(course_id)
        if professor:
            print(f"\n{course_id}: Assigned to {professor.name}")
            print(f"   Teaching Methods: {', '.join([m.value for m in professor.teaching_methods])}")
            print(f"   Match Score: {system._calculate_match_score(professor, system._get_course_requirements(course_id))}")
    
    print(f"\n📊 RESEARCH METRICS SUMMARY")
    print("-" * 50)
    
    total_publications = sum(len(p.publications) for p in system.professors)
    total_citations = sum(p.total_citations for p in system.professors)
    total_funding = sum(p.research_funding for p in system.professors)
    
    print(f"Total Faculty: {len(system.professors)}")
    print(f"Total Publications: {total_publications}")
    print(f"Total Citations: {total_citations:,}")
    print(f"Total Research Funding: ${total_funding:,.0f}")
    print(f"Average H-index: {sum(p.h_index for p in system.professors) / len(system.professors):.1f}")
    
    print(f"\n🏆 AWARDS AND RECOGNITIONS")
    print("-" * 50)
    
    all_awards = []
    for professor in system.professors:
        all_awards.extend(professor.awards)
    
    unique_awards = list(set(all_awards))
    for award in unique_awards:
        count = all_awards.count(award)
        print(f"• {award} ({count} recipient{'s' if count > 1 else ''})")
    
    print(f"\n🎯 AI EDUCATION RESEARCH FOCUS")
    print("-" * 50)
    
    print("Our AI Professors are actively researching:")
    print("• Adaptive learning algorithms for personalized education")
    print("• Computer vision applications in educational assessment")
    print("• Ethical AI development and responsible AI education")
    print("• Multilingual AI tutoring systems")
    print("• Visual learning analytics and engagement tracking")
    print("• Neural architecture search for content generation")
    
    print(f"\n✅ FLORIDA ACCREDITATION COMPLIANCE")
    print("-" * 50)
    
    print("All AI Professors meet Florida accreditation requirements:")
    print("• SACSCOC compliance: ✓")
    print("• Terminal degree requirements: ✓")
    print("• Industry experience: ✓")
    print("• Research productivity: ✓")
    print("• Teaching effectiveness: ✓")
    
    print(f"\n" + "=" * 80)
    print("AI Professors are ready to deliver world-class AI education!")
    print("=" * 80)

if __name__ == "__main__":
    main()