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

import random, re, time, os, sys
import asyncio
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from helpers.Ranks import *


@Client.on_message(filters.text & filters.group, group=36)
async def replaceCode(c,m):
    k = cached_redis_get(f'{Dev_Zaid}:botkey', ttl=120)
    channel = cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) if cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) else 'yqyqy66'
    asyncio.create_task(raplaceCodefunc(c,m,k,channel))
    
async def raplaceCodefunc(c,m,k,channel):
   if not cached_redis_get(f'{m.chat.id}:enable:{Dev_Zaid}', ttl=30):  return
   if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:delCustom:{m.from_user.id}{Dev_Zaid}') or r.get(f'{m.chat.id}:delCustomG:{m.from_user.id}{Dev_Zaid}'):  return 
   if cached_redis_get(f'{m.chat.id}:mute:{Dev_Zaid}', ttl=30) and not admin_pls(m.from_user.id,m.chat.id):  return  
   if r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_Zaid}'):  return 
   text = m.text
   name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'رعد'
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
       
   '''
   if text == 'الملفات':
     if m.from_user.id == 6168217372:
        text = '——— ملفات السورس ———'
        a = os.listdir('Plugins')
        a.sort()
        count = 1
        for file in a:
          if file.endswith('.py'):
            text += f'\n{count}) `{file}`'
            count += 1
        text += f'\n——— @{channel} ———'
        return await m.reply(text, disable_web_page_preview=True)
   '''
   if r.get(f'{m.chat.id}:replace:{m.from_user.id}{Dev_Zaid}') or r.get(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_Zaid}') or r.get(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_Zaid}'):
     if text == 'الغاء':
       r.delete(f'{m.chat.id}:replace:{m.from_user.id}{Dev_Zaid}')
       r.delete(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_Zaid}')
       r.delete(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_Zaid}')
       return await m.reply(f'{k} من عيوني لغيت استبدال كلمة ')
      
   if text == 'استبدال كلمه' or text == 'استبدال كلمة':
      if not devp_pls(m.from_user.id,m.chat.id):
         return await m.reply(f'{k} هذا الأمر يخص ( مبرمج السورس ) بس')
      else:
         r.set(f'{m.chat.id}:replace:{m.from_user.id}{Dev_Zaid}',1,ex=600)
         return await m.reply(f'{k} ارسل الكلمة القديمة الآن')
   
   if r.get(f'{m.chat.id}:replace:{m.from_user.id}{Dev_Zaid}') and devp_pls(m.from_user.id,m.chat.id):
      r.set(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_Zaid}',m.text,ex=600)
      r.delete(f'{m.chat.id}:replace:{m.from_user.id}{Dev_Zaid}')
      return await m.reply(f'{k} ارسل الكلمة الجديدة الحين')
   
   if r.get(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_Zaid}') and devp_pls(m.from_user.id,m.chat.id):
      txt = r.get(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_Zaid}')
      r.delete(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_Zaid}')
      r.set(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_Zaid}',f'{txt}&&new&&{m.text}',ex=600)
      a = os.listdir('Plugins')
      a.sort()
      txt = f'{k} ارسل اسم الملف الي تبي تعدل فيه الحين:'
      count = 1
      txt += '\n\n——— ملفات السورس ———'
      for file in a:
          if file.endswith('.py'):
            txt += f'\n{count}) `{file}`'
            count += 1
      txt += f'\n——— @{channel} ———'
      return await m.reply(txt)
   
   if r.get(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_Zaid}') and devp_pls(m.from_user.id,m.chat.id) and m.text in os.listdir('Plugins'):
      mm = await m.reply(f'{k} جاريع تعديل الملف')
      get = r.get(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_Zaid}')
      old = get.split('&&new&&')[0]
      new = get.split('&&new&&')[1]
      r.delete(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_Zaid}')
      with open(f'Plugins/{m.text}', 'r', encoding='utf-8') as Read:
         old_confing = Read.read()
         await m.edit(f'{k} تم فتح الملف وقراءته')
      with open(f'Plugins/{m.text}', 'w+', encoding='utf-8') as Write:
         await m.edit(f'{k} تم فتح الملف جاري كتابة الكود مع استبدال الكلمة')
         Write.write(old_confing.replace(old,new))
      await m.edit(f'{k} تم فتح الملف `{m.text}` وتعديله\n{k} تم استبدال الكلمة القديمة ( {old} ) بالكلمة الجديدة ( {new} )')
      python = sys.executable
      os.execl(python, python, *sys.argv)
      
      
      
      
      
   