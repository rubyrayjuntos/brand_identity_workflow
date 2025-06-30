"""
Pydantic models for the Brand Identity Management Agent Workflow.
Defines structured data structures for consistent data flow between agents.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

# ===================================================================
# Enums for Type Safety
# ===================================================================

class StylePreference(str, Enum):
    """Brand style preferences."""
    MODERN = "modern"
    CLASSIC = "classic"
    MINIMALIST = "minimalist"
    PLAYFUL = "playful"
    PROFESSIONAL = "professional"
    LUXURY = "luxury"
    TECH = "tech"
    NATURAL = "natural"

class BrandMood(str, Enum):
    """Brand emotional moods."""
    TRUSTWORTHY = "trustworthy"
    INNOVATIVE = "innovative"
    ENERGETIC = "energetic"
    CALMING = "calming"
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"

class Platform(str, Enum):
    """Social media platforms."""
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"

class CampaignType(str, Enum):
    """Email campaign types."""
    WELCOME = "welcome"
    NURTURE = "nurture"
    PROMOTIONAL = "promotional"
    ENGAGEMENT = "engagement"
    EDUCATIONAL = "educational"

# ===================================================================
# Brand Identity Models
# ===================================================================

class LogoConcept(BaseModel):
    """A single logo concept with its rationale and specifications."""
    id: str = Field(..., description="Unique identifier for the logo concept")
    name: str = Field(..., description="Descriptive name for the logo concept")
    file_name: str = Field(..., description="The filename of the generated logo image")
    description: str = Field(..., description="Brief description of the logo design")
    rationale: str = Field(..., description="Detailed explanation of design choices and symbolism")
    style: str = Field(..., description="The style category of this logo concept")
    file_path: str = Field(..., description="Path to the logo file")
    use_cases: List[str] = Field(default_factory=list, description="Recommended use cases for this logo")
    variations: List[str] = Field(default_factory=list, description="Available variations (horizontal, vertical, icon-only, etc.)")

class ColorSpecification(BaseModel):
    """Specification for a single color in the palette."""
    name: str = Field(..., description="Name of the color (e.g., 'Primary Blue')")
    hex: str = Field(..., description="Hex color code")
    rgb: str = Field(..., description="RGB color values")
    cmyk: str = Field(..., description="CMYK color values")
    usage: str = Field(..., description="Primary usage guidelines for this color")
    psychology: str = Field(..., description="Psychological impact and associations")

class ColorPalette(BaseModel):
    """A complete color palette with roles and specifications."""
    primary: ColorSpecification = Field(..., description="Primary brand color")
    secondary: ColorSpecification = Field(..., description="Secondary brand color")
    accent: ColorSpecification = Field(..., description="Accent color for highlights and CTAs")
    neutral: ColorSpecification = Field(..., description="Neutral color for backgrounds and text")
    rationale: str = Field(..., description="Explanation of color psychology and brand fit")
    accessibility_notes: str = Field(..., description="Accessibility considerations and compliance")
    additional_colors: List[ColorSpecification] = Field(default_factory=list, description="Additional colors if needed")

class TypographySpecification(BaseModel):
    """Typography specifications for the brand."""
    primary_font: str = Field(..., description="Primary font family name")
    secondary_font: str = Field(..., description="Secondary font family name")
    font_weights: List[str] = Field(..., description="Available font weights")
    font_sizes: Dict[str, str] = Field(..., description="Standard font sizes (h1, h2, body, etc.)")
    usage_guidelines: str = Field(..., description="Guidelines for font usage")

class ImageryStyle(BaseModel):
    """Imagery style guidelines."""
    photography_style: str = Field(..., description="Photography style description")
    illustration_style: str = Field(..., description="Illustration style description")
    icon_style: str = Field(..., description="Icon style description")
    examples: List[str] = Field(default_factory=list, description="Example image descriptions")

class StyleGuide(BaseModel):
    """Complete visual style guide document."""
    document_info: Dict[str, Any] = Field(..., description="Document metadata")
    brand_overview: Dict[str, Any] = Field(..., description="Brand overview section")
    logo_guidelines: Dict[str, Any] = Field(..., description="Logo usage guidelines")
    color_guidelines: Dict[str, Any] = Field(..., description="Color usage guidelines")
    typography: TypographySpecification = Field(..., description="Typography specifications")
    imagery_style: ImageryStyle = Field(..., description="Imagery style guidelines")
    digital_guidelines: Dict[str, Any] = Field(..., description="Digital application guidelines")
    file_path: str = Field(..., description="Path to the style guide document")

class BrandIdentityOutput(BaseModel):
    """The final structured output of the Brand Identity Crew."""
    brand_name: str = Field(..., description="Name of the brand")
    logo_concepts: List[LogoConcept] = Field(..., description="List of logo concepts")
    color_palette: ColorPalette = Field(..., description="Complete color palette")
    style_guide: StyleGuide = Field(..., description="Complete style guide")
    brand_voice: str = Field(..., description="Defined brand voice")
    target_audience: str = Field(..., description="Target audience description")
    industry: str = Field(..., description="Industry context")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

# ===================================================================
# Marketing Models
# ===================================================================

class SocialMediaPost(BaseModel):
    """A single social media post."""
    platform: Platform = Field(..., description="Target platform")
    caption: str = Field(..., description="Post caption text")
    hashtags: List[str] = Field(..., description="Relevant hashtags")
    visual_concept: str = Field(..., description="Visual concept description")
    call_to_action: str = Field(..., description="Call to action text")
    optimal_posting_time: str = Field(..., description="Optimal posting time")
    engagement_tips: List[str] = Field(default_factory=list, description="Engagement tips")

class SocialMediaStrategy(BaseModel):
    """Complete social media strategy."""
    brand_name: str = Field(..., description="Brand name")
    platforms: Dict[Platform, List[SocialMediaPost]] = Field(..., description="Posts by platform")
    content_themes: List[str] = Field(..., description="Content themes and topics")
    posting_schedule: Dict[str, str] = Field(..., description="Recommended posting schedule")
    hashtag_strategy: Dict[str, List[str]] = Field(..., description="Hashtag strategy by platform")
    engagement_strategy: str = Field(..., description="Overall engagement strategy")

class EmailCampaign(BaseModel):
    """A single email campaign."""
    campaign_type: CampaignType = Field(..., description="Type of email campaign")
    subject_line: str = Field(..., description="Email subject line")
    preheader: str = Field(..., description="Email preheader text")
    body_content: str = Field(..., description="Email body content")
    call_to_action: str = Field(..., description="Call to action text")
    cta_link: str = Field(..., description="Call to action link")
    personalization_fields: List[str] = Field(default_factory=list, description="Personalization fields")
    automation_triggers: Dict[str, str] = Field(..., description="Automation trigger conditions")

class EmailMarketingStrategy(BaseModel):
    """Complete email marketing strategy."""
    brand_name: str = Field(..., description="Brand name")
    campaigns: List[EmailCampaign] = Field(..., description="List of email campaigns")
    design_guidelines: Dict[str, Any] = Field(..., description="Email design guidelines")
    personalization_strategies: List[str] = Field(..., description="Personalization strategies")
    automation_workflows: Dict[str, Any] = Field(..., description="Automation workflow definitions")
    performance_metrics: List[str] = Field(..., description="Key performance metrics to track")

class VideoScript(BaseModel):
    """A video script for social media."""
    platform: Platform = Field(..., description="Target platform")
    concept: str = Field(..., description="Video concept")
    duration: str = Field(..., description="Target duration")
    aspect_ratio: str = Field(..., description="Aspect ratio")
    script: Dict[str, Any] = Field(..., description="Detailed script with scenes")
    production_notes: Dict[str, Any] = Field(..., description="Production guidelines")
    call_to_action: Dict[str, str] = Field(..., description="Call to action details")

class VideoContentStrategy(BaseModel):
    """Complete video content strategy."""
    brand_name: str = Field(..., description="Brand name")
    videos: List[VideoScript] = Field(..., description="List of video scripts")
    content_themes: List[str] = Field(..., description="Video content themes")
    production_guidelines: Dict[str, Any] = Field(..., description="Production guidelines")
    platform_specific_requirements: Dict[Platform, Dict[str, Any]] = Field(..., description="Platform-specific requirements")

class MarketingOutput(BaseModel):
    """The final structured output of the Marketing Crew."""
    brand_name: str = Field(..., description="Brand name")
    social_media_strategy: SocialMediaStrategy = Field(..., description="Social media strategy")
    email_marketing_strategy: EmailMarketingStrategy = Field(..., description="Email marketing strategy")
    video_content_strategy: VideoContentStrategy = Field(..., description="Video content strategy")
    overall_marketing_goals: List[str] = Field(..., description="Overall marketing goals")
    success_metrics: List[str] = Field(..., description="Success metrics to track")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

# ===================================================================
# Workflow Models
# ===================================================================

class BrandBrief(BaseModel):
    """Input brand brief for the workflow."""
    brand_name: str = Field(..., description="Name of the brand")
    industry: str = Field(..., description="Industry the brand operates in")
    target_audience: str = Field(..., description="Description of target audience")
    brand_values: List[str] = Field(..., description="List of brand values")
    style_preference: StylePreference = Field(..., description="Preferred style")
    desired_mood: BrandMood = Field(..., description="Desired brand mood")
    brand_voice: str = Field(..., description="Brand voice description")
    mission: str = Field(..., description="Brand mission")
    vision: str = Field(..., description="Brand vision")
    competitors: List[str] = Field(default_factory=list, description="List of competitors")
    unique_selling_proposition: str = Field(..., description="Unique selling proposition")
    marketing_goals: List[str] = Field(..., description="Marketing goals")
    budget_considerations: str = Field(..., description="Budget considerations")
    timeline: str = Field(..., description="Project timeline")

class WorkflowResult(BaseModel):
    """Complete workflow result."""
    brand_brief: BrandBrief = Field(..., description="Original brand brief")
    brand_identity: BrandIdentityOutput = Field(..., description="Brand identity results")
    marketing: MarketingOutput = Field(..., description="Marketing results")
    metadata: Dict[str, Any] = Field(..., description="Workflow metadata")
    status: str = Field(..., description="Workflow status")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")

# ===================================================================
# Utility Models
# ===================================================================

class TaskContext(BaseModel):
    """Context passed between tasks."""
    brand_brief: BrandBrief = Field(..., description="Brand brief")
    previous_results: Dict[str, Any] = Field(default_factory=dict, description="Results from previous tasks")
    current_step: str = Field(..., description="Current workflow step")
    step_data: Dict[str, Any] = Field(default_factory=dict, description="Step-specific data")

class AgentResponse(BaseModel):
    """Standardized agent response format."""
    success: bool = Field(..., description="Whether the task was successful")
    data: Dict[str, Any] = Field(..., description="Task output data")
    message: str = Field(..., description="Response message")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata") 