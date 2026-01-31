#!/bin/bash
# Run the FastAPI backend server

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "Starting Brand Identity Workflow API on http://localhost:8000"
uvicorn backend.api:app --reload --port 8000
