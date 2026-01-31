"""
Tasks module for the Brand Identity Management Agent Workflow.
Defines specific tasks for agents to execute in the brand identity and marketing processes, now with structured Pydantic outputs.
"""

from crewai import Task
from models import (
    BrandIdentityOutput, LogoConcept, ColorPalette, StyleGuide,
    SocialMediaStrategy, EmailMarketingStrategy, VideoContentStrategy,
    MarketingOutput
)

# ===================================================================
# High-Level Coordinator Tasks (for Manager Agents)
# These tasks are assigned to manager agents who delegate to workers.
# ===================================================================

brand_identity_coordination_task = Task(
    description=(
        "Orchestrate the complete brand identity creation process for the brand: '{brand_name}'. "
        "Your role is to manage the entire workflow and ensure the final deliverable meets all requirements. "
        ""
        "Process to follow:"
        "1. Delegate logo concept creation to the Logo Concept Designer"
        "2. Delegate color palette development to the Color Palette Specialist" 
        "3. Delegate style guide compilation to the Visual Style Guide Creator"
        "4. Assemble all outputs into a final BrandIdentityOutput object"
        ""
        "Brand Context:"
        "- Industry: {industry}"
        "- Target Audience: {target_audience}"
        "- Brand Values: {brand_values}"
        "- Style Preference: {style_preference}"
        "- Desired Mood: {desired_mood}"
        ""
        "Ensure the final output strictly adheres to the BrandIdentityOutput Pydantic model structure."
    ),
    expected_output=(
        "A complete BrandIdentityOutput object containing all brand identity elements: "
        "logo concepts, color palette, style guide, and metadata. "
        "The output must be a valid JSON object that matches the BrandIdentityOutput schema exactly."
    ),
    output_pydantic=BrandIdentityOutput
)

marketing_coordination_task = Task(
    description=(
        "Orchestrate the complete marketing strategy development for the brand: '{brand_name}'. "
        "You have access to the complete brand identity guide and need to create comprehensive marketing strategies. "
        ""
        "Process to follow:"
        "1. Delegate social media strategy to the Social Media Content Strategist"
        "2. Delegate email marketing strategy to the Email Marketing Strategist"
        "3. Delegate video content strategy to the Video Producer"
        "4. Assemble all outputs into comprehensive marketing strategies"
        ""
        "Brand Identity Available: Complete brand guidelines, logo, colors, and style guide"
        "Marketing Goals: {marketing_goals}"
        ""
        "Ensure all outputs strictly adhere to their respective Pydantic model structures."
    ),
    expected_output=(
        "Complete marketing strategies including: "
        "SocialMediaStrategy, EmailMarketingStrategy, and VideoContentStrategy objects. "
        "Each strategy must be a valid JSON object that matches its respective Pydantic schema."
    ),
    output_pydantic=MarketingOutput
)

# ===================================================================
# Worker Tasks - Brand Identity Core Elements (Step-by-Step, Structured Output)
# These tasks are delegated to by manager agents.
# ===================================================================

logo_design_task = Task(
    description=(
        "Analyze the provided brand brief and generate 3 innovative logo concepts. "
        "For each concept, provide a name, file name, description, rationale, style, file path, use cases, and variations. "
        "Output must be a list of LogoConcept objects."
    ),
    expected_output=(
        "A list of 3 LogoConcept objects, each with all required fields as defined in the LogoConcept Pydantic model."
    ),
    output_pydantic=LogoConcept,
    many_output=True
)

color_palette_task = Task(
    description=(
        "Based on the brand brief and logo concepts, develop a comprehensive color palette. "
        "Include primary, secondary, accent, and neutral colors, each with hex, rgb, cmyk, usage, and psychology. "
        "Also provide rationale and accessibility notes. Output must be a ColorPalette object."
    ),
    expected_output=(
        "A ColorPalette object with all required fields as defined in the ColorPalette Pydantic model."
    ),
    output_pydantic=ColorPalette
)

style_guide_task = Task(
    description=(
        "Compile the approved logo concepts and color palette into a single, cohesive visual style guide document. "
        "Include all required sections and output a StyleGuide object."
    ),
    expected_output=(
        "A StyleGuide object with all required fields as defined in the StyleGuide Pydantic model."
    ),
    output_pydantic=StyleGuide
)

brand_identity_task = Task(
    description=(
        "Assemble the final brand identity output by combining the logo concepts, color palette, and style guide. "
        "Output must be a BrandIdentityOutput object."
    ),
    expected_output=(
        "A BrandIdentityOutput object with all required fields as defined in the BrandIdentityOutput Pydantic model."
    ),
    output_pydantic=BrandIdentityOutput
)

# ===================================================================
# Worker Tasks - Community Engagement & Marketing (Structured Output)
# These tasks are delegated to by manager agents.
# ===================================================================

social_media_strategy_task = Task(
    description=(
        "Given the complete brand identity, develop a comprehensive social media strategy. "
        "Output must be a SocialMediaStrategy object, including posts for each platform, content themes, schedule, hashtag and engagement strategies."
    ),
    expected_output=(
        "A SocialMediaStrategy object with all required fields as defined in the SocialMediaStrategy Pydantic model."
    ),
    output_pydantic=SocialMediaStrategy
)

email_marketing_strategy_task = Task(
    description=(
        "Given the brand identity and marketing goals, develop a complete email marketing strategy. "
        "Output must be an EmailMarketingStrategy object, including campaign details, design guidelines, personalization, automation, and metrics."
    ),
    expected_output=(
        "An EmailMarketingStrategy object with all required fields as defined in the EmailMarketingStrategy Pydantic model."
    ),
    output_pydantic=EmailMarketingStrategy
)

video_content_strategy_task = Task(
    description=(
        "Given the brand identity and social media strategy, develop a video content strategy for all relevant platforms. "
        "Output must be a VideoContentStrategy object, including scripts, production guidelines, and platform requirements."
    ),
    expected_output=(
        "A VideoContentStrategy object with all required fields as defined in the VideoContentStrategy Pydantic model."
    ),
    output_pydantic=VideoContentStrategy
)

# ===================================================================
# Task Factory Functions
# ===================================================================

def get_brand_identity_tasks(agents):
    """Return the brand identity tasks (coordinator + workers)."""
    return {
        'brand_identity_coordination': brand_identity_coordination_task,
        'logo_design': logo_design_task,
        'color_palette': color_palette_task,
        'style_guide': style_guide_task,
        'brand_identity': brand_identity_task
    }

def get_marketing_tasks(agents):
    """Return the marketing tasks (coordinator + workers)."""
    return {
        'marketing_coordination': marketing_coordination_task,
        'social_media_strategy': social_media_strategy_task,
        'email_marketing_strategy': email_marketing_strategy_task,
        'video_content_strategy': video_content_strategy_task
    }

def get_coordinator_tasks():
    """Return only the high-level coordinator tasks for hierarchical crews."""
    return {
        'brand_identity_coordination': brand_identity_coordination_task,
        'marketing_coordination': marketing_coordination_task
    }
