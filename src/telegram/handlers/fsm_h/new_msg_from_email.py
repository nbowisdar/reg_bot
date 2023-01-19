import asyncio
import time
from datetime import datetime

from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from setup import admin_router
from aiogram import F
from time import perf_counter
from src.database.queries import check_new_email_message, is_email_exists, get_all_email_messages, get_email_id_by_name
from src.email.methods import receive_msg_in_new_thread
from src.telegram.buttons.admin_btns import cancel_kb, email_kb, main_kb
from src.telegram.messages.admin_msg import build_email_msg

is_parsing = False


class EmailMsg(StatesGroup):
    email = State()


@admin_router.message(EmailMsg.email)
async def waiting_message(message: Message, state: FSMContext):
    # send new msg
    address = message.text
    if not is_email_exists(address):
        await message.answer("Wrong email address", reply_markup=email_kb)
        await state.clear()
        return

    inbox_id = get_email_id_by_name(address)
    # run waiting process
    receive_msg_in_new_thread(inbox_id)
    global is_parsing
    is_parsing = True
    await message.reply("Will be waiting for a new message for 5 minutes...",
                        reply_markup=cancel_kb)
    start = perf_counter()

    all_msgs = get_all_email_messages(address)
    while is_parsing:
        await asyncio.sleep(1)
        new_msg = check_new_email_message(inbox_id, len(all_msgs))
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



