import os
import re
import threading
from flask import Flask
import instaloader
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

# برای اینکه Render خاموش نکند
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=True,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    compress_json=False
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک ریلز اینستا را بفرست 📥")

async def download_insta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com" not in url:
        return
    msg = await update.message.reply_text("⏳ در حال دانلود...")
    try:
        m = re.search(r"/(p|reel|tv)/([^/]+)/", url)
        if not m:
            await msg.edit_text("❌ لینک درست نیست")
            return
        shortcode = m.group(2)
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        if post.is_video:
            await update.message.reply_video(video=post.video_url, caption=post.caption[:300] if post.caption else "")
            await msg.delete()
        else:
            await msg.edit_text("این پست ویدیو ندارد، عکس است.")
    except Exception as e:
        print(e)
        await msg.edit_text("❌ نشد، پیج پرایویت است یا لینک خراب است.")

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_insta))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
