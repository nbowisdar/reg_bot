from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from setup import admin_router
from src.database.queries import get_all_emails, get_all_numbers
from src.sms import get_balance
from src.telegram.buttons.admin_btns import main_kb, phone_kb, email_kb, skip_kb, cancel_kb, how_many_kb, service_kb
from src.telegram.handlers.fsm_h.create_email import MailContext
from src.telegram.handlers.fsm_h.create_number import NumberContext
from src.telegram.handlers.fsm_h.delete_email import DeleteEmail
from src.telegram.handlers.fsm_h.delete_number import DeleteNumber
from src.telegram.handlers.fsm_h.new_msg_from_email import EmailMsg
from src.telegram.handlers.fsm_h.new_msg_number import NumberMsg
from src.telegram.messages.admin_msg import build_all_emails_msg, build_all_numbers_msg


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


@admin_router.message(F.text == 'Show all emails')
async def show_emails(message: Message):
    emails = get_all_emails()
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
                         reply_markup=cancel_kb,
                         parse_mode="MARKDOWN")


@admin_router.message(F.text == "Show all numbers")
async def show_numbers(message: Message):
    numbers = get_all_numbers()
    print(numbers)
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
                         reply_markup=cancel_kb,
                         parse_mode="MARKDOWN")


@admin_router.message(F.text == "Receive msg")
async def show_emails(message: Message, state: FSMContext):
    await state.set_state(NumberMsg.number)
    await message.answer("Write a number you want to send the message to",
                         reply_markup=cancel_kb,
                         parse_mode="MARKDOWN")


@admin_router.message(F.text == "Show balance")
async def show_emails(message: Message):
    balance = get_balance()
    await message.answer(f"Your balance - *{balance}*",
                         reply_markup=phone_kb,
                         parse_mode="MARKDOWN")