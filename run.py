from setup import bot, dp
from src.database.tables import create_tables
from src.sms.flask_app import app, get_flask_thread
from src.telegram.handlers.user_handlers import user_router
from src.telegram.handlers.admin_handlers import admin_router
import asyncio
from loguru import logger


async def _start():
    dp.include_router(admin_router)
    dp.include_router(user_router)
    await dp.start_polling(bot)


def start_bot():
    create_tables()
    logger.info("Telegram bot started")
    asyncio.run(_start())


if __name__ == '__main__':
    try:
        # run flask
        flask_thr = get_flask_thread()
        flask_thr.start()

        start_bot()  # run tg bot
        # app.run(debug=True)
    except KeyboardInterrupt:
        logger.info("Bot stopped by admin")