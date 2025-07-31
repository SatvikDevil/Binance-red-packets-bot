# main.py

import os
import re
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import logging

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Keep-alive server
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# Regex filters
code_regex = re.compile(r'\b[A-Z0-9]{6,12}\b')
url_regex = re.compile(r'(https:\/\/(?:www\.)?binance\.com\/en\/red-packet\/claim\?code=\w+|https:\/\/app\.binance\.com\/uni-qr\/cart\/\w+)', re.IGNORECASE)
blocklist = ['binance', 'packet', 'crypto', 'provided', 'redpackethub', 'ready']

# Handler
async def red_packet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text or ""
    codes = code_regex.findall(message)
    urls = url_regex.findall(message)
    sent = False

    for code in codes:
        if code.lower() not in [w.lower() for w in blocklist]:
            msg = f"🧧 Red Packet Code: `{code}`\n⏰ Claim FAST!"
            await context.bot.send_message(chat_id=TARGET_CHANNEL, text=msg, parse_mode="Markdown")
            sent = True

    for url in urls:
        msg = f"🎁 Claim Link:\n{url}"
        await context.bot.send_message(chat_id=TARGET_CHANNEL, text=msg)
        sent = True

    if sent:
        logger.info("[+] Sent red packet to channel.")

# MAIN
if __name__ == "__main__":
    keep_alive()

    from telegram.ext import Application

    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, red_packet_handler))

    logger.info("✅ Bot is starting...")
    app_bot.run_polling()