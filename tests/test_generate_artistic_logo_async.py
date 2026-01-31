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


def test_background_job_lifecycle(monkeypatch):
    # Patch tools.generate_artistic_logo.func to return quickly
    def fake_generate(brand_name, prompt, style, variants, resolution, model=None):
        return json.dumps({"brand": brand_name, "variants": [{"file_path": f"assets/logos/{brand_name.lower()}_{style}_variant_1.png", "model": model, "prompt": prompt, "style": style, "resolution": resolution}]})

    import tools
    monkeypatch.setattr(tools.generate_artistic_logo, 'func', fake_generate)

    payload = {'brand_name': 'AsyncBrand', 'prompt': 'Async test', 'style': 'vector', 'variants': 1, 'resolution': '256x256', 'model': 'qwen2.5:latest'}

    r = CLIENT.post('/api/generate/artistic-logo/jobs', json=payload)
    assert r.status_code == 202
    data = r.json()
    assert 'task_id' in data and data['status'] == 'pending'
    location = data['location']

    # Poll for completion (BackgroundTasks will run after response in TestClient)
    future = None
    for _ in range(50):
        # also check future from job_manager if available to detect failures
        try:
            from backend.job_manager import job_manager
            t = job_manager._generation_tasks.get(data['task_id'])
            if t:
                print('DEBUG: found task', t.task_id, 'status', t.status, 'error=', getattr(t, 'error', None))
            if t and getattr(t, '_future', None) is not None:
                future = t._future
                print('DEBUG: future present, done=', future.done(), 'cancelled=', future.cancelled())
                if future.done():
                    # if future raised an exception, show it
                    exc = None
                    try:
                        future.result(timeout=0.1)
                    except Exception as e:
                        exc = e
                    print('DEBUG: future.exception=', future.exception())
                    r2 = CLIENT.get(location)
                    assert r2.status_code == 200
                    job = r2.json()
                    if exc:
                        pytest.fail(f"Background job future failed: {exc}")
                    if job['status'] == 'completed':
                        assert job['result']['brand'] == 'AsyncBrand'
                        assert len(job['result']['variants']) == 1
                        break
        except Exception:
            pass
        r2 = CLIENT.get(location)
        assert r2.status_code == 200
        job = r2.json()
        if job['status'] == 'completed':
            assert job['result']['brand'] == 'AsyncBrand'
            assert len(job['result']['variants']) == 1
            break
        time.sleep(0.1)
    else:
        pytest.fail("Background job did not complete in time")


def test_background_job_failure(monkeypatch):
    # Patch tools.generate_artistic_logo.func to raise an exception
    def failing_generate(*args, **kwargs):
        raise RuntimeError('simulated failure')

    import tools
    monkeypatch.setattr(tools.generate_artistic_logo, 'func', failing_generate)

    payload = {'brand_name': 'FailBrand', 'prompt': 'Should fail', 'style': 'vector', 'variants': 1, 'resolution': '256x256', 'model': 'qwen2.5:latest'}

    r = CLIENT.post('/api/generate/artistic-logo/jobs', json=payload)
    assert r.status_code == 202
    task_id = r.json()['task_id']

    # Poll until failed
    for _ in range(10):
        r2 = CLIENT.get(f'/api/generate/artistic-logo/jobs/{task_id}')
        assert r2.status_code == 200
        job = r2.json()
        if job['status'] == 'failed':
            assert 'simulated failure' in job['error']
            break
        time.sleep(0.1)
    else:
        pytest.fail('Background job did not fail as expected')
