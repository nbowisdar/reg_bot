from aiogram.types import Message

from aiogram import Dispatcher, Bot, Router, F
from dotenv import load_dotenv
import os
from pathlib import Path

from src.telegram.buttons.admin_btns import main_kb
from src.telegram.buttons.user_btn import user_main_kb

load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")
SMS_TOKEN = os.getenv("SMS_TOKEN")
domain = os.getenv("DOMAIN")

admins_id = [286365412, 1137700340, 5459347964, 1715541795, 5501113966]
support_id = 5501113966
# chat_id = "-935871430"
# support_id = 286365412
HOST_URL = ""

bot = Bot(TOKEN)
dp = Dispatcher()


# @dp.message((F.text == "Go back") | (F.text == "/start"))
# async def main (message: Message):
#     if message.from_user.id == chat_id:
#         await message.answer("Howdy cowboy 🤠", reply_markup=user_main_kb)
#     else:
#         await message.answer("Main page", reply_markup=main_kb)

# create routes

admin_router = Router()
# user_router = Router()
# common_router = Router()

ROOT_DIR = Path(__file__).parent

TEMP_PASSWORD = "adiowauhawd31232djaiwdaADA@@adab"