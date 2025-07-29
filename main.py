from keep_alive import keep_alive
from telethon import TelegramClient, events
import re, os, asyncio, logging
from dotenv import load_dotenv

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Start keep-alive server
keep_alive()
logger.info("⚙️ Starting bot setup...")

# Load environment variables
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
target_channel = os.getenv("TARGET_CHANNEL")  # Example: @binanceredpackethustle

logger.info(f"✅ Env Loaded: API_ID={api_id}, Phone={phone_number}, Channel={target_channel}")

# List of source channels
source_channels = [
    "BinanceRedPacket_Hub", "thxbox", "redpackcs", "binancewordo",
    "binancecodez", "BOXS_BD", "binanceredpacketcodes17", "binanceredpacketcoddes",
    "RMCryptoEarn", "jidaocaijing", "red_packet_king", "redboxyt1",
    "CMXboxes", "MoonCrypto001", "WebKingBox", "mousecrypto2",
    "DailyEarn00007", "techearncrypto29", "BTC_Boxes5374"
]

# Regex patterns
code_regex = re.compile(r'(?:code|Code|CODE)[^\w]*(\w{5,})')
url_regex = re.compile(r'(https:\/\/(?:www\.)?binance\.com\/en\/red-packet\/claim\?code=\w+|https:\/\/app\.binance\.com\/uni-qr\/\w+)', re.IGNORECASE)

async def main():
    client = TelegramClient("session", api_id, api_hash)
    await client.start(phone=phone_number)

    logger.info("✅ Client started and authorized.")

    @client.on(events.NewMessage(chats=source_channels))
    async def handler(event):
        message = event.raw_text
        logger.info(f"🔔 New message from {event.chat.title or event.chat.username}")
        matches = {
            "codes": code_regex.findall(message),
            "urls": url_regex.findall(message),
        }

        logger.info(f"🎯 Matches: {matches}")
        posted = False

        try:
            # Fetch channel entity from username or ID
            channel = await client.get_entity(target_channel)

            # Post codes
            for code in matches["codes"]:
                msg = f"🧧 Red Packet Code: `{code}`\n⏰ Claim FAST!"
                await client.send_message(channel, msg)
                logger.info(f"✅ Sent Code: {code}")
                posted = True

            # Post URLs
            for url in matches["urls"]:
                msg = f"🎁 Claim Link:\n{url}"
                await client.send_message(channel, msg)
                logger.info(f"✅ Sent URL: {url}")
                posted = True

            if not posted:
                logger.info("❌ No matching red packet content to send.")

        except Exception as e:
            logger.error(f"❌ Error sending to target channel: {e}")

    await client.run_until_disconnected()

asyncio.run(main())