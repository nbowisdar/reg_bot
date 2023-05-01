import asyncio
from concurrent.futures import ProcessPoolExecutor
from pprint import pprint

from run import start_simple
from setup import bot
from src.database.tables import Email
from src.telegram.handlers.admin_handlers import inboxer

if __name__ == '__main__':
    for email in Email.select():
        if not email.sex or email.sex == "❓":
            email.sex = "🙎‍♂️"
            email.save()
