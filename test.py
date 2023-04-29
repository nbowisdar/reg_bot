import asyncio
from pprint import pprint

from run import start_simple
from setup import bot
from src.database.tables import Email
from src.telegram.handlers.admin_handlers import inboxer

# inboxer.add_in_ready("n123ew_test@.com")

async def test():
    await bot.send_message(chat_id="-935871430", text="test")
    # updates = await bot.get_updates()
    # pprint(x)


def clear_emails_danger():
    Email.delete().execute()



if __name__ == '__main__':
    # asyncio.run(test())
    clear_emails_danger()