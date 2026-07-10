import os
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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

SYSTEM_PROMPT = """
You are "Goldhunter Paul" (🦁), an elite financial market trader and mentor.

Rules:
- Speak confidently and professionally.
- Keep replies concise and mobile-friendly.
- Help users with trading questions honestly.
- Never invent results or guarantees.
- If users ask how to join:
  • VIP requires a $300 deposit.
  • VIP PLUS requires a $1,000 deposit.
  • Broker: https://iqcrest.com
  • After funding and closing all open trades, tell them to message you for activation.
"""

if not GEMINI_API_KEY:
    logger.critical("GEMINI_API_KEY environment variable is missing!")
    exit()

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
            model="gemini-2.5-flash",
            contents=update.message.text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.6,
            ),
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        logger.exception(e)
        await update.message.reply_text(
            "⚠️ Sorry bro, something went wrong. Please try again."
        )


def main():
    if not TELEGRAM_TOKEN:
        logger.critical("TELEGRAM_TOKEN environment variable is missing!")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Goldhunter Paul bot started.")
    app.run_polling()


if __name__ == "__main__":
    main()
