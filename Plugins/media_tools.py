"""
تحرير الصور — NSFW scanner + أدوات الصور
"""

import os
import asyncio
import aiohttp
from PIL import Image
from pyrogram import Client
from pyrogram.types import Message
from config import *
from helpers.Ranks import *
from helpers.utils import cached_redis_get


async def scan4(c, m, id, file):
    """فحص NSFW بـ Sightengine API"""
    try:
        async with aiohttp.ClientSession() as session:
            with open(file, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('media', f, filename='media.jpg', content_type='image/jpeg')
                data.add_field('models', 'nudity-2.0')
                data.add_field('api_user', SIGHTENGINE_API_USER)
                data.add_field('api_secret', SIGHTENGINE_API_SECRET)
                async with session.post(
                    'https://api.sightengine.com/1.0/check.json', data=data
                ) as resp:
                    result = await resp.json()
        is_nsfw = False
        try:
            nudity = result.get('nudity', {})
            if nudity.get('sexual_activity', 0) > 0.7 or nudity.get('sexual_display', 0) > 0.7:
                is_nsfw = True
        except Exception:
            is_nsfw = False
        if is_nsfw:
            print("xNSFW")
            await m.delete()
            k = cached_redis_get(f'{Dev_Zaid}:botkey', ttl=120)
            await m.reply(
                f"「 {m.from_user.mention} 」\n{k} تم حذف رسالتك لإحتوائها على محتوى إباحي .\n☆"
            )
    except Exception as e:
        print(f"NSFW scan error: {e}")
    finally:
        if os.path.exists(file):
            os.remove(file)


async def scanR(c, m, id, file):
    await scan4(c, m, id, file)
