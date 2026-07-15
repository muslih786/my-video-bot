import telebot
import yt_dlp
import os
from flask import Flask
import threading
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Alive!"
@bot.message_handler(func=lambda m: True)
def handle(m):
    if "instagram.com" in m.text:
        msg = bot.reply_to(m, "در حال دانلود...")
        try:
            ydl_opts = {'outtmpl': '%(id)s.%(ext)s', 'format': 'mp4'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(m.text, download=True)
                filename = ydl.prepare_filename(info)
            with open(filename, 'rb') as f:
                bot.send_video(m.chat.id, f)
            os.remove(filename)
        except Exception as e:
            bot.reply_to(m, f"خطا: {e}")
    else:
        bot.reply_to(m, "لینک ریلز بفرست")
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
