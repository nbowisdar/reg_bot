from multiprocessing import Process
import argparse

from aiogram import Bot
from aiohttp import web
from setup import bot, dp, HOST_URL
from src.database.tables import create_tables
from src.flask_app.check_incoming_messages import checking_and_save_messages
from src.flask_app.main import app
from src.telegram.handlers.admin_handlers import admin_router
import asyncio
from loguru import logger
from src.telegram.middleware import IsAdmin
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
logger.add("errors.log", format="{time} {level} {message}", level="ERROR")


async def _start():
    dp.include_router(admin_router)
    dp.message.middleware(IsAdmin())
    #dp.include_router(user_router)
    await dp.start_polling(bot)


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
    try:
        flask_proc = Process(target=run_flask)
        pars_emails_proc = Process(target=checking_and_save_messages, args=(17,))
        flask_proc.start()
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
