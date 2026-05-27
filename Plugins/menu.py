from helpers.utils import cached_redis_get
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Dev_Zaid

CATS = {
  'dl':      ('🎵','التحميل',   [('يوت [كلمة]','بحث وتحميل يوتيوب'),('بحث [كلمة]','تحميل أول نتيجة'),('ساوند [كلمة]','ساوند كلاود'),('تيك [رابط]','تحميل تيك توك')]),
  'voice':   ('🔊','الصوت',     [('انطق [نص]','نطق النص صوتياً'),('وش يقول','تحويل صوت لنص'),('ترجمه [نص]','ترجمة فورية'),('تفعيل/تعطيل انطقي','التحكم بالنطق'),('تفعيل/تعطيل شازام','التحكم بالشازام')]),
  'games':   ('🎮','الألعاب',   [('عواصم','لعبة العواصم'),('اكينيتور','أكينيتور'),('صارحني','نظام المصارحة'),('عربي','لعبة الكلمات'),('توب','المتفاعلين'),('استثمار','الاقتصاد')]),
  'ranks':   ('👑','الرتب',     [('رفع مالك [رد]','رفع لمالك'),('رفع مدير [رد]','رفع لمدير'),('رفع ادمن [رد]','رفع لأدمن'),('رفع مميز [رد]','رفع لمميز'),('تنزيل [رد]','تنزيل رتبة'),('تغيير رتبه [نص]','تغيير اسم رتبتك')]),
  'mod':     ('🛡️','الحماية',  [('كتم [رد]','كتم عضو'),('الغاء الكتم [رد]','رفع الكتم'),('حظر عام [رد]','حظر شامل'),('قفل الروابط','منع الروابط'),('قفل الصور','منع الصور'),('قفل الملصقات','منع الملصقات')]),
  'settings':('⚙️','الإعدادات',[('الاعدادات','إعدادات القروب'),('تفعيل / تعطيل','تشغيل البوت'),('وضع الترحيب','رسالة الترحيب'),('وضع قوانين','قوانين القروب'),('قناة الاشتراك','اشتراك إجباري')]),
  'filters': ('💬','الردود',    [('اضف رد','إضافة رد مخصص'),('مسح رد','حذف رد'),('الردود','قائمة الردود'),('اضف رد مميز','رد للكل'),('اضف رد عام','رد لجميع قروباتي')]),
  'info':    ('📊','المعلومات', [('id [رد]','معرّف شخص/قروب'),('رتبتي','رتبتي'),('صلاحياتي','صلاحياتي'),('المتفاعلين','أكثر المتفاعلين'),('كشف [رد]','معلومات مفصّلة')]),
  'fun':     ('🎉','المرح',     [('رفع كيك','ترشيح للكيكة 🍰'),('ميمز','ميم عشوائي'),('كليزق','صورة كليزق'),('اكرهك','رسالة غضب 😤'),('قرآن','آية قرآنية'),('سورة [اسم]','سورة كاملة')]),
}

def _main(k, name):
    hdr = (
        f'<b>{k}  {name}</b>\n'
        '┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n'
        '<b>📋 قائمة الأوامر</b>\n'
        '┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n'
        '✨ <i>اختر قسماً لعرض أوامره:</i>'
    )
    cats = list(CATS.items())
    btns = []
    for i in range(0, len(cats), 3):
        row = []
        for key, (ic, lbl, _) in cats[i:i+3]:
            row.append(InlineKeyboardButton(f'{ic} {lbl}', callback_data=f'men_{key}'))
        btns.append(row)
    btns.append([InlineKeyboardButton('✦ R3D Source ✦', url=f'https://t.me/eFFb0t')])
    return hdr, InlineKeyboardMarkup(btns)

def _page(key):
    ic, lbl, cmds = CATS[key]
    lines = [f'<b>{ic}  {lbl}</b>', '━━━━━━━━━━━━━━━━━━━━']
    for cmd, desc in cmds:
        lines.append(f'  ◈ <code>{cmd}</code>')
        lines.append(f'    ╰ <i>{desc}</i>')
    lines.append('━━━━━━━━━━━━━━━━━━━━')
    return '\n'.join(lines), InlineKeyboardMarkup([[InlineKeyboardButton('⬅️ رجوع', callback_data='men_back')]])

@Client.on_message(filters.text & filters.group, group=99)
async def menu_handler(c, m):
    k = cached_redis_get(f'{Dev_Zaid}:botkey', ttl=120) or ''
    name = cached_redis_get(f'{Dev_Zaid}botname', ttl=120) or 'رعد'
    txt = (m.text or '').strip()
    if txt in ('الاوامر','اوامر','الأوامر','/help','/commands','مساعدة'):
        t, mk = _main(k, name)
        await m.reply(t, reply_markup=mk, parse_mode='html', disable_web_page_preview=True)

@Client.on_callback_query(filters.regex(r'^men_'))
async def menu_cb(c, q):
    k = cached_redis_get(f'{Dev_Zaid}:botkey', ttl=120) or ''
    name = cached_redis_get(f'{Dev_Zaid}botname', ttl=120) or 'رعد'
    key = q.data[4:]
    try:
        if key == 'back':
            t, mk = _main(k, name)
        elif key in CATS:
            t, mk = _page(key)
        else:
            await q.answer('قسم غير موجود', show_alert=True); return
        await q.message.edit_text(t, reply_markup=mk, parse_mode='html')
        await q.answer()
    except Exception:
        await q.answer('خطأ، جرب مرة ثانية', show_alert=True)
