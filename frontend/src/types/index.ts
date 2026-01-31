/**
 * TypeScript interfaces for the Brand Identity Workflow frontend.
 */

// ===================================================================
// Enums
// ===================================================================

export type StylePreference =
  | 'modern'
  | 'classic'
  | 'minimalist'
  | 'playful'
  | 'professional'
  | 'luxury'
  | 'tech'
  | 'natural';

export type BrandMood =
  | 'trustworthy'
  | 'innovative'
  | 'energetic'
  | 'calming'
  | 'professional'
  | 'friendly';

export type JobStatus = 'pending' | 'running' | 'completed' | 'failed';

export type WorkflowStep = 'initializing' | 'brand_identity' | 'marketing' | 'finalizing';

export type WSMessageType = 'connected' | 'progress' | 'step_complete' | 'completed' | 'error';

// ===================================================================
// API Types
// ===================================================================

export interface BrandBriefRequest {
  brand_name: string;
  industry: string;
  target_audience: string;
  brand_values: string[];
  style_preference: StylePreference;
  desired_mood: BrandMood;
  brand_voice: string;
  mission: string;
  vision: string;
  competitors: string[];
  unique_selling_proposition: string;
  marketing_goals: string[];
  budget_considerations: string;
  timeline: string;
}

export interface JobResponse {
  job_id: string;
  status: JobStatus;
  current_step: WorkflowStep | null;
  progress: number;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
  error: string | null;
}

// ===================================================================
// WebSocket Types
// ===================================================================

export interface WorkflowProgress {
  type: WSMessageType;
  job_id: string;
  step: WorkflowStep | null;
  progress: number;
  message: string;
  timestamp: string;
}

// ===================================================================
// Result Types
// ===================================================================

export interface LogoVariant {
  file_path?: string;
  model?: string;
  prompt?: string;
  style?: string;
  resolution?: string;
}

export interface LogoConcept {
  id: string;
  name: string;
  description: string;
  rationale: string;
  style: string;
  file_path?: string;
  variants?: LogoVariant[];
  use_cases: string[];
}

export interface ColorResult {
  name: string;
  hex: string;
  rgb: string;
  usage: string;
}

export interface ColorPalette {
  primary: ColorResult;
  secondary: ColorResult;
  accent: ColorResult;
  neutral: ColorResult;
  rationale: string;
}

export interface StyleGuide {
  typography: Record<string, string>;
  imagery: Record<string, string>;
  voice_and_tone: string;
  usage_guidelines: string;
}

export interface BrandIdentityResult {
  logo_concepts: LogoConcept[];
  color_palette: ColorPalette | null;
  style_guide: StyleGuide | null;
}

export interface SocialMediaPostSample {
  caption?: string;
  image_path?: string;
}

export interface SocialMediaContent {
  platforms: string[];
  posts_per_platform: number;
  content_themes: string[];
  sample_posts: SocialMediaPostSample[];
}

export interface EmailCampaigns {
  campaign_types: string[];
  emails_per_campaign: number;
  sample_emails: Record<string, unknown>[];
}

export interface VideoContent {
  platforms: string[];
  videos_per_platform: number;
  content_concepts: Record<string, unknown>[];
}

export interface MarketingResult {
  social_media: SocialMediaContent | null;
  email_campaigns: EmailCampaigns | null;
  video_content: VideoContent | null;
}

export interface WorkflowResult {
  job_id: string;
  status: JobStatus;
  brand_brief: BrandBriefRequest;
  brand_identity: BrandIdentityResult | null;
  marketing: MarketingResult | null;
  created_at: string;
  completed_at: string | null;
  raw_results: Record<string, unknown>;
}

// ===================================================================
// App State Types
// ===================================================================

export type AppView = 'form' | 'progress' | 'results';

export interface AppState {
  view: AppView;
  currentJobId: string | null;
  jobStatus: JobStatus | null;
  progress: number;
  messages: WorkflowProgress[];
  results: WorkflowResult | null;
  error: string | null;
}
