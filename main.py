from keep_alive import keep_alive
keep_alive()

import os
import re
from dotenv import load_dotenv
from telethon import TelegramClient, events

print("⚙️ Starting bot setup...")

load_dotenv()

api_id = int(os.getenv("API_ID", -1))
api_hash = os.getenv("API_HASH")
target_channel = os.getenv("TARGET_CHANNEL")

# Must match your session file name (uploaded)
client = TelegramClient("session", api_id, api_hash)

# Red Packet Channels
source_channels = [
    "BinanceRedPacket_Hub", "thxbox", "redpackcs", "binancewordo",
    "binancecodez", "BOXS_BD", "binanceredpacketcodes17",
    "binanceredpacketcoddes", "RMCryptoEarn", "jidaocaijing",
    "red_packet_king", "redboxyt1", "CMXboxes", "MoonCrypto001",
    "WebKingBox", "mousecrypto2", "DailyEarn00007", "techearncrypto29",
    "BTC_Boxes5374"
]

code_regex = re.compile(r'(?:code|Code|CODE)[^\w]*(\w{5,})')
url_regex = re.compile(
    r'(https:\/\/(?:www\.)?binance\.com\/en\/red-packet\/claim\?code=\w+|https:\/\/app\.binance\.com\/uni-qr\/cart\/\d+)',
    re.IGNORECASE
)

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    message = event.raw_text
    codes = code_regex.findall(message)
    urls = url_regex.findall(message)
    posted = False

    if codes:
        for code in codes:
            await client.send_message(target_channel, f"🧧 Red Packet Code: `{code}`\n⏰ Claim FAST!")
            posted = True

    if urls:
        for url in urls:
            await client.send_message(target_channel, f"🎁 Claim Link:\n{url}")
            posted = True

    if posted:
        print("[+] Red packet posted.")

async def main():
    await client.start()
    print("🚀 Bot connected and monitoring channels...")
    await client.run_until_disconnected()

# Connect using saved session (NO INPUT REQUIRED)
client.connect()
if not client.is_user_authorized():
    print("❌ ERROR: Session not authorized. Run this bot locally once to login and save session.")
else:
    import asyncio
    asyncio.run(maim())
from keep_alive import keep_alive
keep_alive()

import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
import re

print("⚙️ Starting bot setup...")

# Load .env variables
load_dotenv()
api_id = int(os.getenv("API_ID", -1))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
target_channel = os.getenv("TARGET_CHANNEL")

print(f"✅ Env Loaded: API_ID={api_id}, Phone={phone_number}, Channel={target_channel}")

# Define source channels to monitor
source_channels = [
    "BinanceRedPacket_Hub", "thxbox", "redpackcs", "binancewordo",
    "binancecodez", "BOXS_BD", "binanceredpacketcodes17",
    "binanceredpacketcoddes", "RMCryptoEarn", "jidaocaijing",
    "red_packet_king", "redboxyt1", "CMXboxes", "MoonCrypto001",
    "WebKingBox", "mousecrypto2", "DailyEarn00007", "techearncrypto29",
    "BTC_Boxes5374"
]

# Regular Expressions
code_regex = re.compile(r'(?:code|Code|CODE)[^\w]*(\w{5,})')
url_regex = re.compile(
    r'(https:\/\/(?:www\.)?binance\.com\/en\/red-packet\/claim\?code=\w+|https:\/\/app\.binance\.com\/uni-qr\/cart\/\d+)',
    re.IGNORECASE)

# Initialize Telegram Client
client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    message = event.raw_text
    codes = code_regex.findall(message)
    urls = url_regex.findall(message)
    posted = False

    if codes:
        for code in codes:
            msg = f"🧧 Red Packet Code: `{code}`\n⏰ Claim FAST!"
            await client.send_message(target_channel, msg)
            posted = True

    if urls:
        for url in urls:
            msg = f"🎁 Claim Link:\n{url}"
            await client.send_message(target_channel, msg)
            posted = True

    if posted:
        print("[+] Red Packet Posted.")

# Start the bot
print("🚀 Bot is starting...")
client.start(phone=phone_number)
print("👀 Bot is watching red packet channels...")
client.run_until_disconnected()
