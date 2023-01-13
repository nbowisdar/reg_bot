import asyncio
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from setup import admin_router
from aiogram import F
from time import perf_counter
from src.database.queries import is_number_exists, get_all_number_messages, check_new_number_message
from src.email.methods import receive_msg_in_new_thread
from src.telegram.buttons.admin_btns import cancel_kb, phone_kb
from src.telegram.messages.admin_msg import build_email_msg, build_new_msg_number

is_parsing = False


class NumberMsg(StatesGroup):
    number = State()


@admin_router.message(NumberMsg.number)
async def waiting_message(message: Message, state: FSMContext):
    # send new msg
    number = message.text
    if not is_number_exists(number):
        await message.answer("Wrong number", reply_markup=phone_kb)
        await state.clear()
        return
    # run waiting process
    # receive_msg_in_new_thread(inbox_id)
    global is_parsing
    is_parsing = True
    await message.reply("Will be waiting for a new message for 5 minutes...",
                        reply_markup=cancel_kb)
    start = perf_counter()

    all_msgs = get_all_number_messages(number)
    while is_parsing:
        await asyncio.sleep(1)
        new_msg = check_new_number_message(number, len(all_msgs))
        if new_msg:
            send_msg = build_new_msg_number(new_msg)
            await message.answer(send_msg,
                                 reply_markup=phone_kb)
            await state.clear()
            is_parsing = False
            return
        if perf_counter() - start > 360:
            is_parsing = False
            await message.answer("Got nothing, time is over",
                                 reply_markup=phone_kb)



