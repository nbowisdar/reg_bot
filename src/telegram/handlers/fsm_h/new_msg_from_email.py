import asyncio
import time
from datetime import datetime

from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from loguru import logger

from setup import admin_router, site_url
from aiogram import F
from time import perf_counter
from src.database.queries import check_new_email_message, is_email_exists, get_all_email_messages
from src.email.methods import receive_msg_in_new_thread
from src.telegram.buttons.admin_btns import cancel_kb, email_kb, main_kb, build_web_app_kb
from src.telegram.messages.admin_msg import build_email_msg
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.utils.msg_from_email import extract_data_from_email

# from web_app import run_temp_flask, run_flask_in_thread

is_parsing = False


class EmailMsg(StatesGroup):
    email = State()


@admin_router.message(EmailMsg.email)
async def waiting_message(message: Message, state: FSMContext):
    # send new msg
    inbox = message.text
    if not is_email_exists(inbox):
        await message.answer("Wrong email address", reply_markup=email_kb)
        await state.clear()
        return

    # receive_msg_in_new_thread(inbox)
    global is_parsing
    is_parsing = True
    await message.reply("Will be waiting for a new message for 5 minutes...",
                        reply_markup=cancel_kb)
                        # reply_markup=cancel_kb)
    # time_from = datetime.now()
    start = perf_counter()
    # try:
    amount_msg = len(get_all_email_messages(inbox))
    # except AttributeError:
    #     all_msgs = []
    while is_parsing:
        await asyncio.sleep(5)
        new_msg = check_new_email_message(inbox, amount_msg)
        if new_msg:
            if len(new_msg.body) > 50:
                msg = extract_data_from_email(new_msg.body)
                if not msg:
                    url = site_url + "messages"
                    msg = f"Unknown format, please check email on [{url}]"
                await message.answer(msg, reply_markup=email_kb)
                # await message.answer(send_msg, reply_markup=build_web_app_kb())
            else:
                send_msg = build_email_msg(new_msg)
                await message.answer(send_msg, reply_markup=email_kb)
                is_parsing = False

            await state.clear()
            return
        if perf_counter() - start > 360:
            is_parsing = False
            await message.answer("Got nothing, time is over",
                                 reply_markup=email_kb)



