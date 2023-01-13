from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from loguru import logger

from setup import admin_router
from aiogram import F

from src.sms.methods import ClientNumber, my_client
from src.telegram.buttons.admin_btns import phone_kb, skip_kb
from src.telegram.messages.admin_msg import build_new_number_msg


class NumberContext(StatesGroup):
    number = State()
    amount = State()
    note = State()


# @admin_router.message(F.text == "Cancel")
# async def cancel_handler(message: Message, state: FSMContext) -> None:
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.clear()
#     await message.answer(
#         "Canceled.",
#         reply_markup=phone_kb)


@admin_router.message(NumberContext.amount)
async def save_note(message: Message, state: FSMContext):
    try:
        await state.update_data(amount=int(message.text))
        await state.set_state(NumberContext.note)
    except TypeError:
        await message.reply("Must be a number!", reply_markup=phone_kb)
        await state.clear()
        return
    await message.answer(f"Write some note:",
                         reply_markup=skip_kb, parse_mode="MARKDOWN")


@admin_router.message(NumberContext.note)
async def save_note(message: Message, state: FSMContext):
    note = message.text
    if note == "Skip": note = None
    await state.update_data(note=note)
    data = await state.get_data()
    await state.clear()
    await message.answer("Creating a new number...")
    await handle_data(message, data)


async def handle_data(message: Message, data: dict):
    try:
        numbers = my_client.create_new_number(data['amount'])
        msg = build_new_number_msg(numbers)
        await message.answer(msg, reply_markup=phone_kb, parse_mode="MARKDOWN")
    except Exception as err:
        logger.error(err)
        await message.answer("Error", reply_markup=phone_kb)


