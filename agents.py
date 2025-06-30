"""
Agents module for the Brand Identity Management Agent Workflow.
Defines specialized AI agents for different aspects of brand identity and marketing tasks.
Now implements a hierarchical structure with manager agents and worker agents.
"""

from crewai import Agent
from tools import BrandAssetTools, MarketingTools, DataManagementTools

# ===================================================================
# Worker Agents - Brand Identity Core Elements
# These agents are specialists who perform the actual work.
# Note: allow_delegation is False because they are the final executors.
# ===================================================================

def create_logo_designer_agent():
    """Create the Logo Concept Designer worker agent."""
    return Agent(
        role='Logo Concept Designer',
        goal='Generate innovative and fitting logo concepts based on brand brief and user preferences',
        backstory="""You are an expert graphic designer with over 15 years of experience in brand identity design. 
        You have a keen eye for translating brand values into visual symbols and understand the psychology behind 
        effective logo design. You excel at creating logos that are memorable, scalable, and appropriate for their 
        intended use. You stay current with design trends while maintaining timeless appeal.""",
        tools=[
            BrandAssetTools.generate_logo_concepts,
            DataManagementTools.save_generated_assets
        ],
        verbose=True,
        allow_delegation=False  # Worker agents don't delegate
    )

def create_color_specialist_agent():
    """Create the Color Palette Specialist worker agent."""
    return Agent(
        role='Color Palette Specialist',
        goal='Select compelling color palettes that evoke the desired brand mood and meet accessibility standards',
        backstory="""You are a color theorist and brand strategist with deep expertise in color psychology and 
        accessibility design. You understand how colors influence emotions and behavior, and you create palettes 
        that are both beautiful and effective. You ensure all color combinations meet WCAG accessibility standards 
        and work well for users with color vision deficiencies. You have worked with brands across various 
        industries and understand the unique color needs of different sectors.""",
        tools=[
            BrandAssetTools.analyze_color_psychology,
            DataManagementTools.save_generated_assets
        ],
        verbose=True,
        allow_delegation=False  # Worker agents don't delegate
    )

def create_style_guide_creator_agent():
    """Create the Visual Style Guide Creator worker agent."""
    return Agent(
        role='Visual Style Guide Creator',
        goal='Create comprehensive visual style guide documents that ensure brand consistency across all touchpoints',
        backstory="""You are a meticulous brand manager and design systems expert who has created style guides 
        for Fortune 500 companies. You understand the importance of consistency in brand communication and know 
        how to document every detail to ensure proper implementation. You excel at organizing complex brand 
        information into clear, actionable guidelines that designers, marketers, and developers can easily follow. 
        You have a strong background in typography, layout, and digital design principles.""",
        tools=[
            BrandAssetTools.generate_style_guide_doc,
            DataManagementTools.save_generated_assets
        ],
        verbose=True,
        allow_delegation=False  # Worker agents don't delegate
    )

# ===================================================================
# Manager Agents - Orchestration and Coordination
# These agents manage the workflow and delegate to worker agents.
# Note: allow_delegation is True so they can delegate to the workers.
# ===================================================================

def create_brand_identity_coordinator_agent():
    """Create the Brand Identity Project Manager agent."""
    return Agent(
        role='Brand Identity Project Manager',
        goal=(
            'Efficiently manage the brand identity creation process from start to finish. '
            'Your primary responsibility is to ensure the final deliverable strictly '
            'adheres to the required structured format (Pydantic model).'
        ),
        backstory=(
            "You are an expert project manager at a top-tier branding agency with 20+ years of experience. "
            "You are a master of delegation and coordination. You don't create assets yourself; you orchestrate "
            "the specialists to do their best work and then assemble their outputs into a final, polished client deliverable. "
            "You understand how all brand elements work together and can identify potential conflicts or inconsistencies. "
            "You excel at project management and can coordinate multiple specialists to achieve a unified brand vision."
        ),
        tools=[
            DataManagementTools.save_brand_profile,
            DataManagementTools.save_generated_assets
        ],
        verbose=True,
        allow_delegation=True  # Manager agents can delegate
    )

def create_marketing_coordinator_agent():
    """Create the Marketing Campaign Coordinator agent."""
    return Agent(
        role='Marketing Campaign Coordinator',
        goal=(
            'Coordinate marketing campaigns across multiple channels and ensure brand consistency. '
            'Your primary responsibility is to ensure all marketing deliverables strictly '
            'adhere to the required structured formats (Pydantic models).'
        ),
        backstory=(
            "You are a marketing operations expert with deep experience in multi-channel campaign management. "
            "You understand how different marketing channels work together and can create integrated campaigns "
            "that amplify each other's impact. You have expertise in campaign planning, execution, and measurement. "
            "You know how to maintain brand consistency across diverse marketing materials while adapting content "
            "for different platforms and audiences. You have successfully launched campaigns for brands across "
            "various industries and understand the metrics that drive business results."
        ),
        tools=[
            DataManagementTools.save_generated_assets
        ],
        verbose=True,
        allow_delegation=True  # Manager agents can delegate
    )

# ===================================================================
# Worker Agents - Community Engagement & Marketing
# These agents are specialists who perform the actual marketing work.
# ===================================================================

def create_social_media_manager_agent():
    """Create the Social Media Content Strategist worker agent."""
    return Agent(
        role='Social Media Content Strategist',
        goal='Create engaging social media content that aligns with brand guidelines and drives meaningful engagement',
        backstory="""You are a savvy digital marketer with 10+ years of experience in social media strategy. 
        You understand the nuances of each platform and know how to create content that resonates with specific 
        audiences. You stay current with social media trends and algorithm changes, and you know how to balance 
        brand messaging with platform-specific best practices. You have successfully grown social media 
        communities for brands across various industries and understand the metrics that matter for engagement 
        and conversion.""",
        tools=[
            MarketingTools.search_web_for_trends,
            MarketingTools.generate_social_media_post,
            DataManagementTools.save_generated_assets
        ],
        verbose=True,
        allow_delegation=False  # Worker agents don't delegate
    )

def create_email_marketing_agent():
    """Create the Email Marketing Strategist worker agent."""
    return Agent(
        role='Email Marketing Strategist',
        goal='Develop effective email marketing campaigns that nurture relationships and drive conversions',
        backstory="""You are an email marketing expert with extensive experience in customer lifecycle marketing. 
        You understand the psychology of email engagement and know how to craft compelling subject lines, 
        personalized content, and effective calls-to-action. You have expertise in email automation, segmentation, 
        and A/B testing. You know how to balance promotional content with value-driven messaging and understand 
        the importance of deliverability and compliance with email regulations.""",
        tools=[
            MarketingTools.generate_email_campaign_plan,
            DataManagementTools.save_generated_assets
        ],
        verbose=True,
        allow_delegation=False  # Worker agents don't delegate
    )

def create_video_producer_agent():
    """Create the Social Media Video Producer worker agent."""
    return Agent(
        role='Social Media Video Producer',
        goal='Develop compelling video scripts and storyboards for short-form social media content',
        backstory="""You are a creative storyteller and video producer who specializes in short-form content 
        for social media platforms. You understand the unique requirements of platforms like TikTok, Instagram 
        Reels, and YouTube Shorts. You know how to capture attention in the first few seconds and maintain 
        engagement throughout the video. You have experience with various video styles including educational, 
        entertaining, and promotional content. You understand the importance of brand consistency in video 
        production and know how to adapt brand guidelines for moving content.""",
        tools=[
            MarketingTools.generate_video_script,
            DataManagementTools.save_generated_assets
        ],
        verbose=True,
        allow_delegation=False  # Worker agents don't delegate
    )

# ===================================================================
# Agent Factory Functions
# ===================================================================

def get_brand_identity_agents():
    """Get all agents for the brand identity workflow (manager + workers)."""
    return {
        'brand_identity_coordinator': create_brand_identity_coordinator_agent(),
        'logo_designer': create_logo_designer_agent(),
        'color_specialist': create_color_specialist_agent(),
        'style_guide_creator': create_style_guide_creator_agent()
    }

def get_marketing_agents():
    """Get all agents for the marketing workflow (manager + workers)."""
    return {
        'marketing_coordinator': create_marketing_coordinator_agent(),
        'social_media_manager': create_social_media_manager_agent(),
        'email_marketing_agent': create_email_marketing_agent(),
        'video_producer': create_video_producer_agent()
    }

def get_all_agents():
    """Get all agents for the complete workflow."""
    brand_agents = get_brand_identity_agents()
    marketing_agents = get_marketing_agents()
    return {**brand_agents, **marketing_agents}

def get_brand_identity_crew_agents():
    """Get agents in the correct order for hierarchical brand identity crew (manager first)."""
    agents = get_brand_identity_agents()
    return [
        agents['brand_identity_coordinator'],  # Manager must be first
        agents['logo_designer'],
        agents['color_specialist'],
        agents['style_guide_creator']
    ]

def get_marketing_crew_agents():
    """Get agents in the correct order for hierarchical marketing crew (manager first)."""
    agents = get_marketing_agents()
    return [
        agents['marketing_coordinator'],  # Manager must be first
        agents['social_media_manager'],
        agents['email_marketing_agent'],
        agents['video_producer']
    ]
