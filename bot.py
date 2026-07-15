import os
import re
import instaloader
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

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
    await update.message.reply_text("سلام! لینک پست، ریلز یا استوری اینستاگرام را بفرست تا دانلود کنم 📥")

async def download_insta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com" not in url:
        await update.message.reply_text("لطفا یک لینک معتبر اینستاگرام بفرست 🙏")
        return

    msg = await update.message.reply_text("⏳ در حال دانلود...")

    try:
        m = re.search(r"/(p|reel|tv)/([^/]+)/", url)
        if not m:
            await msg.edit_text("❌ لینک را درست نفهمیدم.")
            return
        
        shortcode = m.group(2)
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        if post.is_video:
            await update.message.reply_video(video=post.video_url, caption=post.caption[:500] if post.caption else "")
            await msg.delete()
        else:
            await msg.edit_text("این پست عکس است، ویدیو ندارد.")

    except Exception as e:
        print(f"Error: {e}")
        await msg.edit_text(f"❌ دانلود نشد. شاید پیج پرایویت است.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_insta))

print("Bot is running...")
app.run_polling()
