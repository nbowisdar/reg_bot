from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from setup import admin_router
from aiogram import F

from src.database.queries import is_email_exists, delete_email_from_db
from src.email.methods import delete_email_on_site
from src.telegram.buttons.admin_btns import email_kb


class DeleteEmail(StatesGroup):
    email_address = State()


@admin_router.message(DeleteEmail.email_address)
async def delete_email_fsm(message: Message, state: FSMContext):
    try:
        email = message.text.strip()
        if not is_email_exists(email):
            await message.reply("Email doesn't exists",
                                reply_markup=email_kb)
            return
        inbox_id = email.split("@")[0]
        delete_email_on_site(inbox_id)  # delete from site
        delete_email_from_db(inbox_id)  # delete from db
        await message.reply("Email deleted",
                            reply_markup=email_kb)
    except Exception as err:
        print(err)
        await message.reply(f"Error", reply_markup=email_kb)
    finally:
        await state.clear()
