from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from setup import admin_router
from aiogram import F
from src.database.queries import save_new_email
from src.email.methods import create_inbox, create_few_inboxes
from src.models import EmailModel
from src.telegram.buttons.admin_btns import email_kb, skip_kb, main_kb
from src.telegram.messages.admin_msg import build_new_emails_msg


class MailContext(StatesGroup):
    email_address = State()
    amount = State()
    note = State()


@admin_router.message(F.text == "Cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(
        "Canceled.",
        reply_markup=main_kb)


@admin_router.message(MailContext.amount)
async def save_note(message: Message, state: FSMContext):
    try:
        await state.update_data(amount=int(message.text))
        await state.set_state(MailContext.note)
    except ValueError:
        await message.reply("Must be a number!", reply_markup=email_kb)
        await state.clear()
        return
    await message.answer(f"Write some note:",
                         reply_markup=skip_kb, parse_mode="MARKDOWN")


@admin_router.message(MailContext.note)
async def save_note(message: Message, state: FSMContext):
    note = message.text
    if note == "Skip": note = None
    await state.update_data(note=note)
    data = await state.get_data()
    await state.clear()
    new_inbox = create_few_inboxes(data['amount'], note)
    msg = build_new_emails_msg(new_inbox)
    await message.answer(msg, reply_markup=email_kb, parse_mode="MARKDOWN")



