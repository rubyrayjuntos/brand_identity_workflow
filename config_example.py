"""
Configuration example for the Brand Identity Management Agent Workflow.
Copy this file to config.py and fill in your actual API keys and settings.
"""

import os
from typing import Dict, Any

# ===================================================================
# API Configuration
# ===================================================================

# OpenAI Configuration
OPENAI_CONFIG = {
    'api_key': os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here'),
    'model': os.getenv('OPENAI_MODEL', 'gpt-4'),
    'temperature': 0.7,
    'max_tokens': 4000
}

# Alternative AI Providers
ANTHROPIC_CONFIG = {
    'api_key': os.getenv('ANTHROPIC_API_KEY', 'your_anthropic_api_key_here'),
    'model': 'claude-3-sonnet-20240229'
}

GOOGLE_AI_CONFIG = {
    'api_key': os.getenv('GOOGLE_AI_API_KEY', 'your_google_ai_api_key_here'),
    'model': 'gemini-pro'
}

# ===================================================================
# Image Generation APIs
# ===================================================================

# DALL-E Configuration
DALLE_CONFIG = {
    'api_key': os.getenv('DALLE_API_KEY', 'your_dalle_api_key_here'),
    'model': 'dall-e-3',
    'size': '1024x1024',
    'quality': 'standard'
}

# Midjourney Configuration (if API becomes available)
MIDJOURNEY_CONFIG = {
    'api_key': os.getenv('MIDJOURNEY_API_KEY', 'your_midjourney_api_key_here'),
    'version': 'v6'
}

# Stability AI Configuration
STABILITY_AI_CONFIG = {
    'api_key': os.getenv('STABILITY_AI_API_KEY', 'your_stability_ai_api_key_here'),
    'model': 'stable-diffusion-xl-1024-v1-0'
}

# ===================================================================
# Social Media APIs
# ===================================================================

# Facebook/Meta Configuration
FACEBOOK_CONFIG = {
    'app_id': os.getenv('FACEBOOK_APP_ID', 'your_facebook_app_id_here'),
    'app_secret': os.getenv('FACEBOOK_APP_SECRET', 'your_facebook_app_secret_here'),
    'access_token': os.getenv('FACEBOOK_ACCESS_TOKEN', 'your_facebook_access_token_here')
}

# Twitter/X Configuration
TWITTER_CONFIG = {
    'api_key': os.getenv('TWITTER_API_KEY', 'your_twitter_api_key_here'),
    'api_secret': os.getenv('TWITTER_API_SECRET', 'your_twitter_api_secret_here'),
    'bearer_token': os.getenv('TWITTER_BEARER_TOKEN', 'your_twitter_bearer_token_here')
}

# LinkedIn Configuration
LINKEDIN_CONFIG = {
    'client_id': os.getenv('LINKEDIN_CLIENT_ID', 'your_linkedin_client_id_here'),
    'client_secret': os.getenv('LINKEDIN_CLIENT_SECRET', 'your_linkedin_client_secret_here'),
    'access_token': os.getenv('LINKEDIN_ACCESS_TOKEN', 'your_linkedin_access_token_here')
}

# Instagram Configuration
INSTAGRAM_CONFIG = {
    'access_token': os.getenv('INSTAGRAM_ACCESS_TOKEN', 'your_instagram_access_token_here'),
    'business_account_id': os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', 'your_instagram_business_account_id_here')
}

# ===================================================================
# Email Marketing APIs
# ===================================================================

# Mailchimp Configuration
MAILCHIMP_CONFIG = {
    'api_key': os.getenv('MAILCHIMP_API_KEY', 'your_mailchimp_api_key_here'),
    'server_prefix': os.getenv('MAILCHIMP_SERVER_PREFIX', 'us1')
}

# SendGrid Configuration
SENDGRID_CONFIG = {
    'api_key': os.getenv('SENDGRID_API_KEY', 'your_sendgrid_api_key_here'),
    'from_email': os.getenv('SENDGRID_FROM_EMAIL', 'noreply@yourbrand.com')
}

# HubSpot Configuration
HUBSPOT_CONFIG = {
    'api_key': os.getenv('HUBSPOT_API_KEY', 'your_hubspot_api_key_here'),
    'portal_id': os.getenv('HUBSPOT_PORTAL_ID', 'your_hubspot_portal_id_here')
}

# ===================================================================
# Storage Configuration
# ===================================================================

# AWS S3 Configuration
AWS_CONFIG = {
    'access_key_id': os.getenv('AWS_ACCESS_KEY_ID', 'your_aws_access_key_here'),
    'secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY', 'your_aws_secret_access_key_here'),
    'region': os.getenv('AWS_REGION', 'us-east-1'),
    's3_bucket': os.getenv('AWS_S3_BUCKET', 'your_s3_bucket_name_here')
}

# Local Storage Configuration
STORAGE_CONFIG = {
    'output_dir': os.getenv('OUTPUT_DIR', 'results'),
    'assets_dir': os.getenv('ASSETS_DIR', 'assets'),
    'temp_dir': os.getenv('TEMP_DIR', 'temp'),
    'max_file_size': 50 * 1024 * 1024  # 50MB
}

# ===================================================================
# Application Configuration
# ===================================================================

# General Application Settings
APP_CONFIG = {
    'debug': os.getenv('DEBUG', 'True').lower() == 'true',
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
    'max_workers': int(os.getenv('MAX_WORKERS', '4')),
    'timeout': int(os.getenv('TIMEOUT', '300')),  # 5 minutes
    'retry_attempts': int(os.getenv('RETRY_ATTEMPTS', '3'))
}

# Database Configuration (for future use)
DATABASE_CONFIG = {
    'url': os.getenv('DATABASE_URL', 'sqlite:///brand_workflow.db'),
    'pool_size': int(os.getenv('DB_POOL_SIZE', '10')),
    'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', '20'))
}

# ===================================================================
# Workflow Configuration
# ===================================================================

# Agent Configuration
AGENT_CONFIG = {
    'default_model': 'gpt-4',
    'temperature': 0.7,
    'max_tokens': 4000,
    'verbose': True,
    'allow_delegation': False
}

# Task Configuration
TASK_CONFIG = {
    'max_iterations': 3,
    'timeout_per_task': 600,  # 10 minutes
    'memory_enabled': True
}

# Brand Identity Configuration
BRAND_IDENTITY_CONFIG = {
    'logo_concepts_count': 3,
    'color_palette_size': 4,
    'style_guide_sections': [
        'brand_overview',
        'logo_guidelines', 
        'color_guidelines',
        'typography',
        'imagery_style',
        'digital_guidelines'
    ]
}

# Marketing Configuration
MARKETING_CONFIG = {
    'social_media_platforms': ['instagram', 'linkedin', 'twitter', 'facebook'],
    'posts_per_platform': 3,
    'email_campaign_types': ['welcome', 'nurture', 'promotional'],
    'video_platforms': ['tiktok', 'instagram', 'youtube', 'linkedin']
}

# ===================================================================
# Validation Functions
# ===================================================================

def validate_config() -> Dict[str, Any]:
    """
    Validate the configuration and return any issues.
    
    Returns:
        Dictionary containing validation results
    """
    issues = []
    warnings = []
    
    # Check required API keys
    if OPENAI_CONFIG['api_key'] == 'your_openai_api_key_here':
        issues.append("OpenAI API key not configured")
    
    # Check optional configurations
    if DALLE_CONFIG['api_key'] == 'your_dalle_api_key_here':
        warnings.append("DALL-E API key not configured - logo generation will be simulated")
    
    if FACEBOOK_CONFIG['app_id'] == 'your_facebook_app_id_here':
        warnings.append("Facebook API not configured - social media posting will be simulated")
    
    if MAILCHIMP_CONFIG['api_key'] == 'your_mailchimp_api_key_here':
        warnings.append("Mailchimp API not configured - email campaigns will be simulated")
    
    # Check storage configuration
    for dir_name in ['output_dir', 'assets_dir', 'temp_dir']:
        dir_path = STORAGE_CONFIG[dir_name]
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create directory {dir_path}: {str(e)}")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': warnings
    }

def get_config_summary() -> str:
    """
    Get a summary of the current configuration.
    
    Returns:
        String containing configuration summary
    """
    validation = validate_config()
    
    summary = "Configuration Summary:\n"
    summary += "=" * 50 + "\n"
    
    # API Status
    summary += f"OpenAI API: {'✅ Configured' if OPENAI_CONFIG['api_key'] != 'your_openai_api_key_here' else '❌ Not configured'}\n"
    summary += f"DALL-E API: {'✅ Configured' if DALLE_CONFIG['api_key'] != 'your_dalle_api_key_here' else '❌ Not configured'}\n"
    summary += f"Social Media APIs: {'✅ Configured' if FACEBOOK_CONFIG['app_id'] != 'your_facebook_app_id_here' else '❌ Not configured'}\n"
    summary += f"Email Marketing APIs: {'✅ Configured' if MAILCHIMP_CONFIG['api_key'] != 'your_mailchimp_api_key_here' else '❌ Not configured'}\n"
    
    # Storage
    summary += f"Storage: {'✅ Configured' if validation['valid'] else '❌ Issues found'}\n"
    
    # Issues and Warnings
    if validation['issues']:
        summary += "\nIssues:\n"
        for issue in validation['issues']:
            summary += f"  ❌ {issue}\n"
    
    if validation['warnings']:
        summary += "\nWarnings:\n"
        for warning in validation['warnings']:
            summary += f"  ⚠️  {warning}\n"
    
    return summary

# ===================================================================
# Usage Example
# ===================================================================

if __name__ == "__main__":
    print(get_config_summary())
    
    validation = validate_config()
    if not validation['valid']:
        print("\n❌ Configuration has issues that need to be resolved.")
        exit(1)
    else:
        print("\n✅ Configuration is valid!") 