# main.py

from keep_alive import keep_alive
from telethon import TelegramClient, events
from telegram import Bot
from telegram.error import TelegramError
import re
import os
import asyncio
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# 🌐 Keep app alive on Railway
keep_alive()

# ✅ Load environment
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
target_channel = os.getenv("TARGET_CHANNEL")

# ✅ Start Bot
bot = Bot(token=bot_token)

# 🔍 Channels to monitor
source_channels = [
    "BinanceRedPacket_Hub", "thxbox", "redpackcs", "binancewordo", "binancecodez",
    "BOXS_BD", "binanceredpacketcodes17", "binanceredpacketcoddes", "RMCryptoEarn",
    "jidaocaijing", "red_packet_king", "redboxyt1", "CMXboxes", "MoonCrypto001",
    "WebKingBox", "mousecrypto2", "DailyEarn00007", "techearncrypto29", "BTC_Boxes5374"
]

# 🔎 Regex filters
code_regex = re.compile(r'\b([A-Z0-9]{8,})\b')
url_regex = re.compile(r'(https:\/\/(?:www\.)?binance\.com\/en\/red-packet\/claim\?code=\w+|https:\/\/app\.binance\.com\/uni-qr\/cart\/\w+)', re.IGNORECASE)

sent_codes = set()

async def main():
    client = TelegramClient("session", api_id, api_hash)
    await client.start()
    logger.info("✅ Client started and authorized.")

    @client.on(events.NewMessage(chats=source_channels))
    async def handler(event):
        message = event.raw_text
        logger.info(f"📥 New message from {event.chat.username or 'unknown'}")
        
        codes = code_regex.findall(message)
        urls = url_regex.findall(message)

        for code in codes:
            if code.lower() not in sent_codes and code.lower() not in ["binance", "packet", "crypto", "provided", "redpackethub", "ready"]:
                msg = f"🧧 Red Packet Code: `{code}`\n⏰ Claim FAST!"
                try:
                    await bot.send_message(chat_id=target_channel, text=msg, parse_mode="Markdown")
                    sent_codes.add(code.lower())
                    logger.info(f"[+] Sent code: {code}")
                except TelegramError as e:
                    logger.error(f"❌ Failed to send code: {e}")

        for url in urls:
            if url not in sent_codes:
                try:
                    await bot.send_message(chat_id=target_channel, text=f"🎁 Claim Link:\n{url}")
                    sent_codes.add(url)
                    logger.info(f"[+] Sent link: {url}")
                except TelegramError as e:
                    logger.error(f"❌ Failed to send URL: {e}")

    await client.run_until_disconnected()

asyncio.run(main())