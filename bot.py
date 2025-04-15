import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from data import data
from keep_alive import keep_alive

import nest_asyncio
import asyncio

logging.basicConfig(level=logging.INFO)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in data.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! یکی از چهارده معصوم را انتخاب کن:", reply_markup=reply_markup)

# انتخاب معصوم و نمایش دسته‌بندی اطلاعات
async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    name = query.data
    context.user_data["selected"] = name
    keyboard = [[InlineKeyboardButton(key, callback_data=f"info|{key}")] for key in data[name].keys()]
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"🔍 {name} - یکی از دسته‌ها را انتخاب کن:", reply_markup=reply_markup)

# نمایش اطلاعات هر دسته
async def show_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, key = query.data.split("|")
    name = context.user_data.get("selected")
    content = data[name][key]
    if len(content) > 4000:
        content = content[:3990] + "\n\n[...] ادامه مطلب زیاد است."
    keyboard = [
        [InlineKeyboardButton("🔙 بازگشت", callback_data=name)],
        [InlineKeyboardButton("🔝 بازگشت به منوی اصلی", callback_data="back_to_main")]
    ]
    await query.edit_message_text(f"📌 {key} از {name}:\n\n{content}", reply_markup=InlineKeyboardMarkup(keyboard))

# بازگشت به لیست معصومین
async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in data.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("🔙 بازگشت به لیست معصومین:", reply_markup=reply_markup)

# اجرای ربات
async def main():
    TOKEN = "7659733690:AAFqmjsngQPqIUg72Bmm8iH5OO6F6s6NMSc"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_categories, pattern="^(?!info\\||back_to_main).+"))
    app.add_handler(CallbackQueryHandler(show_detail, pattern="^info\\|"))
    app.add_handler(CallbackQueryHandler(go_back, pattern="^back_to_main$"))

    logging.info("✅ ربات تلگرام با موفقیت اجرا شد.")
    await app.run_polling()

# اجرای نهایی
if __name__ == "__main__":
    keep_alive()
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
