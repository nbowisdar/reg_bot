from aiogram import Dispatcher, Bot, Router
from dotenv import load_dotenv
import os
from pathlib import Path

from src.email.messages import InboxInfo
from src.models import EmailMessageModel

load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")
SMS_TOKEN = os.getenv("SMS_TOKEN")
domain = os.getenv("DOMAIN")

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

import json


class EmailSaver:
    def __init__(self):
        with open("emails.json", mode='r', encoding="utf-8") as file:
            self.data = json.load(file)
            # self.active = data['active']
            # self.deleted = data['deleted']

    def get_emails(self) -> list[str]:
        return self.data['active']

    def filter_deleted(self, emails: list[InboxInfo]):
        return [email for email in emails if email.inbox not in self.data['deleted']]

    def delete_email(self, inbox: str):
        self.data['deleted'].append(inbox)
        with open("emails.json", mode='w', encoding="utf-8") as file:
            json.dump(self.data, file)

    def add_inbox(self, inbox):
        self.data['active'].append(inbox)
        with open("emails.json", mode='r', encoding="utf-8") as file:
            json.dump(self.data, file)