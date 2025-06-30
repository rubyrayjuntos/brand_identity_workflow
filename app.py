"""
Streamlit GUI for the Brand Identity Management Agent Workflow.
Provides a user-friendly interface for creating brand identities using AI agents.
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, Any

# Import your existing workflow components
from main import BrandIdentityWorkflow
from models import BrandBrief, StylePreference, BrandMood

# --- Page Configuration ---
st.set_page_config(
    page_title="Brand Identity MAS Orchestrator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for better styling ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e9ecef;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.title("🎨 Brand Identity Workflow")
    st.markdown("---")
    
    st.subheader("About")
    st.markdown("""
    This tool uses a **Multi-Agent System (MAS)** to generate complete brand identities.
    
    **Features:**
    - 🎯 Logo concept generation
    - 🎨 Color palette selection
    - 📋 Style guide creation
    - 📱 Marketing strategy development
    
    **Process:**
    1. Fill out the brand brief
    2. AI agents collaborate
    3. Get structured results
    """)
    
    st.markdown("---")
    
    st.subheader("Quick Start")
    if st.button("🚀 Use Sample Brand"):
        st.session_state.use_sample = True
        st.rerun()
    
    st.markdown("---")
    
    st.subheader("Configuration")
    st.markdown("""
    **Current Setup:**
    - Hierarchical Process ✅
    - Pydantic Validation ✅
    - Structured Outputs ✅
    """)

# --- Main Content ---
st.markdown('<h1 class="main-header">🎨 Brand Identity MAS Orchestrator</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>Welcome!</strong> This tool uses a Multi-Agent System (MAS) to generate a complete brand identity. 
    Fill out the details below to define your brand, and the AI agents will collaborate to create your brand identity.
</div>
""", unsafe_allow_html=True)

# --- Input Form ---
st.markdown('<h2 class="sub-header">1. Define Your Brand Brief</h2>', unsafe_allow_html=True)

# Check if user wants to use sample brand
if 'use_sample' in st.session_state and st.session_state.use_sample:
    sample_brand = {
        'brand_name': 'AquaPure',
        'industry': 'Sustainable Consumer Goods',
        'target_audience': 'Eco-conscious millennials and outdoor enthusiasts aged 25-40',
        'brand_values': ['Sustainability', 'Health', 'Purity', 'Trust', 'Innovation'],
        'style_preference': StylePreference.MODERN,
        'desired_mood': BrandMood.CALMING,
        'brand_voice': 'warm and educational',
        'mission': 'To make sustainable living accessible and beautiful for everyday people',
        'vision': 'To inspire a global movement toward conscious consumption and environmental stewardship',
        'competitors': ['Method', 'Seventh Generation', 'Mrs. Meyer\'s'],
        'unique_selling_proposition': 'Premium sustainable products with transparent sourcing and beautiful design',
        'marketing_goals': ['Build brand awareness', 'Educate on sustainability', 'Drive online sales', 'Create brand advocates'],
        'budget_considerations': 'Mid-premium pricing with direct-to-consumer focus',
        'timeline': '3-6 months for product launch'
    }
    st.session_state.brand_brief = sample_brand
    st.session_state.use_sample = False

with st.form("brand_brief_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        brand_name = st.text_input(
            "Brand Name *", 
            value=st.session_state.get('brand_brief', {}).get('brand_name', ''),
            placeholder="e.g., AquaPure, TechFlow, GreenLife"
        )
        
        industry = st.text_input(
            "Industry / Field *", 
            value=st.session_state.get('brand_brief', {}).get('industry', ''),
            placeholder="e.g., Sustainable Consumer Goods, AI Software, Healthcare"
        )
        
        target_audience = st.text_area(
            "Target Audience *", 
            value=st.session_state.get('brand_brief', {}).get('target_audience', ''),
            placeholder="e.g., Eco-conscious millennials and outdoor enthusiasts aged 25-40"
        )
        
        brand_values = st.text_input(
            "Brand Values (comma-separated) *", 
            value=', '.join(st.session_state.get('brand_brief', {}).get('brand_values', [])),
            placeholder="e.g., Sustainability, Health, Purity, Trust, Innovation"
        )
    
    with col2:
        style_preference = st.selectbox(
            "Style Preference *",
            options=list(StylePreference),
            index=list(StylePreference).index(st.session_state.get('brand_brief', {}).get('style_preference', StylePreference.MODERN)),
            format_func=lambda x: x.value.title()
        )
        
        desired_mood = st.selectbox(
            "Desired Brand Mood *",
            options=list(BrandMood),
            index=list(BrandMood).index(st.session_state.get('brand_brief', {}).get('desired_mood', BrandMood.TRUSTWORTHY)),
            format_func=lambda x: x.value.title()
        )
        
        brand_voice = st.text_input(
            "Brand Voice *", 
            value=st.session_state.get('brand_brief', {}).get('brand_voice', ''),
            placeholder="e.g., professional yet approachable, warm and educational"
        )
        
        timeline = st.text_input(
            "Project Timeline", 
            value=st.session_state.get('brand_brief', {}).get('timeline', ''),
            placeholder="e.g., 3-6 months for full brand rollout"
        )
    
    # Full-width fields
    mission = st.text_area(
        "Brand Mission *", 
        value=st.session_state.get('brand_brief', {}).get('mission', ''),
        placeholder="e.g., To make sustainable living accessible and beautiful for everyday people"
    )
    
    vision = st.text_area(
        "Brand Vision", 
        value=st.session_state.get('brand_brief', {}).get('vision', ''),
        placeholder="e.g., To inspire a global movement toward conscious consumption and environmental stewardship"
    )
    
    marketing_goals = st.text_input(
        "Marketing Goals (comma-separated)", 
        value=', '.join(st.session_state.get('brand_brief', {}).get('marketing_goals', [])),
        placeholder="e.g., Build brand awareness, Drive product adoption, Generate leads"
    )
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.form_submit_button(
            "🚀 Launch Agent Workflow", 
            type="primary",
            use_container_width=True
        )

# --- Workflow Execution ---
if submitted:
    # Validate required fields
    required_fields = [brand_name, industry, target_audience, brand_values, brand_voice, mission]
    if not all(required_fields):
        st.error("❌ Please fill out all required fields (marked with *) before launching the workflow.")
    else:
        st.divider()
        st.markdown('<h2 class="sub-header">2. Workflow Execution & Results</h2>', unsafe_allow_html=True)
        
        # Prepare brand brief
        brand_brief = {
            'brand_name': brand_name,
            'industry': industry,
            'target_audience': target_audience,
            'brand_values': [value.strip() for value in brand_values.split(',')],
            'style_preference': style_preference,
            'desired_mood': desired_mood,
            'brand_voice': brand_voice,
            'mission': mission,
            'vision': vision,
            'marketing_goals': [goal.strip() for goal in marketing_goals.split(',')] if marketing_goals else [],
            'timeline': timeline,
            'competitors': [],
            'unique_selling_proposition': '',
            'budget_considerations': ''
        }
        
        # Save brand brief to session state
        st.session_state.brand_brief = brand_brief
        
        # Display workflow progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialize workflow
        try:
            workflow = BrandIdentityWorkflow()
            
            # Update progress
            progress_bar.progress(25)
            status_text.text("🤖 Initializing AI agents...")
            
            # Execute workflow
            with st.spinner("🤖 AI agents are collaborating to create your brand identity..."):
                results = workflow.run_complete_workflow(brand_brief)
                
                progress_bar.progress(100)
                status_text.text("✅ Workflow completed successfully!")
            
            # Display success message
            st.markdown("""
            <div class="success-box">
                <strong>🎉 Brand Identity Created Successfully!</strong><br>
                Your AI agents have collaborated to create a complete brand identity package.
            </div>
            """, unsafe_allow_html=True)
            
            # Display results in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "🎨 Brand Identity", "📱 Marketing", "📄 Raw Data"])
            
            with tab1:
                st.subheader("Workflow Summary")
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Brand Name", brand_brief['brand_name'])
                
                with col2:
                    st.metric("Industry", brand_brief['industry'])
                
                with col3:
                    st.metric("Style", brand_brief['style_preference'].value.title())
                
                with col4:
                    st.metric("Mood", brand_brief['desired_mood'].value.title())
                
                # Workflow metadata
                metadata = results.get('metadata', {})
                st.subheader("Workflow Details")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Status:** {metadata.get('status', 'Unknown')}")
                    st.write(f"**Started:** {metadata.get('start_time', 'Unknown')}")
                
                with col2:
                    st.write(f"**Completed:** {metadata.get('end_time', 'Unknown')}")
                    st.write(f"**Process Type:** Hierarchical (Manager Agents)")
                
                # Brand values
                st.subheader("Brand Values")
                for value in brand_brief['brand_values']:
                    st.write(f"• {value}")
            
            with tab2:
                st.subheader("Brand Identity Deliverables")
                
                brand_identity = results.get('brand_identity', {})
                
                # Logo concepts
                st.write("**🎨 Logo Concepts:**")
                logo_concepts = brand_identity.get('logo_concepts', {})
                st.write(f"Generated {logo_concepts.get('concepts_count', 0)} logo concepts")
                
                # Color palette
                st.write("**🎨 Color Palette:**")
                color_palette = brand_identity.get('color_palette', {})
                st.write(f"Created {color_palette.get('colors_count', 0)} color categories")
                
                # Style guide
                st.write("**📋 Style Guide:**")
                style_guide = brand_identity.get('style_guide', {})
                st.write(f"Compiled {style_guide.get('sections_count', 0)} style guide sections")
            
            with tab3:
                st.subheader("Marketing Deliverables")
                
                marketing = results.get('marketing', {})
                
                # Social media
                st.write("**📱 Social Media Strategy:**")
                social_media = marketing.get('social_media_content', {})
                platforms = social_media.get('platforms_covered', [])
                st.write(f"Covered {len(platforms)} platforms: {', '.join(platforms)}")
                
                # Email campaigns
                st.write("**📧 Email Marketing:**")
                email_campaigns = marketing.get('email_campaigns', {})
                campaign_types = email_campaigns.get('campaign_types', [])
                st.write(f"Created {len(campaign_types)} campaign types: {', '.join(campaign_types)}")
                
                # Video content
                st.write("**🎥 Video Content:**")
                video_content = marketing.get('video_content', {})
                video_platforms = video_content.get('platforms_covered', [])
                st.write(f"Covered {len(video_platforms)} platforms: {', '.join(video_platforms)}")
            
            with tab4:
                st.subheader("Raw Workflow Data")
                st.json(results)
                
                # Download button
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"brand_identity_{brand_brief['brand_name']}_{timestamp}.json"
                
                st.download_button(
                    label="📥 Download Results (JSON)",
                    data=json.dumps(results, indent=2, default=str),
                    file_name=filename,
                    mime="application/json"
                )
        
        except Exception as e:
            st.error(f"❌ An error occurred during the workflow: {str(e)}")
            st.markdown("""
            <div class="warning-box">
                <strong>⚠️ Workflow Error</strong><br>
                Please check your configuration and try again. If the problem persists, 
                check the console output for more details.
            </div>
            """, unsafe_allow_html=True)

# --- Footer ---
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    Built with ❤️ using CrewAI and Streamlit | 
    <a href="https://github.com/your-repo/brand_identity_workflow" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True) 