/**
 * Custom hook for managing WebSocket connection to workflow progress.
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import type { WorkflowProgress } from '../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_BASE = API_BASE.replace('http', 'ws');

interface UseWorkflowSocketReturn {
  status: 'disconnected' | 'connecting' | 'connected' | 'error';
  progress: number;
  currentStep: string | null;
  messages: WorkflowProgress[];
  isComplete: boolean;
  error: string | null;
  connect: (jobId: string) => void;
  disconnect: () => void;
}

export function useWorkflowSocket(): UseWorkflowSocketReturn {
  const [status, setStatus] = useState<'disconnected' | 'connecting' | 'connected' | 'error'>('disconnected');
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState<string | null>(null);
  const [messages, setMessages] = useState<WorkflowProgress[]>([]);
  const [isComplete, setIsComplete] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);
  const pingIntervalRef = useRef<number | null>(null);

  const cleanup = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    if (pingIntervalRef.current) {
      clearInterval(pingIntervalRef.current);
      pingIntervalRef.current = null;
    }
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  const connect = useCallback((jobId: string) => {
    cleanup();
    setStatus('connecting');
    setMessages([]);
    setProgress(0);
    setCurrentStep(null);
    setIsComplete(false);
    setError(null);

    const ws = new WebSocket(`${WS_BASE}/ws/${jobId}`);
    wsRef.current = ws;

    ws.onopen = () => {
      setStatus('connected');

      // Set up ping interval
      pingIntervalRef.current = window.setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send('ping');
        }
      }, 25000);
    };

    ws.onmessage = (event) => {
      // Ignore plain text pong responses
      if (event.data === 'pong') {
        return;
      }

      try {
        const data = JSON.parse(event.data);

        // Ignore keepalive messages
        if (data.type === 'keepalive') {
          return;
        }

        const message = data as WorkflowProgress;

        setMessages(prev => [...prev, message]);

        if (message.progress !== undefined) {
          setProgress(message.progress);
        }

        if (message.step) {
          setCurrentStep(message.step);
        }

        switch (message.type) {
          case 'completed':
            setIsComplete(true);
            setProgress(100);
            cleanup();
            break;
          case 'error':
            setError(message.message);
            setStatus('error');
            cleanup();
            break;
        }
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e);
      }
    };

    ws.onerror = () => {
      setStatus('error');
      setError('WebSocket connection error');
    };

    ws.onclose = () => {
      if (status !== 'error' && !isComplete) {
        setStatus('disconnected');
      }
    };
  }, [cleanup, status, isComplete]);

  const disconnect = useCallback(() => {
    cleanup();
    setStatus('disconnected');
  }, [cleanup]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      cleanup();
    };
  }, [cleanup]);

  return {
    status,
    progress,
    currentStep,
    messages,
    isComplete,
    error,
    connect,
    disconnect,
  };
}
