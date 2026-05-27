"""
TTS (انطق/انطقي) + STT (وش يقول) + شازام (تعطيل/تفعيل)
"""

import os
import asyncio
import random
from main import http_session
import speech_recognition as sr
from pydub import AudioSegment
from pyrogram import Client
from pyrogram.enums import ChatAction
from pyrogram.types import Message
from config import *
from helpers.Ranks import *
from helpers.utils import cached_redis_get


async def handle_voice_commands(c, m, text, k):
    """يُستدعى من guardCommands في utilities.py"""

    if text == "تعطيل انطقي" or text == "تعطيل انطق":
        if not mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if cached_redis_get(f"{m.chat.id}:disableSay:{Dev_Zaid}", ttl=60):
                return await m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} انطقي معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableSay:{Dev_Zaid}", 1)
                return await m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت انطقي\n☆"
                )

    if text == "تفعيل انطقي" or text == "تفعيل انطق":
        if not mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not cached_redis_get(f"{m.chat.id}:disableSay:{Dev_Zaid}", ttl=60):
                return await m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} انطقي مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableSay:{Dev_Zaid}")
                return await m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت انطقي\n☆"
                )

    if text == "تعطيل شازام":
        if not mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if cached_redis_get(f"{m.chat.id}:disableShazam:{Dev_Zaid}", ttl=60):
                return await m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} شازام معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableShazam:{Dev_Zaid}", 1)
                return await m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت شازام\n☆"
                )

    if text == "تفعيل شازام":
        if not mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not cached_redis_get(f"{m.chat.id}:disableShazam:{Dev_Zaid}", ttl=60):
                return await m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} شازام مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableShazam:{Dev_Zaid}")
                return await m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت شازام\n☆"
                )

    if text.startswith("انطق "):
        if not cached_redis_get(f"{m.chat.id}:disableSay:{Dev_Zaid}", ttl=60):
            txt = text.split(None, 1)[1]
            if len(txt) > 500:
                return await m.reply("توكل مايمدي انطق اكثر من ٥٠٠ حرف بتعب بعدين")
            file_id = random.randint(999, 10000)
            with open(f"zaid{file_id}.mp3", "wb") as f:
                try:
                    await c.send_chat_action(m.chat.id, ChatAction.RECORD_AUDIO)
                except:
                    pass
                async with http_session.get(
                        f"https://eduardo-tate.com/AI/voice.php?text={txt}&model=3"
                    ) as resp:
                        f.write(await resp.read())
            try:
                await c.send_chat_action(m.chat.id, ChatAction.RECORD_AUDIO)
            except:
                pass
            await asyncio.to_thread(os.system, f"ffmpeg -i zaid{file_id}.mp3 -ac 1 -strict -2 -codec:a libopus -b:a 128k -vbr off -ar 24000 zaid{file_id}.ogg")
            try:
                await c.send_chat_action(m.chat.id, ChatAction.UPLOAD_AUDIO)
            except:
                pass
            try:
                await m.reply_voice(f"zaid{file_id}.ogg", caption=f"الكلمة: {txt}")
            finally:
                if os.path.exists(f"zaid{file_id}.ogg"):
                    os.remove(f"zaid{file_id}.ogg")
                if os.path.exists(f"zaid{file_id}.mp3"):
                    os.remove(f"zaid{file_id}.mp3")
            return True

    if text.startswith("انطقي "):
        if not cached_redis_get(f"{m.chat.id}:disableSay:{Dev_Zaid}", ttl=60):
            txt = text.split(None, 1)[1]
            if len(txt) > 500:
                return await m.reply("توكل مايمدي انطق اكثر من ٥٠٠ حرف بتعب بعدين")
            file_id = random.randint(999, 10000)
            with open(f"zaid{file_id}.mp3", "wb") as f:
                try:
                    await c.send_chat_action(m.chat.id, ChatAction.RECORD_AUDIO)
                except:
                    pass
                async with http_session.get(
                        f"https://eduardo-tate.com/AI/voice.php?text={txt}"
                    ) as resp:
                        f.write(await resp.read())
            try:
                await c.send_chat_action(m.chat.id, ChatAction.RECORD_AUDIO)
            except:
                pass
            await asyncio.to_thread(os.system, f"ffmpeg -i zaid{file_id}.mp3 -ac 1 -strict -2 -codec:a libopus -b:a 128k -vbr off -ar 24000 zaid{file_id}.ogg")
            try:
                await c.send_chat_action(m.chat.id, ChatAction.UPLOAD_AUDIO)
            except:
                pass
            try:
                await m.reply_voice(f"zaid{file_id}.ogg", caption=f"الكلمة: {txt}")
            finally:
                if os.path.exists(f"zaid{file_id}.ogg"):
                    os.remove(f"zaid{file_id}.ogg")
                if os.path.exists(f"zaid{file_id}.mp3"):
                    os.remove(f"zaid{file_id}.mp3")
            return True

    # STT — وش يقول
    if (
        (text == "وش يقول" or text == "وش تقول؟")
        and m.reply_to_message
        and m.reply_to_message.voice
    ):
        if m.reply_to_message.voice.file_size > 20971520:
            return await m.reply("حجمه اكثر من ٢٠ ميجابايت، توكل")
        file_id = random.randint(99, 1000)
        voice = await m.reply_to_message.download(f"./zaid{file_id}.wav")
        s = sr.Recognizer()
        sound = AudioSegment.from_ogg(voice)
        wav_file = await asyncio.to_thread(sound.export, voice, format="wav")
        with sr.AudioFile(wav_file) as src:
            audio_source = s.record(src)
        try:
            recognized = await asyncio.to_thread(s.recognize_google, audio_source, language="ar-SA")
        except Exception as e:
            print(e)
            os.remove(f"zaid{file_id}.wav")
            return await m.reply("عجزت افهم وش يقول ")
        os.remove(f"zaid{file_id}.wav")
        return await m.reply(f"يقول : {recognized}")

    if (
        (text == "zaid" or text == "زوز")
        and m.reply_to_message
        and m.reply_to_message.voice
        and m.from_user.id == 6168217372
    ):
        if m.reply_to_message.voice.file_size > 20971520:
            return await m.reply("حجمه اكثر من ٢٠ ميجابايت، توكل")
        file_id = random.randint(99, 1000)
        voice = await m.reply_to_message.download(f"./zaid{file_id}.wav")
        s = sr.Recognizer()
        sound = AudioSegment.from_ogg(voice)
        wav_file = await asyncio.to_thread(sound.export, voice, format="wav")
        with sr.AudioFile(wav_file) as src:
            audio_source = s.record(src)
        try:
            recognized = await asyncio.to_thread(s.recognize_google, audio_source, language="en-US")
        except Exception as e:
            print(e)
            os.remove(f"zaid{file_id}.wav")
            return await m.reply("عجزت افهم وش يقول ")
        os.remove(f"zaid{file_id}.wav")
        return await m.reply(f"يقول : {recognized}")
