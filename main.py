import os
import subprocess
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = '8533150180:AAGvKHO3pF4VrElFCrnGDbZjK8Ny00SFe1o'

async def download_song(query: str) -> str:
    output_template = f"{query}.%(ext)s"
    command = [
        "yt-dlp",
        f"ytsearch1:{query}",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",  # best quality (320kbps)
        "-o", output_template
    ]
    subprocess.run(command)
    filename = f"{query}.mp3"
    return filename if os.path.exists(filename) else None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"Downloading '{query}' in 320kbps MP3...")
    filename = await download_song(query)
    if filename:
        await update.message.reply_audio(audio=open(filename, 'rb'))
        os.remove(filename)
    else:
        await update.message.reply_text("Sorry, I couldn't find or download that song.")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()