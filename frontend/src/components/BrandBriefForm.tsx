/**
 * Form component for submitting brand brief information.
 */

import React, { useState } from 'react';
import { GlassCard } from './GlassCard';
import type { BrandBriefRequest, StylePreference, BrandMood } from '../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface BrandBriefFormProps {
  onSubmit: (jobId: string) => void;
}

const styleOptions: { value: StylePreference; label: string }[] = [
  { value: 'modern', label: 'Modern' },
  { value: 'classic', label: 'Classic' },
  { value: 'minimalist', label: 'Minimalist' },
  { value: 'playful', label: 'Playful' },
  { value: 'professional', label: 'Professional' },
  { value: 'luxury', label: 'Luxury' },
  { value: 'tech', label: 'Tech' },
  { value: 'natural', label: 'Natural' },
];

const moodOptions: { value: BrandMood; label: string }[] = [
  { value: 'innovative', label: 'Innovative' },
  { value: 'trustworthy', label: 'Trustworthy' },
  { value: 'energetic', label: 'Energetic' },
  { value: 'calming', label: 'Calming' },
  { value: 'professional', label: 'Professional' },
  { value: 'friendly', label: 'Friendly' },
];

export function BrandBriefForm({ onSubmit }: BrandBriefFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<BrandBriefRequest>({
    brand_name: 'InnovateTech',
    industry: 'AI Software Development',
    target_audience: 'Tech-savvy professionals aged 25-45, working in software development, data science, and IT management',
    brand_values: ['Innovation', 'Reliability', 'Efficiency', 'Collaboration', 'Excellence'],
    style_preference: 'modern',
    desired_mood: 'innovative',
    brand_voice: 'Professional yet approachable',
    mission: 'To empower developers and organizations with cutting-edge AI tools that streamline workflows and drive innovation',
    vision: 'To be the leading platform for AI-powered development tools, making advanced technology accessible to every developer',
    competitors: ['GitHub Copilot', 'Tabnine', 'Kite'],
    unique_selling_proposition: 'Seamless integration with existing development workflows with advanced customization and team collaboration features',
    marketing_goals: ['Increase brand awareness', 'Drive product adoption', 'Build developer community', 'Generate qualified leads'],
    budget_considerations: 'Mid-market pricing with freemium model',
    timeline: '3-6 months for full brand rollout',
  });

  const [brandValuesInput, setBrandValuesInput] = useState('Innovation, Reliability, Efficiency, Collaboration, Excellence');
  const [competitorsInput, setCompetitorsInput] = useState('GitHub Copilot, Tabnine, Kite');
  const [marketingGoalsInput, setMarketingGoalsInput] = useState('Increase brand awareness, Drive product adoption, Build developer community, Generate qualified leads');

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleArrayInputChange = (
    value: string,
    setter: React.Dispatch<React.SetStateAction<string>>,
    field: 'brand_values' | 'competitors' | 'marketing_goals'
  ) => {
    setter(value);
    const items = value
      .split(',')
      .map(item => item.trim())
      .filter(item => item.length > 0);
    setFormData(prev => ({ ...prev, [field]: items }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/api/jobs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create job');
      }

      const data = await response.json();
      onSubmit(data.job_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <GlassCard className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-white mb-6">Brand Brief</h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-200 mb-2">
              Brand Name *
            </label>
            <input
              type="text"
              name="brand_name"
              value={formData.brand_name}
              onChange={handleInputChange}
              required
              className="input-glass w-full"
              placeholder="Enter brand name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-200 mb-2">
              Industry *
            </label>
            <input
              type="text"
              name="industry"
              value={formData.industry}
              onChange={handleInputChange}
              required
              className="input-glass w-full"
              placeholder="e.g., Technology, Healthcare"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-200 mb-2">
            Target Audience *
          </label>
          <textarea
            name="target_audience"
            value={formData.target_audience}
            onChange={handleInputChange}
            required
            rows={2}
            className="input-glass w-full"
            placeholder="Describe your target audience"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-200 mb-2">
            Brand Values (comma-separated)
          </label>
          <input
            type="text"
            value={brandValuesInput}
            onChange={e => handleArrayInputChange(e.target.value, setBrandValuesInput, 'brand_values')}
            className="input-glass w-full"
            placeholder="e.g., Innovation, Trust, Excellence"
          />
        </div>

        {/* Style Preferences */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-200 mb-2">
              Style Preference
            </label>
            <select
              name="style_preference"
              value={formData.style_preference}
              onChange={handleInputChange}
              className="input-glass w-full"
            >
              {styleOptions.map(opt => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-200 mb-2">
              Desired Mood
            </label>
            <select
              name="desired_mood"
              value={formData.desired_mood}
              onChange={handleInputChange}
              className="input-glass w-full"
            >
              {moodOptions.map(opt => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Brand Voice & Mission */}
        <div>
          <label className="block text-sm font-medium text-gray-200 mb-2">
            Brand Voice
          </label>
          <input
            type="text"
            name="brand_voice"
            value={formData.brand_voice}
            onChange={handleInputChange}
            className="input-glass w-full"
            placeholder="e.g., Professional yet approachable"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-200 mb-2">
              Mission
            </label>
            <textarea
              name="mission"
              value={formData.mission}
              onChange={handleInputChange}
              rows={3}
              className="input-glass w-full"
              placeholder="What is your brand's mission?"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-200 mb-2">
              Vision
            </label>
            <textarea
              name="vision"
              value={formData.vision}
              onChange={handleInputChange}
              rows={3}
              className="input-glass w-full"
              placeholder="What is your brand's vision?"
            />
          </div>
        </div>

        {/* Competition & USP */}
        <div>
          <label className="block text-sm font-medium text-gray-200 mb-2">
            Competitors (comma-separated)
          </label>
          <input
            type="text"
            value={competitorsInput}
            onChange={e => handleArrayInputChange(e.target.value, setCompetitorsInput, 'competitors')}
            className="input-glass w-full"
            placeholder="e.g., Competitor A, Competitor B"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-200 mb-2">
            Unique Selling Proposition
          </label>
          <textarea
            name="unique_selling_proposition"
            value={formData.unique_selling_proposition}
            onChange={handleInputChange}
            rows={2}
            className="input-glass w-full"
            placeholder="What makes your brand unique?"
          />
        </div>

        {/* Marketing */}
        <div>
          <label className="block text-sm font-medium text-gray-200 mb-2">
            Marketing Goals (comma-separated)
          </label>
          <input
            type="text"
            value={marketingGoalsInput}
            onChange={e => handleArrayInputChange(e.target.value, setMarketingGoalsInput, 'marketing_goals')}
            className="input-glass w-full"
            placeholder="e.g., Brand awareness, Lead generation"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-200 mb-2">
              Budget Considerations
            </label>
            <input
              type="text"
              name="budget_considerations"
              value={formData.budget_considerations}
              onChange={handleInputChange}
              className="input-glass w-full"
              placeholder="e.g., Mid-market, Premium"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-200 mb-2">
              Timeline
            </label>
            <input
              type="text"
              name="timeline"
              value={formData.timeline}
              onChange={handleInputChange}
              className="input-glass w-full"
              placeholder="e.g., 3-6 months"
            />
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-4 text-red-200">
            {error}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isSubmitting}
          className="btn-primary w-full"
        >
          {isSubmitting ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Starting Workflow...
            </span>
          ) : (
            'Start Brand Identity Workflow'
          )}
        </button>
      </form>
    </GlassCard>
  );
}
