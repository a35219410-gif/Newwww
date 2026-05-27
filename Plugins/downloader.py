import aiohttp
from helpers.utils import cached_redis_get
'''


██████╗░██████╗░██████╗░
██╔══██╗╚════██╗██╔══██╗
██████╔╝░█████╔╝██║░░██║
██╔══██╗░╚═══██╗██║░░██║
██║░░██║██████╔╝██████╔╝
╚═╝░░╚═╝╚═════╝░╚═════╝░


[ = This plugin is a part from R3D Source code = ]
{"Developer":"https://t.me/yqyqy66"}

'''

import yt_dlp, os, re, time, random, json, asyncio
from yt_dlp import YoutubeDL
from pyrogram import *
from pyrogram.enums import *
from shazamio import Shazam
from pyrogram.types import *
from config import *
from helpers.Ranks import *
from helpers.Ranks import isLockCommand
from PIL import Image, ImageFilter
#from pySmartDL import SmartDL

shazam = Shazam()

def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":")))
    )
    
def Find(text):
  m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
  url = re.findall(m,text)  
  return [x[0] for x in url]

@Client.on_message(filters.text & filters.group, group=32)
async def ytdownloaderHandler(c,m):
    k = cached_redis_get(f'{Dev_Zaid}:botkey', ttl=120)
    channel = cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) if cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) else 'w7G_BoT'
    asyncio.create_task(yt_func(c,m,k,channel))
    
async def yt_func(c,m,k,channel):
   if not cached_redis_get(f'{m.chat.id}:enable:{Dev_Zaid}', ttl=30):
        return False 
   if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return False
   if cached_redis_get(f'{m.chat.id}:mute:{Dev_Zaid}', ttl=30) and not admin_pls(m.from_user.id,m.chat.id):  return False 
   if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return False 
   text = m.text
   if isLockCommand(m.from_user.id, m.chat.id, text): return
   rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url=f'https://t.me/{channel}')
     ]]
   )

   if text.startswith('يوت '):
     if cached_redis_get(f'{m.chat.id}:disableYT:{Dev_Zaid}', ttl=60):  return
     if r.get(f':disableYT:{Dev_Zaid}'):  return
     query = text.split(None,1)[1]
     keyboard= []
     ydl_search_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True}
     with yt_dlp.YoutubeDL(ydl_search_opts) as ydl:
         search_results = ydl.extract_info(f'ytsearch4:{query}', download=False)
     results = search_results.get('entries', [])
     for res in results:
       title = res.get('title','')
       id = res.get('id','')
       keyboard.append([InlineKeyboardButton (title, callback_data=f'{m.from_user.id}GET{id}')])     
     a = await m.reply(f'{k} البحث ~ {query}',reply_markup=InlineKeyboardMarkup (keyboard), disable_web_page_preview=True)
     r.set(f'{a.id}:one_minute:{m.from_user.id}', 1, ex=60)
     return True
     
   
   if text.startswith('بحث ') or text.startswith('yt '):
     if cached_redis_get(f'{m.chat.id}:disableYT:{Dev_Zaid}', ttl=60):  return
     if r.get(f':disableYT:{Dev_Zaid}'):  return
     query = text.split(None,1)[1]
     ydl_search_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True}
     with yt_dlp.YoutubeDL(ydl_search_opts) as ydl:
         search_results = ydl.extract_info(f'ytsearch1:{query}', download=False)
     res = search_results.get('entries', [{}])[0]
     title = res.get('title','')
     duration = int(res.get('duration') or 0)
     duration_string = time.strftime('%M:%S', time.gmtime(duration))
     if ytdb.get(f'ytvideo{res["id"]}'):
        aud = ytdb.get(f'ytvideo{res["id"]}')
        duration_string = time.strftime('%M:%S', time.gmtime(aud["duration"]))
        return await m.reply_audio(aud["audio"],caption=f'@{channel} ~ {duration_string} ⏳',reply_markup=rep)
     url = f'https://youtu.be/{res["id"]}'
     ydl_ops = {"format": "bestaudio[ext=m4a]",'forceduration':True, "username": "oauth2", "password": ''}
     with yt_dlp.YoutubeDL(ydl_ops) as ydl:
       info = ydl.extract_info(url, download=False)
       if int(info['duration']) > 15555555:
           return await m.reply("صوت فوق 25 دقيقة ما اقدر انزله",reply_markup=rep)
       duration_string = time.strftime('%M:%S', time.gmtime(int(info['duration'])))
       audio_file = ydl.prepare_filename(info)
       ydl.process_info(info)
     thumb_url = info.get('thumbnail', '')
     if thumb_url:
         thumb = 'thumb_tmp.jpg'
         _timeout = aiohttp.ClientTimeout(total=15)
         async with aiohttp.ClientSession(timeout=_timeout) as session:
             async with session.get(thumb_url) as resp:
                 with open(thumb, 'wb') as f:
                     f.write(await resp.read())
     else:
         thumb = None
     os.rename(audio_file,audio_file.replace(".m4a",".mp3"))
     audio_file = audio_file.replace(".m4a",".mp3")
     try:
         a = await m.reply_audio(
         audio_file,
         title=info.get('title',''),
         thumb=thumb,
         duration=int(info['duration']),
         caption=f'@{channel} ~ {duration_string} ⏳',
         performer=info.get('channel', info.get('uploader','')),reply_markup=rep)
         ytdb.set(f'ytvideo{res["id"]}',{"type":"audio","audio":a.audio.file_id,"duration":a.audio.duration})
     finally:
         if os.path.exists(audio_file): os.remove(audio_file)
         if thumb and os.path.exists(thumb): os.remove(thumb)
     return True
  
   if text == "نسخة اليوتيوب" and m.from_user.id == 6168217372:
     if not ytdb.keys(): return await m.reply("تخزين اليوتيوب فاضي")
     else:
        videos = []
        audios = []
        for key in ytdb.keys():
           get = {"key":key[0],"value":ytdb.get(key[0])}
           if get["value"]["type"] == "audio":
             audios.append(get)
           if get["value"]["type"] == "video":
             videos.append(get)
        id = random.randint(1,10000)
        if audios:
          with open(f"audios-{id}.json","w+") as f:
            f.write(json.dumps(audios, indent=4, ensure_ascii=False))
          try:
              await m.reply_document(f"audios-{id}.json")
          finally:
              if os.path.exists(f"audios-{id}.json"): os.remove(f"audios-{id}.json")
        if videos:
          with open(f"videos-{id}.json","w+") as f:
            f.write(json.dumps(videos, indent=4, ensure_ascii=False))
          try:
              await m.reply_document(f"videos-{id}.json")
          finally:
              if os.path.exists(f"videos-{id}.json"): os.remove(f"videos-{id}.json")
        return True

   if text.startswith('ساوند '):
     if cached_redis_get(f'{m.chat.id}:disableSound:{Dev_Zaid}', ttl=60):  return
     if r.get(f':disableYT:{Dev_Zaid}'):  return
     #https://soundcloud.com
     query = text.split(None,1)[1]
     _timeout = aiohttp.ClientTimeout(total=15)
     async with aiohttp.ClientSession(timeout=_timeout) as s:
         async with s.get(f"https://m.soundcloud.com/search?q={query}") as resp:
             data_text = await resp.text()
     urls = re.findall(r'data-testid="cell-entity-link" href="([^"]+)', data_text)
     names = re.findall(r'<div class="Information_CellTitle__2KitR">([^<]+)', data_text)
     result = []
     for i in range(len(urls)): result.append({'name': names[i], 'url': f'{urls[i]}'})
     buttons = []
     btns = InlineKeyboardMarkup(buttons)
     count = 0
     for a in result:
       if count == 5:
         break
       url = a['url']
       buttons.append([
       InlineKeyboardButton (a['name'], switch_inline_query_current_chat=f'{url}#SOUND')
       ]
       )
       count += 1
     await m.reply(f'{k} بحث الساوند ~ {query}', reply_markup=btns)
     return True
   
   if text.startswith('تيك '):
     if cached_redis_get(f'{m.chat.id}:disableTik:{Dev_Zaid}', ttl=60):  return
     if r.get(f':disableYT:{Dev_Zaid}'):  return
     if Find(text):
       query = Find(text)[0]
     else:  return False
     with yt_dlp.YoutubeDL({}) as ytdl:
           vid_data = ytdl.extract_info(query, download=False)
     title=vid_data['fulltitle']
     duration=int(vid_data['duration'])
     string_d = time.strftime('%M:%S', time.gmtime(duration))
     uploader=vid_data['uploader']
     uploader_url=vid_data['uploader_url']
     creator=vid_data['creator']
     file_name=vid_data['url']
     url=vid_data['original_url']
     likes=vid_data['like_count']
     comments=vid_data['comment_count']
     views=vid_data['view_count']
     reposts=vid_data['repost_count']
     caption=f"`{title}`\n{k} طول المقطع : {string_d}\n{k} المشاهدات : {views:,}\n{k} اللايكات : {likes:,}\n{k} الكومنت : {comments:,}\n{k} الاكسبلور : {reposts:,}\n\n~ @{channel}"
     reply_markup=InlineKeyboardMarkup (
       [
       [InlineKeyboardButton (f"{creator} - @{uploader}",url=uploader_url)]
       ]
     )
     try:
       await m.reply_video(file_name, caption=caption, reply_markup=reply_markup)
     except:
       with yt_dlp.YoutubeDL({}) as ytdl:
           vid_data = ytdl.extract_info(query[0].lower(), download=True)
           file_name = ytdl.prepare_filename(vid_data)
       try:
           await m.reply_video(file_name, caption=caption, reply_markup=reply_markup)
       finally:
           if os.path.exists(file_name): os.remove(file_name)
     return True

   if text.endswith(' #AUDIO'):
    find = Find(text)
    if find:
     url = find[0]
     if 'soundcloud' in url:
       if cached_redis_get(f'{m.chat.id}:disableSound:{Dev_Zaid}', ttl=60):  return
       if r.get(f':disableYT:{Dev_Zaid}'):  return
       id = url.split('soundcloud.com/')[1]
       if sounddb.get(f'{id}:sound'):
          return await m.reply_audio(sounddb.get(f'{id}:sound'))
       with yt_dlp.YoutubeDL({}) as ytdl:
           ytdl_dataa = ytdl.extract_info(url, download=False)
           if int(ytdl_dataa['duration']) > 155555555:
              return await m.reply('مقطع اكثر من ٢٥ دقيقة مقدر انزله')
       with yt_dlp.YoutubeDL({}) as ytdl:
           ytdl_dataa = ytdl.extract_info(url, download=True)
           file_name = ytdl.prepare_filename(ytdl_dataa)
       title = ytdl_dataa['title']
       try:
           a = await m.reply_audio(file_name,title=title, performer=f'@{channel}', duration=int(ytdl_dataa['duration']))       
           sounddb.set(f'{id}:sound',a.audio.file_id)
       finally:
           if os.path.exists(file_name): os.remove(file_name)
       return True
   
   if text.endswith(' #VOICE'):
    find = Find(text)
    if find:
     url = find[0]
     if 'soundcloud' in url:
       if cached_redis_get(f'{m.chat.id}:disableSound:{Dev_Zaid}', ttl=60):  return
       if r.get(f':disableYT:{Dev_Zaid}'):  return
       idd = url.split('soundcloud.com/')[1]
       if sounddb.get(f'{idd}:soundVoice'):
          return await m.reply_voice(sounddb.get(f'{idd}:soundVoice'))
       with yt_dlp.YoutubeDL({}) as ytdl:
           ytdl_dataa = ytdl.extract_info(url, download=False)
           if int(ytdl_dataa['duration']) > 55555252:
              return await m.reply('مقطع اكثر من ٢٥ دقيقة مقدر انزله')
       with yt_dlp.YoutubeDL({}) as ytdl:
           ytdl_dataa = ytdl.extract_info(url, download=True)
           file_name = ytdl.prepare_filename(ytdl_dataa)
       id = random.randint(1,100)
       os.rename(file_name, f"zaid{id}.mp3")
       os.system(f'ffmpeg -i zaid{id}.mp3 -ac 1 -strict -2 -codec:a libopus -b:a 128k -vbr off -ar 24000 zaid{id}.ogg')
       try:
           a = await m.reply_voice(f"zaid{id}.ogg")       
           sounddb.set(f'{idd}:soundVoice',a.voice.file_id)
       finally:
           if os.path.exists(f"zaid{id}.mp3"): os.remove(f"zaid{id}.mp3")
           if os.path.exists(f"zaid{id}.ogg"): os.remove(f"zaid{id}.ogg")
       return True
   
   find = Find(text)
   if find:
     url = find[0]
     if 'soundcloud' in url:
       if cached_redis_get(f'{m.chat.id}:disableSound:{Dev_Zaid}', ttl=60):  return
       if r.get(f':disableYT:{Dev_Zaid}'):  return
       id = url.split('soundcloud.com')[1]
       return await m.reply(f"@{channel} - ☁️",reply_markup=InlineKeyboardMarkup ([
       [InlineKeyboardButton ("اضغط هنا لاختيار صيغة التحميل", switch_inline_query_current_chat=f'{id}#SOUND')],
       [InlineKeyboardButton ("☁️", url=f't.me/{channel}')],
       ]))
       
       
     
@Client.on_message(filters.regex("^شازام$") & filters.group)
async def shazamFunc(c,m):
   if cached_redis_get(f'{m.chat.id}:disableShazam:{Dev_Zaid}', ttl=60):  return False
   if m.reply_to_message and (m.reply_to_message.audio or m.reply_to_message.voice or m.reply_to_message.video):
     if m.reply_to_message.audio:
       duration=m.reply_to_message.audio.duration if m.reply_to_message.audio.duration else 301
       fileSize=m.reply_to_message.audio.file_size
     if m.reply_to_message.voice:
       duration=m.reply_to_message.voice.duration if m.reply_to_message.voice.duration else 301
       fileSize=m.reply_to_message.voice.file_size
     if m.reply_to_message.video:
       duration=m.reply_to_message.video.duration if m.reply_to_message.video.duration else 301
       fileSize=m.reply_to_message.video.file_size
     if duration > 300:
       return await m.reply("🧚‍♀️ مدة المقطع أكثر من 5 دقايق ..")
     if fileSize > 26214400:
       return await m.reply("🧚‍♀️ حجم المقطع أكثر من 25 ميجابايت ..")
     id = random.randint(1,1000)
     msg = await m.reply("جاري المعالجة ...")
     audio = await m.reply_to_message.download(f'./shazam{id}.ogg')
     try:
         out = await shazam.recognize(f'shazam{id}.ogg')
     finally:
         if os.path.exists(f'shazam{id}.ogg'): os.remove(f'shazam{id}.ogg')
     await msg.delete()
     if not out["matches"]:
       return await m.reply("فشل بالتعرف على الصوت")
     else:
       title = out["track"]["title"]
       author = out["track"]["subtitle"]
       try:
         photo = out["track"]["images"]["background"]
       except:
         photo = "https://telegra.ph/file/49ace69e7c43c0041fb63.jpg"
       k = cached_redis_get(f'{Dev_Zaid}:botkey', ttl=120)
       channel = cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) if cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) else 'w7G_BoT'
       url = out["track"]["url"]
       TEXT = f"""
{k} اسم الصوت ( [{title}]({url}) )
{k} اسم الفنان : {author}
"""           
       key = InlineKeyboardMarkup ([[InlineKeyboardButton ("🧚‍♀️",url=f"t.me/{channel}")]])
       await m.reply_photo(
         photo,caption=TEXT,reply_markup=key)
       
@Client.on_message(filters.regex("^شازام ") & filters.group)
async def shazamLyrics(c,m):
   if cached_redis_get(f'{m.chat.id}:disableShazam:{Dev_Zaid}', ttl=60):  return False
   query = m.text.split(None,1)[1]
   out = await shazam.search_track(query=query, limit=1)
   if not out:
     return await m.reply("فشل العثور")
   else:
    try:
     key = int(out["tracks"]["hits"][0]["key"])
     title = out["tracks"]["hits"][0]["heading"]["title"][:35]
     author = out["tracks"]["hits"][0]["heading"]["subtitle"]
     url = out["tracks"]["hits"][0]["url"]
     track_id = key
     about_track = await shazam.track_about(track_id=track_id)
     text=about_track["sections"][1]["text"]
     lyrics=""
     for tt in text:
       lyrics+=tt+"\n"
     return await m.reply(lyrics[:4096],reply_markup=InlineKeyboardMarkup (
       [[InlineKeyboardButton (f"{title} - {author}",url=url)]]
     )
     )
    except:
     return await m.reply("فشل العثور")
     
@Client.on_inline_query(filters.regex("SOUND"))
async def SoundCloud(c, query):
  url = query.query.split("#SOUND")[0]
  channel = cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) if cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) else 'w7G_BoT'
  if url.count('/') > 1:
    await query.answer(
        results=[           
            InlineQueryResultArticle(
                title="اضغط هنا للتحميل - صوت",
                thumb_url='https://t.me/D7BotResources/161',
                description='~ @YQYQY6 ',
                url='https://t.me/w7G_BoT',
                reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("🧚‍♀️", url=f't.me/{channel}')]]),
                input_message_content=InputTextMessageContent(f'https://soundcloud.com{url} #AUDIO',disable_web_page_preview=True)
            ),
            InlineQueryResultArticle(
                title="اضغط هنا للتحميل - بصمة",
                thumb_url='https://t.me/D7BotResources/163',
                description='~ @YQYQY6 ',
                url='https://t.me/w7G_BoT',
                reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("🧚‍♀️", url=f't.me/{channel}')]]),
                input_message_content=InputTextMessageContent(f'https://soundcloud.com{url} #VOICE',disable_web_page_preview=True)
            ),
        ],
        cache_time=1
        )
  else:
    await query.answer(
        results=[           
            InlineQueryResultArticle(
                title="اضغط هنا للتحميل - صوت",
                thumb_url='https://t.me/D7BotResources/161',
                description='~ @YQYQY6 ',
                url='https://t.me/w7G_BoT',
                reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("🧚‍♀️", url=f't.me/{channel}')]]),
                input_message_content=InputTextMessageContent(f'https://on.soundcloud.com{url} #AUDIO',disable_web_page_preview=True)
            ),
            InlineQueryResultArticle(
                title="اضغط هنا للتحميل - بصمة",
                thumb_url='https://t.me/D7BotResources/163',
                description='~ @YQYQY6 ',
                url='https://t.me/w7G_BoT',
                reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("🧚‍♀️", url=f't.me/{channel}')]]),
                input_message_content=InputTextMessageContent(f'https://on.soundcloud.com{url} #VOICE',disable_web_page_preview=True)
            ),
        ],
        cache_time=1
        )


    
@Client.on_callback_query(filters.regex("GET"))
async def get_info(c,query):
    asyncio.create_task(getInfo(c,query))

async def getInfo(c, query):
    user_id = query.data.split("GET")[0]
    vid_id = query.data.split("GET")[1]
    if not query.from_user.id == int(user_id):
      return
    if not r.get(f'{query.message.id}:one_minute:{user_id}'):
      k = cached_redis_get(f'{Dev_Zaid}:botkey', ttl=120)
      query.answer(f'{k} مر على البحث اكثر من دقيقة ابحث مرة ثانية',show_alert=True)
      return query.message.delete()
    if r.get(f'{query.message.chat.id}:disableYT:{Dev_Zaid}'):  return
    if r.get(f':disableYT:{Dev_Zaid}'):  return
    query.message.delete()
    channel = cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) if cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) else 'w7G_BoT'
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        _info = ydl.extract_info(f'https://youtu.be/{vid_id}', download=False)
    photo = _info.get('thumbnail', '')
    url = f'https://youtu.be/{vid_id}'
    reply_markup = InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton ("♫ ملف صوتي", callback_data=f'{user_id}AUDIO{vid_id}'),
          InlineKeyboardButton ("❖ فيديو", callback_data=f'{user_id}VIDEO{vid_id}'),
        ],
        [
          InlineKeyboardButton ('🧚‍♀️', url=f'https://t.me/{channel}')
        ]
      ]
    )
    query.message.reply_to_message.reply_photo(
       photo,
       caption=f'@{channel} ~ {url}',
       reply_markup=reply_markup
    )
    #os.remove(f'{vid_id}.jpg')
    

@Client.on_callback_query(filters.regex("AUDIO"))
async def get_audii(c, query):
    asyncio.create_task(audio_down(c,query))


async def audio_down(c, query):
    user_id = query.data.split("AUDIO")[0]
    vid_id = query.data.split("AUDIO")[1]
    if not query.from_user.id == int(user_id):
      return False
    if r.get(f'{query.message.chat.id}:disableYT:{Dev_Zaid}'):  return
    if r.get(f':disableYT:{Dev_Zaid}'):  return
    channel = cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) if cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) else 'w7G_BoT'
    rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url=f'https://t.me/{channel}')
     ]]
    )
    if ytdb.get(f'ytvideo{vid_id}'):
       aud = ytdb.get(f'ytvideo{vid_id}')
       query.edit_message_caption(f"@{channel} :)", reply_markup=rep)
       duration= aud["duration"]
       sec = time.strftime('%M:%S', time.gmtime(duration))
       return query.message.reply_audio(aud["audio"],caption=f'@{channel} ~ ⏳ {sec}')       
    url = f'https://youtu.be/{vid_id}'
    query.edit_message_caption("جاري التحميل ..", reply_markup=rep)    
    #ydl_ops = {"format": "bestaudio[ext=m4a]"}
    ydl_ops = {"format": "bestaudio[ext=m4a]",'forceduration':True, "username": "oauth2", "password": ''}
    with yt_dlp.YoutubeDL(ydl_ops) as ydl:
        info = ydl.extract_info(url, download=False)
        if int(info['duration']) > 1555555555555:
          return query.edit_message_caption("صوت اكثر من 25 دقيقة مقدر انزله",reply_markup=rep)
        audio_file = ydl.prepare_filename(info)
        ydl.process_info(info)
    query.edit_message_caption("✈️✈️✈️✈️✈️", reply_markup=rep)
    duration= int(info['duration'])
    sec = time.strftime('%M:%S', time.gmtime(duration))
    os.rename(audio_file,audio_file.replace(".m4a",".mp3"))
    audio_file = audio_file.replace(".m4a",".mp3")
    try:
        a = query.message.reply_audio(
          audio_file,
          title=info['title'],
          duration=int(info['duration']),
          performer=info['channel'],
          caption=f'@{channel} ~ ⏳ {sec}',
        )
        query.edit_message_caption(f"@{channel} :)", reply_markup=rep)    
        ytdb.set(f'ytvideo{vid_id}',{"type":"audio","audio":a.audio.file_id,"duration":a.audio.duration})
    finally:
        if os.path.exists(audio_file): os.remove(audio_file)


"""
@Client.on_callback_query(filters.regex("AUDIO"))
def get_audii(c, query):
    Thread(target=audio_down,args=(c,query)).start()
    
def audio_down(c, query):
    user_id = query.data.split("AUDIO")[0]
    vid_id = query.data.split("AUDIO")[1]
    if not query.from_user.id == int(user_id):
      return
    if r.get(f'{query.message.chat.id}:disableYT:{Dev_Zaid}'):  return
    if r.get(f':disableYT:{Dev_Zaid}'):  return
    channel = cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) if cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) else 'w7G_BoT'
    rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url=f'https://t.me/{channel}')
     ]]
    )
    url = f'https://youtu.be/{vid_id}'
    if r.get(f'ytvideo{vid_id}'):
       aud = r.get(f'ytvideo{vid_id}')
       query.edit_message_caption(f"@{channel} :)", reply_markup=rep)
       yt = YouTube(url)
       duration= int(yt.length)
       sec = time.strftime('%M:%S', time.gmtime(duration))
       return query.message.reply_audio(aud,caption=f'@{channel} ~ ⏳ {sec}')
    query.edit_message_caption("جاري التحميل ..", reply_markup=rep)
    yt = YouTube(url)
    duration= int(yt.length)
    sec = time.strftime('%M:%S', time.gmtime(duration))  
    if duration > 1505:
      return query.edit_message_caption("صوت اكثر من 25 دقيقة مقدر انزله",reply_markup=rep)
    yt.streams.get_audio_only().download(filename=f'{vid_id}.mp3')
    query.edit_message_caption("✈️✈️✈️✈️✈️", reply_markup=rep)
    a = query.message.reply_audio(
      f'{vid_id}.mp3',
      title=yt.title,
      duration=yt.length,
      performer=yt.author,
      caption=f'@{channel} ~ ⏳ {sec}',
    )
    query.edit_message_caption(f"@{channel} :)", reply_markup=rep)
    
    r.set(f'ytvideo{vid_id}',b.link)
    os.remove(f'{vid_id}.mp3')
"""

@Client.on_callback_query(filters.regex("VIDEO"))
async def get_video(c, query):
   asyncio.create_task(video_down(c,query))

async def video_down(c, query):
    user_id = query.data.split("VIDEO")[0]
    vid_id = query.data.split("VIDEO")[1]
    if not query.from_user.id == int(user_id):
      return False
    if r.get(f'{query.message.chat.id}:disableYT:{Dev_Zaid}'):  return
    if r.get(f':disableYT:{Dev_Zaid}'):  return
    channel = cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) if cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) else 'w7G_BoT'
    rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url=f'https://t.me/{channel}')
     ]]
    )
    if ytdb.get(f'ytvideoV{vid_id}'):
       vid = ytdb.get(f'ytvideoV{vid_id}')
       query.edit_message_caption(f"@{channel} :)", reply_markup=rep)
       duration=vid["duration"]
       sec = time.strftime('%M:%S', time.gmtime(duration))
       return query.message.reply_video(vid["video"],caption=f'@{channel} ~ ⏳ {sec}')
    url = f'https://youtu.be/{vid_id}'
    query.edit_message_caption("جاري التحميل ..", reply_markup=rep)
    with yt_dlp.YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)
        if int(info['duration']) > 1555555555:
          return query.edit_message_caption("فيديو اكثر من 25 دقيقة مقدر انزله",reply_markup=rep)
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
        "username": "oauth2", 
        "password": ''
    }
    with YoutubeDL(ydl_opts) as ytdl:
        ytdl_data = ytdl.extract_info(url, download=True)
        file_name = ytdl.prepare_filename(ytdl_data)
    query.edit_message_caption("✈️✈️✈️✈️✈️", reply_markup=rep)
    duration= int(info['duration'])
    sec = time.strftime('%M:%S', time.gmtime(duration))
    try:
        a = query.message.reply_video(
          file_name,
          duration=int(info['duration']),
          caption=f'@{channel} ~ ⏳ {sec}',
        )
        query.edit_message_caption(f"@{channel} :)", reply_markup=rep)    
        ytdb.set(f'ytvideoV{vid_id}',{"type":"video","video":a.video.file_id,"duration":a.video.duration})
    finally:
        if os.path.exists(file_name): os.remove(file_name)

"""
@Client.on_callback_query(filters.regex("VIDEO"))
async def get_video(c, query):
    Thread(target=video_down,args=(c,query)).start()
    
def video_down(c, query):
    user_id = query.data.split("VIDEO")[0]
    vid_id = query.data.split("VIDEO")[1]
    if not query.from_user.id == int(user_id):
      return
    if r.get(f'{query.message.chat.id}:disableYT:{Dev_Zaid}'):  return
    if r.get(f':disableYT:{Dev_Zaid}'):  return
    channel = cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) if cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) else 'w7G_BoT'
    rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url=f'https://t.me/{channel}')
     ]]
    )
    url = f'https://youtu.be/{vid_id}'    
    if r.get(f'ytvideoV{vid_id}'):
       vid = r.get(f'ytvideoV{vid_id}')       
       query.edit_message_caption(f"@{channel} :)", reply_markup=rep)
       yt = YouTube(url)
       duration= int(yt.length)
       sec = time.strftime('%M:%S', time.gmtime(duration))
       return query.message.reply_video(vid,caption=f'@{channel} ~ ⏳ {sec}')
    query.edit_message_caption("جاري التحميل ..", reply_markup=rep)
    yt = YouTube(url)
    duration= int(yt.length)
    sec = time.strftime('%M:%S', time.gmtime(duration))
    if duration > 1505:
      return query.edit_message_caption("صوت اكثر من 25 دقيقة مقدر انزله",reply_markup=rep)
    yt.streams.get_highest_resolution().download(filename=f'{vid_id}.mp4')
    query.edit_message_caption("✈️✈️✈️✈️✈️", reply_markup=rep)       
    a = query.message.reply_video(
      f'{vid_id}.mp4',
      duration=duration,
      caption=f'@{channel} ~ ⏳ {sec}',
    )
    query.edit_message_caption(f"@{channel} :)", reply_markup=rep)
    
    r.set(f'ytvideoV{vid_id}',b.link)    
    os.remove(f'{vid_id}.mp4')
"""