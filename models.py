"""
Pydantic models for the Brand Identity Management Agent Workflow.
Defines structured data structures for consistent data flow between agents.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
import uuid

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
    PRODUCT_ANNOUNCEMENT = "product_announcement"
    NEWSLETTER = "newsletter"
    ONBOARDING = "onboarding"
    REENGAGEMENT = "re-engagement"
    ANNOUNCEMENT = "announcement"

# ===================================================================
# Brand Identity Models
# ===================================================================

def _generate_id():
    return str(uuid.uuid4())[:8]

class LogoConcept(BaseModel):
    """A single logo concept with its rationale and specifications."""
    id: str = Field(default_factory=_generate_id, description="Unique identifier for the logo concept")
    name: str = Field(default="", description="Descriptive name for the logo concept")
    file_name: str = Field(default="", description="The filename of the generated logo image")
    description: str = Field(default="", description="Brief description of the logo design")
    rationale: str = Field(default="", description="Detailed explanation of design choices and symbolism")
    style: str = Field(default="", description="The style category of this logo concept")
    file_path: str = Field(default="", description="Path to the logo file")
    use_cases: List[str] = Field(default_factory=list, description="Recommended use cases for this logo")
    variations: List[str] = Field(default_factory=list, description="Available variations (horizontal, vertical, icon-only, etc.)")

    @field_validator('id', mode='before')
    @classmethod
    def coerce_id_to_str(cls, v):
        if v is None:
            return _generate_id()
        return str(v)

class ColorSpecification(BaseModel):
    """Specification for a single color in the palette."""
    name: str = Field(default="", description="Name of the color (e.g., 'Primary Blue')")
    hex: str = Field(default="#000000", description="Hex color code")
    rgb: str = Field(default="0, 0, 0", description="RGB color values")
    cmyk: str = Field(default="0, 0, 0, 100", description="CMYK color values")
    usage: str = Field(default="", description="Primary usage guidelines for this color")
    psychology: str = Field(default="", description="Psychological impact and associations")

class ColorPalette(BaseModel):
    """A complete color palette with roles and specifications."""
    primary: Optional[ColorSpecification] = Field(default=None, description="Primary brand color")
    secondary: Optional[ColorSpecification] = Field(default=None, description="Secondary brand color")
    accent: Optional[ColorSpecification] = Field(default=None, description="Accent color for highlights and CTAs")
    neutral: Optional[ColorSpecification] = Field(default=None, description="Neutral color for backgrounds and text")
    rationale: str = Field(default="", description="Explanation of color psychology and brand fit")
    accessibility_notes: str = Field(default="", description="Accessibility considerations and compliance")
    additional_colors: List[ColorSpecification] = Field(default_factory=list, description="Additional colors if needed")

class TypographySpecification(BaseModel):
    """Typography specifications for the brand."""
    primary_font: str = Field(default="", description="Primary font family name")
    secondary_font: str = Field(default="", description="Secondary font family name")
    font_weights: List[str] = Field(default_factory=list, description="Available font weights")
    font_sizes: Dict[str, str] = Field(default_factory=dict, description="Standard font sizes (h1, h2, body, etc.)")
    usage_guidelines: str = Field(default="", description="Guidelines for font usage")

class ImageryStyle(BaseModel):
    """Imagery style guidelines."""
    photography_style: str = Field(default="", description="Photography style description")
    illustration_style: str = Field(default="", description="Illustration style description")
    icon_style: str = Field(default="", description="Icon style description")
    examples: List[str] = Field(default_factory=list, description="Example image descriptions")

class StyleGuide(BaseModel):
    """Complete visual style guide document."""
    document_info: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    brand_overview: Dict[str, Any] = Field(default_factory=dict, description="Brand overview section")
    logo_guidelines: Dict[str, Any] = Field(default_factory=dict, description="Logo usage guidelines")
    color_guidelines: Dict[str, Any] = Field(default_factory=dict, description="Color usage guidelines")
    typography: Optional[TypographySpecification] = Field(default=None, description="Typography specifications")
    imagery_style: Optional[ImageryStyle] = Field(default=None, description="Imagery style guidelines")
    digital_guidelines: Dict[str, Any] = Field(default_factory=dict, description="Digital application guidelines")
    file_path: str = Field(default="", description="Path to the style guide document")

class BrandIdentityOutput(BaseModel):
    """The final structured output of the Brand Identity Crew."""
    brand_name: str = Field(default="", description="Name of the brand")
    logo_concepts: List[LogoConcept] = Field(default_factory=list, description="List of logo concepts")
    color_palette: Optional[ColorPalette] = Field(default=None, description="Complete color palette")
    style_guide: Optional[StyleGuide] = Field(default=None, description="Complete style guide")
    brand_voice: str = Field(default="", description="Defined brand voice")
    target_audience: str = Field(default="", description="Target audience description")
    industry: str = Field(default="", description="Industry context")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

# ===================================================================
# Marketing Models
# ===================================================================

class SocialMediaPost(BaseModel):
    """A single social media post."""
    platform: Optional[Platform] = Field(default=None, description="Target platform")
    caption: str = Field(default="", description="Post caption text")
    hashtags: List[str] = Field(default_factory=list, description="Relevant hashtags")
    visual_concept: str = Field(default="", description="Visual concept description")
    call_to_action: str = Field(default="", description="Call to action text")
    optimal_posting_time: str = Field(default="", description="Optimal posting time")
    engagement_tips: List[str] = Field(default_factory=list, description="Engagement tips")

class SocialMediaStrategy(BaseModel):
    """Complete social media strategy."""
    brand_name: str = Field(default="", description="Brand name")
    platforms: Dict[str, List[SocialMediaPost]] = Field(default_factory=dict, description="Posts by platform")
    content_themes: List[str] = Field(default_factory=list, description="Content themes and topics")
    posting_schedule: Dict[str, str] = Field(default_factory=dict, description="Recommended posting schedule")
    hashtag_strategy: Dict[str, List[str]] = Field(default_factory=dict, description="Hashtag strategy by platform")
    engagement_strategy: str = Field(default="", description="Overall engagement strategy")

    @field_validator('platforms', mode='before')
    @classmethod
    def normalize_platforms(cls, v):
        """Wrap single post dicts in lists for each platform."""
        if not isinstance(v, dict):
            return v
        normalized = {}
        for platform, posts in v.items():
            if isinstance(posts, dict):
                # Single post dict - wrap in list
                normalized[platform] = [posts]
            elif isinstance(posts, list):
                normalized[platform] = posts
            else:
                normalized[platform] = []
        return normalized

class EmailCampaign(BaseModel):
    """A single email campaign."""
    campaign_type: Optional[CampaignType] = Field(default=None, description="Type of email campaign")
    subject_line: str = Field(default="", description="Email subject line")
    preheader: str = Field(default="", description="Email preheader text")
    body_content: str = Field(default="", description="Email body content")
    call_to_action: str = Field(default="", description="Call to action text")
    cta_link: str = Field(default="", description="Call to action link")
    personalization_fields: List[str] = Field(default_factory=list, description="Personalization fields")
    automation_triggers: Dict[str, str] = Field(default_factory=dict, description="Automation trigger conditions")

    @field_validator('campaign_type', mode='before')
    @classmethod
    def normalize_campaign_type(cls, v):
        """Handle unknown campaign types gracefully."""
        if v is None:
            return None
        if isinstance(v, CampaignType):
            return v
        if isinstance(v, str):
            # Try exact match first
            v_lower = v.lower().replace('-', '_').replace(' ', '_')
            for ct in CampaignType:
                if ct.value == v_lower:
                    return ct
            # Map common variations
            mappings = {
                'product': CampaignType.PRODUCT_ANNOUNCEMENT,
                'launch': CampaignType.PRODUCT_ANNOUNCEMENT,
                'promo': CampaignType.PROMOTIONAL,
                'sale': CampaignType.PROMOTIONAL,
                'discount': CampaignType.PROMOTIONAL,
                'intro': CampaignType.WELCOME,
                'introduction': CampaignType.WELCOME,
                'drip': CampaignType.NURTURE,
                'followup': CampaignType.NURTURE,
                'follow_up': CampaignType.NURTURE,
                'news': CampaignType.NEWSLETTER,
                'update': CampaignType.NEWSLETTER,
                'learn': CampaignType.EDUCATIONAL,
                'tutorial': CampaignType.EDUCATIONAL,
                'winback': CampaignType.REENGAGEMENT,
                'win_back': CampaignType.REENGAGEMENT,
            }
            for key, campaign_type in mappings.items():
                if key in v_lower:
                    return campaign_type
            # Default to promotional for unknown types
            return CampaignType.PROMOTIONAL
        return None

class EmailMarketingStrategy(BaseModel):
    """Complete email marketing strategy."""
    brand_name: str = Field(default="", description="Brand name")
    campaigns: List[EmailCampaign] = Field(default_factory=list, description="List of email campaigns")
    design_guidelines: Dict[str, Any] = Field(default_factory=dict, description="Email design guidelines")
    personalization_strategies: List[str] = Field(default_factory=list, description="Personalization strategies")
    automation_workflows: Dict[str, Any] = Field(default_factory=dict, description="Automation workflow definitions")
    performance_metrics: List[str] = Field(default_factory=list, description="Key performance metrics to track")

class VideoScript(BaseModel):
    """A video script for social media."""
    platform: Optional[Platform] = Field(default=None, description="Target platform")
    concept: str = Field(default="", description="Video concept")
    duration: str = Field(default="", description="Target duration")
    aspect_ratio: str = Field(default="", description="Aspect ratio")
    script: Dict[str, Any] = Field(default_factory=dict, description="Detailed script with scenes")
    production_notes: Dict[str, Any] = Field(default_factory=dict, description="Production guidelines")
    call_to_action: Dict[str, str] = Field(default_factory=dict, description="Call to action details")

class VideoContentStrategy(BaseModel):
    """Complete video content strategy."""
    brand_name: str = Field(default="", description="Brand name")
    videos: List[VideoScript] = Field(default_factory=list, description="List of video scripts")
    content_themes: List[str] = Field(default_factory=list, description="Video content themes")
    production_guidelines: Dict[str, Any] = Field(default_factory=dict, description="Production guidelines")
    platform_specific_requirements: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Platform-specific requirements")

class MarketingOutput(BaseModel):
    """The final structured output of the Marketing Crew."""
    brand_name: str = Field(default="", description="Brand name")
    social_media_strategy: Optional[SocialMediaStrategy] = Field(default=None, description="Social media strategy")
    email_marketing_strategy: Optional[EmailMarketingStrategy] = Field(default=None, description="Email marketing strategy")
    video_content_strategy: Optional[VideoContentStrategy] = Field(default=None, description="Video content strategy")
    overall_marketing_goals: List[str] = Field(default_factory=list, description="Overall marketing goals")
    success_metrics: List[str] = Field(default_factory=list, description="Success metrics to track")
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