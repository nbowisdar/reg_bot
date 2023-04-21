from aiogram import Dispatcher, Bot, Router
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")
SMS_TOKEN = os.getenv("SMS_TOKEN")


allowed_servieces = ['go']
admins_id = [286365412, 1137700340, 5459347964]
HOST_URL = ""


bot = Bot(TOKEN)
dp = Dispatcher()

# create routes

admin_router = Router()
# user_router = Router()
# common_router = Router()

ROOT_DIR = Path(__file__).parent

TEMP_PASSWORD = "adiowauhawd31232djaiwdaADA@@adab"



