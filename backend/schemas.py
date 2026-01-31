"""
API request/response Pydantic models for the Brand Identity Workflow API.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


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


class JobStatus(str, Enum):
    """Job execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStep(str, Enum):
    """Workflow execution steps."""
    INITIALIZING = "initializing"
    BRAND_IDENTITY = "brand_identity"
    MARKETING = "marketing"
    FINALIZING = "finalizing"


# ===================================================================
# API Request Models
# ===================================================================

class BrandBriefRequest(BaseModel):
    """API input for creating a new brand identity workflow job."""
    brand_name: str = Field(..., description="Name of the brand")
    industry: str = Field(..., description="Industry the brand operates in")
    target_audience: str = Field(..., description="Description of target audience")
    brand_values: List[str] = Field(default_factory=list, description="List of brand values")
    style_preference: StylePreference = Field(default=StylePreference.MODERN, description="Preferred style")
    desired_mood: BrandMood = Field(default=BrandMood.INNOVATIVE, description="Desired brand mood")
    brand_voice: str = Field(default="", description="Brand voice description")
    mission: str = Field(default="", description="Brand mission")
    vision: str = Field(default="", description="Brand vision")
    competitors: List[str] = Field(default_factory=list, description="List of competitors")
    unique_selling_proposition: str = Field(default="", description="Unique selling proposition")
    marketing_goals: List[str] = Field(default_factory=list, description="Marketing goals")
    budget_considerations: str = Field(default="", description="Budget considerations")
    timeline: str = Field(default="", description="Project timeline")


# ===================================================================
# API Response Models
# ===================================================================

class JobResponse(BaseModel):
    """Response for job creation and status queries."""
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatus = Field(..., description="Current job status")
    current_step: Optional[WorkflowStep] = Field(None, description="Current workflow step")
    progress: int = Field(0, description="Overall progress percentage (0-100)")
    created_at: datetime = Field(..., description="Job creation timestamp")
    started_at: Optional[datetime] = Field(None, description="Job start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Job completion timestamp")
    error: Optional[str] = Field(None, description="Error message if failed")


class JobListResponse(BaseModel):
    """Response for listing jobs."""
    jobs: List[JobResponse] = Field(..., description="List of jobs")
    total: int = Field(..., description="Total number of jobs")


# ===================================================================
# WebSocket Message Models
# ===================================================================

class WSMessageType(str, Enum):
    """WebSocket message types."""
    CONNECTED = "connected"
    PROGRESS = "progress"
    STEP_COMPLETE = "step_complete"
    COMPLETED = "completed"
    ERROR = "error"


class WorkflowProgress(BaseModel):
    """WebSocket message for workflow progress updates."""
    type: WSMessageType = Field(..., description="Message type")
    job_id: str = Field(..., description="Job identifier")
    step: Optional[WorkflowStep] = Field(None, description="Current step")
    progress: int = Field(0, description="Progress percentage (0-100)")
    message: str = Field("", description="Status message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")


# ===================================================================
# Workflow Result Models
# ===================================================================

class LogoConceptResult(BaseModel):
    """A logo concept in the results."""
    id: str = Field(..., description="Concept identifier")
    name: str = Field(..., description="Concept name")
    description: str = Field(..., description="Concept description")
    rationale: str = Field(..., description="Design rationale")
    style: str = Field(..., description="Style category")
    file_path: Optional[str] = Field("", description="Path to the rendered logo image")
    use_cases: List[str] = Field(default_factory=list, description="Recommended use cases")


class ColorResult(BaseModel):
    """A color in the palette."""
    name: str = Field(..., description="Color name")
    hex: str = Field(..., description="Hex color code")
    rgb: str = Field(..., description="RGB values")
    usage: str = Field(..., description="Usage guidelines")


class ColorPaletteResult(BaseModel):
    """Color palette results."""
    primary: ColorResult = Field(..., description="Primary color")
    secondary: ColorResult = Field(..., description="Secondary color")
    accent: ColorResult = Field(..., description="Accent color")
    neutral: ColorResult = Field(..., description="Neutral color")
    rationale: str = Field("", description="Color palette rationale")


class StyleGuideResult(BaseModel):
    """Style guide results."""
    typography: Dict[str, Any] = Field(default_factory=dict, description="Typography guidelines")
    imagery: Dict[str, Any] = Field(default_factory=dict, description="Imagery guidelines")
    voice_and_tone: str = Field("", description="Voice and tone guidelines")
    usage_guidelines: str = Field("", description="General usage guidelines")


class SocialMediaContentResult(BaseModel):
    """Social media content results."""
    platforms: List[str] = Field(default_factory=list, description="Covered platforms")
    posts_per_platform: int = Field(0, description="Number of posts per platform")
    content_themes: List[str] = Field(default_factory=list, description="Content themes")
    sample_posts: List[Dict[str, Any]] = Field(default_factory=list, description="Sample posts")


class EmailCampaignResult(BaseModel):
    """Email campaign results."""
    campaign_types: List[str] = Field(default_factory=list, description="Campaign types")
    emails_per_campaign: int = Field(0, description="Emails per campaign")
    sample_emails: List[Dict[str, Any]] = Field(default_factory=list, description="Sample emails")


class VideoContentResult(BaseModel):
    """Video content results."""
    platforms: List[str] = Field(default_factory=list, description="Target platforms")
    videos_per_platform: int = Field(0, description="Videos per platform")
    content_concepts: List[Dict[str, Any]] = Field(default_factory=list, description="Video concepts")


class BrandIdentityResult(BaseModel):
    """Brand identity workflow results."""
    logo_concepts: List[LogoConceptResult] = Field(default_factory=list, description="Logo concepts")
    color_palette: Optional[ColorPaletteResult] = Field(None, description="Color palette")
    style_guide: Optional[StyleGuideResult] = Field(None, description="Style guide")


class MarketingResult(BaseModel):
    """Marketing workflow results."""
    social_media: Optional[SocialMediaContentResult] = Field(None, description="Social media content")
    email_campaigns: Optional[EmailCampaignResult] = Field(None, description="Email campaigns")
    video_content: Optional[VideoContentResult] = Field(None, description="Video content")


class WorkflowResult(BaseModel):
    """Complete workflow results."""
    job_id: str = Field(..., description="Job identifier")
    status: JobStatus = Field(..., description="Job status")
    brand_brief: BrandBriefRequest = Field(..., description="Original brand brief")
    brand_identity: Optional[BrandIdentityResult] = Field(None, description="Brand identity results")
    marketing: Optional[MarketingResult] = Field(None, description="Marketing results")
    created_at: datetime = Field(..., description="Creation timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    raw_results: Dict[str, Any] = Field(default_factory=dict, description="Raw workflow results")
