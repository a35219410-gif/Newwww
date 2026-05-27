"""
دوال الترجمة
"""

import asyncio
from pyrogram import Client
from pyrogram.types import Message
from config import *
from helpers.Ranks import *
from helpers.utils import cached_redis_get
from main import http_session

from deep_translator import GoogleTranslator as googletranstr


async def _translate(text, target='ar', source='auto'):
    return await asyncio.to_thread(
        lambda: googletranstr(source=source, target=target).translate(text)
    )


@Client.on_message(filters.group & filters.text, group=28)
async def translationCommands(c, m):
    """يُعالَج من guardCommandsHandler في utilities.py — هذا الملف يحتوي دوال الترجمة فقط"""
    pass


async def handle_translation_commands(c, m, text, k):
    """يُستدعى من guardCommands في utilities.py"""

    if text == "تعطيل الترجمة" or text == "تعطيل الترجمه":
        if not mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if cached_redis_get(f"{m.chat.id}:disableTrans:{Dev_Zaid}", ttl=60):
                return await m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الترجمه معطله من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableTrans:{Dev_Zaid}", 1)
                return await m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت الترجمه\n☆"
                )

    if text == "تفعيل الترجمة" or text == "تفعيل الترجمه":
        if not mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not cached_redis_get(f"{m.chat.id}:disableTrans:{Dev_Zaid}", ttl=60):
                return await m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الترجمه مفعله من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableTrans:{Dev_Zaid}")
                return await m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت الترجمه\n☆"
                )

    if (
        text == "/ar"
        and m.reply_to_message
        and (m.reply_to_message.text or m.reply_to_message.caption)
    ):
        if not cached_redis_get(f"{m.chat.id}:disableTrans:{Dev_Zaid}", ttl=60):
            txt = m.reply_to_message.text or m.reply_to_message.caption
            async with http_session.get(f"https://hozory.com/translate/?target=ar&text={txt}") as resp:
                translation = (await resp.json())["result"]["translate"]
            return await m.reply(f"`{translation}`")

    if (
        text == "/en"
        and m.reply_to_message
        and (m.reply_to_message.text or m.reply_to_message.caption)
    ):
        if not cached_redis_get(f"{m.chat.id}:disableTrans:{Dev_Zaid}", ttl=60):
            txt = m.reply_to_message.text or m.reply_to_message.caption
            async with http_session.get(f"https://hozory.com/translate/?target=en&text={txt}") as resp:
                translation = (await resp.json())["result"]["translate"]
            return await m.reply(f"`{translation}`")

    if (
        text == "ترجمه"
        and m.reply_to_message
        and (m.reply_to_message.text or m.reply_to_message.caption)
    ):
        if not cached_redis_get(f"{m.chat.id}:disableTrans:{Dev_Zaid}", ttl=60):
            txt = m.reply_to_message.text or m.reply_to_message.caption
            async with http_session.get(f"https://hozory.com/translate/?target=en&text={txt}") as resp:
                en = (await resp.json())["result"]["translate"]
            async with http_session.get(f"https://hozory.com/translate/?target=ar&text={txt}") as resp:
                ar = (await resp.json())["result"]["translate"]
            async with http_session.get(f"https://hozory.com/translate/?target=ru&text={txt}") as resp:
                ru = (await resp.json())["result"]["translate"]
            async with http_session.get(f"https://hozory.com/translate/?target=zh&text={txt}") as resp:
                zh = (await resp.json())["result"]["translate"]
            async with http_session.get(f"https://hozory.com/translate/?target=fr&text={txt}") as resp:
                fr = (await resp.json())["result"]["translate"]
            async with http_session.get(f"https://hozory.com/translate/?target=nl&text={txt}") as resp:
                du = (await resp.json())["result"]["translate"]
            async with http_session.get(f"https://hozory.com/translate/?target=tr&text={txt}") as resp:
                tr = (await resp.json())["result"]["translate"]
            result = f"🇷🇺 : \n {ru}\n\n🇨🇳 : \n {zh}\n\n🇫🇷 :\n {fr}\n\n🇩🇪 :\n {du}\n\n🇹🇷 : \n{tr}"
            return await m.reply(result)

    if (
        text.startswith("ترجمه ")
        and m.reply_to_message
        and (m.reply_to_message.text or m.reply_to_message.caption)
    ):
        if not cached_redis_get(f"{m.chat.id}:disableTrans:{Dev_Zaid}", ttl=60):
            lang = text.split()[1]
            txt = m.reply_to_message.text or m.reply_to_message.caption
            async with http_session.get(f"https://hozory.com/translate/?target={lang}&text={txt}") as resp:
                translation = (await resp.json())["result"]["translate"]
            return await m.reply(f"`{translation}`")
