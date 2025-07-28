# main.py

from keep_alive import keep_alive
from telethon import TelegramClient, events
import re
import os
import asyncio
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

keep_alive()
logger.info("⚙️ Starting bot setup...")

load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
target_channel = os.getenv("TARGET_CHANNEL")

logger.info(f"✅ Env Loaded: API_ID={api_id}, Phone={phone_number}, Channel={target_channel}")

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

code_regex = re.compile(r'(?:code|Code|CODE)[^\w]*(\w{5,})')
url_regex = re.compile(r'(https:\/\/(?:www\.)?binance\.com\/en\/red-packet\/claim\?code=\w+|https:\/\/app\.binance\.com\/uni-qr\/cart\/\w+)', re.IGNORECASE)

async def main():
    client = TelegramClient("session", api_id, api_hash)

    @client.on(events.NewMessage(chats=source_channels))
    async def handler(event):
        message = event.raw_text
        logger.info(f"🔔 New message from {event.chat.username or event.chat_id}")
        matches = {
            "codes": code_regex.findall(message),
            "urls": url_regex.findall(message),
        }

        posted = False
        try:
            channel_entity = await client.get_entity(target_channel)

            for code in matches["codes"]:
                msg = f"🧧 Red Packet Code: `{code}`\n⏰ Claim FAST!"
                await client.send_message(channel_entity, msg)
                posted = True

            for url in matches["urls"]:
                msg = f"🎁 Claim Link:\n{url}"
                await client.send_message(channel_entity, msg)
                posted = True

            if posted:
                logger.info("[+] Red packet sent to target channel.")
        except Exception as e:
            logger.error(f"❌ Failed to send: {e}")

    await client.start(phone=phone_number)
    logger.info("✅ Client started and authorized.")

    # ⏳ KEEP IT ALIVE!
    while True:
        await asyncio.sleep(100)

asyncio.run(main())
