/**
 * Component for displaying real-time workflow progress.
 */

import { GlassCard } from './GlassCard';
import type { WorkflowProgress as WorkflowProgressType, WorkflowStep } from '../types';

interface WorkflowProgressProps {
  progress: number;
  currentStep: string | null;
  messages: WorkflowProgressType[];
  isComplete: boolean;
  error: string | null;
  onComplete: () => void;
}

const steps: { id: WorkflowStep; label: string; description: string }[] = [
  { id: 'initializing', label: 'Initializing', description: 'Setting up workflow' },
  { id: 'brand_identity', label: 'Brand Identity', description: 'Creating logo, colors & style guide' },
  { id: 'marketing', label: 'Marketing', description: 'Developing marketing content' },
  { id: 'finalizing', label: 'Finalizing', description: 'Completing workflow' },
];

function getStepIndex(step: string | null): number {
  if (!step) return -1;
  return steps.findIndex(s => s.id === step);
}

export function WorkflowProgress({
  progress,
  currentStep,
  messages,
  isComplete,
  error,
  onComplete,
}: WorkflowProgressProps) {
  const currentStepIndex = getStepIndex(currentStep);

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Progress Header */}
      <GlassCard>
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-2">
            {isComplete ? 'Workflow Complete!' : error ? 'Workflow Failed' : 'Processing...'}
          </h2>
          <p className="text-gray-300">
            {isComplete
              ? 'Your brand identity and marketing materials are ready.'
              : error
              ? error
              : 'Creating your brand identity and marketing content...'}
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mt-6">
          <div className="flex justify-between text-sm text-gray-400 mb-2">
            <span>Progress</span>
            <span>{progress}%</span>
          </div>
          <div className="h-3 bg-white/10 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-500 rounded-full ${
                error
                  ? 'bg-red-500'
                  : isComplete
                  ? 'bg-green-500'
                  : 'bg-gradient-to-r from-blue-500 to-purple-500'
              }`}
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Step Indicators */}
        <div className="mt-8 flex justify-between">
          {steps.map((step, index) => {
            const isActive = index === currentStepIndex;
            const isCompleted = index < currentStepIndex || isComplete;
            const isPending = index > currentStepIndex;

            return (
              <div key={step.id} className="flex flex-col items-center flex-1">
                {/* Step Circle */}
                <div
                  className={`
                    w-10 h-10 rounded-full flex items-center justify-center
                    transition-all duration-300
                    ${
                      isCompleted
                        ? 'bg-green-500 text-white'
                        : isActive
                        ? 'bg-blue-500 text-white animate-pulse'
                        : isPending
                        ? 'bg-white/10 text-gray-400'
                        : 'bg-white/10 text-gray-400'
                    }
                  `}
                >
                  {isCompleted ? (
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <span className="text-sm font-medium">{index + 1}</span>
                  )}
                </div>

                {/* Step Label */}
                <span
                  className={`mt-2 text-xs font-medium ${
                    isCompleted ? 'text-green-400' : isActive ? 'text-blue-400' : 'text-gray-500'
                  }`}
                >
                  {step.label}
                </span>

                {/* Connector Line */}
                {index < steps.length - 1 && (
                  <div
                    className={`absolute h-0.5 top-5 left-1/2 -translate-y-1/2 ${
                      index < currentStepIndex || isComplete ? 'bg-green-500' : 'bg-white/10'
                    }`}
                    style={{ width: 'calc(100% - 2.5rem)' }}
                  />
                )}
              </div>
            );
          })}
        </div>
      </GlassCard>

      {/* Messages Log */}
      <GlassCard>
        <h3 className="text-lg font-semibold text-white mb-4">Activity Log</h3>
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {messages.length === 0 ? (
            <p className="text-gray-400 text-sm">Waiting for updates...</p>
          ) : (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`flex items-start gap-3 p-2 rounded-lg ${
                  msg.type === 'error'
                    ? 'bg-red-500/10'
                    : msg.type === 'completed'
                    ? 'bg-green-500/10'
                    : msg.type === 'step_complete'
                    ? 'bg-blue-500/10'
                    : 'bg-white/5'
                }`}
              >
                {/* Icon */}
                <div className="flex-shrink-0 mt-0.5">
                  {msg.type === 'error' ? (
                    <svg className="w-4 h-4 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  ) : msg.type === 'completed' || msg.type === 'step_complete' ? (
                    <svg className="w-4 h-4 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <svg className="w-4 h-4 text-blue-400 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                  )}
                </div>

                {/* Message */}
                <div className="flex-1 min-w-0">
                  <p
                    className={`text-sm ${
                      msg.type === 'error' ? 'text-red-300' : 'text-gray-300'
                    }`}
                  >
                    {msg.message}
                  </p>
                  <p className="text-xs text-gray-500 mt-0.5">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
      </GlassCard>

      {/* Action Button */}
      {(isComplete || error) && (
        <div className="text-center">
          <button onClick={onComplete} className="btn-primary">
            {isComplete ? 'View Results' : 'Try Again'}
          </button>
        </div>
      )}
    </div>
  );
}
