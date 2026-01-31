"""
Simple persistence abstraction for generation tasks.
Supports optional Redis (if REDIS_URL is set) or file-based JSON storage.
"""
import os
import json
import threading
from typing import Dict, Optional, List

REDIS_URL = os.getenv("REDIS_URL", "")

lock = threading.Lock()
storage_file = os.path.join(os.path.dirname(__file__), "..", ".data", "generation_tasks.json")

# Try to lazily import redis if available
_redis_client = None
if REDIS_URL:
    try:
        import redis
        _redis_client = redis.Redis.from_url(REDIS_URL)
    except Exception:
        _redis_client = None


def _ensure_storage_file():
    dirpath = os.path.dirname(storage_file)
    os.makedirs(dirpath, exist_ok=True)
    if not os.path.exists(storage_file):
        with open(storage_file, "w") as f:
            json.dump({}, f)


def save_task(task_id: str, data: Dict):
    if _redis_client:
        _redis_client.set(f"generation_task:{task_id}", json.dumps(data))
        return
    with lock:
        _ensure_storage_file()
        with open(storage_file, "r+") as f:
            try:
                all_data = json.load(f)
            except Exception:
                all_data = {}
            all_data[task_id] = data
            f.seek(0)
            json.dump(all_data, f)
            f.truncate()


def get_task(task_id: str) -> Optional[Dict]:
    if _redis_client:
        v = _redis_client.get(f"generation_task:{task_id}")
        if not v:
            return None
        return json.loads(v)
    with lock:
        _ensure_storage_file()
        with open(storage_file, "r") as f:
            try:
                all_data = json.load(f)
            except Exception:
                return None
            return all_data.get(task_id)


def delete_task(task_id: str):
    if _redis_client:
        _redis_client.delete(f"generation_task:{task_id}")
        return
    with lock:
        _ensure_storage_file()
        with open(storage_file, "r+") as f:
            try:
                all_data = json.load(f)
            except Exception:
                all_data = {}
            if task_id in all_data:
                del all_data[task_id]
                f.seek(0)
                json.dump(all_data, f)
                f.truncate()


def list_tasks() -> List[Dict]:
    if _redis_client:
        keys = _redis_client.keys("generation_task:*")
        res = []
        for k in keys:
            v = _redis_client.get(k)
            if v:
                res.append(json.loads(v))
        return res
    with lock:
        _ensure_storage_file()
        with open(storage_file, "r") as f:
            try:
                all_data = json.load(f)
            except Exception:
                return []
            return list(all_data.values())
