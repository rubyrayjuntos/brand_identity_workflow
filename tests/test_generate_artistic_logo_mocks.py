import os
import sys
import json
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools import generate_artistic_logo


# Mock subprocess.run to produce an SVG
class FakeProc:
    def __init__(self, stdout, stderr='', returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


def test_qwen_cli_produces_svg(monkeypatch, tmp_path):
    fake_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256"><rect width="100%" height="100%" fill="#ccc"/></svg>'
    fake_proc = FakeProc(fake_svg)
    monkeypatch.setattr('subprocess.run', lambda *args, **kwargs: fake_proc)

    resp = generate_artistic_logo.func('CliBrand', prompt='SVG test', style='vector', variants=1, resolution='256x256', model='qwen2.5:latest')
    data = json.loads(resp)
    assert data['brand'] == 'CliBrand'
    assert len(data['variants']) == 1
    path = data['variants'][0]['file_path']
    assert path.endswith('.svg')
    assert os.path.exists(path)

    # cleanup
    os.remove(path)


def test_http_image_api_success(monkeypatch, tmp_path):
    # Mock requests.post to return a base64 image
    class FakeResp:
        def __init__(self, ok, status_code, text, data):
            self.ok = ok
            self.status_code = status_code
            self.text = text
            self._data = data

        def json(self):
            return self._data

    # a tiny valid PNG base64 (1x1 white pixel)
    b64_png = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMBAQkGq1sAAAAASUVORK5CYII='
    fake_resp = FakeResp(True, 200, 'OK', {'images': [b64_png]})

    monkeypatch.setattr('requests.post', lambda *args, **kwargs: fake_resp)

    resp = generate_artistic_logo.func('HttpBrand', prompt='HTTP test', style='vector', variants=1, resolution='256x256', model='sdxl')
    data = json.loads(resp)
    assert data['brand'] == 'HttpBrand'
    assert len(data['variants']) == 1
    path = data['variants'][0]['file_path']
    assert path.endswith('.png')
    assert os.path.exists(path)

    # cleanup
    os.remove(path)
