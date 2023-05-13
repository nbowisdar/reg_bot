import time
from multiprocessing import Process
import argparse

from aiogram import Bot

from src.flask_app.check_incoming_messages import checking_and_save_messages

from loguru import logger

logger.add("errors.log", format="{time} {level} {message}", level="ERROR")



async def on_startup(bot: Bot, base_url: str):
    await bot.set_webhook(f"{base_url}")


async def on_shutdown(bot: Bot, base_url: str):
    await bot.delete_webhook()


#
# def run_program():
#     if not prod:
#         return
#         # start_simple()
#     try:
#         # to run tg bot wi need to use flag --with_tg
#         parser = argparse.ArgumentParser()
#         parser.add_argument("--with_tg", '-tg', action="store_true")
#         args = parser.parse_args()
#         # if args.with_tg:
#         #     while True:
#         #         try:
#         #             start_simple()  # run without webhook
#         #         except Exception as err:
#         #             logger.error(err)
#         #             logger.debug("Reload server!")
#         #             start_simple()
#
#     except KeyboardInterrupt:
#         logger.info("Bot stopped by admin")
#
#
# def counter(c=360, start=0):
#     while start < c:
#         start += 1
#         time.sleep(1)
#         print('live')
#
#
# def run_prod():
#     count_proc = Process(target=counter)
#     main_proc = Process(target=run_program)
#     count_proc.start()
#     main_proc.start()
#     pars_emails_proc = Process(target=checking_and_save_messages, args=(17,))
#     pars_emails_proc.start()
#     while True:
#         if not count_proc.is_alive() or not main_proc.is_alive() or not pars_emails_proc.is_alive():
#             logger.debug("restarting!")
#
#             main_proc.terminate()
#             pars_emails_proc.terminate()
#             count_proc.terminate()
#
#             pars_emails_proc = Process(target=checking_and_save_messages, args=(17,))
#             main_proc = Process(target=run_program)
#             count_proc = Process(target=counter)
#
#             count_proc.start()
#             main_proc.start()
#             pars_emails_proc.start()
#         time.sleep(10)


if __name__ == '__main__':
    checking_and_save_messages()


