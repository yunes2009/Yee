import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ⚠️ ضع رابط موقعك الرئيسي على GitHub Pages هنا (بدون / في النهاية)
GITHUB_BASE_URL = "https://yunes2009.github.io/Yee/"
BOT_TOKEN = "8538003058:AAG4mtW37JnPDkQBprB6dYfKFbV3vfhmrW8"
# القائمة الرئيسية للوحدات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📸 الوحدة 1: خدع الصور والأذونات", callback_data="u1_menu")],
        [InlineKeyboardButton("🎙️ الوحدة 2: خدع الصوت والتنصت", callback_data="u2_menu")],
        [InlineKeyboardButton("📱 الوحدة 3: الهاتف وكلمات السر", callback_data="u3_menu")],
        [InlineKeyboardButton("⚠️ الوحدة 4: الابتزاز والهندسة الاجتماعية", callback_data="u4_menu")],
        [InlineKeyboardButton("🛡️ الوحدة 5: التأمين واستخراج الخبايا", callback_data="u5_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎓 **لوحة تحكم الأستاذ - التجارب التفاعلية الحية**\nاختر الوحدة الدراسية لتوليد رابط الخدعة للطلاب:", reply_markup=reply_markup, parse_mode="Markdown")

# التعامل مع الضغط على الأزرار
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # --- أزرار القوائم الفرعية ---
    if data == "u1_menu":
        kb = [
            [InlineKeyboardButton("📸 التقاط صورة واحدة خاطفة", callback_data="gen_u1_snap1")],
            [InlineKeyboardButton("🎞️ سحب 3 صور متتالية (تسلسلي)", callback_data="gen_u1_snap3")],
            [InlineKeyboardButton("🔍 سحب بيانات EXIF للموقع مع الصورة", callback_data="gen_u1_exif")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")]
        ]
        await query.edit_message_text("📸 **الوحدة الأولى: خدع الصور والتقاطها**\nاختر التجربة المراد توليد رابطها:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "u2_menu":
        kb = [
            [InlineKeyboardButton("🎧 تسجيل صوتي سريع (3 ثوانٍ)", callback_data="gen_u2_rec3")],
            [InlineKeyboardButton("🗣️ تنصت وتماثل صوتي (استคลون)", callback_data="gen_u2_stream")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")]
        ]
        await query.edit_message_text("🎙️ **الوحدة الثانية: خدع الصوت**\nاختر التجربة المراد توليد رابطها:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "u3_menu":
        kb = [
            [InlineKeyboardButton("🔋 سحب معلومات الجهاز والبطارية كاملة", callback_data="gen_u3_sys")],
            [InlineKeyboardButton("🔑 خدعة صفحة قفل الشاشة المزيفة", callback_data="gen_u3_pin")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")]
        ]
        await query.edit_message_text("📱 **الوحدة الثالثة: الهواتف والسرية**\nاختر التجربة المراد توليد رابطها:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "u4_menu":
        kb = [
            [InlineKeyboardButton("🎁 فخ عجلة الحظ والجوائز (Phishing)", callback_data="gen_u4_wheel")],
            [InlineKeyboardButton("🚨 فخ إنذار الفيروسات والتخويف", callback_data="gen_u4_scare")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")]
        ]
        await query.edit_message_text("⚠️ **الوحدة الرابعة: الابتزاز والهندسة الاجتماعية**\nاختر التجربة المراد توليد رابطها:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "u5_menu":
        kb = [
            [InlineKeyboardButton("📍 كشف الموقع الجغرافي دقيقاً (GPS)", callback_data="gen_u5_gps")],
            [InlineKeyboardButton("🧪 فحص الأذونات الشامل (All-in-One)", callback_data="gen_u5_full")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")]
        ]
        await query.edit_message_text("🛡️ **الوحدة الخامسة: التأمين والحماية**\nاختر التجربة المراد توليد رابطها:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "main_menu":
        await start(query, context)

    # --- توليد الروابط المباشرة ---
    elif data.startswith("gen_"):
        mode = data.replace("gen_", "")
        generated_link = f"{GITHUB_BASE_URL}/index.html?mode={mode}"
        
        reply_msg = f"🔗 **الرابط الجاهز للإرسال للطلاب:**\n`{generated_link}`\n\n💡 *انسخ الرابط وأرسله في مجموعة الفصل، وبمجرد تفاعل الطالب سيصلك التقرير مباشرة هنا!*"
        
        kb = [[InlineKeyboardButton("⬅️ العودة للقوائم", callback_data="main_menu")]]
        await query.edit_message_text(reply_msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    print("🤖 البوت يعمل الآن وتأهب لتوليد الروابط...")
    app.run_polling()

if __name__ == "__main__":
    main()
