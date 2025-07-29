# main.py

from keep_alive import keep_alive
from telethon import TelegramClient, events
import re
import os
import asyncio
from dotenv import load_dotenv
import logging

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Keep alive
keep_alive()
logger.info("⚙️ Starting bot setup...")

# Load .env variables
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
target_channel = os.getenv("TARGET_CHANNEL")

logger.info(f"✅ Env Loaded: API_ID={api_id}, Phone={phone_number}, Channel={target_channel}")

# List of monitored public channels
source_channels = [
    "BinanceRedPacket_Hub",
    "thxbox",
    "redpackcs",
    "binancewordo",
    "binancecodez",
    "BOXS_BD",
    "binanceredpacketcodes17",
    "binanceredpacketcoddes",
    "RMCryptoEarn",
    "jidaocaijing",
    "red_packet_king",
    "redboxyt1",
    "CMXboxes",
    "MoonCrypto001",
    "WebKingBox",
    "mousecrypto2",
    "DailyEarn00007",
    "techearncrypto29",
    "BTC_Boxes5374"
]

# Regex: strict alphanumeric codes (5–12 chars), MUST contain a letter
code_regex = re.compile(r'\b(?=\w*[A-Za-z])\w{5,12}\b')
url_regex = re.compile(r'(https:\/\/(?:www\.)?binance\.com\/en\/red-packet\/claim\?code=\w+|https:\/\/app\.binance\.com\/uni-qr\/cart\/\w+)', re.IGNORECASE)

# Cache to track sent codes/URLs
sent_cache = set()

async def main():
    client = TelegramClient("session", api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        logger.warning("❌ Not authorized. Sending code...")
        await client.send_code_request(phone_number)
        code = input("📨 Enter login code: ")
        await client.sign_in(phone_number, code)

    logger.info("✅ Client started and authorized.")

    @client.on(events.NewMessage(chats=source_channels))
    async def handler(event):
        message = event.raw_text.strip()
        logger.info(f"🔔 New message from {event.chat.title}")

        codes = [code for code in code_regex.findall(message) if code not in sent_cache]
        urls = [url for url in url_regex.findall(message) if url not in sent_cache]

        try:
            channel_entity = await client.get_entity(target_channel)
            sent = 0

            for code in codes:
                msg = f"🧧 Red Packet Code: `{code}`\n⏰ Claim FAST!"
                await client.send_message(channel_entity, msg)
                sent_cache.add(code)
                sent += 1

            for url in urls:
                msg = f"🎁 Claim Link:\n{url}"
                await client.send_message(channel_entity, msg)
                sent_cache.add(url)
                sent += 1

            if sent > 0:
                logger.info(f"[+] ✅ Sent {sent} red packets to {target_channel}")
            else:
                logger.info("❌ No new codes or links to send.")

        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")

    await client.run_until_disconnected()

asyncio.run(main())