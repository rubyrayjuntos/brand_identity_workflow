/**
 * Component for displaying workflow results with tabs/sections.
 */

import { useState } from 'react';
import { GlassCard } from './GlassCard';
import type { WorkflowResult } from '../types';

interface ResultsDisplayProps {
  results: WorkflowResult;
  onNewWorkflow: () => void;
}

type Tab = 'logo' | 'colors' | 'style' | 'social' | 'email' | 'video';

export function ResultsDisplay({ results, onNewWorkflow }: ResultsDisplayProps) {
  const [activeTab, setActiveTab] = useState<Tab>('colors');

  const tabs: { id: Tab; label: string; icon: string }[] = [
    { id: 'colors', label: 'Colors', icon: '🎨' },
    { id: 'logo', label: 'Logos', icon: '🏷️' },
    { id: 'style', label: 'Style Guide', icon: '📋' },
    { id: 'social', label: 'Social Media', icon: '📱' },
    { id: 'email', label: 'Email', icon: '📧' },
    { id: 'video', label: 'Video', icon: '🎬' },
  ];

  const handleDownload = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${results.brand_brief.brand_name.replace(/\s+/g, '_')}_brand_results.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <GlassCard>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold text-white">
              {results.brand_brief.brand_name}
            </h2>
            <p className="text-gray-400">
              {results.brand_brief.industry} • {results.brand_brief.style_preference} style
            </p>
          </div>
          <div className="flex gap-3">
            <button onClick={handleDownload} className="btn-secondary">
              Download JSON
            </button>
            <button onClick={onNewWorkflow} className="btn-primary">
              New Workflow
            </button>
          </div>
        </div>
      </GlassCard>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeTab === tab.id
                ? 'bg-white/20 text-white'
                : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-gray-200'
            }`}
          >
            <span className="mr-2">{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <GlassCard>
        {activeTab === 'colors' && <ColorPaletteSection results={results} />}
        {activeTab === 'logo' && <LogoSection results={results} />}
        {activeTab === 'style' && <StyleGuideSection results={results} />}
        {activeTab === 'social' && <SocialMediaSection results={results} />}
        {activeTab === 'email' && <EmailSection results={results} />}
        {activeTab === 'video' && <VideoSection results={results} />}
      </GlassCard>
    </div>
  );
}

function ColorPaletteSection({ results }: { results: WorkflowResult }) {
  const palette = results.brand_identity?.color_palette;

  if (!palette) {
    return <EmptyState message="Color palette not available" />;
  }

  const colors = [
    { ...palette.primary, role: 'Primary' },
    { ...palette.secondary, role: 'Secondary' },
    { ...palette.accent, role: 'Accent' },
    { ...palette.neutral, role: 'Neutral' },
  ];

  return (
    <div>
      <h3 className="text-xl font-semibold text-white mb-4">Color Palette</h3>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {colors.map(color => (
          <div key={color.role} className="space-y-2">
            <div
              className="h-24 rounded-lg shadow-lg"
              style={{ backgroundColor: color.hex }}
            />
            <div>
              <p className="font-medium text-white">{color.role}</p>
              <p className="text-sm text-gray-400">{color.name}</p>
              <p className="text-xs text-gray-500 font-mono">{color.hex}</p>
              <p className="text-xs text-gray-500">RGB: {color.rgb}</p>
            </div>
          </div>
        ))}
      </div>

      {palette.rationale && (
        <div className="bg-white/5 rounded-lg p-4">
          <p className="text-sm text-gray-300">{palette.rationale}</p>
        </div>
      )}
    </div>
  );
}

function LogoSection({ results }: { results: WorkflowResult }) {
  const logos = results.brand_identity?.logo_concepts || [];
  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  if (logos.length === 0) {
    return <EmptyState message="Logo concepts not available" />;
  }

  return (
    <div>
      <h3 className="text-xl font-semibold text-white mb-4">Logo Concepts</h3>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {logos.map(logo => (
          <div key={logo.id} className="bg-white/5 rounded-lg p-4">
            {logo.file_path ? (
              <img
                src={`${API_BASE}/${logo.file_path}`}
                alt={logo.name}
                className="h-32 w-full object-contain rounded-lg mb-3 bg-white/10"
              />
            ) : (
              <div className="h-32 bg-white/10 rounded-lg mb-3 flex items-center justify-center">
                <span className="text-4xl text-gray-500">{results.brand_brief.brand_name[0]}</span>
              </div>
            )}

            <h4 className="font-medium text-white">{logo.name}</h4>
            <p className="text-sm text-gray-400 mt-1">{logo.description}</p>
            <p className="text-xs text-gray-500 mt-2">Style: {logo.style}</p>
            {logo.use_cases.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1">
                {logo.use_cases.map((useCase, i) => (
                  <span key={i} className="text-xs bg-white/10 px-2 py-0.5 rounded">
                    {useCase}
                  </span>
                ))}
              </div>
            )}

            {/* Artistic variants gallery */}
            {logo.variants && logo.variants.length > 0 && (
              <div className="mt-3 grid grid-cols-3 gap-2">
                {logo.variants.map((v, idx) => (
                  <img
                    key={idx}
                    src={`${API_BASE}/${v.file_path}`}
                    alt={`${logo.name}-variant-${idx+1}`}
                    className="h-20 w-full object-cover rounded cursor-pointer"
                    onClick={() => window.open(`${API_BASE}/${v.file_path}`, '_blank')}
                  />
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function StyleGuideSection({ results }: { results: WorkflowResult }) {
  const guide = results.brand_identity?.style_guide;

  if (!guide) {
    return <EmptyState message="Style guide not available" />;
  }

  return (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold text-white">Style Guide</h3>

      {/* Typography */}
      <div>
        <h4 className="font-medium text-white mb-2">Typography</h4>
        <div className="bg-white/5 rounded-lg p-4">
          {Object.entries(guide.typography).map(([key, value]) => (
            <p key={key} className="text-sm text-gray-300">
              <span className="text-gray-500">{key}:</span> {String(value)}
            </p>
          ))}
        </div>
      </div>

      {/* Voice & Tone */}
      {guide.voice_and_tone && (
        <div>
          <h4 className="font-medium text-white mb-2">Voice & Tone</h4>
          <div className="bg-white/5 rounded-lg p-4">
            <p className="text-sm text-gray-300">{guide.voice_and_tone}</p>
          </div>
        </div>
      )}

      {/* Imagery */}
      {Object.keys(guide.imagery).length > 0 && (
        <div>
          <h4 className="font-medium text-white mb-2">Imagery Guidelines</h4>
          <div className="bg-white/5 rounded-lg p-4">
            {Object.entries(guide.imagery).map(([key, value]) => (
              <p key={key} className="text-sm text-gray-300">
                <span className="text-gray-500">{key}:</span> {String(value)}
              </p>
            ))}
          </div>
        </div>
      )}

      {/* Usage Guidelines */}
      {guide.usage_guidelines && (
        <div>
          <h4 className="font-medium text-white mb-2">Usage Guidelines</h4>
          <div className="bg-white/5 rounded-lg p-4">
            <p className="text-sm text-gray-300">{guide.usage_guidelines}</p>
          </div>
        </div>
      )}
    </div>
  );
}

function SocialMediaSection({ results }: { results: WorkflowResult }) {
  const social = results.marketing?.social_media;
  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  if (!social) {
    return <EmptyState message="Social media content not available" />;
  }

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold text-white">Social Media Strategy</h3>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard label="Platforms" value={social.platforms.length} />
        <StatCard label="Posts/Platform" value={social.posts_per_platform} />
        <StatCard label="Content Themes" value={social.content_themes.length} />
        <StatCard label="Sample Posts" value={social.sample_posts.length} />
      </div>

      {social.platforms.length > 0 && (
        <div>
          <h4 className="font-medium text-white mb-2">Target Platforms</h4>
          <div className="flex flex-wrap gap-2">
            {social.platforms.map((platform, i) => (
              <span key={i} className="bg-blue-500/20 text-blue-300 px-3 py-1 rounded-full text-sm">
                {platform}
              </span>
            ))}
          </div>
        </div>
      )}

      {social.content_themes.length > 0 && (
        <div>
          <h4 className="font-medium text-white mb-2">Content Themes</h4>
          <div className="flex flex-wrap gap-2">
            {social.content_themes.map((theme, i) => (
              <span key={i} className="bg-purple-500/20 text-purple-300 px-3 py-1 rounded-full text-sm">
                {theme}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Sample post preview */}
      {social.sample_posts.length > 0 && social.sample_posts[0].image_path && (
        <div>
          <h4 className="font-medium text-white mb-2">Sample Post Preview</h4>
          <div className="bg-white/5 rounded-lg p-4">
            <img
              src={`${API_BASE}/${social.sample_posts[0].image_path}`}
              alt="Sample post"
              className="w-full rounded-md object-cover"
            />
            <p className="text-sm text-gray-300 mt-2">{social.sample_posts[0].caption}</p>
          </div>
        </div>
      )}
    </div>
  );
}

function EmailSection({ results }: { results: WorkflowResult }) {
  const email = results.marketing?.email_campaigns;

  if (!email) {
    return <EmptyState message="Email campaigns not available" />;
  }

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold text-white">Email Marketing Strategy</h3>

      <div className="grid grid-cols-3 gap-4">
        <StatCard label="Campaign Types" value={email.campaign_types.length} />
        <StatCard label="Emails/Campaign" value={email.emails_per_campaign} />
        <StatCard label="Sample Emails" value={email.sample_emails.length} />
      </div>

      {email.campaign_types.length > 0 && (
        <div>
          <h4 className="font-medium text-white mb-2">Campaign Types</h4>
          <div className="flex flex-wrap gap-2">
            {email.campaign_types.map((type, i) => (
              <span key={i} className="bg-green-500/20 text-green-300 px-3 py-1 rounded-full text-sm">
                {type}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function VideoSection({ results }: { results: WorkflowResult }) {
  const video = results.marketing?.video_content;

  if (!video) {
    return <EmptyState message="Video content not available" />;
  }

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold text-white">Video Content Strategy</h3>

      <div className="grid grid-cols-3 gap-4">
        <StatCard label="Platforms" value={video.platforms.length} />
        <StatCard label="Videos/Platform" value={video.videos_per_platform} />
        <StatCard label="Concepts" value={video.content_concepts.length} />
      </div>

      {video.platforms.length > 0 && (
        <div>
          <h4 className="font-medium text-white mb-2">Target Platforms</h4>
          <div className="flex flex-wrap gap-2">
            {video.platforms.map((platform, i) => (
              <span key={i} className="bg-red-500/20 text-red-300 px-3 py-1 rounded-full text-sm">
                {platform}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="bg-white/5 rounded-lg p-4 text-center">
      <p className="text-2xl font-bold text-white">{value}</p>
      <p className="text-sm text-gray-400">{label}</p>
    </div>
  );
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="text-center py-12">
      <p className="text-gray-400">{message}</p>
    </div>
  );
}
