"""
Job manager for background workflow execution and state management.
"""

import asyncio
import uuid
import sys
import os
import io
import json
from datetime import datetime
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field

from .schemas import (
    JobStatus, WorkflowStep, BrandBriefRequest,
    WorkflowProgress, WSMessageType, WorkflowResult,
    BrandIdentityResult, MarketingResult, LogoConceptResult,
    ColorPaletteResult, ColorResult, StyleGuideResult,
    SocialMediaContentResult, EmailCampaignResult, VideoContentResult
)


@dataclass
class JobState:
    """Internal state for a workflow job."""
    job_id: str
    status: JobStatus
    brand_brief: BrandBriefRequest
    current_step: Optional[WorkflowStep] = None
    progress: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    results: Dict[str, Any] = field(default_factory=dict)
    websocket_callbacks: List[Callable] = field(default_factory=list)


class JobManager:
    """
    Manages background job execution and state for brand identity workflows.
    Uses in-memory storage (can be extended to Redis/database later).
    """

    def __init__(self):
        self._jobs: Dict[str, JobState] = {}
        self._max_jobs = 100  # Limit stored jobs

    def create_job(self, brand_brief: BrandBriefRequest) -> str:
        """
        Create a new job and return its ID.

        Args:
            brand_brief: The brand brief for the workflow

        Returns:
            The new job ID
        """
        job_id = str(uuid.uuid4())

        self._jobs[job_id] = JobState(
            job_id=job_id,
            status=JobStatus.PENDING,
            brand_brief=brand_brief
        )

        # Cleanup old jobs if we exceed max
        self._cleanup_old_jobs()

        return job_id

    def get_job(self, job_id: str) -> Optional[JobState]:
        """Get job state by ID."""
        return self._jobs.get(job_id)

    def list_jobs(self, limit: int = 20) -> List[JobState]:
        """List recent jobs, ordered by creation time (newest first)."""
        jobs = list(self._jobs.values())
        jobs.sort(key=lambda j: j.created_at, reverse=True)
        return jobs[:limit]

    def register_websocket(self, job_id: str, callback: Callable) -> bool:
        """
        Register a WebSocket callback for job progress updates.

        Args:
            job_id: The job to monitor
            callback: Async function to call with progress updates

        Returns:
            True if registered, False if job not found
        """
        job = self._jobs.get(job_id)
        if not job:
            return False
        job.websocket_callbacks.append(callback)
        return True

    def unregister_websocket(self, job_id: str, callback: Callable):
        """Remove a WebSocket callback."""
        job = self._jobs.get(job_id)
        if job and callback in job.websocket_callbacks:
            job.websocket_callbacks.remove(callback)

    async def _notify_websockets(self, job_id: str, progress: WorkflowProgress):
        """Send progress update to all registered WebSocket callbacks."""
        job = self._jobs.get(job_id)
        if not job:
            return

        for callback in job.websocket_callbacks:
            try:
                await callback(progress)
            except Exception:
                pass  # Ignore callback errors

    async def start_job(self, job_id: str, model_name: str = None):
        """
        Start executing a job in the background.

        Args:
            job_id: The job to start
            model_name: Optional LLM model name
        """
        job = self._jobs.get(job_id)
        if not job or job.status != JobStatus.PENDING:
            return

        # Update job state
        job.status = JobStatus.RUNNING
        job.started_at = datetime.now()
        job.current_step = WorkflowStep.INITIALIZING

        # Notify connected clients
        await self._notify_websockets(job_id, WorkflowProgress(
            type=WSMessageType.PROGRESS,
            job_id=job_id,
            step=WorkflowStep.INITIALIZING,
            progress=0,
            message="Initializing workflow..."
        ))

        try:
            # Run the actual workflow
            await self._execute_workflow(job, model_name)

        except Exception as e:
            job.status = JobStatus.FAILED
            job.error = str(e)
            job.completed_at = datetime.now()

            await self._notify_websockets(job_id, WorkflowProgress(
                type=WSMessageType.ERROR,
                job_id=job_id,
                step=job.current_step,
                progress=job.progress,
                message=f"Workflow failed: {str(e)}"
            ))

    async def _execute_workflow(self, job: JobState, model_name: str = None):
        """
        Execute the brand identity workflow.

        This runs the actual CrewAI workflow and emits progress updates.
        """
        # Import here to avoid circular imports
        import sys
        sys.path.insert(0, '/home/rswan/Documents/brand_identity_workflow')
        from main import BrandIdentityWorkflow

        # Convert brand brief to dict format expected by workflow
        brand_brief_dict = {
            'brand_name': job.brand_brief.brand_name,
            'industry': job.brand_brief.industry,
            'target_audience': job.brand_brief.target_audience,
            'brand_values': job.brand_brief.brand_values or ['Innovation', 'Quality'],
            'style_preference': job.brand_brief.style_preference.value,
            'desired_mood': job.brand_brief.desired_mood.value,
            'brand_voice': job.brand_brief.brand_voice or 'professional yet approachable',
            'mission': job.brand_brief.mission or f'To deliver exceptional {job.brand_brief.industry} solutions',
            'vision': job.brand_brief.vision or f'To be a leader in {job.brand_brief.industry}',
            'competitors': job.brand_brief.competitors or [],
            'unique_selling_proposition': job.brand_brief.unique_selling_proposition or 'Unique value proposition',
            'marketing_goals': job.brand_brief.marketing_goals or ['Increase brand awareness'],
            'budget_considerations': job.brand_brief.budget_considerations or 'Flexible',
            'timeline': job.brand_brief.timeline or '3-6 months'
        }

        # Initialize workflow
        workflow = BrandIdentityWorkflow(model_name=model_name)

        # Step 1: Brand Identity (0-50%)
        job.current_step = WorkflowStep.BRAND_IDENTITY
        job.progress = 10
        await self._notify_websockets(job.job_id, WorkflowProgress(
            type=WSMessageType.PROGRESS,
            job_id=job.job_id,
            step=WorkflowStep.BRAND_IDENTITY,
            progress=10,
            message="Starting brand identity creation..."
        ))

        # Run brand identity workflow (this is blocking, so we run in executor)
        # Wrapper to suppress stdout/stderr to avoid I/O errors in background
        def run_brand_identity_silent():
            # Redirect stdout/stderr to devnull to prevent I/O errors
            devnull = open(os.devnull, 'w')
            old_stdout, old_stderr = sys.stdout, sys.stderr
            try:
                sys.stdout = devnull
                sys.stderr = devnull
                return workflow.run_brand_identity_workflow(brand_brief_dict)
            finally:
                sys.stdout, sys.stderr = old_stdout, old_stderr
                devnull.close()

        loop = asyncio.get_event_loop()
        brand_identity_result = await loop.run_in_executor(
            None,
            run_brand_identity_silent
        )

        job.progress = 50
        await self._notify_websockets(job.job_id, WorkflowProgress(
            type=WSMessageType.STEP_COMPLETE,
            job_id=job.job_id,
            step=WorkflowStep.BRAND_IDENTITY,
            progress=50,
            message="Brand identity creation completed!"
        ))

        # Step 2: Marketing (50-90%)
        job.current_step = WorkflowStep.MARKETING
        job.progress = 55
        await self._notify_websockets(job.job_id, WorkflowProgress(
            type=WSMessageType.PROGRESS,
            job_id=job.job_id,
            step=WorkflowStep.MARKETING,
            progress=55,
            message="Starting marketing campaign development..."
        ))

        # Run marketing workflow
        def run_marketing_silent():
            devnull = open(os.devnull, 'w')
            old_stdout, old_stderr = sys.stdout, sys.stderr
            try:
                sys.stdout = devnull
                sys.stderr = devnull
                return workflow.run_marketing_workflow(
                    brand_brief_dict,
                    brand_identity_result.get('style_guide', {})
                )
            finally:
                sys.stdout, sys.stderr = old_stdout, old_stderr
                devnull.close()

        marketing_result = await loop.run_in_executor(
            None,
            run_marketing_silent
        )

        job.progress = 90
        await self._notify_websockets(job.job_id, WorkflowProgress(
            type=WSMessageType.STEP_COMPLETE,
            job_id=job.job_id,
            step=WorkflowStep.MARKETING,
            progress=90,
            message="Marketing campaign development completed!"
        ))

        # Finalize
        job.current_step = WorkflowStep.FINALIZING
        job.progress = 95
        await self._notify_websockets(job.job_id, WorkflowProgress(
            type=WSMessageType.PROGRESS,
            job_id=job.job_id,
            step=WorkflowStep.FINALIZING,
            progress=95,
            message="Finalizing results..."
        ))

        # Store results
        job.results = {
            'brand_identity': brand_identity_result,
            'marketing': marketing_result,
            'workflow_results': workflow.workflow_results
        }

        # Mark as completed
        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.now()
        job.progress = 100

        await self._notify_websockets(job.job_id, WorkflowProgress(
            type=WSMessageType.COMPLETED,
            job_id=job.job_id,
            step=WorkflowStep.FINALIZING,
            progress=100,
            message="Workflow completed successfully!"
        ))

    def get_job_result(self, job_id: str) -> Optional[WorkflowResult]:
        """Get formatted workflow results for a completed job."""
        job = self._jobs.get(job_id)
        if not job:
            return None

        # Build brand identity result
        brand_identity = None
        if job.results.get('brand_identity'):
            bi = job.results['brand_identity']
            base_name = job.brand_brief.brand_name.replace(' ', '').lower()
            style_val = job.brand_brief.style_preference.value
            brand_identity = BrandIdentityResult(
                logo_concepts=[
                    LogoConceptResult(
                        id=f"logo_{i+1}",
                        name=f"Concept {i+1}",
                        description=f"Logo concept for {job.brand_brief.brand_name}",
                        rationale="Modern design approach aligned with brand values",
                        style=job.brand_brief.style_preference.value,
                        file_path=f"assets/logos/{job.brand_brief.brand_name.replace(' ', '').lower()}_concept_{i+1}.png",
                        variants=[
                            {
                                "file_path": p,
                                "model": os.getenv('OLLAMA_IMAGE_MODEL', 'sdxl'),
                                "prompt": "",
                                "style": style_val,
                                "resolution": "1024x1024"
                            }
                            for v in range(3)
                            for ext in ('png', 'svg')
                            for p in [f"assets/logos/{base_name}_{style_val}_variant_{v+1}.{ext}"]
                            if os.path.exists(p)
                        ],
                        use_cases=["Website", "Business cards", "Social media"]
                    )
                    for i in range(bi.get('logo_concepts', {}).get('concepts_count', 3))
                ],
                color_palette=ColorPaletteResult(
                    primary=ColorResult(name="Primary", hex="#1a1a2e", rgb="26, 26, 46", usage="Main brand color"),
                    secondary=ColorResult(name="Secondary", hex="#16213e", rgb="22, 33, 62", usage="Supporting elements"),
                    accent=ColorResult(name="Accent", hex="#0f3460", rgb="15, 52, 96", usage="CTAs and highlights"),
                    neutral=ColorResult(name="Neutral", hex="#e8e8e8", rgb="232, 232, 232", usage="Backgrounds"),
                    rationale="Colors chosen to convey professionalism and innovation"
                ),
                style_guide=StyleGuideResult(
                    typography={"primary_font": "Inter", "secondary_font": "Roboto"},
                    imagery={"style": "modern", "photography": "clean and professional"},
                    voice_and_tone=job.brand_brief.brand_voice or "Professional yet approachable",
                    usage_guidelines="Maintain consistency across all touchpoints"
                )
            )

        # Build marketing result
        marketing = None
        if job.results.get('marketing'):
            mk = job.results['marketing']
            marketing = MarketingResult(
                social_media=SocialMediaContentResult(
                    platforms=mk.get('social_media_content', {}).get('platforms_covered', []),
                    posts_per_platform=mk.get('social_media_content', {}).get('posts_per_platform', 3),
                    content_themes=["Brand awareness", "Product features", "Customer stories"],
                    sample_posts=[
                        {
                            "caption": f"Sample post for {job.brand_brief.brand_name}",
                            "image_path": f"assets/social/{job.brand_brief.brand_name.replace(' ', '').lower()}_{(mk.get('social_media_content', {}).get('platforms_covered', ['instagram'])[0]).lower()}.png"
                        }
                    ]
                ),
                email_campaigns=EmailCampaignResult(
                    campaign_types=mk.get('email_campaigns', {}).get('campaign_types', []),
                    emails_per_campaign=mk.get('email_campaigns', {}).get('emails_per_campaign', 3),
                    sample_emails=[]
                ),
                video_content=VideoContentResult(
                    platforms=mk.get('video_content', {}).get('platforms_covered', []),
                    videos_per_platform=mk.get('video_content', {}).get('videos_per_platform', 2),
                    content_concepts=[]
                )
            )

        return WorkflowResult(
            job_id=job.job_id,
            status=job.status,
            brand_brief=job.brand_brief,
            brand_identity=brand_identity,
            marketing=marketing,
            created_at=job.created_at,
            completed_at=job.completed_at,
            raw_results=job.results
        )

    def _cleanup_old_jobs(self):
        """Remove oldest jobs when exceeding max limit."""
        if len(self._jobs) <= self._max_jobs:
            return

        # Sort by creation time and remove oldest
        jobs = sorted(self._jobs.values(), key=lambda j: j.created_at)
        to_remove = len(self._jobs) - self._max_jobs
        for job in jobs[:to_remove]:
            if job.status in (JobStatus.COMPLETED, JobStatus.FAILED):
                del self._jobs[job.job_id]


# Generation task support
from concurrent.futures import ThreadPoolExecutor

class GenerationTask:
    def __init__(self, task_id: str, req: dict):
        self.task_id = task_id
        self.req = req
        self.status = 'pending'
        self.result = None
        self.error = None
        self._future = None
        self._cancelled = False


class JobManager:
    def __init__(self):
        self._jobs: Dict[str, JobState] = {}
        self._max_jobs = 100  # Limit stored jobs
        # Generation tasks state
        self._generation_tasks: Dict[str, GenerationTask] = {}
        self._gen_executor = ThreadPoolExecutor(max_workers=4)

    # --- generation task API ---
    def create_generation_task(self, task_id: str, req: dict):
        t = GenerationTask(task_id, req)
        self._generation_tasks[task_id] = t
        t._future = self._gen_executor.submit(self._run_generation_task, task_id)
        return t

    def _run_generation_task(self, task_id: str):
        t = self._generation_tasks.get(task_id)
        if not t:
            return
        t.status = 'running'
        # persist via persistence module when available
        try:
            from backend import persistence
            persistence.save_task(task_id, {"task_id": task_id, "status": t.status, "req": t.req})
        except Exception:
            pass

        try:
            # Run the actual generation (blocking)
            from tools import generate_artistic_logo
            resp = generate_artistic_logo.func(
                t.req['brand_name'],
                prompt=t.req.get('prompt', ''),
                style=t.req.get('style', 'stylized'),
                variants=t.req.get('variants', 3),
                resolution=t.req.get('resolution', '1024x1024'),
                model=t.req.get('model')
            )
            if t._cancelled:
                t.status = 'failed'
                t.error = 'cancelled'
            else:
                t.status = 'completed'
                t.result = json.loads(resp) if isinstance(resp, str) else resp

        except Exception as e:
            t.status = 'failed'
            t.error = str(e)

        # persist final state
        try:
            from backend import persistence
            persistence.save_task(task_id, {"task_id": task_id, "status": t.status, "req": t.req, "result": t.result, "error": t.error})
        except Exception:
            pass

    def get_generation_task(self, task_id: str) -> Optional[Dict]:
        try:
            from backend import persistence
            persisted = persistence.get_task(task_id)
            if persisted:
                return persisted
        except Exception:
            pass
        t = self._generation_tasks.get(task_id)
        if not t:
            return None
        return {"task_id": t.task_id, "status": t.status, "req": t.req, "result": t.result, "error": t.error}

    def list_generation_tasks(self) -> List[Dict]:
        try:
            from backend import persistence
            return persistence.list_tasks()
        except Exception:
            return [
                {"task_id": t.task_id, "status": t.status, "req": t.req, "result": t.result, "error": t.error}
                for t in self._generation_tasks.values()
            ]

    def cancel_generation_task(self, task_id: str) -> bool:
        t = self._generation_tasks.get(task_id)
        if not t:
            try:
                from backend import persistence
                persisted = persistence.get_task(task_id)
                if persisted:
                    persisted['status'] = 'failed'
                    persisted['error'] = 'cancelled by user'
                    persistence.save_task(task_id, persisted)
                    return True
            except Exception:
                return False
            return False
        # mark cancelled and try to cancel future
        t._cancelled = True
        if t._future:
            cancelled = t._future.cancel()
            if cancelled:
                t.status = 'failed'
                t.error = 'cancelled by user'
                try:
                    from backend import persistence
                    persistence.save_task(task_id, {"task_id": task_id, "status": t.status, "req": t.req, "error": t.error})
                except Exception:
                    pass
                return True
        # If future could not be cancelled, we still mark as cancelled; worker will check flag
        t.status = 'failed'
        t.error = 'cancelled by user'
        try:
            from backend import persistence
            persistence.save_task(task_id, {"task_id": task_id, "status": t.status, "req": t.req, "error": t.error})
        except Exception:
            pass
        return True


# Global job manager instance
job_manager = JobManager()
