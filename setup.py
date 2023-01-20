from aiogram import Dispatcher, Bot, Router
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")
MAILSLURP_KEY = os.getenv("MAILSLURP_KEY")
SMS_TOKEN = os.getenv("SMS_TOKEN")


allowed_servieces = ['go']
admins_id = [286365412, 1137700340, 5459347964]
ngrok_url = "https://6e3f-178-150-202-198.eu.ngrok.io"


bot = Bot(TOKEN)
dp = Dispatcher()

# create routes

admin_router = Router()
# admin_router.message.middleware(IsAdmin())
# user_router = Router()
# common_router = Router()

ROOT_DIR = Path(__file__).parent





