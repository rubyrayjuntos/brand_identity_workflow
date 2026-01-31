import os
import sys
import json
import time
from fastapi.testclient import TestClient
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.api import app, GENERATION_TASKS

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
    for _ in range(10):
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
