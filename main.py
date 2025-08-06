# main.py

import os
import re
import logging
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from telegram import Update, MessageEntity
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RedPacketBot")

# Flask app to keep alive
app = Flask('')

@app.route('/')
def home():
    return "🤖 I'm alive and scanning!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# Regex patterns
code_regex = re.compile(r'\b[A-Z0-9]{6,}\b')
url_regex = re.compile(r'https:\/\/(?:www\.)?binance\.com\/en\/red-packet\/claim\?code=[\w-]+|https:\/\/app\.binance\.com\/uni-qr\/cart\/[\w-]+', re.IGNORECASE)
blocklist = {'binance', 'packet', 'crypto', 'provided', 'redpackethub', 'ready'}

# Memory for sent codes to avoid duplicates
sent_codes = set()

# Message handler
async def red_packet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text
    codes = code_regex.findall(text)
    urls = url_regex.findall(text)
    hidden_urls = []

    # Extract hidden link buttons
    if message.entities:
        for entity in message.entities:
            if isinstance(entity, MessageEntity) and entity.type == "text_link":
                hidden_urls.append(entity.url)

    sent = False

    for code in codes:
        if code.lower() not in blocklist and code not in sent_codes:
            sent_codes.add(code)
            msg = f"🧧 Red Packet Code: `{code}`\n⏰ Claim FAST!"
            await context.bot.send_message(chat_id=TARGET_CHANNEL, text=msg, parse_mode="Markdown")
            logger.info(f"[+] Sent code: {code}")
            sent = True

    for url in set(urls + hidden_urls):
        await context.bot.send_message(chat_id=TARGET_CHANNEL, text=f"🎁 Claim Link:\n{url}")
        logger.info(f"[+] Sent URL: {url}")
        sent = True

    if not sent:
        logger.info("[-] No valid red packet content found.")

# Start bot
if __name__ == "__main__":
    keep_alive()

    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, red_packet_handler))

    logger.info("✅ Bot is starting...")
    app_bot.run_polling()
