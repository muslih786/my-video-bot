import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! یک لینک بفرست تا دانلود کنم.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        return
    await update.message.reply_text("در حال دانلود...")
    try:
        ydl_opts = {'format': 'best[ext=mp4]/best', 'outtmpl': '%(title)s.%(ext)s', 'max_filesize': 50*1024*1024}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        with open(filename, 'rb') as f:
            await update.message.reply_video(video=f, caption=f"{info.get('title','')}")
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"خطا: {str(e)[:300]}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()

if __name__ == "__main__":
    main()
