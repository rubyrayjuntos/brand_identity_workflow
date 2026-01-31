# Asset Explorer Feature Design

**Date:** 2026-01-30
**Status:** Approved

## Overview

Add project-based asset management with a visual explorer to the Brand Identity Workflow frontend. Users can save brand artifacts to a user-specified folder and browse/download them via a sidebar explorer.

## Design Decisions

| Decision | Choice |
|----------|--------|
| Storage location | User-specified path (folder picker in form) |
| Folder structure | Categorized folders by artifact type |
| UI layout | Sidebar panel with tree navigation + preview area |
| Path selection | In brand brief form before generation |

## Folder Structure

When a user creates a new brand project at `/path/to/MyBrand`:

```
/path/to/MyBrand/
├── project.json                    # Project metadata
├── brand_brief.json                # Original brand brief input
├── brand_identity/
│   ├── color_palette.json
│   ├── logos/
│   │   ├── concept_1.json
│   │   ├── concept_2.json
│   │   └── concept_3.json
│   └── style_guide.json
└── marketing/
    ├── social_media/
    │   ├── strategy.json
    │   ├── instagram.json
    │   ├── linkedin.json
    │   └── twitter.json
    ├── email/
    │   ├── strategy.json
    │   └── campaigns/
    │       ├── welcome.json
    │       ├── nurture.json
    │       └── promotional.json
    └── video/
        ├── strategy.json
        └── scripts/
            ├── youtube.json
            └── tiktok.json
```

## Backend API

### New File: `backend/project_manager.py`

Functions:
- `create_project(path, brand_name)` - Creates folder structure
- `save_artifact(project_path, artifact_type, data)` - Saves individual artifacts
- `scan_project(path)` - Returns project tree structure
- `list_projects(paths)` - Scans multiple paths for projects
- `get_artifact(project_path, artifact_path)` - Returns artifact content
- `delete_project(path)` - Removes project folder

### New API Endpoints

```python
# Project Management
POST   /api/projects/create          # Create new project folder
GET    /api/projects/scan            # Scan a path for existing projects
GET    /api/projects/{path}/tree     # Get folder tree for a project
DELETE /api/projects/{path}          # Delete a project

# Artifact Operations
GET    /api/artifacts/{path}         # Get artifact content
GET    /api/artifacts/{path}/download # Download artifact file
POST   /api/artifacts/{path}         # Update/save artifact

# Directory Browsing (for path picker)
GET    /api/filesystem/browse        # List directories at a path
```

### Modified Schema

```python
class BrandBriefRequest(BaseModel):
    # ... existing fields ...
    project_path: str  # NEW: User-selected folder path
```

## Frontend UI

### Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Brand Identity Workflow                        [+ New Brand]    │
├────────────┬─────────────────────────────────────────────────────┤
│ PROJECTS   │                                                     │
│            │              MAIN CONTENT AREA                      │
│ ▼ MyBrand  │                                                     │
│   📄 brief │   (Shows: Form / Progress / Results / Preview)     │
│   📁 brand │                                                     │
│     🎨 colors                                                    │
│     🏷️ logos│                                                     │
│   📁 marketing                                                   │
│     📱 social                                                    │
│            │                                                     │
│ ▶ OtherBrand                                                     │
│            │                                                     │
│ [Open Folder]                                                    │
└────────────┴─────────────────────────────────────────────────────┘
```

### New Components

1. **`ProjectSidebar.tsx`** (~150 lines)
   - Collapsible project tree with icons
   - Click file → show preview in main area
   - "Open Folder" button to add project paths

2. **`ArtifactPreview.tsx`** (~200 lines)
   - Renders artifact content based on type
   - Download button for current artifact

3. **`PathPicker.tsx`** (~80 lines)
   - Input field with "Browse" button
   - Calls `/api/filesystem/browse` for folder modal

### Modified Components

- `App.tsx` - Add sidebar, manage selected project/artifact state
- `BrandBriefForm.tsx` - Add PathPicker for project location
- `ResultsDisplay.tsx` - Add individual download buttons per section

## Implementation Order

| Phase | Files | Description |
|-------|-------|-------------|
| 1 | `backend/project_manager.py` | File system operations |
| 2 | `backend/api.py`, `backend/schemas.py` | New API routes |
| 3 | `backend/job_manager.py` | Save artifacts during workflow |
| 4 | `frontend/src/types/index.ts` | New TypeScript interfaces |
| 5 | `frontend/src/components/PathPicker.tsx` | Folder selection |
| 6 | `frontend/src/components/ProjectSidebar.tsx` | Tree navigation |
| 7 | `frontend/src/components/ArtifactPreview.tsx` | Content rendering |
| 8 | `frontend/src/App.tsx` | Wire up sidebar + state |
| 9 | `frontend/src/components/BrandBriefForm.tsx` | Add path picker |

## Files Summary

**Create:**
- `backend/project_manager.py` (~200 lines)
- `frontend/src/components/ProjectSidebar.tsx` (~150 lines)
- `frontend/src/components/ArtifactPreview.tsx` (~200 lines)
- `frontend/src/components/PathPicker.tsx` (~80 lines)

**Modify:**
- `backend/api.py` - Add 6 new endpoints
- `backend/schemas.py` - Add project/artifact schemas
- `backend/job_manager.py` - Integrate artifact saving
- `frontend/src/types/index.ts` - Add new interfaces
- `frontend/src/App.tsx` - Add sidebar layout + state
- `frontend/src/components/BrandBriefForm.tsx` - Add path picker field
