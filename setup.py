from aiogram import Dispatcher, Bot, Router
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
MAILSLURP_KEY = os.getenv("MAILSLURP_KEY")
NGROK_LINK = os.getenv("NGROK_LINK")

admin_id = 286365412

bot = Bot(TOKEN)
dp = Dispatcher()

# create routes

admin_router = Router()
# admin_router.message.middleware(IsAdmin())
# user_router = Router()
# common_router = Router()

ROOT_DIR = Path(__file__).parent





