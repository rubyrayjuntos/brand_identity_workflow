"""
Example usage script for the Brand Identity Management Agent Workflow.
Demonstrates how to use the system with different brand configurations.
"""

from main import BrandIdentityWorkflow
import json

def example_tech_startup():
    """Example: Tech startup brand identity workflow."""
    print("🚀 Example 1: Tech Startup")
    print("=" * 50)
    
    workflow = BrandIdentityWorkflow()
    
    tech_brief = {
        'brand_name': 'DataFlow',
        'industry': 'Data Analytics & Business Intelligence',
        'target_audience': 'Data scientists, business analysts, and IT professionals aged 28-45 who need powerful yet user-friendly analytics tools',
        'brand_values': ['Innovation', 'Clarity', 'Efficiency', 'Insight', 'Reliability'],
        'style_preference': 'modern',
        'desired_mood': 'innovative',
        'brand_voice': 'confident and approachable',
        'mission': 'To democratize data analytics by making complex insights accessible to everyone',
        'vision': 'To be the leading platform that transforms raw data into actionable business intelligence',
        'competitors': ['Tableau', 'Power BI', 'Looker'],
        'unique_selling_proposition': 'AI-powered insights with natural language queries and automated reporting',
        'marketing_goals': ['Establish thought leadership', 'Drive product adoption', 'Build developer community', 'Generate enterprise leads'],
        'budget_considerations': 'Premium pricing with enterprise focus',
        'timeline': '6-12 months for full market presence'
    }
    
    results = workflow.run_complete_workflow(tech_brief)
    workflow.save_results(f"DataFlow_results.json")
    
    return results

def example_eco_friendly_brand():
    """Example: Eco-friendly consumer brand workflow."""
    print("\n🌱 Example 2: Eco-Friendly Consumer Brand")
    print("=" * 50)
    
    workflow = BrandIdentityWorkflow()
    
    eco_brief = {
        'brand_name': 'GreenLife',
        'industry': 'Sustainable Consumer Products',
        'target_audience': 'Environmentally conscious consumers aged 25-40, primarily urban professionals and families who prioritize sustainability',
        'brand_values': ['Sustainability', 'Transparency', 'Quality', 'Community', 'Innovation'],
        'style_preference': 'natural',
        'desired_mood': 'calming',
        'brand_voice': 'warm and educational',
        'mission': 'To make sustainable living accessible and beautiful for everyday people',
        'vision': 'To inspire a global movement toward conscious consumption and environmental stewardship',
        'competitors': ['Method', 'Seventh Generation', 'Mrs. Meyer\'s'],
        'unique_selling_proposition': 'Premium sustainable products with transparent sourcing and beautiful design',
        'marketing_goals': ['Build brand awareness', 'Educate on sustainability', 'Drive online sales', 'Create brand advocates'],
        'budget_considerations': 'Mid-premium pricing with direct-to-consumer focus',
        'timeline': '3-6 months for product launch'
    }
    
    results = workflow.run_complete_workflow(eco_brief)
    workflow.save_results(f"GreenLife_results.json")
    
    return results

def example_consulting_firm():
    """Example: Professional consulting firm workflow."""
    print("\n💼 Example 3: Professional Consulting Firm")
    print("=" * 50)
    
    workflow = BrandIdentityWorkflow()
    
    consulting_brief = {
        'brand_name': 'StrategicEdge',
        'industry': 'Management Consulting',
        'target_audience': 'C-level executives and senior managers at mid to large companies seeking strategic transformation and growth',
        'brand_values': ['Excellence', 'Trust', 'Innovation', 'Results', 'Partnership'],
        'style_preference': 'professional',
        'desired_mood': 'trustworthy',
        'brand_voice': 'authoritative and collaborative',
        'mission': 'To empower organizations with strategic insights that drive sustainable growth and competitive advantage',
        'vision': 'To be the most trusted partner for strategic transformation in the digital age',
        'competitors': ['McKinsey', 'BCG', 'Bain'],
        'unique_selling_proposition': 'Boutique consulting with deep industry expertise and personalized approach',
        'marketing_goals': ['Establish credibility', 'Generate qualified leads', 'Build thought leadership', 'Create referral network'],
        'budget_considerations': 'High-value consulting services with premium positioning',
        'timeline': '12-18 months for market establishment'
    }
    
    results = workflow.run_complete_workflow(consulting_brief)
    workflow.save_results(f"StrategicEdge_results.json")
    
    return results

def example_fitness_brand():
    """Example: Fitness and wellness brand workflow."""
    print("\n💪 Example 4: Fitness & Wellness Brand")
    print("=" * 50)
    
    workflow = BrandIdentityWorkflow()
    
    fitness_brief = {
        'brand_name': 'VitalCore',
        'industry': 'Fitness & Wellness',
        'target_audience': 'Health-conscious individuals aged 18-45, including fitness enthusiasts, busy professionals, and wellness beginners',
        'brand_values': ['Health', 'Empowerment', 'Community', 'Balance', 'Transformation'],
        'style_preference': 'energetic',
        'desired_mood': 'energetic',
        'brand_voice': 'motivational and supportive',
        'mission': 'To inspire and empower people to achieve their health and fitness goals through innovative solutions',
        'vision': 'To create a world where everyone has access to the tools and community they need to live their healthiest life',
        'competitors': ['Peloton', 'Fitbit', 'MyFitnessPal'],
        'unique_selling_proposition': 'Personalized fitness experiences with AI coaching and community support',
        'marketing_goals': ['Build community', 'Drive app downloads', 'Increase engagement', 'Generate subscriptions'],
        'budget_considerations': 'Freemium model with premium subscription tiers',
        'timeline': '6-9 months for platform launch'
    }
    
    results = workflow.run_complete_workflow(fitness_brief)
    workflow.save_results(f"VitalCore_results.json")
    
    return results

def compare_results(results_list, brand_names):
    """Compare results from different brand workflows."""
    print("\n📊 COMPARISON SUMMARY")
    print("=" * 80)
    
    for i, (results, brand_name) in enumerate(zip(results_list, brand_names), 1):
        print(f"\n{i}. {brand_name}")
        print("-" * 40)
        
        # Brand Identity Summary
        brand_identity = results.get('brand_identity', {})
        print(f"   Brand Identity:")
        print(f"   - Logo Concepts: {brand_identity.get('logo_concepts', {}).get('concepts_count', 0)}")
        print(f"   - Color Palette: {brand_identity.get('color_palette', {}).get('colors_count', 0)} colors")
        print(f"   - Style Guide: {brand_identity.get('style_guide', {}).get('sections_count', 0)} sections")
        
        # Marketing Summary
        marketing = results.get('marketing', {})
        print(f"   Marketing:")
        print(f"   - Social Media: {len(marketing.get('social_media_content', {}).get('platforms_covered', []))} platforms")
        print(f"   - Email Campaigns: {len(marketing.get('email_campaigns', {}).get('campaign_types', []))} types")
        print(f"   - Video Content: {len(marketing.get('video_content', {}).get('platforms_covered', []))} platforms")
        
        # Status
        status = results.get('metadata', {}).get('status', 'unknown')
        print(f"   Status: {status}")

def main():
    """Run all example workflows."""
    print("🎯 BRAND IDENTITY WORKFLOW EXAMPLES")
    print("=" * 80)
    print("This script demonstrates the system with different brand types.")
    print("=" * 80)
    
    results_list = []
    brand_names = []
    
    try:
        # Run all examples
        results_list.append(example_tech_startup())
        brand_names.append("DataFlow (Tech Startup)")
        
        results_list.append(example_eco_friendly_brand())
        brand_names.append("GreenLife (Eco-Friendly)")
        
        results_list.append(example_consulting_firm())
        brand_names.append("StrategicEdge (Consulting)")
        
        results_list.append(example_fitness_brand())
        brand_names.append("VitalCore (Fitness)")
        
        # Compare results
        compare_results(results_list, brand_names)
        
        print("\n" + "=" * 80)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("Check the 'results' directory for detailed output files:")
        print("- DataFlow_results.json")
        print("- GreenLife_results.json") 
        print("- StrategicEdge_results.json")
        print("- VitalCore_results.json")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        print("Please check the error details and try again.")

if __name__ == "__main__":
    main() 