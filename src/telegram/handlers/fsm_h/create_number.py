from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from loguru import logger
from setup import admin_router
from aiogram import F
from requests.exceptions import ConnectionError
from src.database.queries import save_number
from src.sms import buy_new_number
from src.telegram.buttons.admin_btns import phone_kb, skip_kb


class NumberContext(StatesGroup):
    number = State()
    service = State()


@admin_router.message(NumberContext.service)
async def save_note(message: Message, state: FSMContext):
    service = message.text
    # TODO change this later"ub"
    if service != "Google (gmail)" and service != "Uber":
        await message.reply("Wrong service❌", reply_markup=phone_kb)
        await state.clear()
        return
    if service == "Uber":
        await state.update_data(service='ub')
    else:
        await state.update_data(service="go")
    data = await state.get_data()
    await state.clear()
    # await message.answer("Creating a new number...")
    await handle_data(message, data)


async def handle_data(message: Message, data: dict = None):
    try:

        number = buy_new_number(service=data['service'])
        save_number(number)  # -> save number into db
        await message.answer(f"Created new number -> `+{number.number}`",
                             reply_markup=phone_kb, parse_mode="MARKDOWN")
    except ConnectionError:
        await message.reply("At the moment server is not available😢", reply_markup=phone_kb)

    except Exception as err:
        logger.error(err)
        await message.answer("Error", reply_markup=phone_kb)


