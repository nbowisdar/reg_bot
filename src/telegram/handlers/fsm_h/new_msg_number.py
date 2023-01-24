import asyncio
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from setup import admin_router
from aiogram import F
from time import perf_counter
from src.database.queries import is_number_exists, get_all_number_messages, check_new_number_message, is_active, \
    get_number_by_name, delete_number_from_db
from src.email.methods import receive_msg_in_new_thread
from src.sms import create_waiting_thread, request_new_sms, cancel_number
from src.telegram.buttons.admin_btns import cancel_kb, phone_kb, cancel_kb_number
from src.telegram.messages.admin_msg import build_email_msg, build_new_msg_number
from loguru import logger

is_parsing = False


class NumberMsg(StatesGroup):
    number = State()


@admin_router.message(F.text == 'Cancel number')
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    global is_parsing
    is_parsing = False
    data = await state.get_data()
    struct_number = get_number_by_name(data['number'])
    one = cancel_number(activation_id=struct_number.activation_id)  # delete number from site
    two = delete_number_from_db(data['number'])  # delete it from db
    if not one:
        await message.reply("Can't delete on site",
                            reply_markup=phone_kb)
    if not two:
        await message.reply("Can't delete in db",
                            reply_markup=phone_kb)
    await state.clear()
    await message.answer(
        "Canceled, number released",
        reply_markup=phone_kb)


@admin_router.message(NumberMsg.number)
async def waiting_message(message: Message, state: FSMContext):
    # send new msg
    try:
        number = message.text[1:]
        await state.update_data(number=number)
        if not is_number_exists(number):
            await message.answer("Wrong number", reply_markup=phone_kb)
            return
        if not is_active(number):
            await message.answer("This number has expired", reply_markup=phone_kb)
            return
        # run waiting process
        global is_parsing
        is_parsing = True
        await message.reply("Will be waiting for a new message for 5 minutes...",
                            reply_markup=cancel_kb_number)
        start = perf_counter()
        struct_number = get_number_by_name(number)
        request_new_sms(struct_number.activation_id)
        wait_thread = create_waiting_thread(phone_number=number)
        wait_thread.start()
        all_msgs = get_all_number_messages(number)
        while is_parsing:
            await asyncio.sleep(1)
            new_msg = check_new_number_message(number, len(all_msgs))
            if new_msg:
                send_msg = build_new_msg_number(new_msg)
                await message.answer(send_msg,
                                     reply_markup=phone_kb)
                is_parsing = False
                return
            if perf_counter() - start > 360:
                is_parsing = False
                await message.answer("Got nothing, time is over",
                                     reply_markup=phone_kb)
    except Exception as err:
        logger.error(err)
    finally:
        await message.answer(f"Error occurred, please your number here https://sms-activate.org/getNumber")
        await state.clear()



