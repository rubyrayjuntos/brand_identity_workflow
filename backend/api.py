"""
FastAPI application for the Brand Identity Workflow API.
Provides REST endpoints and WebSocket support for real-time updates.
"""

import asyncio
from datetime import datetime
from typing import Optional, List
from contextlib import asynccontextmanager
import os
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .schemas import (
    BrandBriefRequest, JobResponse, JobListResponse,
    WorkflowProgress, WSMessageType, WorkflowResult, JobStatus,
    ArtisticLogoRequest, ArtisticLogoResponse,
    GenerationJobResponse, GenerationJobResult, GenerationStatus
)
from .job_manager import job_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    yield


app = FastAPI(
    title="Brand Identity Workflow API",
    description="API for managing brand identity and marketing workflows",
    version="1.0.0",
    lifespan=lifespan
)

# Serve generated asset files (logos, social images, style guides, etc.)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative React port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===================================================================
# REST Endpoints
# ===================================================================

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Brand Identity Workflow API",
        "version": "1.0.0",
        "endpoints": {
            "jobs": "/api/jobs",
            "websocket": "/ws/{job_id}"
        }
    }


@app.post("/api/jobs", response_model=JobResponse)
async def create_job(
    brand_brief: BrandBriefRequest,
    background_tasks: BackgroundTasks,
    model: Optional[str] = None
):
    """
    Submit a new brand identity workflow job.

    Returns immediately with a job ID. Use WebSocket or GET endpoint to monitor progress.
    """
    # Create the job
    job_id = job_manager.create_job(brand_brief)
    job = job_manager.get_job(job_id)

    # Start the job in the background
    background_tasks.add_task(job_manager.start_job, job_id, model)

    return JobResponse(
        job_id=job_id,
        status=job.status,
        current_step=job.current_step,
        progress=job.progress,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        error=job.error
    )


@app.get("/api/jobs", response_model=JobListResponse)
async def list_jobs(limit: int = 20):
    """List recent workflow jobs."""
    jobs = job_manager.list_jobs(limit=limit)

    return JobListResponse(
        jobs=[
            JobResponse(
                job_id=job.job_id,
                status=job.status,
                current_step=job.current_step,
                progress=job.progress,
                created_at=job.created_at,
                started_at=job.started_at,
                completed_at=job.completed_at,
                error=job.error
            )
            for job in jobs
        ],
        total=len(jobs)
    )


@app.get("/api/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    """Get the status of a specific job."""
    job = job_manager.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobResponse(
        job_id=job.job_id,
        status=job.status,
        current_step=job.current_step,
        progress=job.progress,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        error=job.error
    )


@app.get("/api/jobs/{job_id}/results", response_model=WorkflowResult)
async def get_job_results(job_id: str):
    """Get the complete results of a finished job."""
    job = job_manager.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status == JobStatus.PENDING:
        raise HTTPException(status_code=400, detail="Job has not started yet")

    if job.status == JobStatus.RUNNING:
        raise HTTPException(status_code=400, detail="Job is still running")

    if job.status == JobStatus.FAILED:
        raise HTTPException(status_code=400, detail=f"Job failed: {job.error}")

    result = job_manager.get_job_result(job_id)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to format results")

    return result


# Synchronous on-demand generation (unchanged)
@app.post("/api/generate/artistic-logo", response_model=ArtisticLogoResponse)
async def generate_artistic_logo_endpoint(req: ArtisticLogoRequest):
    """Generate artistic logo variants on demand using local Ollama or placeholders (synchronous).

    Warning: this will block the request until generation completes — use the background job endpoint for long-running requests.
    """
    try:
        from tools import generate_artistic_logo
        model = req.model or os.getenv('OLLAMA_IMAGE_MODEL', 'qwen2.5:latest')
        loop = asyncio.get_running_loop()
        resp = await loop.run_in_executor(None, lambda: generate_artistic_logo.func(
            req.brand_name, prompt=req.prompt, style=req.style,
            variants=req.variants, resolution=req.resolution, model=model
        ))
        data = json.loads(resp) if isinstance(resp, str) else resp
        return ArtisticLogoResponse(brand=data.get('brand', req.brand_name), variants=data.get('variants', []))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/artistic-logo/jobs", response_model=GenerationJobResponse, status_code=202)
async def create_artistic_logo_job(req: ArtisticLogoRequest, background_tasks: BackgroundTasks):
    """Create a background generation job (returns 202 and a location to poll)."""
    from uuid import uuid4
    task_id = str(uuid4())

    # register and start task via job_manager
    job_manager.create_generation_task(task_id, {
        "brand_name": req.brand_name,
        "prompt": req.prompt,
        "style": req.style,
        "variants": req.variants,
        "resolution": req.resolution,
        "model": req.model or os.getenv('OLLAMA_IMAGE_MODEL', 'qwen2.5:latest')
    })

    location = f"/api/generate/artistic-logo/jobs/{task_id}"
    return GenerationJobResponse(task_id=task_id, status=GenerationStatus.PENDING, location=location)


@app.get("/api/generate/artistic-logo/jobs/{task_id}", response_model=GenerationJobResult)
async def get_artistic_logo_job(task_id: str):
    """Get the status and result of a background generation job."""
    task = job_manager.get_generation_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    status = GenerationStatus(task.get("status", "pending"))
    result = None
    if task.get("result"):
        result = ArtisticLogoResponse(brand=task["result"].get("brand"), variants=task["result"].get("variants", []))

    return GenerationJobResult(task_id=task_id, status=status, result=result, error=task.get("error"))


@app.post("/api/generate/artistic-logo/jobs/{task_id}/cancel", response_model=GenerationJobResult)
async def cancel_artistic_logo_job(task_id: str):
    """Cancel a background generation job (best-effort)."""
    ok = job_manager.cancel_generation_task(task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found or could not be cancelled")
    task = job_manager.get_generation_task(task_id)
    status = GenerationStatus(task.get("status", "failed"))
    return GenerationJobResult(task_id=task_id, status=status, result=None, error=task.get("error"))


@app.get("/api/generate/artistic-logo/jobs", response_model=List[GenerationJobResult])
async def list_artistic_logo_jobs():
    """List generation jobs."""
    tasks = job_manager.list_generation_tasks()
    out = []
    for t in tasks:
        status = GenerationStatus(t.get("status", "pending"))
        result = None
        if t.get("result"):
            result = ArtisticLogoResponse(brand=t["result"].get("brand"), variants=t["result"].get("variants", []))
        out.append(GenerationJobResult(task_id=t.get("task_id"), status=status, result=result, error=t.get("error")))
    return out


# ===================================================================
# WebSocket Endpoint
# ===================================================================

@app.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    """
    WebSocket endpoint for real-time job progress updates.

    Connect to receive:
    - connected: Initial connection confirmation
    - progress: Progress updates during execution
    - step_complete: Notification when a step completes
    - completed: Final completion notification
    - error: Error notification if job fails
    """
    await websocket.accept()

    job = job_manager.get_job(job_id)
    if not job:
        await websocket.send_json({
            "type": "error",
            "job_id": job_id,
            "message": "Job not found"
        })
        await websocket.close()
        return

    # Send connection confirmation
    await websocket.send_json(
        WorkflowProgress(
            type=WSMessageType.CONNECTED,
            job_id=job_id,
            step=job.current_step,
            progress=job.progress,
            message="Connected to job progress stream"
        ).model_dump(mode='json')
    )

    # If job is already completed, send completion message
    if job.status == JobStatus.COMPLETED:
        await websocket.send_json(
            WorkflowProgress(
                type=WSMessageType.COMPLETED,
                job_id=job_id,
                step=job.current_step,
                progress=100,
                message="Job already completed"
            ).model_dump(mode='json')
        )
        await websocket.close()
        return

    # If job failed, send error message
    if job.status == JobStatus.FAILED:
        await websocket.send_json(
            WorkflowProgress(
                type=WSMessageType.ERROR,
                job_id=job_id,
                step=job.current_step,
                progress=job.progress,
                message=f"Job failed: {job.error}"
            ).model_dump(mode='json')
        )
        await websocket.close()
        return

    # Define callback for progress updates
    async def send_progress(progress: WorkflowProgress):
        try:
            await websocket.send_json(progress.model_dump(mode='json'))
        except Exception:
            pass

    # Register the callback
    job_manager.register_websocket(job_id, send_progress)

    try:
        # Keep connection open until job completes or client disconnects
        while True:
            # Wait for messages from client (primarily for keepalive)
            try:
                message = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0
                )
                # Handle ping/pong
                if message == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                # Send keepalive
                try:
                    await websocket.send_json({"type": "keepalive"})
                except Exception:
                    break

            # Check if job is done
            job = job_manager.get_job(job_id)
            if job and job.status in (JobStatus.COMPLETED, JobStatus.FAILED):
                break

    except WebSocketDisconnect:
        pass
    finally:
        job_manager.unregister_websocket(job_id, send_progress)


# ===================================================================
# Health Check
# ===================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
