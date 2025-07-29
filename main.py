# main.py

from keep_alive import keep_alive
from telethon import TelegramClient, events
import re
import os
import asyncio
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Keep-alive server
keep_alive()
logger.info("⚙️ Starting bot setup...")

# Load .env variables
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
target_channel = os.getenv("TARGET_CHANNEL")

logger.info(f"✅ Env Loaded: API_ID={api_id}, Phone={phone_number}, Channel={target_channel}")

# Red packet source channels
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

# Updated Regex
code_regex = re.compile(r'\b[A-Z0-9]{5,15}\b')  # Broad match for red packet codes
url_regex = re.compile(r'(https:\/\/(?:www\.)?binance\.com\/en\/red-packet\/claim\?code=\w+|https:\/\/app\.binance\.com\/uni-qr\/cart\/\w+)', re.IGNORECASE)

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
        # Read full message (text, caption, etc.)
        msg_parts = [
            event.message.message or '',
            getattr(event.message, 'text', '') or '',
            getattr(event.message, 'raw_text', '') or '',
            getattr(event.message, 'caption', '') or ''
        ]
        message = '\n'.join([m for m in msg_parts if m])

        logger.info(f"🔔 New message from {event.chat.title}")
        logger.info(f"📩 Content: {message.strip()}")

        matches = {
            "codes": code_regex.findall(message),
            "urls": url_regex.findall(message),
        }

        logger.info(f"🎯 Matches: {matches}")

        count = 0
        try:
            channel_entity = await client.get_entity(target_channel)

            for code in matches["codes"]:
                msg = f"🧧 Red Packet Code: `{code}`\n⏰ Claim FAST!"
                await client.send_message(channel_entity, msg)
                count += 1

            for url in matches["urls"]:
                msg = f"🎁 Claim Link:\n{url}"
                await client.send_message(channel_entity, msg)
                count += 1

            if count > 0:
                logger.info(f"[+] 🔥 {count} red packets posted to {target_channel}")
            else:
                logger.info("❌ No matching red packet content to send.")

        except Exception as e:
            logger.error(f"❌ Failed to send red packet: {e}")

    await client.run_until_disconnected()

# Start bot
asyncio.run(main())