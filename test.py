import asyncio
from concurrent.futures import ProcessPoolExecutor
from pprint import pprint

from run import start_simple
from setup import bot
from src.database.tables import Email, Template
from src.telegram.handlers.admin_handlers import inboxer



if __name__ == '__main__':
    with open("lyft.html", mode='r', encoding="utf-8") as file:
        data = file.read()
    data = extract_data_from_email(data)
    print(data)