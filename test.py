import asyncio
from concurrent.futures import ProcessPoolExecutor
from pprint import pprint

from run import start_simple
from setup import bot
from src.database.tables import Email, Template
from src.telegram.handlers.admin_handlers import inboxer

if __name__ == '__main__':
    x = Template.select()[0]
    print(x.delete_instance())
