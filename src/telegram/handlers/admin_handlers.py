from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from setup import admin_router
from src.database.queries import get_all_emails, get_all_numbers
from src.database.tables import Email, EmailSaver
from src.sms import get_balance
from src.telegram.buttons.admin_btns import main_kb, phone_kb, email_kb, skip_kb, cancel_kb, how_many_kb, service_kb, \
    cancel_and_delete_kb, cancel_and_delete_email_kb, build_ready_emails_kb
from src.telegram.handlers.fsm_h.create_email import MailContext
from src.telegram.handlers.fsm_h.create_number import NumberContext
from src.telegram.handlers.fsm_h.delete_email import DeleteEmail
from src.telegram.handlers.fsm_h.delete_number import DeleteNumber
from src.telegram.handlers.fsm_h.new_msg_from_email import EmailMsg
from src.telegram.handlers.fsm_h.new_msg_number import NumberMsg
from src.telegram.messages.admin_msg import build_all_emails_msg, build_all_numbers_msg, balance_message, \
    build_emails_in_work
from requests.exceptions import ConnectionError

from src.utils.msg import divide_big_msg

inboxer = EmailSaver()


@admin_router.message((F.text == "Go back") | (F.text == "/start"))
async def main (message: Message):
    await message.answer("Main page",
                         reply_markup=main_kb)


@admin_router.message(F.text == "Email")
async def e (message: Message):
    await message.answer("Email page",
                         reply_markup=email_kb)


@admin_router.message(F.text == "Number")
async def n (message: Message):
    await message.answer("Number page",
                         reply_markup=phone_kb)


@admin_router.message(F.text == 'In work')
async def anon(message: Message):
    emails = Email.select().where(Email.status == "in_use")
    if not emails:
        await message.answer("Zero emails in work 👎")
        return
    msg = build_emails_in_work(emails)
    chunks = divide_big_msg(msg)
    for chunk in chunks:
        await message.answer(chunk, reply_markup=email_kb, parse_mode="MARKDOWN")


@admin_router.message(F.text == 'Ready')
async def anon(message: Message):
    emails = inboxer.get_ready_emails()
    if not emails:
        await message.answer("Zero emails are ready 👎")
        return
    # msg = build_emails_in_work(emails)
    await message.answer("Choose email you want to use",
                         reply_markup=build_ready_emails_kb(emails),
                         parse_mode="MARKDOWN")


from aiogram.fsm.state import State, StatesGroup
class Add_Note(StatesGroup):
    note = State()


@admin_router.callback_query(Text(startswith="read_email"))
async def anon(callback: CallbackQuery, state: FSMContext):
    _, email = callback.data.split('|')
    await callback.message.delete()
    await callback.message.answer("Write some note", reply_markup=skip_kb)
    await state.set_state(Add_Note.note)
    await state.update_data(email=email)


@admin_router.message(Add_Note.note)
async def anon(message: Message, state: FSMContext):
    note = message.text
    if note == "Skip": note = None
    data = await state.get_data()
    email, created = Email.get_or_create(email_address=data['email'])
    email.status = "in_use"
    email.note = note
    email.save()

    inboxer.drop_ready_email(data['email'])
    await message.reply('Status of email was changed to "In work"', reply_markup=email_kb)


@admin_router.message(F.text == 'All emails')
async def show_emails(message: Message):
    matrix = get_all_emails()
    if not matrix:
        return "You haven't created any emails 👎"
    for emails in matrix:
        msg = build_all_emails_msg(emails)
        await message.answer(msg, reply_markup=email_kb, parse_mode="MARKDOWN")


@admin_router.message(F.text == 'Create new email')
async def show_emails(message: Message, state: FSMContext):
    await state.set_state(MailContext.amount)
    await message.answer("How many emails do you want to create?",
                         reply_markup=how_many_kb, parse_mode="MARKDOWN")


@admin_router.message(F.text == "Receive message")
async def show_emails(message: Message, state: FSMContext):
    await state.set_state(EmailMsg.email)
    await message.answer("Write an email address you want to send the message to",
                         reply_markup=cancel_kb,
                         parse_mode="MARKDOWN")


@admin_router.message(F.text == 'Delete email')
async def show_emails(message: Message, state: FSMContext):
    await state.set_state(DeleteEmail.email_address)
    await message.answer("Write an email address you want delete:",
                         reply_markup=cancel_and_delete_email_kb,
                         parse_mode="MARKDOWN")


@admin_router.message(F.text == "Show all numbers")
async def show_numbers(message: Message):
    numbers = get_all_numbers()
    msg = build_all_numbers_msg(numbers)
    await message.answer(msg, reply_markup=phone_kb, parse_mode="MARKDOWN")


@admin_router.message(F.text == "Create new number")
async def create_numbers(message: Message, state: FSMContext):
    await state.set_state(NumberContext.service)
    await message.answer("Please select your service",
                         reply_markup=service_kb, parse_mode="MARKDOWN")


@admin_router.message(F.text == 'Delete number')
async def show_emails(message: Message, state: FSMContext):
    await state.set_state(DeleteNumber.number)
    await message.answer("Write a number you want delete:",
                         reply_markup=cancel_and_delete_kb,
                         parse_mode="MARKDOWN")


@admin_router.message(F.text == "Receive msg")
async def show_emails(message: Message, state: FSMContext):
    await state.set_state(NumberMsg.number)
    await message.answer("Write a number you want to send the message to",
                         reply_markup=cancel_kb,
                         parse_mode="MARKDOWN")


@admin_router.message(F.text == "Show balance")
async def show_emails(message: Message):
    try:
        balance = get_balance()
        msg = balance_message(balance)
        await message.answer(msg, reply_markup=phone_kb, parse_mode="MARKDOWN")
    except ConnectionError:
        await message.reply("At the moment server is not available😢", reply_markup=phone_kb)