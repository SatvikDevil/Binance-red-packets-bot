# main.py

from keep_alive import keep_alive
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
import re
import os
import asyncio
from dotenv import load_dotenv
import logging

# Keep-alive ping server
keep_alive()

# Setup logs
logging.basicConfig(level=logging.INFO)
print("⚙️ Starting bot setup...")

# Load .env config
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
target_channel = os.getenv("TARGET_CHANNEL")

print(f"✅ Env Loaded: API_ID={api_id}, Phone={phone_number}, Channel={target_channel}")

# List of source channels
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
url_regex = re.compile(r'(https:\/\/(?:www\.)?binance\.com\/en\/red-packet\/claim\?code=\w+|https:\/\/app\.binance\.com\/uni-qr\/cart\/\d+)', re.IGNORECASE)

async def main():
    client = TelegramClient("session", api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        code = input("📨 Enter the login code you received: ")
        await client.sign_in(phone_number, code)

    # Auto join all red packet channels
    for channel in source_channels:
        try:
            await client(JoinChannelRequest(channel))
            logging.info(f"✅ Joined channel: {channel}")
        except Exception as e:
            logging.warning(f"❌ Failed to join {channel}: {e}")

    @client.on(events.NewMessage())
    async def handler(event):
        chat = await event.get_chat()
        logging.info(f"🔔 Message from {getattr(chat, 'title', 'Unknown')}: {event.raw_text[:50]}...")

        message = event.raw_text
        matches = {
            "codes": code_regex.findall(message),
            "urls": url_regex.findall(message),
        }

        posted = False

        if matches["codes"]:
            for code in matches["codes"]:
                msg = f"🧧 Red Packet Code: `{code}`\n⏰ Claim FAST!"
                await client.send_message(target_channel, msg)
                posted = True

        if matches["urls"]:
            for url in matches["urls"]:
                msg = f"🎁 Claim Link:\n{url}"
                await client.send_message(target_channel, msg)
                posted = True

        if posted:
            logging.info("[+] Red packet posted to target channel.")

    await client.run_until_disconnected()

# Run the bot
asyncio.run(main())
