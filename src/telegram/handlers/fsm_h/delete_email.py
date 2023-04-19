from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from loguru import logger

from setup import admin_router
from aiogram import F

from src.database.queries import is_email_exists, delete_email_from_db, get_all_emails
from src.telegram.buttons.admin_btns import email_kb
from src.telegram.messages.admin_msg import build_all_emails_msg


class DeleteEmail(StatesGroup):
    email_address = State()
    list_of_emails = State()


@admin_router.message(DeleteEmail.email_address)
async def delete_email_fsm(message: Message, state: FSMContext):
    try:
        email = message.text.strip()
        if email == "🗑 Delete list of emails":
            await state.set_state(DeleteEmail.list_of_emails)
            matrix = get_all_emails()
            if not matrix:
                return "You haven't created any emails 👎"
            for emails in matrix:
                msg = build_all_emails_msg(emails, only_email=True)
                await message.answer(f"Past emails you want to delete\n\n{msg}")
            return
        # if email == "Delete all":
        #     delete_all_email_from_db()
        #     delete_all_inboxes()
        #     await message.reply("Deleted all emails",
        #                         reply_markup=email_kb)
        #     return
        if not is_email_exists(email):
            await message.reply("Email doesn't exists",
                                reply_markup=email_kb)
            return
        delete_email_from_db(email)  # delete from db
        await message.reply("Email deleted",
                            reply_markup=email_kb)
        await state.clear()

    except Exception as err:
        logger.error(err)
        await message.reply(f"Error", reply_markup=email_kb)
        await state.clear()


@admin_router.message(DeleteEmail.list_of_emails)
async def delete_email_fsm(message: Message, state: FSMContext):
    emails = message.text.split("\n")
    deleted = 0
    for email in emails:
        try:
            delete_email_from_db(email)  # delete from db
            deleted += 1
        except Exception as err:
            logger.error(err)

    await message.answer(f'Emails deleted - *{deleted}*', parse_mode="MARKDOWN",
                         reply_markup=email_kb)
    return await state.clear()
