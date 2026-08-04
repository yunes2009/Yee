#!/usr/bin/env python3
"""
Telegram bot for interactive lab links (ready for Render).
Usage:
- Set environment variables:
    BOT_TOKEN (required)
    GITHUB_BASE_URL (optional, defaults to example)
    RENDER_EXTERNAL_URL (optional, e.g. https://your-service.onrender.com)
      If present, the bot will try to run as a webhook server and register webhook at:
        {RENDER_EXTERNAL_URL}/webhook/{BOT_TOKEN}
      Otherwise the bot falls back to long polling (useful for Render Background Worker).
    ADMIN_ID (optional) - comma-separated Telegram user IDs allowed to use the admin panel.
    ADMIN_USERNAME (optional) - comma-separated Telegram usernames (without @) allowed to use the admin panel.
- Start: `python bot.py` or use uvicorn if you adapt to ASGI (not required here).
"""
import os
import logging
import asyncio

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# --- Configuration ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required. Set it in Render dashboard secrets.")

GITHUB_BASE_URL = os.environ.get("GITHUB_BASE_URL", "https://example.github.io/Yee")
# Optional: external URL of Render service (with https://). If set, webhook mode will be used.
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

# Admin access control
ADMIN_IDS = set()
admin_env = os.environ.get("ADMIN_ID", "")
if admin_env:
    for part in admin_env.split(","):
        part = part.strip()
        if part.isdigit():
            ADMIN_IDS.add(int(part))

# Optional: allow matching by username as well (comma-separated, without @)
ADMIN_USERNAMES = set()
admin_user_env = os.environ.get("ADMIN_USERNAME", "")
if admin_user_env:
    for part in admin_user_env.split(","):
        p = part.strip().lstrip("@")
        if p:
            ADMIN_USERNAMES.add(p.lower())

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
if not ADMIN_IDS and not ADMIN_USERNAMES:
    logger.warning("No ADMIN_ID or ADMIN_USERNAME set; admin checks are disabled and the bot will allow anyone to open the admin panel.")

# --- Admin helpers ---

def _get_user_from_update(update: Update):
    if update.effective_user:
        return update.effective_user
    if update.callback_query and update.callback_query.from_user:
        return update.callback_query.from_user
    return None


def is_admin(update: Update) -> bool:
    user = _get_user_from_update(update)
    if not user:
        return False
    # If no admin configured, fall back to allow all (backwards compatibility)
    if not ADMIN_IDS and not ADMIN_USERNAMES:
        return True
    if user.id in ADMIN_IDS:
        return True
    if user.username and user.username.lower() in ADMIN_USERNAMES:
        return True
    return False

# --- Handlers ---
async def send_main_menu_target(target, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📸 الوحدة 1: خدع الصور والأذونات", callback_data="u1_menu")],
        [InlineKeyboardButton("🎙️ الوحدة 2: خدع الصوت والتنصت", callback_data="u2_menu")],
        [InlineKeyboardButton("📱 الوحدة 3: الهاتف وكلمات السر", callback_data="u3_menu")],
        [InlineKeyboardButton("⚠️ الوحدة 4: الابتزاز والهندسة الاجتماعية", callback_data="u4_menu")],
        [InlineKeyboardButton("🛡️ الوحدة 5: التأمين واستخراج الخبايا", callback_data="u5_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "🎓 *لوحة تحكم الأستاذ - التجارب التفاعلية الحية*\n"
        "اختر الوحدة الدراسية لتوليد رابط الخدعة الذي سترسله للطلاب."
    )
    # target can be Message (has reply_text) or CallbackQuery (we'll edit)
    if hasattr(target, "edit_message_text"):
        await target.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await target.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Restrict /start to admins only
    if not is_admin(update):
        # reply differently depending on source
        if update.callback_query:
            await update.callback_query.answer("❌ غير مصرح. هذه لوحة خاصة بالأستاذ فقط.", show_alert=True)
        else:
            await update.message.reply_text("❌ غير مصرح. هذه لوحة خاصة بالأستاذ فقط.")
        return

    # start may be called from /start message
    if update.callback_query:
        await send_main_menu_target(update.callback_query, context)
    else:
        await send_main_menu_target(update.message, context)


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    # Only admins may interact with the admin buttons
    if not is_admin(update):
        # Inform the user that they are not authorized (use alert so they see it)
        await query.answer("❌ غير مصرح لك. هذه لوحة خاصة بالأستاذ.", show_alert=True)
        return

    # acknowledge silently
    await query.answer()
    data = query.data

    # Submenus
    if data == "u1_menu":
        kb = [
            [InlineKeyboardButton("📸 التقاط صورة واحدة خاطفة", callback_data="gen_u1_snap1")],
            [InlineKeyboardButton("🎞️ سحب 3 صور متتالية (تسلسلي)", callback_data="gen_u1_snap3")],
            [InlineKeyboardButton("🔍 سحب بيانات EXIF للموقع مع الصورة", callback_data="gen_u1_exif")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            "📸 *الوحدة الأولى: خدع الصور والتقاطها*\nاختر التجربة المراد توليد رابطها:",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data == "u2_menu":
        kb = [
            [InlineKeyboardButton("🎧 تسجيل صوتي سريع (3 ثوانٍ)", callback_data="gen_u2_rec3")],
            [InlineKeyboardButton("🗣️ تنصت وتماثل صوتي (استنسخ صوت)", callback_data="gen_u2_stream")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            "🎙️ *الوحدة الثانية: خدع الصوت*\nاختر التجربة المراد توليد رابطها:",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data == "u3_menu":
        kb = [
            [InlineKeyboardButton("🔋 سحب معلومات الجهاز والبطارية كاملة", callback_data="gen_u3_sys")],
            [InlineKeyboardButton("🔑 خدعة صفحة قفل الشاشة المزيفة", callback_data="gen_u3_pin")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            "📱 *الوحدة الثالثة: الهواتف والسرية*\nاختر التجربة المراد توليد رابطها:",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data == "u4_menu":
        kb = [
            [InlineKeyboardButton("🎁 فخ عجلة الحظ والجوائز (Phishing)", callback_data="gen_u4_wheel")],
            [InlineKeyboardButton("🚨 فخ إنذار الفيروسات والتخويف", callback_data="gen_u4_scare")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            "⚠️ *الوحدة الرابعة: الابتزاز والهندسة الاجتماعية*\nاختر التجربة المراد توليد رابطها:",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data == "u5_menu":
        kb = [
            [InlineKeyboardButton("📍 كشف الموقع الجغرافي دقيقاً (GPS)", callback_data="gen_u5_gps")],
            [InlineKeyboardButton("🧪 فحص الأذونات الشامل (All-in-One)", callback_data="gen_u5_full")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            "🛡️ *الوحدة الخامسة: التأمين والحماية*\nاختر التجربة المراد توليد رابطها:",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data == "main_menu":
        # reuse start to render menu
        # note: start expects Update with callback_query or message; we have query so pass update
        await start(update, context)
        return

    # --- generate links ---
    if data.startswith("gen_"):
        mode = data.replace("gen_", "")
        generated_link = f"{GITHUB_BASE_URL.rstrip('/')}/index.html?mode={mode}"

        reply_msg = (
            f"🔗 *الرابط الجاهز للإرسال للطلاب:*\n`{generated_link}`\n\n"
            "💡 انسخ الرابط وأرسله في مجموعة الفصل. عند فتح الرابط على جهاز الطالب، سيُجرى الاختبار/التجربة المحددة.\n\n"
            "⚠️ ملاحظة أمان: تأكد أن الروابط تُستخدم لأغراض تعليمية وأخلاقية داخل إطار التجربة."
        )
        kb = [[InlineKeyboardButton("⬅️ العودة للقوائم", callback_data="main_menu")]]
        await query.edit_message_text(reply_msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
        return

    # Fallback
    await query.edit_message_text("خيارات غير معروفة. 👀 الرجاء العودة للقائمة.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة", callback_data="main_menu")]]))


# --- Build application and add handlers ---
def build_app():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    return application


# --- Entrypoint ---
def main():
    application = build_app()

    # If RENDER_EXTERNAL_URL is provided, try to run webhook mode and register webhook.
    port = int(os.environ.get("PORT", "8443"))

    if RENDER_EXTERNAL_URL:
        # Use a path that includes token to avoid guessing
        webhook_path = f"/webhook/{BOT_TOKEN}"
        webhook_url = f"{RENDER_EXTERNAL_URL.rstrip('/')}{webhook_path}"
        logger.info("Starting in webhook mode. Registering webhook at: %s", webhook_url)

        # run_webhook will start an aiohttp server listening on the given port and path
        # This will block.
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_path=webhook_path,
            webhook_url=webhook_url,
        )
    else:
        # Fallback: polling mode (useful for Render background worker)
        logger.info("RENDER_EXTERNAL_URL not set. Starting in polling mode.")
        application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Bot crashed: %s", e)
        raise
