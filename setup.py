from aiogram import Dispatcher, Bot, Router, F
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")
SMS_TOKEN = os.getenv("SMS_TOKEN")
domain = os.getenv("DOMAIN")

admins_id = [286365412, 1954476972, 1137700340, 5459347964, 1715541795, 5501113966, 1215997618]
support_id = 5501113966

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

site_url = "http://134.209.127.175/"

HOST_URL = ""

check_ready_uber = True

bot = Bot(TOKEN, parse_mode="MARKDOWN")
dp = Dispatcher()



admin_router = Router()


ROOT_DIR = Path(__file__).parent

TEMP_PASSWORD = "adiowauhawd31232djaiwdaADA@@adab"