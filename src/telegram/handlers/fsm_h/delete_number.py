from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from setup import admin_router
from aiogram import F

from src.database.queries import is_email_exists, is_number_exists, delete_number_from_db, get_number_by_name, \
    delete_all_numbers_from_db
from src.sms import cancel_number
# from src.sms.methods import my_client
from src.telegram.buttons.admin_btns import phone_kb


class DeleteNumber(StatesGroup):
    number = State()


@admin_router.message(DeleteNumber.number)
async def delete_email_fsm(message: Message, state: FSMContext):
    try:
        if message.text == "Delete all":
            delete_all_numbers_from_db()
            await message.reply("Deleted all numbers",
                                reply_markup=phone_kb)
            return
        number = message.text.strip()[1:]
        if not is_number_exists(number):
            await message.reply("Number doesn't exist",
                                reply_markup=phone_kb)

        else:
            struct_number = get_number_by_name(number)
            one = cancel_number(activation_id=struct_number.activation_id)  # delete number from site
            two = delete_number_from_db(number)  # delete it from db
            if not one:
                raise Exception("Can't delete on site")
            if not two:
                raise Exception("Can't delete in db")
            await message.reply("Number deleted",
                                reply_markup=phone_kb)

    except Exception as err:
        print(err)
        await message.reply(f"Error", reply_markup=phone_kb)
    finally:
        await state.clear()
        return
