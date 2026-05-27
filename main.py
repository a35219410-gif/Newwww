import logging
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler('bot.log'), logging.StreamHandler()])

import time, redis, os, glob, json, re, asyncio, aiohttp
from dotenv import load_dotenv
from pyrogram import Client, idle

load_dotenv()
token    = os.getenv('BOT_TOKEN', '')
owner_id = int(os.getenv('OWNER_ID', '0'))
api_id   = int(os.getenv('API_ID', '0'))
api_hash = os.getenv('API_HASH', '')
if not token:    raise RuntimeError('BOT_TOKEN not found in .env')
if not owner_id: raise RuntimeError('OWNER_ID not found in .env')
if not api_id:   raise RuntimeError('API_ID not found in .env')
if not api_hash: raise RuntimeError('API_HASH not found in .env')
Dev_Zaid = token.split(':')[0]

# Redis pool — 80 connections to match workers=50 + headroom
pool = redis.ConnectionPool(
    host="localhost", decode_responses=True, max_connections=80,
    socket_timeout=2, socket_connect_timeout=2, retry_on_timeout=True,
)
r = redis.Redis(connection_pool=pool)
logging.info('Loading... 0%')

app = Client(
    f'{Dev_Zaid}r3d', api_id, api_hash,
    bot_token=token, plugins={"root": "Plugins"},
    workers=50, max_concurrent_transmissions=20,
)
http_session: aiohttp.ClientSession = None

def Find(text):
    m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!\(\)\[\]{};:',<>?]))"
    url = re.findall(m, text)
    return [x[0] for x in url]

import atexit
from config import ytdb, sounddb, wsdb
from helpers.utils import prewarm_cache
from keep_alive import start_web
atexit.register(lambda: [db.close() for db in (ytdb, sounddb, wsdb)])

async def cleanup_temp():
    while True:
        await asyncio.sleep(3600)
        for f in glob.glob('./downloads/*') + glob.glob('./shazam*'):
            try: os.remove(f)
            except Exception: pass

async def main():
    global http_session
    http_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15))
    await start_web()
    logging.info('10%  startup...')
    async with app:
        r.set(f'{Dev_Zaid}botowner', owner_id)
        logging.info('30%  owner registered')
        if not r.get(f'{Dev_Zaid}:botkey'):     r.set(f'{Dev_Zaid}:botkey', '⇜')
        if not r.get(f'{Dev_Zaid}botname'):     r.set(f'{Dev_Zaid}botname', 'رعد')
        if not r.get(f'{Dev_Zaid}:BotChannel'): r.set(f'{Dev_Zaid}:BotChannel', 'eFFb0t')
        logging.info('50%  redis ready')

        # Pre-warm cache: load the 3 most-read keys into LRU cache
        # so the first 1000 messages don't hit Redis cold
        await prewarm_cache([
            (f'{Dev_Zaid}:botkey',   600),  # bot key emoji
            (f'{Dev_Zaid}:BotChannel', 600), # bot channel
            (f'{Dev_Zaid}botname',   600),  # bot display name
        ])
        logging.info('60%  cache prewarmed')
        asyncio.ensure_future(cleanup_temp())
        logging.info('100% Bot started - R3D Source')
        if r.get(f'DevGroup:{Dev_Zaid}'):
            logging.info(f'Dev group: ' + str(int(r.get('DevGroup:' + Dev_Zaid) or 0)))
        await idle()
    if http_session: await http_session.close()

if __name__ == '__main__':
    asyncio.run(main())
