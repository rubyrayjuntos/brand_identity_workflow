/**
 * Main application component for Brand Identity Workflow.
 */

import { useState, useEffect } from 'react';
import { BrandBriefForm } from './components/BrandBriefForm';
import { WorkflowProgress } from './components/WorkflowProgress';
import { ResultsDisplay } from './components/ResultsDisplay';
import { useWorkflowSocket } from './hooks/useWorkflowSocket';
import type { AppView, WorkflowResult } from './types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [view, setView] = useState<AppView>('form');
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);
  const [results, setResults] = useState<WorkflowResult | null>(null);
  const [fetchError, setFetchError] = useState<string | null>(null);

  const {
    progress,
    currentStep,
    messages,
    isComplete,
    error: socketError,
    connect,
  } = useWorkflowSocket();

  // Handle form submission
  const handleFormSubmit = (jobId: string) => {
    setCurrentJobId(jobId);
    setView('progress');
    setFetchError(null);
    connect(jobId);
  };

  // Fetch results when workflow completes
  useEffect(() => {
    if (isComplete && currentJobId) {
      fetchResults(currentJobId);
    }
  }, [isComplete, currentJobId]);

  const fetchResults = async (jobId: string) => {
    try {
      const response = await fetch(`${API_BASE}/api/jobs/${jobId}/results`);
      if (!response.ok) {
        throw new Error('Failed to fetch results');
      }
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setFetchError(err instanceof Error ? err.message : 'Failed to fetch results');
    }
  };

  // Handle progress view actions
  const handleProgressComplete = () => {
    if (socketError || fetchError) {
      // Reset to form on error
      setView('form');
      setCurrentJobId(null);
      setResults(null);
    } else if (results) {
      setView('results');
    }
  };

  // Handle starting new workflow
  const handleNewWorkflow = () => {
    setView('form');
    setCurrentJobId(null);
    setResults(null);
    setFetchError(null);
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="py-6 px-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold gradient-text">Brand Identity Workflow</h1>
            <p className="text-sm text-gray-400">AI-powered brand creation</p>
          </div>

          {view !== 'form' && (
            <button
              onClick={handleNewWorkflow}
              className="text-sm text-gray-400 hover:text-white transition-colors"
            >
              Start Over
            </button>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="px-4 pb-12">
        <div className="animate-fade-in">
          {view === 'form' && (
            <BrandBriefForm onSubmit={handleFormSubmit} />
          )}

          {view === 'progress' && (
            <WorkflowProgress
              progress={progress}
              currentStep={currentStep}
              messages={messages}
              isComplete={isComplete}
              error={socketError || fetchError}
              onComplete={handleProgressComplete}
            />
          )}

          {view === 'results' && results && (
            <ResultsDisplay
              results={results}
              onNewWorkflow={handleNewWorkflow}
            />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="py-6 text-center text-sm text-gray-500">
        <p>Powered by CrewAI</p>
      </footer>
    </div>
  );
}

export default App;
