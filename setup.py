from aiogram import Dispatcher, Bot, Router
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")
SMS_TOKEN = os.getenv("SMS_TOKEN")
domain = os.getenv("DOMAIN")

admins_id = [286365412, 1137700340, 5459347964, 1715541795, 5501113966]
chat_id = "-935871430"
HOST_URL = ""

bot = Bot(TOKEN)
dp = Dispatcher()

# create routes

admin_router = Router()
# user_router = Router()
# common_router = Router()

ROOT_DIR = Path(__file__).parent

TEMP_PASSWORD = "adiowauhawd31232djaiwdaADA@@adab"