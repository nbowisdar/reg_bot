import time

from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from setup import admin_router
from aiogram import F
from time import perf_counter

from src.database.queries import check_new_message
from src.email.methods import receive_msg_in_new_thread
from src.telegram.messages.admin_msg import build_email_msg

is_parsing = False

class EmailMsg(StatesGroup):
    email = State()


@admin_router.message(F.text == "Cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Canceled.",
        reply_markup=admin_main_kb)


@admin_router.message(EmailMsg.email)
async def waiting_message(message: Message, state: FSMContext):
    # send new msg
    inbox_id = message.text.split("@")[0]
    msg = receive_msg_in_new_thread(inbox_id)
    global is_parsing
    is_parsing = True
    await message.reply("Will be waiting a new message for 2 minutes...",
                        reply_markup=stop_kb)
    start = perf_counter()
    while perf_counter() - start < 360 and is_parsing:
        time.sleep(1)
        new_msg = check_new_message(msg)
        if new_msg:
            send_msg = build_email_msg(new_msg)
            await message.answer(send_msg,
                                 reply_markup=admin_main_kb)
            await state.clear()
            is_parsing = False




