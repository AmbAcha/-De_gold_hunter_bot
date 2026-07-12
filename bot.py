import os
import io
import logging
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from google import genai
from google.genai import types

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Load Environment Variables and strip accidental line breaks/spaces
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Retrieve your personal Telegram ID for automatic forwarding
MY_TELEGRAM_ID = os.getenv("MY_TELEGRAM_ID", "").strip()
MY_ID = int(MY_TELEGRAM_ID) if MY_TELEGRAM_ID and MY_TELEGRAM_ID.isdigit() else None

SYSTEM_PROMPT = """
You are "Goldhunter Paul" (🦁), an elite financial market trader and mentor.

Rules:
- Speak confidently and professionally.
- Keep replies concise and mobile-friendly.
- Help users with trading questions honestly.
- Never invent results or guarantees.
- If users send an image or screenshot (like a deposit slip or chart):
  • Review it as Goldhunter Paul.
  • Confirm if it matches requirements.
- If users ask how to join:
  • VIP requires a $300 deposit.
  • VIP PLUS requires a $1,000 deposit.
  • Broker: https://iqcrest.com
  • After funding and closing all open trades, tell them to message you for activation.
"""

if not GEMINI_API_KEY:
    logger.critical("GEMINI_API_KEY environment variable is missing!")
    exit()

# Initialize the Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
😎 Yo bro, sup?

Goldhunter Paul here 🦁

Welcome! If you're serious about taking your trading to the next level, you're in the right place.

⚠️ Only 5 VIP spots left!

🌐 https://iqcrest.com

💎 VIP Channel
✅ Deposit $300+

👑 VIP PLUS
✅ Deposit $1,000+

Includes:
• Live trading course
• Premium content
• 1-on-1 support

Already have an account?

1. Log in
2. Make your deposit
3. Close all open trades

🚨 Then message me immediately so I can activate your VIP access.
"""
    await update.message.reply_text(text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    try:
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING,
        )

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=update.message.text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.6,
            ),
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        logger.exception(e)
        await update.message.reply_text(f"⚠️ Error:\n{e}")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.photo:
        return

    try:
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING,
        )

        # 1. Get highest quality variant photo and its network file object
        photo_size_object = update.message.photo[-1]
        file_id = photo_size_object.file_id
        tg_file = await context.bot.get_file(file_id)

        # 2. Forward seamlessly to your personal account if ID is configured
        if MY_ID:
            sender = update.effective_user.username or update.effective_user.first_name
            user_id = update.effective_user.id
            caption_text = f"📸 Screenshot from @{sender} (ID: {user_id})"
            
            if update.message.caption:
                caption_text += f"\n\n💬 User Message: {update.message.caption}"

            await context.bot.send_photo(
                chat_id=MY_ID,
                photo=file_id,
                caption=caption_text
            )
        else:
            logger.warning("Photo received, but MY_TELEGRAM_ID environment variable is not set up.")

        # 3. Download image into buffer memory
        image_bytes = io.BytesIO()
        await tg_file.download_to_memory(image_bytes)
        image_bytes.seek(0)  # Reset stream pointer back to start

        # 4. Construct input payload
        user_prompt = update.message.caption or "Analyze this screenshot or proof of deposit."
        
        contents_payload = [
            types.Part.from_bytes(
                data=image_bytes.read(),
                mime_type="image/jpeg",
            ),
            user_prompt
        ]

        # 5. Hand off to Gemini
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=contents_payload,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.6,
            ),
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        logger.exception(e)
        await update.message.reply_text(f"⚠️ Error handling screenshot:\n{e}")


def main():
    if not TELEGRAM_TOKEN:
        logger.critical("TELEGRAM_TOKEN environment variable is missing!")
        return

    # Build Telegram Bot application
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Read the custom port Render binds our application to
    port = int(os.environ.get("PORT", 8000))
    
    # Render provides this environment variable automatically on Web Services
    render_url = os.environ.get("RENDER_EXTERNAL_URL", "").strip()

    if render_url:
        logger.info(f"Starting bot using Webhooks on port {port}...")
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TELEGRAM_TOKEN,
            webhook_url=f"{render_url}/{TELEGRAM_TOKEN}"
        )
    else:
        # Fallback to Polling for local development testing
        logger.info("No Render environment found. Starting bot via Polling...")
        app.run_polling()


if __name__ == "__main__":
    main()
