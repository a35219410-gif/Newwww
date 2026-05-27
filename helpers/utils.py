import asyncio
from collections import OrderedDict
import time, uuid
import aiohttp
from config import r, r_async

MAX_CACHE_SIZE = 8000
_cache: OrderedDict = OrderedDict()

def cached_redis_get(key: str, ttl: int = 60):
    now = time.time()
    if key in _cache:
        value, expiry = _cache[key]
        if now < expiry:
            _cache.move_to_end(key); return value
        del _cache[key]
    value = r.get(key)
    _cache[key] = (value, now + ttl)
    if len(_cache) > MAX_CACHE_SIZE: _cache.popitem(last=False)
    return value

async def async_cached_redis_get(key: str, ttl: int = 60):
    now = time.time()
    if key in _cache:
        value, expiry = _cache[key]
        if now < expiry:
            _cache.move_to_end(key); return value
        del _cache[key]
    value = await r_async.get(key)
    _cache[key] = (value, now + ttl)
    if len(_cache) > MAX_CACHE_SIZE: _cache.popitem(last=False)
    return value

async def prewarm_cache(keys_with_ttl: list):
    pipe = r_async.pipeline(transaction=False)
    for key, _ in keys_with_ttl: pipe.get(key)
    values = await pipe.execute()
    now = time.time()
    for (key, ttl), value in zip(keys_with_ttl, values):
        _cache[key] = (value, now + ttl)

def cache_invalidate(key: str): _cache.pop(key, None)
def cache_invalidate_prefix(prefix: str):
    for k in [k for k in list(_cache) if k.startswith(prefix)]: _cache.pop(k, None)
def cache_clear_all(): _cache.clear()
def get_cache_stats(): return {"size": len(_cache), "max": MAX_CACHE_SIZE, "pct": f"{len(_cache)/MAX_CACHE_SIZE*100:.1f}%"}

async def shell_exec(code: str):
    process = await asyncio.create_subprocess_shell(code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
    return (await process.communicate())[0].decode().strip(), process

async def cssworker_url(target_url: str, session: aiohttp.ClientSession = None):
    url = "https://htmlcsstoimage.com/demo_run"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"}
    data = {"url": target_url, "css": f"r: {uuid.uuid4()}", "render_when_ready": False, "viewport_width": 1280, "viewport_height": 720, "device_scale": 1}
    try:
        owned = session is None
        s = session or aiohttp.ClientSession()
        async with s.post(url, headers=headers, json=data) as resp: result = await resp.json()
        if owned: await s.close()
        return result
    except Exception: return None
