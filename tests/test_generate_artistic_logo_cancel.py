import os
import sys
import json
import time
from fastapi.testclient import TestClient
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.api import app
from backend.job_manager import job_manager

CLIENT = TestClient(app)


def test_create_and_cancel_immediate():
    payload = {'brand_name': 'CancelableBrand', 'prompt': 'Cancel test', 'style': 'vector', 'variants': 1, 'resolution': '256x256', 'model': 'qwen2.5:latest'}
    r = CLIENT.post('/api/generate/artistic-logo/jobs', json=payload)
    assert r.status_code == 202
    task_id = r.json()['task_id']

    # Immediately cancel
    r2 = CLIENT.post(f'/api/generate/artistic-logo/jobs/{task_id}/cancel')
    assert r2.status_code == 200
    job = r2.json()
    assert job['status'] in ('failed', 'completed')


def test_cancel_running_job(monkeypatch):
    # make a long-running generator by patching job_manager._run_generation_task to check cancellation flag
    def slow_runner(task_id):
        t = job_manager._generation_tasks.get(task_id)
        t.status = 'running'
        job_manager._generation_tasks[task_id] = t
        for i in range(5):
            if t._cancelled:
                t.status = 'failed'
                t.error = 'cancelled by user'
                return
            time.sleep(0.1)
        t.status = 'completed'
        t.result = {'brand': 'SlowBrand', 'variants': []}

    monkeypatch.setattr(job_manager, '_run_generation_task', slow_runner)

    payload = {'brand_name': 'SlowBrand', 'prompt': 'Slow test', 'style': 'vector', 'variants': 1, 'resolution': '256x256', 'model': 'qwen2.5:latest'}
    r = CLIENT.post('/api/generate/artistic-logo/jobs', json=payload)
    assert r.status_code == 202
    task_id = r.json()['task_id']

    # Wait briefly then cancel
    time.sleep(0.05)
    r2 = CLIENT.post(f'/api/generate/artistic-logo/jobs/{task_id}/cancel')
    assert r2.status_code == 200

    # Poll until cancelled
    for _ in range(20):
        r3 = CLIENT.get(f'/api/generate/artistic-logo/jobs/{task_id}')
        assert r3.status_code == 200
        j = r3.json()
        if j['status'] == 'failed':
            assert 'cancelled' in (j.get('error') or '')
            break
        time.sleep(0.05)
    else:
        pytest.fail('Task was not cancelled in time')
