# Brand Identity Workflow - Project Overview

## Purpose
A comprehensive system for automating brand identity creation and marketing campaign development using AI. The system uses a multi-agent architecture (MAS) powered by CrewAI to orchestrate specialized AI agents that handle different aspects of brand development.

## Tech Stack

### Backend (Python)
- **Framework**: CrewAI for multi-agent orchestration
- **API**: FastAPI with WebSocket support for real-time progress updates
- **LLM Support**: 
  - OpenAI GPT models (paid)
  - Ollama local models (free): qwen2.5, llama3.2, deepseek-v3, mistral
- **Key Libraries**: langchain-openai, langchain-ollama, litellm, uvicorn

### Frontend (React/TypeScript)
- **Build Tool**: Vite 7.x
- **Framework**: React 19
- **Styling**: Tailwind CSS 3.4
- **Type Checking**: TypeScript 5.9

## Architecture

### Core Python Modules
- `main.py` - Main orchestrator with `BrandIdentityWorkflow` class
- `agents.py` - Agent factory functions (logo_designer, color_specialist, style_guide_creator, etc.)
- `tasks.py` - Task definitions for brand identity and marketing workflows
- `tools.py` - Tool implementations for AI agents
- `models.py` - Pydantic models for data structures
- `llm_config.py` - LLM configuration with model presets

### Backend API (`backend/`)
- `api.py` - FastAPI routes with WebSocket endpoint
- `schemas.py` - API request/response schemas
- `job_manager.py` - Background job management

### Frontend (`frontend/`)
- `App.tsx` - Main application component
- `components/` - UI components (BrandBriefForm, WorkflowProgress, ResultsDisplay, GlassCard)
- `hooks/useWorkflowSocket.ts` - WebSocket hook for real-time updates
- `types/index.ts` - TypeScript type definitions

## Workflow Types
1. **Brand Identity Workflow**: Logo concepts, color palette, style guide
2. **Marketing Workflow**: Social media strategy, email campaigns, video content
3. **Complete Workflow**: Both brand identity and marketing combined
