# Code Style and Conventions

## Python

### General Style
- Follow PEP 8 style guidelines
- Use snake_case for functions and variables
- Use PascalCase for classes
- Use UPPER_SNAKE_CASE for constants

### Type Hints
- Use type hints for function parameters and return types
- Use Pydantic models for data validation (see `models.py`)

### Docstrings
- Use triple-quoted docstrings for modules, classes, and functions
- Follow Google-style docstring format

### Imports
- Standard library imports first
- Third-party imports second
- Local imports third
- Alphabetical order within each group

### Agent Pattern
- Agent factory functions in `agents.py` follow naming: `create_<role>_agent()`
- Tasks defined as module-level variables in `tasks.py`
- Tools as standalone functions or classes in `tools.py`

### Model Pattern (Pydantic)
```python
class MyModel(BaseModel):
    field_name: str
    optional_field: Optional[int] = None
```

## TypeScript/React

### General Style
- Use TypeScript strict mode
- Use functional components with hooks
- Use PascalCase for components
- Use camelCase for functions and variables

### File Organization
- Components in `src/components/`
- Hooks in `src/hooks/`
- Types in `src/types/`

### Styling
- Use Tailwind CSS utility classes
- Follow mobile-first responsive design
