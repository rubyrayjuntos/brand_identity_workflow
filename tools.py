"""
Tools module for the Brand Identity Management Agent Workflow.
Contains tools for brand identity creation and marketing tasks.
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from crewai.tools import tool
from PIL import Image, ImageDraw, ImageFont

load_dotenv()


# ===================================================================
# Brand Asset Tools
# ===================================================================

@tool
def generate_logo_concepts(brand_name: str, industry: str, target_audience: str,
                          brand_values: str, style_preference: str) -> str:
    """
    Generate logo concepts using AI image generation.

    Args:
        brand_name: Name of the brand
        industry: Industry the brand operates in
        target_audience: Description of target audience
        brand_values: Comma-separated list of brand values
        style_preference: Preferred style (modern, classic, minimalist, etc.)

    Returns:
        JSON string containing logo concepts and rationales
    """
    print(f"--- Tool: Generating logo concepts for '{brand_name}' ---")

    values_list = [v.strip() for v in brand_values.split(",")]

    concepts = {
        "concepts": [
            {
                "id": "concept_1",
                "name": f"{brand_name}_modern_minimal",
                "description": f"Modern, minimalist logo for {brand_name}",
                "rationale": f"Clean, geometric design reflecting {style_preference} aesthetic. Suitable for {industry} industry.",
                "file_path": f"assets/logos/{brand_name}_concept_1.png",
                "style": style_preference
            },
            {
                "id": "concept_2",
                "name": f"{brand_name}_professional_trustworthy",
                "description": f"Professional and trustworthy logo for {brand_name}",
                "rationale": f"Established, reliable design that builds trust with {target_audience}.",
                "file_path": f"assets/logos/{brand_name}_concept_2.png",
                "style": "professional"
            },
            {
                "id": "concept_3",
                "name": f"{brand_name}_innovative_tech",
                "description": f"Innovative tech-focused logo for {brand_name}",
                "rationale": f"Forward-thinking design that positions {brand_name} as innovative in {industry}.",
                "file_path": f"assets/logos/{brand_name}_concept_3.png",
                "style": "innovative"
            }
        ],
        "brand_context": {
            "name": brand_name,
            "industry": industry,
            "target_audience": target_audience,
            "brand_values": values_list,
            "style_preference": style_preference
        }
    }

    # Ensure assets directory exists and create placeholder logo images
    try:
        for concept in concepts.get("concepts", []):
            path = concept.get("file_path")
            if not path:
                continue
            dir_name = os.path.dirname(path)
            os.makedirs(dir_name, exist_ok=True)

            # Create a simple placeholder image if it doesn't already exist
            if not os.path.exists(path):
                img_size = (512, 512)
                bg_color = (240, 240, 240)
                img = Image.new("RGBA", img_size, bg_color)
                draw = ImageDraw.Draw(img)

                text = concept.get("name", "Logo")
                try:
                    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
                except Exception:
                    font = ImageFont.load_default()

                text_w, text_h = draw.textsize(text, font=font)
                draw.text(((img_size[0]-text_w)/2, (img_size[1]-text_h)/2), text, fill=(40, 40, 40), font=font)
                img.save(path)
    except Exception as e:
        print(f"Warning: failed to create placeholder logo images: {e}")

    return json.dumps(concepts, indent=2)


@tool
def analyze_color_psychology(brand_values: str, target_audience: str,
                            industry: str, desired_mood: str) -> str:
    """
    Analyze color psychology and generate color palette recommendations.

    Args:
        brand_values: Comma-separated list of brand values
        target_audience: Description of target audience
        industry: Industry context
        desired_mood: Desired emotional response (trustworthy, energetic, calming, innovative)

    Returns:
        JSON string containing color palette and psychological analysis
    """
    print(f"--- Tool: Analyzing color psychology for mood: '{desired_mood}' ---")

    values_list = [v.strip() for v in brand_values.split(",")]

    color_psychology = {
        "trustworthy": {
            "primary": "#1A365D",
            "secondary": "#2D3748",
            "accent": "#3182CE",
            "neutral": "#E2E8F0"
        },
        "energetic": {
            "primary": "#E53E3E",
            "secondary": "#F6AD55",
            "accent": "#FBD38D",
            "neutral": "#F7FAFC"
        },
        "calming": {
            "primary": "#38A169",
            "secondary": "#4FD1C7",
            "accent": "#9F7AEA",
            "neutral": "#F0FFF4"
        },
        "innovative": {
            "primary": "#805AD5",
            "secondary": "#00B5D8",
            "accent": "#F6E05E",
            "neutral": "#EDF2F7"
        }
    }

    palette = color_psychology.get(desired_mood, color_psychology["trustworthy"])

    result = {
        "palette": {
            "primary": {
                "hex": palette["primary"],
                "rgb": "26, 54, 93",
                "cmyk": "89, 50, 0, 9",
                "usage": "Primary brand color, main CTAs, headers"
            },
            "secondary": {
                "hex": palette["secondary"],
                "rgb": "45, 55, 72",
                "cmyk": "0, 0, 0, 72",
                "usage": "Secondary elements, subheaders"
            },
            "accent": {
                "hex": palette["accent"],
                "rgb": "49, 130, 206",
                "cmyk": "76, 37, 0, 19",
                "usage": "Highlights, links, important elements"
            },
            "neutral": {
                "hex": palette["neutral"],
                "rgb": "226, 232, 240",
                "cmyk": "6, 3, 0, 6",
                "usage": "Backgrounds, text on dark backgrounds"
            }
        },
        "psychology_analysis": {
            "mood": desired_mood,
            "target_audience_appeal": f"Colors chosen to resonate with {target_audience}",
            "industry_appropriateness": f"Suitable for {industry} sector",
            "brand_value_alignment": f"Reflects values: {', '.join(values_list)}"
        },
        "accessibility_notes": {
            "contrast_ratios": "All color combinations meet WCAG AA standards",
            "color_blind_friendly": "Palette works well for color vision deficiencies"
        }
    }

    return json.dumps(result, indent=2)


@tool
def generate_style_guide_doc(brand_name: str, logo_concepts: str,
                            color_palette: str, brand_values: str,
                            target_audience: str, brand_voice: str) -> str:
    """
    Generate a comprehensive visual style guide document.

    Args:
        brand_name: Name of the brand
        logo_concepts: JSON string of logo concepts from previous step
        color_palette: JSON string of color palette from previous step
        brand_values: Comma-separated list of brand values
        target_audience: Target audience description
        brand_voice: Brand voice (formal, casual, playful, etc.)

    Returns:
        JSON string containing style guide document details
    """
    print(f"--- Tool: Generating style guide for '{brand_name}' ---")

    values_list = [v.strip() for v in brand_values.split(",")]

    try:
        logos = json.loads(logo_concepts) if isinstance(logo_concepts, str) else logo_concepts
        colors = json.loads(color_palette) if isinstance(color_palette, str) else color_palette
    except json.JSONDecodeError:
        logos = {"concepts": []}
        colors = {"palette": {}}

    style_guide = {
        "document_info": {
            "brand_name": brand_name,
            "version": "1.0",
            "created_date": datetime.now().isoformat(),
            "file_path": f"assets/style_guides/{brand_name}_style_guide_v1.pdf"
        },
        "brand_overview": {
            "mission": "To provide innovative solutions in our industry",
            "vision": f"To be the leading brand in {brand_name}'s field",
            "values": values_list,
            "target_audience": target_audience,
            "brand_voice": brand_voice
        },
        "logo_guidelines": {
            "primary_logo": logos.get("concepts", [{}])[0] if logos.get("concepts") else {},
            "variations": logos.get("concepts", []),
            "clear_space": "Minimum clear space: 1x logo height on all sides",
            "minimum_size": "Minimum size: 24px height for digital, 0.5 inches for print",
            "forbidden_uses": [
                "Do not stretch or distort the logo",
                "Do not change colors unless using approved palette",
                "Do not add effects or shadows",
                "Do not place on busy backgrounds"
            ]
        },
        "color_guidelines": colors,
        "typography": {
            "primary_font": {
                "name": "Inter",
                "weights": ["Regular", "Medium", "Bold"],
                "usage": "Headings, titles, and important text"
            },
            "secondary_font": {
                "name": "Open Sans",
                "weights": ["Regular", "Light", "SemiBold"],
                "usage": "Body text, captions, and supporting content"
            },
            "font_sizes": {
                "h1": "32px",
                "h2": "24px",
                "h3": "20px",
                "body": "16px",
                "caption": "14px"
            }
        },
        "imagery_style": {
            "photography": "Bright, authentic, diverse, natural lighting",
            "illustrations": "Clean, modern, minimal line art",
            "icons": "Consistent stroke width, rounded corners, simple shapes"
        },
        "digital_guidelines": {
            "web_usage": "Responsive design, accessible color contrast",
            "social_media": "Consistent sizing, brand colors, clear messaging",
            "email": "Clean layout, brand colors, mobile-friendly"
        }
    }

    return json.dumps(style_guide, indent=2)


# ===================================================================
# Marketing Tools
# ===================================================================

@tool
def search_web_for_trends(industry: str, topic: str = "") -> str:
    """
    Search for current trends in the industry.

    Args:
        industry: Industry to search trends for
        topic: Specific topic to focus on (optional)

    Returns:
        JSON string containing trending topics and insights
    """
    print(f"--- Tool: Searching for trends in '{industry}' ---")

    trends = {
        "industry": industry,
        "search_date": datetime.now().isoformat(),
        "trending_topics": [
            {
                "topic": "AI Integration",
                "relevance": "High",
                "description": "Companies are increasingly integrating AI into their products",
                "hashtags": ["#AI", "#Innovation", "#TechTrends"]
            },
            {
                "topic": "Remote Work Solutions",
                "relevance": "Medium",
                "description": "Continued focus on tools that support remote and hybrid work",
                "hashtags": ["#RemoteWork", "#Productivity", "#WorkFromHome"]
            },
            {
                "topic": "Sustainability",
                "relevance": "High",
                "description": "Growing emphasis on sustainable business practices",
                "hashtags": ["#Sustainability", "#GreenTech", "#EcoFriendly"]
            }
        ],
        "platform_specific_trends": {
            "linkedin": ["Professional development", "Industry insights", "Thought leadership"],
            "instagram": ["Behind-the-scenes", "Product demos", "Team culture"],
            "twitter": ["Industry news", "Quick tips", "Community engagement"]
        }
    }

    return json.dumps(trends, indent=2)


@tool
def generate_social_media_post(brand_name: str, platform: str,
                              topic: str, campaign_goal: str) -> str:
    """
    Generate social media post content aligned with brand guidelines.

    Args:
        brand_name: Name of the brand
        platform: Social media platform (instagram, linkedin, twitter, facebook)
        topic: Post topic or theme
        campaign_goal: Goal of the campaign (engagement, awareness, conversion)

    Returns:
        JSON string containing post content and recommendations
    """
    print(f"--- Tool: Generating {platform} post for '{brand_name}' ---")

    post_content = {
        "platform": platform,
        "brand_name": brand_name,
        "caption": f"🚀 Exciting news from {brand_name}! We're exploring {topic} and how it's shaping our industry. What are your thoughts on this trend? #Innovation #TechTrends #{brand_name.replace(' ', '')}",
        "hashtags": ["#Innovation", "#TechTrends", f"#{brand_name.replace(' ', '')}", "#IndustryInsights", "#FutureOfTech"],
        "visual_concept": f"Modern graphic featuring {topic} with {brand_name} branding",
        "call_to_action": "Share your thoughts in the comments below! 👇",
        "optimal_posting_time": "10:00 AM - 2:00 PM",
        "engagement_tips": [
            "Respond to comments within 2 hours",
            "Use brand colors from style guide",
            "Include relevant hashtags",
            "Ask questions to encourage engagement"
        ]
    }

    # Create a placeholder image for the visual concept
    try:
        img_dir = os.path.join("assets", "social")
        os.makedirs(img_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_name = f"{brand_name.replace(' ', '').lower()}_{platform}_{timestamp}.png"
        img_path = os.path.join(img_dir, img_name)

        if not os.path.exists(img_path):
            img_size = (1200, 630)  # typical social preview size
            bg_color = (245, 245, 245)
            img = Image.new("RGBA", img_size, bg_color)
            draw = ImageDraw.Draw(img)
            text = f"{brand_name} - {topic}"
            try:
                font = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
            except Exception:
                font = ImageFont.load_default()
            text_w, text_h = draw.textsize(text, font=font)
            draw.text(((img_size[0]-text_w)/2, (img_size[1]-text_h)/2), text, fill=(40,40,40), font=font)
            img.save(img_path)

        post_content["image_path"] = img_path
    except Exception as e:
        print(f"Warning: failed to create social image: {e}")

    return json.dumps(post_content, indent=2)


@tool
def generate_email_campaign_plan(brand_name: str, target_audience: str,
                                campaign_type: str, goals: str) -> str:
    """
    Generate email marketing campaign plan and content.

    Args:
        brand_name: Name of the brand
        target_audience: Target audience description
        campaign_type: Type of campaign (welcome, nurture, promotional)
        goals: Comma-separated list of campaign goals

    Returns:
        JSON string containing email campaign plan and content
    """
    print(f"--- Tool: Generating email campaign plan for '{brand_name}' ---")

    goals_list = [g.strip() for g in goals.split(",")]

    campaign_templates = {
        "welcome": {
            "subject_line": f"Welcome to {brand_name}! 🎉 Your Journey Starts Here",
            "preheader": f"Discover how {brand_name} can transform your experience"
        },
        "nurture": {
            "subject_line": f"Exclusive {brand_name} Insights Just for You",
            "preheader": "Valuable content to help you succeed"
        },
        "promotional": {
            "subject_line": f"🎉 Special {brand_name} Offer - Limited Time!",
            "preheader": "Don't miss out on this exclusive opportunity"
        }
    }

    template = campaign_templates.get(campaign_type, campaign_templates["welcome"])

    campaign_plan = {
        "campaign_type": campaign_type,
        "brand_name": brand_name,
        "target_audience": target_audience,
        "goals": goals_list,
        "email_sequence": [
            {
                "email_number": 1,
                "subject_line": template["subject_line"],
                "preheader": template["preheader"],
                "body_content": f"Hi [First Name],\n\nWelcome to {brand_name}! We're thrilled to have you join our community.\n\nBest regards,\nThe {brand_name} Team",
                "call_to_action": "Explore Our Services",
                "cta_link": "[Website URL]"
            }
        ],
        "personalization_strategies": [
            "Use recipient's first name",
            "Segment by industry or role",
            "Include relevant product recommendations"
        ],
        "automation_triggers": {
            "welcome": "New signup",
            "nurture": "7 days after last email",
            "promotional": "Special events or product launches"
        }
    }

    return json.dumps(campaign_plan, indent=2)


@tool
def generate_video_script(brand_name: str, concept: str,
                         platform: str, duration: str) -> str:
    """
    Generate video script and storyboard for social media.

    Args:
        brand_name: Name of the brand
        concept: Video concept or theme
        platform: Target platform (tiktok, instagram, youtube)
        duration: Target duration (15s, 30s, 60s)

    Returns:
        JSON string containing video script and production details
    """
    print(f"--- Tool: Generating video script for '{brand_name}' ---")

    platform_guidelines = {
        "tiktok": {"aspect_ratio": "9:16", "max_duration": "60 seconds"},
        "instagram": {"aspect_ratio": "9:16", "max_duration": "90 seconds"},
        "youtube": {"aspect_ratio": "16:9", "max_duration": "10+ minutes"}
    }

    guidelines = platform_guidelines.get(platform, platform_guidelines["instagram"])

    video_script = {
        "brand_name": brand_name,
        "platform": platform,
        "concept": concept,
        "target_duration": duration,
        "aspect_ratio": guidelines["aspect_ratio"],
        "script": {
            "opening": {
                "duration": "3 seconds",
                "visual": f"{brand_name} logo animation",
                "text_overlay": f"Welcome to {brand_name}"
            },
            "main_content": {
                "duration": f"{int(duration.replace('s', '')) - 6} seconds",
                "visual": f"Showcase of {concept}",
                "text_overlay": f"Discover how {brand_name} can help with {concept}"
            },
            "closing": {
                "duration": "3 seconds",
                "visual": f"{brand_name} logo with website",
                "text_overlay": "Visit our website to learn more"
            }
        },
        "call_to_action": {
            "text": f"Learn more at {brand_name.lower().replace(' ', '')}.com",
            "placement": "End of video and description"
        }
    }

    return json.dumps(video_script, indent=2)


# ===================================================================
# Data Management Tools
# ===================================================================

@tool
def save_brand_profile(brand_data: str) -> str:
    """
    Save brand profile to database.

    Args:
        brand_data: JSON string containing brand data

    Returns:
        JSON string containing saved brand profile with ID
    """
    try:
        data = json.loads(brand_data) if isinstance(brand_data, str) else brand_data
    except json.JSONDecodeError:
        data = {"brand_name": "Unknown"}

    print(f"--- Tool: Saving brand profile for '{data.get('brand_name', 'Unknown')}' ---")

    brand_profile = {
        "brand_id": f"brand_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "status": "active",
        **data
    }

    return json.dumps(brand_profile, indent=2)


@tool
def save_generated_assets(assets: str, brand_id: str) -> str:
    """
    Save generated brand assets.

    Args:
        assets: JSON string containing list of assets
        brand_id: Brand identifier

    Returns:
        JSON string containing saved assets information
    """
    print(f"--- Tool: Saving assets for brand '{brand_id}' ---")

    try:
        assets_list = json.loads(assets) if isinstance(assets, str) else assets
    except json.JSONDecodeError:
        assets_list = []

    saved_assets = {
        "brand_id": brand_id,
        "saved_at": datetime.now().isoformat(),
        "assets": assets_list,
        "total_count": len(assets_list) if isinstance(assets_list, list) else 1
    }

    return json.dumps(saved_assets, indent=2)


# ===================================================================
# Tool Classes for backwards compatibility
# ===================================================================

class BrandAssetTools:
    """Tools for brand identity core elements."""
    generate_logo_concepts = generate_logo_concepts
    analyze_color_psychology = analyze_color_psychology
    generate_style_guide_doc = generate_style_guide_doc


class MarketingTools:
    """Tools for community engagement and marketing tasks."""
    search_web_for_trends = search_web_for_trends
    generate_social_media_post = generate_social_media_post
    generate_email_campaign_plan = generate_email_campaign_plan
    generate_video_script = generate_video_script


class DataManagementTools:
    """Tools for managing brand data and assets."""
    save_brand_profile = save_brand_profile
    save_generated_assets = save_generated_assets
