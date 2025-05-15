import logging
import asyncio
import nest_asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, ContextTypes
)
from data import data
from keep_alive import keep_alive

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in data.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! یکی از چهارده معصوم را انتخاب کن:", reply_markup=reply_markup)

# نمایش دسته‌بندی‌ها
async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    name = query.data
    context.user_data["selected"] = name

    keyboard = [[InlineKeyboardButton(key, callback_data=f"info|{key}")] for key in data[name].keys()]
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(f"🔍 {name} - یکی از دسته‌ها را انتخاب کن:", reply_markup=reply_markup)

# نمایش اطلاعات دسته
async def show_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        _, key = query.data.split("|")
        name = context.user_data.get("selected")

        if not name or name not in data:
            await query.edit_message_text("❌ مشکلی پیش آمده. لطفاً دوباره /start را بزنید.")
            return

        content = data[name][key]

        if len(content) > 4000:
            content = content[:3990] + "\n\n[...] ادامه مطلب زیاد است."

        keyboard = [
            [InlineKeyboardButton("🔙 بازگشت", callback_data=name)],
            [InlineKeyboardButton("🔝 بازگشت به منوی اصلی", callback_data="back_to_main")]
        ]

        await query.edit_message_text(f"📌 {key} از {name}:\n\n{content}", reply_markup=InlineKeyboardMarkup(keyboard))

    except Exception as e:
        logging.error(f"❌ خطا در show_detail: {e}")
        await query.edit_message_text("⚠️ مشکلی در نمایش اطلاعات پیش آمد. لطفاً دوباره تلاش کنید.")

# بازگشت به منوی اصلی
async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in data.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("🔙 بازگشت به لیست معصومین:", reply_markup=reply_markup)

# اجرای ربات
async def main():
    TOKEN = "7518724231:AAFYFJfS15QoG7RCslSywqRHOLCRXaAm534"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_categories, pattern="^(?!info\\||back_to_main).+"))
    app.add_handler(CallbackQueryHandler(show_detail, pattern="^info\\|"))
    app.add_handler(CallbackQueryHandler(go_back, pattern="^back_to_main$"))

    logging.info("✅ ربات تلگرام با موفقیت اجرا شد.")
    await app.run_polling()

# راه‌اندازی نهایی
if __name__ == "__main__":
    keep_alive()  # فعال نگه داشتن ربات در render با پینگ مداوم
    nest_asyncio.apply()
    asyncio.run(main())
