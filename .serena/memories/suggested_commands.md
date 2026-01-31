# Suggested Commands

## Backend Development

### Running the Backend API
```bash
# Start FastAPI server with uvicorn
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000

# Or use the run script
./run_backend.sh
```

### Running the Main Workflow (CLI)
```bash
python main.py
```

### Testing Python
```bash
python test_python.py
```

### Installing Python Dependencies
```bash
pip install -r requirements.txt
# Or minimal version
pip install -r requirements_minimal.txt
```

## Frontend Development

### Starting Development Server
```bash
cd frontend
npm run dev
# Or use the run script from root
./run_frontend.sh
```

### Building for Production
```bash
cd frontend
npm run build
```

### Linting
```bash
cd frontend
npm run lint
```

### Preview Production Build
```bash
cd frontend
npm run preview
```

### Installing Frontend Dependencies
```bash
cd frontend
npm install
```

## Environment Configuration

### Setting LLM Model
```bash
# Use free local Ollama models
export CREWAI_MODEL=qwen2.5

# Or paid OpenAI
export CREWAI_MODEL=gpt-4o-mini
export OPENAI_API_KEY=your_key_here
```

### Available Models
Run `python llm_config.py` to see all available model presets.

## Git Commands
```bash
git status
git add <files>
git commit -m "message"
git push
```

## Utility Commands (Linux)
```bash
ls -la           # List files
find . -name "*.py"  # Find files
grep -r "pattern" .  # Search in files
```
