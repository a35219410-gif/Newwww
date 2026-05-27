# keep_alive.py — خادم ويب للإبقاء على Web Service نشطاً على Render
from aiohttp import web
import asyncio, os

async def handle(request):
    return web.Response(text="✅ Bot is running!", content_type="text/plain")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server running on port {port}")
