from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os


TOKEN = os.environ["BOT_TOKEN"]


WELCOME_MESSAGE = """
😎 Yo bro sup 😎

Goldhunter Paul here 🦁.

I'm the first trader in the world with a license. I've a lot of experience. If you want to join the VIP .. I send you the link right now. Just follow the steps and I see you there.

⚠️ Only 5 spots left be quick !!

Here's how to join:
https://iqcrest.com

– VIP Channel: FREE access with a deposit of $300+
– VIP PLUS Channel: Join with $1000+ and unlock exclusive access to Goldhunter Paul's live-streamed trading course 🎓📈

🔗 Start with PU Prime here
👉 https://iqcrest.com

Already have an account? Connect to active trades:
1️⃣ Log in to your broker
2️⃣ Make a deposit
3️⃣ Make sure all positions are closed

🚨 Once your account is set up, send me a message right away so I can activate your access and guide you further! 📨
"""

FAQ = {
    "register": "To register, visit https://iqcrest.com and create your trading account. After funding it, send me a message so I can activate your VIP access.",
    "deposit": "VIP requires a deposit of $300+. VIP PLUS requires a deposit of $1000+.",
    "vip": "VIP is FREE with a $300+ deposit. VIP PLUS is available with a $1000+ deposit.",
    "account": "If you already have an account, make a deposit and ensure all positions are closed before contacting us for activation.",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "register" in text:
        await update.message.reply_text(FAQ["register"])
    elif "deposit" in text:
        await update.message.reply_text(FAQ["deposit"])
    elif "vip" in text:
        await update.message.reply_text(FAQ["vip"])
    elif "account" in text:
        await update.message.reply_text(FAQ["account"])
    else:
        await update.message.reply_text(
            "Thanks for your message! 😊\n\n"
            "I can help you with:\n"
            "• Registration\n"
            "• Deposits\n"
            "• VIP access\n"
            "• Existing accounts\n\n"
            "Type your question, or contact Goldhunter Paul for personal assistance."
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
