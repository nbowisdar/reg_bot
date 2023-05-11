from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from setup import admin_router, domain
from src.database.queries import get_all_emails, get_all_numbers
from src.database.tables import Email, EmailSaver
from src.sms import get_balance
from src.telegram.buttons.admin_btns import main_kb, phone_kb, email_kb, skip_kb, cancel_kb, how_many_kb, service_kb, \
    cancel_and_delete_kb, cancel_and_delete_email_kb, build_ready_emails_kb, ready_action_inl, ready_type_inl, sex_inl, \
    sex_inl_out
from src.telegram.handlers.fsm_h.create_email import MailContext
from src.telegram.handlers.fsm_h.create_number import NumberContext
from src.telegram.handlers.fsm_h.delete_email import DeleteEmail
from src.telegram.handlers.fsm_h.delete_number import DeleteNumber
from src.telegram.handlers.fsm_h.new_msg_from_email import EmailMsg
from src.telegram.handlers.fsm_h.new_msg_number import NumberMsg
from src.telegram.messages.admin_msg import build_all_emails_msg, build_all_numbers_msg, balance_message, \
    build_emails_in_work
from requests.exceptions import ConnectionError
from aiogram.fsm.state import State, StatesGroup

from src.utils.msg import divide_big_msg

inboxer = EmailSaver()


@admin_router.message((F.text == "Go back") | (F.text == "/start"))
async def main(message: Message):
    await message.answer("Main page",
                         reply_markup=main_kb)


@admin_router.message(F.text == "Email")
async def e(message: Message):
    await message.answer("Email page",
                         reply_markup=email_kb)


@admin_router.message(F.text == "Number")
async def n(message: Message):
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


@admin_router.message(F.text == 'Ready emails')
async def anon(message: Message):
    counts = {
        "Uber": 0,
        "Doorsdash": 0,
        "Lyft": 0,
    }
    emails = Email.select().where(Email.status == "ready")
    for email in emails:
        match email.type:
            case "Uber":
                counts['Uber'] += 1
            case "Doorsdash":
                counts['Doorsdash'] += 1
            case "Lyft":
                counts['Lyft'] += 1
    # counts['Uber'] += len(inboxer.get_ready_emails())
    msg = f"Uber - {counts['Uber']}\n" \
          f"Lyft - {counts['Lyft']}\n" \
          f"Doorsdash - {counts['Doorsdash']}\n"
    await message.answer("Ready amount:\n" + msg + "\nChoose type 👇",
                         reply_markup=ready_type_inl,
                         parse_mode="MARKDOWN")


@admin_router.callback_query(Text(startswith="choose_ready_type"))
async def anon(callback: CallbackQuery):
    _, service_type = callback.data.split("|")
    await callback.message.edit_text("What do you want to do?",
                                     reply_markup=ready_action_inl(service_type),
                                     parse_mode="MARKDOWN")


class Add_New_Email(StatesGroup):
    email = State()
    note = State()


@admin_router.callback_query(Text(startswith='ready'))
async def anon(callback: CallbackQuery, state: FSMContext):
    _, action, sr_type = callback.data.split("|")
    await state.update_data(sr_type=sr_type)
    if action == "take":
        emails = Email.select().where(
            (Email.type == sr_type) & (Email.status == "ready")
        )
        if not emails:
            await callback.message.edit_text("Zero emails are ready 👎")  ##
            await state.clear()
            return

        m, w, o = 0, 0, 0
        for email in emails:
            if email.sex == "female":
                w += 1
            elif email.sex == "male":
                m += 1
            else:
                o += 1

        await callback.message.edit_text("Choose sex that you need 👇\n"
                                         f"🙎‍♂️ - {m}       🙎‍♀️ - {w}",
                                         reply_markup=sex_inl_out)

    elif action == "add":
        await callback.message.delete()
        await callback.message.answer("Write email you want to add",
                                      reply_markup=cancel_kb)
        await state.set_state(Add_New_Email.email)


@admin_router.callback_query(Text(startswith="out_sex"))
async def anon(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    _, sex = callback.data.split("|")
    emails = Email.select().where(
        (Email.type == data['sr_type']) & (Email.status == "ready") & (Email.sex == sex)
    )


    await callback.message.edit_text("Choose email you want to use",
                                     reply_markup=build_ready_emails_kb(emails),
                                     parse_mode="MARKDOWN")


@admin_router.message(Add_New_Email.email)
async def anon(message: Message, state: FSMContext):
    email_addr = message.text
    if domain not in email_addr:
        await message.answer(f"❌ Wrong email address\nMust contain - `@{domain}`",
                             reply_markup=email_kb, parse_mode="MARKDOWN")
        await state.clear()
        return
    email, created = Email.get_or_create(email_address=email_addr)
    if not created:
        if email.status == "ready" or email.status == "in_use":
            await message.answer(f'❌ Email already in the {email.status.capitalize()} section!',
                                 reply_markup=email_kb)
            await state.clear()
            return

    data = await state.get_data()
    sr_type = data['sr_type']
    email.type = sr_type
    email.status = "ready"
    email.save()
    if email.note:
        await message.reply(f"`{email.email_address}` is ready now! 🥳",
                            reply_markup=email_kb, parse_mode="MARKDOWN")
        await state.clear()
    else:
        await message.reply(f"Add client's name or other note",
                            reply_markup=cancel_kb, parse_mode="MARKDOWN")
        await state.set_state(Add_New_Email.note)
        await state.update_data(email=email.email_address)


@admin_router.message(Add_New_Email.note)
async def anon(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    Email.update(note=message.text).where(Email.email_address == data['email']).execute()
    await message.reply(f"`{data['email']}` is ready now! 🥳",
                        reply_markup=email_kb, parse_mode="MARKDOWN")


# class Add_Note(StatesGroup):
#     note = State()

@admin_router.callback_query(Text(startswith="read_email"))
async def anon(callback: CallbackQuery):
    _, id = callback.data.split('|')
    email = Email.get_by_id(id)
    email.status = "in_use"
    email.save()
    await callback.message.delete()
    await callback.message.answer(f"♻️ Dropped                       sex - {email.sex}\n"
                                  f"`{email.email_address}\n{email.note}`",
                                  reply_markup=email_kb,
                                  parse_mode="MARKDOWN")

    try:
        inboxer.drop_ready_email(email)
    except ValueError:
        Email.update(status="in_use").where(Email.email_address == email).execute()
    # await callback.message.answer("Write client's name or username", reply_markup=skip_kb)

    # await state.set_state(Add_Note.note)
    # await state.update_data(email=email)


# @admin_router.message(Add_Note.note)
# async def anon(message: Message, state: FSMContext):
#     note = message.text
#     if note == "Skip": note = None
#     data = await state.get_data()
#     email, created = Email.get_or_create(email_address=data['email'])
#     email.status = "in_use"
#     email.note = note
#     email.save()
#     if email.type == "Uber":
#         inboxer.drop_ready_email(data['email'])
#     await message.reply('✅ Status changed to "In work"', reply_markup=email_kb)
#     await state.clear()


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
    # await state.set_state(MailContext.amount)
    await message.answer("Choose sex? 👇", reply_markup=sex_inl, parse_mode="MARKDOWN")


@admin_router.callback_query(Text(startswith='choose_sex'))
async def show_emails(callback: CallbackQuery, state: FSMContext):
    _, sex = callback.data.split("|")
    await state.set_state(MailContext.amount)
    await state.update_data(sex=sex)
    await callback.message.delete()
    await callback.message.answer("How many emails do you want to create?",
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


@admin_router.message(F.text == "/test")
async def show_emails(message: Message):
    await message.answer("[hello](https://www.google.com/)", reply_markup=None)