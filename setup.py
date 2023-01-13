from aiogram import Dispatcher, Bot, Router
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv()
TOKEN = os.getenv("TOKEN")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
MAILSLURP_KEY = os.getenv("MAILSLURP_KEY")


bot = Bot(TOKEN)
dp = Dispatcher()

# create routes

admin_router = Router()
user_router = Router()
# common_router = Router()

ROOT_DIR = Path(__file__).parent



