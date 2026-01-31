/**
 * Reusable glassmorphic card component.
 */

import React from 'react';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

export function GlassCard({
  children,
  className = '',
  hover = false,
  padding = 'md',
}: GlassCardProps) {
  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  return (
    <div
      className={`
        glass-card
        ${paddingClasses[padding]}
        ${hover ? 'glass-card-hover' : ''}
        ${className}
      `}
    >
      {children}
    </div>
  );
}
