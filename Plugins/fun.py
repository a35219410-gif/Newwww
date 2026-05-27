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

import random, re, time
import asyncio
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from helpers.Ranks import *
from helpers.Ranks import isLockCommand


@Client.on_message(filters.text & filters.group, group=34)
async def funHandler(c,m):
    k = cached_redis_get(f'{Dev_Zaid}:botkey', ttl=120)
    channel = cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) if cached_redis_get(f'{Dev_Zaid}:BotChannel', ttl=120) else 'yqyqy66'
    asyncio.create_task(funFunc(c,m,k,channel))
    
async def funFunc(c,m,k,channel):
   if cached_redis_get(f'{m.chat.id}:disableFun:{Dev_Zaid}', ttl=60):  return 
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
   if isLockCommand(m.from_user.id, m.chat.id, text): return
   ################# CAKE #################
   if text == 'رفع كيك' or text == 'رفع كيكه' or text == 'رفع كيكة':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:CakeList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} كيكه من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:CakeList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:CakeName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته كيكه 🍰\n☆')
   
   if text == 'تنزيل كيك' or text == 'تنزيل كيكه' or text == 'تنزيل كيكة':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:CakeList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو كيكه من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:CakeList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:CakeName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من كيكه\n☆')
   
   if text == 'قائمه الكيك' or text == 'قائمة الكيك':
     if not r.smembers(f'{Dev_Zaid}:CakeList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة الكيك فاضية')
     else:
       txt = '- قائمة الكيك 🍰\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:CakeList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:CakeName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الكيك' or text == 'مسح قائمه الكيك':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:CakeList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة الكيك فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة الكيك')
         for cake in r.smembers(f'{Dev_Zaid}:CakeList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:CakeList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:CakeName:{cake}')
           
   ################# CAKE #################
   
   ################# 3SL #################
   if text == 'رفع عسل':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:3SLList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} عسل من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:3SLList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:3SLName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته عسل 🍯\n☆')
   
   if text == 'تنزيل عسل':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:3SLList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو عسل من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:3SLList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:3SLName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من عسل\n☆')
   
   if text == 'قائمه العسل' or text == 'قائمة العسل':
     if not r.smembers(f'{Dev_Zaid}:3SLList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة العسل فاضية')
     else:
       txt = '- قائمة العسل 🍯\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:3SLList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:3SLName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة العسل' or text == 'مسح قائمه العسل':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:3SLList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة العسل فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة العسل')
         for cake in r.smembers(f'{Dev_Zaid}:3SLList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:3SLList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:3SLName:{cake}')

   ################# 3SL #################
   
   ################# ZQ #################
   if text == 'رفع نصاب':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:ZQList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} نصاب من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:ZQList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:ZQName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته نصاب 💩\n☆')
   
   if text == 'تنزيل نصاب':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:ZQList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو نصاب من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:ZQList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:ZQName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من نصاب\n☆')
   
   if text == 'قائمه النصابين' or text == 'قائمة النصابين':
     if not r.smembers(f'{Dev_Zaid}:ZQList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة النصابين فاضية')
     else:
       txt = '- قائمة النصابين 💩\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:ZQList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:ZQName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة النصابين' or text == 'مسح قائمه النصابين':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:ZQList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة النصابين فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة النصابين')
         for cake in r.smembers(f'{Dev_Zaid}:ZQList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:ZQList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:ZQName:{cake}')

   ################# ZQ #################
   
   ################# 7MR #################
   if text == 'رفع حمار':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:7MRList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} حمار من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:7MRList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:7MRName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته حمار 🦓\n☆')
   
   if text == 'تنزيل حمار':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:7MRList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو حمار من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:7MRList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:7MRName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من حمار\n☆')
   
   if text == 'قائمه الحمير' or text == 'قائمة الحمير':
     if not r.smembers(f'{Dev_Zaid}:7MRList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة الحمير فاضية')
     else:
       txt = '- قائمة الحمير 🦓\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:7MRList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:7MRName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الحمير' or text == 'مسح قائمه الحمير':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:7MRList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة الحمير فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة الحمير')
         for cake in r.smembers(f'{Dev_Zaid}:7MRList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:7MRList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:7MRName:{cake}')

   ################# 7MR #################
   
   ################# COW #################
   if text == 'رفع بقرة' or text == 'رفع بقره':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:COWList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} بقرة من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:COWList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:COWName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته بقرة 🐄\n☆')
   
   if text == 'تنزيل بقرة' or text == 'تنزيل بقره':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:COWList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو بقرة من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:COWList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:COWName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من بقرة\n☆')
   
   if text == 'قائمه البقر' or text == 'قائمة البقر':
     if not r.smembers(f'{Dev_Zaid}:COWList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة البقر فاضية')
     else:
       txt = '- قائمة البقر 🐄\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:COWList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:COWName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة البقر' or text == 'مسح قائمه البقر':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:COWList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة البقر فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة البقر')
         for cake in r.smembers(f'{Dev_Zaid}:COWList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:COWList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:COWName:{cake}')

   ################# COW #################
   
   ################# DOG #################
   if text == 'رفع كلب':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:DOGList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} كلب من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:DOGList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:DOGName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته كلب 🐩\n☆')
   
   if text == 'تنزيل كلب':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:DOGList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو كلب من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:DOGList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:DOGName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من كلب\n☆')
   
   if text == 'قائمه الكلاب' or text == 'قائمة الكلاب':
     if not r.smembers(f'{Dev_Zaid}:DOGList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة الكلاب فاضية')
     else:
       txt = '- قائمة الكلاب 🐩\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:DOGList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:DOGName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الكلاب' or text == 'مسح قائمه الكلاب':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:DOGList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة الكلاب فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة الكلاب')
         for cake in r.smembers(f'{Dev_Zaid}:DOGList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:DOGList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:DOGName:{cake}')

   ################# DOG #################
   
   ################# MON #################
   if text == 'رفع قرد':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:MONList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} قرد من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:MONList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:MONName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته قرد 🐒\n☆')
   
   if text == 'تنزيل قرد':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:MONList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو قرد من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:MONList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:MONName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من قرد\n☆')
   
   if text == 'قائمه القرود' or text == 'قائمة القرود':
     if not r.smembers(f'{Dev_Zaid}:MONList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة القرود فاضية')
     else:
       txt = '- قائمة القرود 🐒\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:MONList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:MONName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة القرود' or text == 'مسح قائمه القرود':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:MONList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة القرود فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة القرود')
         for cake in r.smembers(f'{Dev_Zaid}:MONList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:MONList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:MONName:{cake}')

   ################# MON #################
   
   ################# TES #################
   if text == 'رفع تيس':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:TESList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} تيس من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:TESList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:TESName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته تيس 🐐\n☆')
   
   if text == 'تنزيل تيس':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:TESList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو تيس من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:TESList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:TESName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من تيس\n☆')
   
   if text == 'قائمه التيس' or text == 'قائمة التيس':
     if not r.smembers(f'{Dev_Zaid}:TESList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة التيوس فاضية')
     else:
       txt = '- قائمة التيوس 🐐\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:TESList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:TESName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة التيس' or text == 'مسح قائمه التيس':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:TESList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة التيوس فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة التيوس')
         for cake in r.smembers(f'{Dev_Zaid}:TESList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:TESList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:TESName:{cake}')

   ################# TES #################
   
   
   ################# TOR #################
   if text == 'رفع ثور':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:TORList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ثور من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:TORList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:TORName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته ثور 🐂\n☆')
   
   if text == 'تنزيل ثور':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:TORList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو ثور من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:TORList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:TORName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من ثور\n༄')
   
   if text == 'قائمه الثور' or text == 'قائمة الثور':
     if not r.smembers(f'{Dev_Zaid}:TORList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة الثور فاضية')
     else:
       txt = '- قائمة الثور 🐂\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:TORList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:TORName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الثور' or text == 'مسح قائمه الثور':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:TORList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة الثور فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة الثور')
         for cake in r.smembers(f'{Dev_Zaid}:TORList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:TORList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:TORName:{cake}')

   ################# TOR #################
   
   
   ################# B3S #################
   if text == 'رفع هكر':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:B3SList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} هكر من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:B3SList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:B3SName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته هكر 🏅\n☆')
   
   if text == 'تنزيل هكر':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:B3SList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو هكر من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:B3SList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:B3SName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من هكر\n☆')
   
   if text == 'قائمه الهكر' or text == 'قائمة الهكر':
     if not r.smembers(f'{Dev_Zaid}:B3SList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة الهكر فاضية')
     else:
       txt = '- قائمة الهكر 🏅\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:B3SList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:B3SName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الهكر' or text == 'مسح قائمه الهكر':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:B3SList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة الهكر فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة الهكر')
         for cake in r.smembers(f'{Dev_Zaid}:B3SList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:B3SList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:B3SName:{cake}')

   ################# B3S #################
   
   ################# DJJ #################
   if text == 'رفع دجاجه' or text == 'رفع دجاجة':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:DJJList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} دجاجه من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:DJJList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:DJJName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته دجاجه 🐓\n☆')
   
   if text == 'تنزيل دجاجه' or text == 'تنزيل دجاجة':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:DJJList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو دجاجه من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:DJJList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:DJJName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من دجاجه\n☆')
   
   if text == 'قائمه الدجاج' or text == 'قائمة الدجاج':
     if not r.smembers(f'{Dev_Zaid}:DJJList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة الدجاج فاضية')
     else:
       txt = '- قائمة الدجاج 🐓\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:DJJList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:DJJName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الدجاج' or text == 'مسح قائمه الدجاج':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:DJJList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة الدجاج فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة الدجاج')
         for cake in r.smembers(f'{Dev_Zaid}:DJJList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:DJJList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:DJJName:{cake}')

   ################# DJJ #################
   
   ################# HTF #################
   if text == 'رفع ملكه':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:HTFList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ملكه من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:HTFList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:HTFName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته ملكه 🧱\n☆')
   
   if text == 'تنزيل ملكه':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:HTFList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو ملكه من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:HTFList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:HTFName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من ملكه\n☆')
   
   if text == 'قائمه الهطوف' or text == 'قائمة الهطوف':
     if not r.smembers(f'{Dev_Zaid}:HTFList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة الهطوف فاضية')
     else:
       txt = '- قائمة الهطوف 🧱\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:HTFList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:HTFName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الهطوف' or text == 'مسح قائمه الهطوف':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:HTFList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة الهطوف فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة الهطوف')
         for cake in r.smembers(f'{Dev_Zaid}:HTFList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:HTFList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:HTFName:{cake}')

   ################# HTF #################
   
   ################# SYD #################
   if text == 'رفع صياد':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:SYDList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} صياد من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:SYDList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:SYDName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته صياد 🔫\n☆')
   
   if text == 'تنزيل صياد':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:SYDList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو صياد من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:SYDList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:SYDName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من صياد\n☆')
   
   if text == 'قائمه الصيادين' or text == 'قائمة الصيادين':
     if not r.smembers(f'{Dev_Zaid}:SYDList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة الصيادين فاضية')
     else:
       txt = '- قائمة الصيادين 🔫\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:SYDList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:SYDName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الصيادين' or text == 'مسح قائمه الصيادين':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:SYDList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة الصيادين فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة الصيادين')
         for cake in r.smembers(f'{Dev_Zaid}:SYDList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:SYDList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:SYDName:{cake}')

   ################# SYD #################
   
   ################# 5RF #################
   if text == 'رفع خروف':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:5RFList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} خروف من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:5RFList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:5RFName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته خروف 🐏\n☆')
   
   if text == 'تنزيل خروف':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:5RFList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو خروف من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:5RFList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:5RFName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من خروف\n☆')
   
   if text == 'قائمه الخرفان' or text == 'قائمة الخرفان':
     if not r.smembers(f'{Dev_Zaid}:5RFList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة الخرفان فاضية')
     else:
       txt = '- قائمة الخرفان 🐏\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:5RFList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:5RFName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الخرفان' or text == 'مسح قائمه الخرفان':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:5RFList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة الخرفان فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة الخرفان')
         for cake in r.smembers(f'{Dev_Zaid}:5RFList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:5RFList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:5RFName:{cake}')

   ################# 5RF #################
   
   ################# TEZ #################
   if text == 'رفع هكر':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:TEZList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} هكر من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:TEZList:{m.chat.id}',id)
         r.set(f'{Dev_Zaid}:TEZName:{id}', mention)
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته هكر ♕\n☆')
   
   if text == 'تنزيل هكر':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention
       id = m.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:TEZList:{m.chat.id}',id):
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو هكر من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:TEZList:{m.chat.id}',id)
         r.delete(f'{Dev_Zaid}:TEZName:{id}')
         return await m.reply(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من هكر\n☆')
   
   if text == 'قائمه هكر' or text == 'قائمة هكر':
     if not r.smembers(f'{Dev_Zaid}:TEZList:{m.chat.id}'):
       return await m.reply(f'{k} قائمة هكر فاضية')
     else:
       txt = '- قائمة هكر ♕\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:TEZList:{m.chat.id}'):
          mention = r.get(f'{Dev_Zaid}:TEZName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة هكر' or text == 'مسح قائمه هكر':
     if not admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:TEZList:{m.chat.id}'):
         return await m.reply(f'{k} قائمة هكر فاضية')
       else:
         await m.reply(f'{k} ابشر مسحت قائمة هكر')
         for cake in r.smembers(f'{Dev_Zaid}:TEZList:{m.chat.id}'):
           r.srem(f'{Dev_Zaid}:TEZList:{m.chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:TEZName:{cake}')

   ################# TEZ #################
   
   ################# 🔮 #################
   
   if text == 'رفع لقلبي' and m.reply_to_message:
     return await m.reply('{} رفعته لقلبك\n{} اللهم حسد 😔'.format(k,k))
   
   if text == 'تنزيل من قلبي' and m.reply_to_message:
     return await m.reply('اح اح ماتوصل')
   
   ################# 🔮 #################
   
   
   
   
       
      
   
   
   