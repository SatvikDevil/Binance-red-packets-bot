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

# Start web server
keep_alive()
logger.info("⚙️ Starting bot setup...")

# Load env vars
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
target_channel = os.getenv("TARGET_CHANNEL")

logger.info(f"✅ Env Loaded: API_ID={api_id}, Phone={phone_number}, Channel={target_channel}")

# Channels to watch
source_channels = [
    "BinanceRedPacket_Hub", "thxbox", "redpackcs", "binancewordo",
    "binancecodez", "BOXS_BD", "binanceredpacketcodes17", "binanceredpacketcoddes",
    "RMCryptoEarn", "jidaocaijing", "red_packet_king", "redboxyt1",
    "CMXboxes", "MoonCrypto001", "WebKingBox", "mousecrypto2",
    "DailyEarn00007", "techearncrypto29", "BTC_Boxes5374"
]

# Regex (stricter: only uppercase + digit + 8-12 length)
code_regex = re.compile(r'\b(?=\w*[A-Z])(?=\w*\d)\w{8,12}\b')
url_regex = re.compile(r'(https:\/\/(?:www\.)?binance\.com\/en\/red-packet\/claim\?code=\w+|https:\/\/app\.binance\.com\/uni-qr\/cart\/\w+)', re.IGNORECASE)

# Cache to prevent repeats
sent_cache = set()

# Common spammy words
common_words = {"binance", "packet", "crypto", "provided", "redpackethub", "ready"}

# Bot main
async def main():
    client = TelegramClient("session", api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        logger.warning("Not authorized. Sending code...")
        await client.send_code_request(phone_number)
        code = input("📨 Enter login code: ")
        await client.sign_in(phone_number, code)

    logger.info("✅ Client started and authorized.")

    @client.on(events.NewMessage(chats=source_channels))
    async def handler(event):
        message = event.raw_text
        logger.info(f"🔔 New message from {event.chat.username if event.chat else 'Unknown'}")

        codes = [
            code for code in code_regex.findall(message)
            if code.lower() not in common_words and code not in sent_cache
        ]

        urls = url_regex.findall(message)
        matches = {"codes": codes, "urls": urls}
        logger.info(f"🎯 Matches: {matches}")

        posted = False
        try:
            channel_entity = await client.get_entity(target_channel)

            for code in codes:
                msg = f"🧧 Red Packet Code: `{code}`\n⏰ Claim FAST!"
                await client.send_message(channel_entity, msg)
                sent_cache.add(code)
                posted = True

            for url in urls:
                msg = f"🎁 Claim Link:\n{url}"
                await client.send_message(channel_entity, msg)
                posted = True

            if posted:
                logger.info("[+] Red packet sent to target channel.")
            else:
                logger.info("❌ No matching red packet content to send.")
        except Exception as e:
            logger.error(f"❌ Failed to send: {e}")

    await client.run_until_disconnected()

# Run the bot
asyncio.run(main())