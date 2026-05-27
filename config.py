import os
import redis
import redis.asyncio as aioredis
from dotenv import load_dotenv

load_dotenv()

# Redis connection — supports both local and cloud (Upstash/Railway)
# On your own server: set host=localhost (default)
# On Replit/Railway: set REDIS_URL env variable
_redis_url = os.getenv("REDIS_URL", "")

if _redis_url:
    # Cloud Redis (Upstash, Railway, etc.) — uses URL connection
    pool   = redis.ConnectionPool.from_url(_redis_url, decode_responses=True, max_connections=20)
    apool  = aioredis.ConnectionPool.from_url(_redis_url, decode_responses=True, max_connections=10)
else:
    # Local Redis (your own server) — uses localhost
    pool  = redis.ConnectionPool(
        host="localhost", decode_responses=True, max_connections=80,
        socket_timeout=2, socket_connect_timeout=2, retry_on_timeout=True,
    )
    apool = aioredis.ConnectionPool(
        host="localhost", decode_responses=True, max_connections=40,
    )

r       = redis.Redis(connection_pool=pool)
r_async = aioredis.Redis(connection_pool=apool)

token       = os.getenv("BOT_TOKEN", "")
Dev_Zaid    = token.split(":")[0] if token else ""
sudo_id     = int(os.getenv("OWNER_ID", "0"))
botUsername = os.getenv("BOT_USERNAME", "")

SIGHTENGINE_API_USER   = os.getenv("SIGHTENGINE_API_USER", "")
SIGHTENGINE_API_SECRET = os.getenv("SIGHTENGINE_API_SECRET", "")

from kvsqlite.sync import Client as DB
ytdb    = DB("ytdb.sqlite")
sounddb = DB("sounddb.sqlite")
wsdb    = DB("wsdb.sqlite")
