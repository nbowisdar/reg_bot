import logging
from multiprocessing import Process
import argparse

from aiogram import Bot
from aiohttp import web

from run_userbot import userbot_app, run_userbot
from setup import bot, dp, HOST_URL, prod
from src.database.tables import create_tables
from src.flask_app.check_incoming_messages import checking_and_save_messages
from src.flask_app.main import app
from src.telegram.handlers.admin_handlers import admin_router
from src.telegram.handlers.todo import todo_router, reminding
from src.telegram.handlers.userbot import userbot_router
import asyncio
from loguru import logger
from src.telegram.middleware.admin_only import IsAdmin
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
logger.add("errors.log", format="{time} {level} {message}", level="ERROR")


from loguru import logger
import logging

logger_pw = logging.getLogger('peewee')
file_handler = logging.FileHandler('peewee.log')
logger_pw.addHandler(file_handler)
logger_pw.setLevel(logging.DEBUG)


async def _start():
    admin_router.message.middleware(IsAdmin())
    todo_router.message.middleware(IsAdmin())
    userbot_router.message.middleware(IsAdmin())
    dp.include_router(admin_router)
    dp.include_router(userbot_router)
    dp.include_router(todo_router)
    asyncio.get_event_loop().create_task(reminding())
    await dp.start_polling(bot, skip_updates=True)


def start_simple():
    logger.info("Telegram bot started")
    asyncio.run(_start())



async def on_startup(bot: Bot, base_url: str):
    await bot.set_webhook(f"{base_url}")


async def on_shutdown(bot: Bot, base_url: str):
    await bot.delete_webhook()


def start_webhook():
    dp["base_url"] = HOST_URL
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(admin_router)
    dp.message.middleware(IsAdmin())

    app = web.Application()
    app["bot"] = bot
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path='')
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="207.154.234.52", port=8080)


def run_flask():
    logger.info("web aplication started")
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    # run_userbot()
    # if not prod:
    logger.info("Run on DEV variant")
    if not prod:
        start_simple()
    try:
        logger.info("Run on PROD variant")
        pars_emails_proc = Process(target=checking_and_save_messages, args=(17,))
        pars_emails_proc.start()

        # to run tg bot wi need to use flag --with_tg
        parser = argparse.ArgumentParser()
        parser.add_argument("--with_tg", '-tg', action="store_true")
        args = parser.parse_args()
        if args.with_tg:
            start_simple()   # run without webhook
        #start_webhook()  # run tg bot

    except KeyboardInterrupt:
        logger.info("Bot stopped by admin")
