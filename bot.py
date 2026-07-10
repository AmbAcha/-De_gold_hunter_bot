import os
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"].strip()

bot = Bot(TOKEN)

print("Bot initialized successfully!")
