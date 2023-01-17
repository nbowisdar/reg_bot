from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from loguru import logger
from setup import admin_router
from aiogram import F

from src.database.queries import save_number
from src.sms import buy_new_number
from src.telegram.buttons.admin_btns import phone_kb, skip_kb


class NumberContext(StatesGroup):
    number = State()
    service = State()


# @admin_router.message(F.text == "Cancel")
# async def cancel_handler(message: Message, state: FSMContext) -> None:
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.clear()
#     await message.answer(
#         "Canceled.",
#         reply_markup=phone_kb)


@admin_router.message(NumberContext.service)
async def save_note(message: Message, state: FSMContext):
    service = message.text
    # TODO change this later
    if service != "Google (gmail)":
        await message.reply("Wrong service❌", reply_markup=phone_kb)
        await state.clear()
        return
    # await state.update_data(service=service)
    # data = await state.get_data()
    await state.clear()
    # await message.answer("Creating a new number...")
    await handle_data(message)


async def handle_data(message: Message, data: dict = None):
    try:
        number = buy_new_number(service="go")
        save_number(number)  # -> save number into db
        await message.answer(f"Created new number -> `+{number.number}`",
                             reply_markup=phone_kb, parse_mode="MARKDOWN")
    except Exception as err:
        logger.error(err)
        await message.answer("Error", reply_markup=phone_kb)


