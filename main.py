# main.py

from keep_alive import keep_alive
from telethon import TelegramClient, events
import re
import os
import asyncio
from dotenv import load_dotenv

# Start web server to keep bot alive
keep_alive()

print("⚙️ Starting bot setup...")

# Load environment variables
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
target_channel = os.getenv("TARGET_CHANNEL")

print(f"✅ Env Loaded: API_ID={api_id}, Phone={phone_number}, Channel={target_channel}")

# Source channels to monitor
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

# Regex
code_regex = re.compile(r'(?:code|Code|CODE)[^\w]*(\w{5,})')
url_regex = re.compile(r'(https:\/\/(?:www\.)?binance\.com\/en\/red-packet\/claim\?code=\w+|https:\/\/app\.binance\.com\/uni-qr\/cart\/\d+)', re.IGNORECASE)

# Define async function
async def main():
    client = TelegramClient("session", api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        code = input("📨 Enter the login code you received: ")
        await client.sign_in(phone_number, code)
    
    print("👀 Bot is watching red packet channels...")

    @client.on(events.NewMessage(chats=source_channels))
    async def handler(event):
        message = event.raw_text

        matches = {
            "codes": code_regex.findall(message),
            "urls": url_regex.findall(message),
        }

        posted = False

        if matches["codes"]:
            for code in matches["codes"]:
                msg = f"""🧧 Red Packet Code: `{code}`  
⏰ Claim FAST!"""
                await client.send_message(target_channel, msg)
                posted = True

        if matches["urls"]:
            for url in matches["urls"]:
                msg = f"""🎁 Claim Link:  
{url}"""
                await client.send_message(target_channel, msg)
                posted = True

        if posted:
            print("[+] Red packet posted.")

    await client.run_until_disconnected()

# Run the bot
asyncio.run(main())
