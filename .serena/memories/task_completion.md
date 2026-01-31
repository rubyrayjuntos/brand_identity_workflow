# Task Completion Checklist

## Before Marking a Task Complete

### For Python Changes
1. Ensure code follows PEP 8 style
2. Add/update type hints where appropriate
3. Test the changes manually if applicable
4. Check for import errors: `python -c "import module_name"`

### For Frontend Changes
1. Run `npm run lint` in the frontend directory
2. Run `npm run build` to ensure TypeScript compiles
3. Test the UI in browser if applicable

### For API Changes
1. Test endpoint with curl or API client
2. Verify WebSocket connections if modified
3. Check schema compatibility

## After Making Changes

### Git Workflow
1. Stage relevant files: `git add <specific-files>`
2. Create descriptive commit message
3. Push to remote if appropriate

### Documentation
- Update README.md if adding new features
- Update relevant .md documentation files
- Add docstrings for new functions/classes

## Common Verification Commands

```bash
# Python syntax check
python -m py_compile <file.py>

# Frontend lint
cd frontend && npm run lint

# Frontend build
cd frontend && npm run build

# Test backend API
curl http://localhost:8000/health
```
