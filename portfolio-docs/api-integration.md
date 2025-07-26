# 🔌 API Integration & Data Validation

## Overview

The Brand Identity Management System integrates with multiple AI APIs and implements comprehensive data validation patterns to ensure structured, reliable outputs. This document details the integration architecture and validation strategies.

## AI API Integration

### 1. OpenAI API Integration

#### **Core Integration Points**
```python
# OpenAI API configuration
import openai
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Text generation for brand content
def generate_brand_content(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content

# Image generation for logo concepts
def generate_logo_image(prompt: str) -> str:
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    return response.data[0].url
```

#### **API Usage Patterns**
- **Text Generation**: Brand descriptions, marketing copy, style guidelines
- **Image Generation**: Logo concepts, visual elements, brand assets
- **Structured Output**: JSON-formatted responses for data validation

### 2. CrewAI Framework Integration

#### **Agent Configuration**
```python
from crewai import Agent, Task, Crew, Process

# Agent with OpenAI integration
logo_designer = Agent(
    role='Logo Concept Designer',
    goal='Generate innovative logo concepts',
    backstory='Expert graphic designer with 15+ years experience',
    tools=[BrandAssetTools.generate_logo_concepts],
    llm=ChatOpenAI(model="gpt-4", temperature=0.7),
    verbose=True
)
```

#### **Task Orchestration**
```python
# Hierarchical task execution
brand_identity_crew = Crew(
    agents=[brand_identity_coordinator, logo_designer, color_specialist],
    tasks=[brand_identity_coordination_task],
    process=Process.hierarchical,
    verbose=2
)
```

## Data Validation Architecture

### 1. Pydantic Model Implementation

#### **Core Data Models**
```python
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict, Any, Optional
from datetime import datetime

class LogoConcept(BaseModel):
    """Validated logo concept structure."""
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Descriptive name")
    description: str = Field(..., description="Design description")
    rationale: str = Field(..., description="Design rationale")
    style: str = Field(..., description="Style category")
    file_path: str = Field(..., description="Asset path")
    use_cases: List[str] = Field(default_factory=list)
    variations: List[str] = Field(default_factory=list)

class ColorSpecification(BaseModel):
    """Validated color specification."""
    name: str = Field(..., description="Color name")
    hex: str = Field(..., regex=r"^#[0-9A-Fa-f]{6}$")
    rgb: str = Field(..., description="RGB values")
    cmyk: str = Field(..., description="CMYK values")
    usage: str = Field(..., description="Usage guidelines")
    psychology: str = Field(..., description="Psychological impact")
```

#### **Validation Features**
- **Type Safety**: All fields have defined types
- **Regex Validation**: Color codes, URLs, and formats
- **Field Descriptions**: Self-documenting models
- **Default Values**: Sensible defaults for optional fields
- **Custom Validators**: Business logic validation

### 2. Structured Output Validation

#### **Task Output Validation**
```python
# Task with structured output
logo_task = Task(
    description="Generate 3 logo concepts",
    expected_output="List of LogoConcept objects",
    output_pydantic=LogoConcept,
    many_output=True  # Multiple outputs
)

# Validation during execution
try:
    result = crew.kickoff(inputs=brand_brief)
    # Pydantic automatically validates the output
    validated_result = LogoConcept.parse_obj(result)
except ValidationError as e:
    # Handle validation errors
    print(f"Validation failed: {e}")
```

#### **Error Handling**
```python
from pydantic import ValidationError

def validate_agent_output(output: Dict[str, Any], model: BaseModel) -> BaseModel:
    """Validate agent output against Pydantic model."""
    try:
        return model.parse_obj(output)
    except ValidationError as e:
        # Log validation errors
        logger.error(f"Validation failed: {e}")
        # Return default or retry
        return model.parse_obj(get_default_output())
```

## Tool Integration Patterns

### 1. BrandAssetTools

#### **Logo Generation Tool**
```python
class BrandAssetTools:
    @staticmethod
    def generate_logo_concepts(
        brand_name: str, 
        industry: str, 
        target_audience: str,
        brand_values: List[str], 
        style_preference: str
    ) -> Dict[str, Any]:
        """Generate logo concepts using AI."""
        
        # Construct AI prompt
        prompt = f"""
        Create 3 logo concepts for {brand_name}, a {industry} company.
        Target audience: {target_audience}
        Brand values: {', '.join(brand_values)}
        Style preference: {style_preference}
        
        Return structured JSON with:
        - concept_id
        - name
        - description
        - rationale
        - style
        - file_path
        - use_cases (array)
        - variations (array)
        """
        
        # Call OpenAI API
        response = generate_brand_content(prompt)
        
        # Parse and validate response
        try:
            concepts = json.loads(response)
            return {"concepts": concepts}
        except json.JSONDecodeError:
            # Fallback to structured generation
            return generate_structured_concepts(brand_name, industry)
```

#### **Color Analysis Tool**
```python
@staticmethod
def analyze_color_psychology(
    brand_values: List[str],
    target_audience: str,
    industry: str,
    desired_mood: str
) -> Dict[str, Any]:
    """Analyze color psychology and generate palette."""
    
    # Color psychology mapping
    color_psychology = {
        "trustworthy": {
            "primary": "#1A365D",  # Deep blue
            "secondary": "#2D3748",  # Dark gray
            "accent": "#3182CE",  # Bright blue
            "neutral": "#E2E8F0"  # Light gray
        },
        "energetic": {
            "primary": "#E53E3E",  # Red
            "secondary": "#F6AD55",  # Orange
            "accent": "#FBD38D",  # Yellow
            "neutral": "#F7FAFC"  # White
        }
    }
    
    # Select palette based on mood
    palette = color_psychology.get(desired_mood, color_psychology["trustworthy"])
    
    # Validate color accessibility
    accessibility_notes = validate_color_accessibility(palette)
    
    return {
        "palette": palette,
        "psychology_analysis": {
            "mood": desired_mood,
            "target_audience_appeal": f"Colors chosen for {target_audience}",
            "industry_appropriateness": f"Suitable for {industry}",
            "brand_value_alignment": f"Reflects: {', '.join(brand_values)}"
        },
        "accessibility_notes": accessibility_notes
    }
```

### 2. MarketingTools

#### **Social Media Content Generation**
```python
class MarketingTools:
    @staticmethod
    def generate_social_media_post(
        brand_name: str,
        style_guide: Dict,
        platform: str,
        topic: str,
        campaign_goal: str
    ) -> Dict[str, Any]:
        """Generate platform-specific social media content."""
        
        # Platform-specific prompts
        platform_prompts = {
            "linkedin": "Professional tone, business-focused content",
            "instagram": "Visual-first, engaging storytelling",
            "twitter": "Concise, trending topics, hashtags",
            "facebook": "Community-focused, shareable content"
        }
        
        prompt = f"""
        Create a {platform} post for {brand_name} about {topic}.
        Goal: {campaign_goal}
        Style: {platform_prompts[platform]}
        
        Include:
        - Caption text
        - Relevant hashtags
        - Visual concept
        - Call to action
        - Optimal posting time
        """
        
        response = generate_brand_content(prompt)
        return parse_social_media_response(response)
```

## Error Handling & Resilience

### 1. API Error Handling

#### **Rate Limiting**
```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def api_call_with_retry(func, *args, **kwargs):
    """Retry API calls with exponential backoff."""
    try:
        return func(*args, **kwargs)
    except openai.RateLimitError:
        logger.warning("Rate limit hit, retrying...")
        time.sleep(60)  # Wait 1 minute
        raise
    except openai.APIError as e:
        logger.error(f"API error: {e}")
        raise
```

#### **Fallback Strategies**
```python
def generate_content_with_fallback(prompt: str) -> str:
    """Generate content with multiple fallback strategies."""
    try:
        # Primary: GPT-4
        return generate_with_gpt4(prompt)
    except Exception as e:
        logger.warning(f"GPT-4 failed: {e}")
        try:
            # Fallback 1: GPT-3.5
            return generate_with_gpt35(prompt)
        except Exception as e:
            logger.warning(f"GPT-3.5 failed: {e}")
            # Fallback 2: Template-based generation
            return generate_from_template(prompt)
```

### 2. Data Validation Recovery

#### **Partial Validation**
```python
def validate_partial_output(output: Dict[str, Any], model: BaseModel) -> BaseModel:
    """Validate output with partial data recovery."""
    try:
        return model.parse_obj(output)
    except ValidationError as e:
        # Try to fix common issues
        fixed_output = fix_common_validation_issues(output, e)
        try:
            return model.parse_obj(fixed_output)
        except ValidationError:
            # Use default values for missing fields
            return model.parse_obj(get_default_values(model))
```

## Performance Optimization

### 1. Caching Strategy

#### **Response Caching**
```python
import hashlib
import json
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_api_call(prompt_hash: str, model: str) -> str:
    """Cache API responses to reduce costs and improve performance."""
    # Implementation would use prompt_hash to retrieve cached response
    pass

def get_prompt_hash(prompt: str) -> str:
    """Generate hash for prompt caching."""
    return hashlib.md5(prompt.encode()).hexdigest()
```

### 2. Batch Processing

#### **Efficient API Usage**
```python
def batch_generate_content(prompts: List[str]) -> List[str]:
    """Batch multiple API calls for efficiency."""
    # Group similar prompts
    grouped_prompts = group_similar_prompts(prompts)
    
    results = []
    for group in grouped_prompts:
        # Use batch API if available
        batch_response = batch_api_call(group)
        results.extend(batch_response)
    
    return results
```

## Security & Compliance

### 1. API Key Management

#### **Secure Configuration**
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Secure API key handling
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found in environment variables")

# Validate API key format
if not OPENAI_API_KEY.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format")
```

### 2. Data Privacy

#### **Input Sanitization**
```python
import re

def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', user_input)
    # Limit length
    return sanitized[:1000]

def validate_brand_brief(brief: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize brand brief input."""
    sanitized_brief = {}
    for key, value in brief.items():
        if isinstance(value, str):
            sanitized_brief[key] = sanitize_input(value)
        else:
            sanitized_brief[key] = value
    return sanitized_brief
```

This API integration architecture ensures reliable, validated, and secure communication between the multi-agent system and external AI services while maintaining high performance and error resilience. 