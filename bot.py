import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]

WELCOME_MESSAGE = (
    "😎 Yo bro sup 😎\n\n"
    "Goldhunter Paul here 🦁.\n\n"
    "Welcome! If you're serious about joining my VIP trading community, "
    "you're in the right place.\n\n"
    "⚠️ Only 5 spots left. Be quick!\n\n"
    "How to join:\n"
    "https://iqcrest.com\n\n"
    "💎 VIP Channel\n"
    "FREE access with a qualifying deposit of $300+\n\n"
    "👑 VIP PLUS\n"
    "Join with a qualifying deposit of $1000+ and unlock exclusive access "
    "to Goldhunter Paul's live-streamed trading course.\n\n"
    "🌐 Register here:\n"
    "https://iqcrest.com\n\n"
    "Already have an account?\n"
    "1. Log in to your broker.\n"
    "2. Make a deposit.\n"
    "3. Make sure all positions are closed.\n\n"
    "📩 Once your account is set up, send me a message so I can activate "
    "your access and guide you further!"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "You can ask me about:\n\n"
        "• Registration\n"
        "• Deposits\n"
        "• VIP\n"
        "• Existing accounts"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "register" in text:
        reply = (
            "To register, visit:\n"
            "https://iqcrest.com\n\n"
            "Create your account, make the required deposit, "
            "then message Goldhunter Paul for activation."
        )

    elif "deposit" in text:
        reply = (
            "Deposit requirements:\n\n"
            "• VIP: $300+\n"
            "• VIP PLUS: $1000+"
        )

    elif "vip" in text:
        reply = (
            "VIP gives you access to our trading community.\n"
            "VIP PLUS includes additional premium training."
        )

    elif "account" in text:
        reply = (
            "If you already have an account, "
            "make your deposit and contact Goldhunter Paul "
            "to activate your VIP access."
        )

    else:
        reply = (
            "I can help with:\n"
            "• Registration\n"
            "• Deposits\n"
            "• VIP\n"
            "• Existing accounts\n\n"
            "Please type your question."
        )

    await update.message.reply_text(reply)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started successfully.")
    app.run_polling()


if __name__ == "__main__":
    main()
