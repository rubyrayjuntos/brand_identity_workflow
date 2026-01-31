import os
import sys
import json
from fastapi.testclient import TestClient
import pytest

# Ensure repository root is on sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.api import app
from tools import generate_artistic_logo

CLIENT = TestClient(app)


def cleanup_files(paths):
    for p in paths:
        try:
            if os.path.exists(p):
                os.remove(p)
        except Exception:
            pass


def test_generate_artistic_logo_placeholder_fallback(tmp_path):
    # Use 'sdxl' which will hit the HTTP image path and (in local test) fall back to placeholder images
    resp_str = generate_artistic_logo.func('UnitTestBrand', prompt='Placeholder test', style='vector', variants=2, resolution='256x256', model='sdxl')
    data = json.loads(resp_str)

    assert data.get('brand') == 'UnitTestBrand'
    variants = data.get('variants', [])
    assert len(variants) == 2

    # Files should exist
    paths = [v['file_path'] for v in variants]
    for p in paths:
        assert os.path.exists(p)

    # Clean up
    cleanup_files(paths)


def test_generate_artistic_logo_endpoint_placeholder():
    payload = {'brand_name': 'EndpointBrand', 'prompt': 'Endpoint test', 'style': 'vector', 'variants': 2, 'resolution': '256x256', 'model': 'sdxl'}
    r = CLIENT.post('/api/generate/artistic-logo', json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data.get('brand') == 'EndpointBrand'
    variants = data.get('variants', [])
    assert len(variants) == 2

    # Files should exist
    paths = [v['file_path'] for v in variants]
    for p in paths:
        assert os.path.exists(p)

    # Clean up
    cleanup_files(paths)
