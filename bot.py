import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai
from google.genai import types

# 1. Enable logging for debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. Retrieve Secret Tokens from Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 3. Define the System Prompt for the AI
SYSTEM_PROMPT = """
You are "Goldhunter Paul" (🦁), an elite financial market trader and mentor running a highly exclusive Telegram trading bot. 
Your primary job is to provide sharp, direct, and valuable responses to user messages while keeping them aligned with your premium trading funnel.

### 1. Persona & Tone
- **Identity:** Goldhunter Paul. High-energy, confident, professional, and brotherly ("Yo bro", "sup"). 
- **Style:** Concise, authoritative, and blunt. Avoid corporate fluff. Use short paragraphs and clear bullet points so messages read quickly on mobile.

### 2. Funnel Alignment & Knowledge base
- **The Core Offer:** You run two exclusive groups via your partner broker:
  1. VIP Channel: Requires a deposit of $300+.
  2. VIP PLUS Channel: Requires a deposit of $1,000+ (includes your live trading course, exclusive premium content, and 1-on-1 support).
- **Broker Link:** Always direct clients looking to register or fund their accounts to: https://iqcrest.com
- **Action Plan:** If users ask how to get started or say they already have an account, remind them of the rules:
  1. Log in or sign up at iqcrest.com
  2. Fund the account ($300+ for VIP, $1,000+ for VIP PLUS).
  3. Ensure all active trading positions are entirely closed.
  4. Message you immediately to get their access activated.

### 3. Handling General Chat & Directions
- **Market/Chat Queries:** Answer questions about gold (XAUUSD), setups, or technical analysis with sharp, high-probability trading wisdom. Be accurate but encourage them that the real inner-circle execution happens in the VIP groups.
- **Directions/Navigation:** If a user randomly asks for physical directions or mapping layout guidance, keep your Goldhunter Paul persona but give them clean, logical, step-by-step navigation cues (A ➔ B ➔ C) using landmarks without breaking character.

### 4. Constraints
- Never lie or fake results. Maintain high credibility.
- If a client is ready to activate, instruct them to drop their account details/deposit proof right here in the chat so you can guide them.
"""

# 4. Initialize the Gemini Client
if GEMINI_API_KEY:
    ai_client = genai.Client(api_key=GEMINI_API_KEY)
else:
    logger.error("GEMINI_API_KEY environment variable is missing!")
    ai_client = None

# 5. Define Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends your exact custom welcome onboarding script when /start is clicked."""
    welcome_text = (
        "😎 Yo bro, sup?\n\n"
        "Goldhunter Paul here 🦁\n\n"
        "Welcome! If you’re serious about taking your trading to the next level, you’re in the right place.\n\n"
        "⚠️ *Only 5 VIP spots left! Don’t miss out.*\n\n"
        "Here’s how to join:\n\n"
        "🌐 https://iqcrest.com\n\n"
        "💎 *VIP Channel*\n"
        "✅ FREE access when you deposit $300+\n\n"
        "👑 *VIP PLUS Channel*\n"
        "✅ Deposit $1,000+ to unlock:\n"
        "• Goldhunter Paul’s live trading course 🎓📈\n"
        "• Exclusive VIP PLUS content\n"
        "• Premium trading support\n\n"
        "Already have an account?\n\n"
        "1️⃣ Log in to your broker.\n"
        "2️⃣ Make a deposit.\n"
        "3️⃣ Make sure all positions are closed.\n\n"
        "🚨 *Once your account is ready, send me a message immediately so I can activate your access and guide you further! 📨*"
    )
    # Using default HTML or clear text handling to preserve your exact spacing and link layout safely.
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes any subsequent user messages ensuring they align with Goldhunter Paul's logic."""
    user_text = update.message.text
    
    if not ai_client:
        await update.message.reply_text("Error: AI client configuration missing on backend.")
        return

    try:
        # Show typing status while processing
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Call Gemini with system prompt instructions
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.6,
            )
        )
        
        await update.message.reply_text(response.text, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Error processing AI message: {e}")
        await update.message.reply_text("Yo bro, ran into a slight network glitch processing that. Send it again!")

# 6. Main Runner
d.    import os  # Make sure this is at the very top of your file

def main() -> None:
    # Fetch the token from Render's environment variables
    telegram_token = os.environ.get('TELEGRAM_TOKEN')

    if not telegram_token:
        logger.critical("TELEGRAM_TOKEN env var is missing!")
        return

    # Pass the fetched token into the builder
    application = Application.builder().token(telegram_token).build()


    # Link the commands and messages
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Goldhunter Paul bot is going live...")
    application.run_polling()

if __name__ == '__main__':
    main()
