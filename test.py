import asyncio
from concurrent.futures import ProcessPoolExecutor
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


async def run_process_and_reply_after(message: types.Message, data: StructData):
    logger.info("runner process")

    reddit_link = data.reddit_link
    upvote_int = data.upvote_int

    with ProcessPoolExecutor(max_workers=2) as executor:
        q = await asyncio.get_running_loop().run_in_executor(executor, start_reddit_work, reddit_link, upvote_int)

    if q:
        await message.reply(q)
        return


# async def run_process_and_reply_after(message: types.Message, data: StructData):
#     logger.info("runner process")
#
#     reddit_link = data.reddit_link
#     upvote_int = data.upvote_int
#
#     with ProcessPoolExecutor(max_workers=2) as executor:
#         try:
#             q = await asyncio.wait_for(asyncio.get_running_loop().run_in_executor(executor, start_reddit_work, reddit_link, upvote_int), timeout=180)
#         except asyncio.TimeoutError:
#             logger.info("Timeout occurred. Restarting process...")
#             return await run_process_and_reply_after(message, data) # Рекурсивно перезапускає функцію, якщо вона завершилася через timeout
#
#     if q:
#         await message.reply(q)
#         return