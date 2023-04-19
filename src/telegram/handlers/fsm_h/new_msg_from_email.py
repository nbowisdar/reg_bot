import asyncio
import time
from datetime import datetime

from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from setup import admin_router
from aiogram import F
from time import perf_counter
from src.database.queries import check_new_email_message, is_email_exists, get_all_email_messages
from src.email.methods import receive_msg_in_new_thread
from src.telegram.buttons.admin_btns import cancel_kb, email_kb, main_kb
from src.telegram.messages.admin_msg import build_email_msg
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_web_app_kb() -> InlineKeyboardMarkup:
    app = WebAppInfo(url="http://127.0.0.1:5000/")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="test", web_app=app)]
        ]
    )


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

    receive_msg_in_new_thread(inbox)
    global is_parsing
    is_parsing = True
    await message.reply("Will be waiting for a new message for 5 minutes...",
                        reply_markup=build_web_app_kb())
                        # reply_markup=cancel_kb)
    start = perf_counter()

    all_msgs = get_all_email_messages(inbox)
    while is_parsing:
        await asyncio.sleep(1)
        new_msg = check_new_email_message(inbox, len(all_msgs))
        if new_msg:
            send_msg = build_email_msg(new_msg)
            await message.answer(send_msg,
                                 reply_markup=email_kb)
            await state.clear()
            is_parsing = False
            return
        if perf_counter() - start > 360:
            is_parsing = False
            await message.answer("Got nothing, time is over",
                                 reply_markup=email_kb)



