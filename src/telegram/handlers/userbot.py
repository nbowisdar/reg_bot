import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Text, Command
from aiogram import F, Router
from loguru import logger
import src.telegram.buttons.admin_btns as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram import types
from setup import bot, support_id
from src.database.tables import Task, Template, Trigger, db
from src.telegram.buttons import admin_btns as kb
from src.telegram.messages.admin_msg import get_template_full_msg

userbot_router = Router()

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🛑 Cancel")]],
    resize_keyboard=True
)

cancel_inl = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="🛑 Cancel", callback_data="ai_cancel")]],
    resize_keyboard=True
)


@userbot_router.message(F.text == "🛑 Cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("🧠 User AI page.", reply_markup=kb.ai_kb)
        return
    await state.clear()
    await message.answer("🛑 Canceled", reply_markup=kb.ai_kb)


@userbot_router.callback_query(F.text == "ai_cancel")
async def cancel_handler(callback: CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    await callback.message.delete()
    if current_state is None:
        await callback.message.answer("🧠 User AI page.", reply_markup=kb.ai_kb)
        return
    await state.clear()
    await callback.message.answer("🛑 Canceled", reply_markup=kb.ai_kb)


@userbot_router.message(F.text == "🤖 AI")
async def anon(message: Message):
    await message.answer("🧠 User AI page", reply_markup=kb.ai_kb)


@userbot_router.message(F.text == "📒 Templates")
async def anon(message: Message):
    await message.answer("What to do?", reply_markup=kb.temp_first_inl)


class TemplateFSM(StatesGroup):
    name = State()
    text = State()


@userbot_router.callback_query(Text("new_template"))
async def anon(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TemplateFSM.name)
    await callback.message.delete()
    await callback.message.answer("Write short and unique name for template",
                                  reply_markup=cancel_kb)


@userbot_router.message(TemplateFSM.name)
async def anon(message: Message, state: FSMContext):
    await state.set_state(TemplateFSM.text)

    if Template.select().where(Template.name == message.text):
        await message.reply("❌ This name not unique!", reply_markup=kb.ai_kb)
        await state.clear()
        return

    await state.update_data(name=message.text)
    await message.answer("Write full template", reply_markup=cancel_kb)


@userbot_router.message(TemplateFSM.text)
async def anon(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.clear()
    temp = Template.create(**data)
    await message.answer(f"✅ You created new template!\nName - {temp.name}\nText - {temp.text}",
                         reply_markup=kb.ai_kb)


@userbot_router.callback_query(Text("new_template"))
async def anon(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TemplateFSM.name)
    await callback.message.delete()
    await callback.message.answer("Write short and unique name for template",
                                  reply_markup=cancel_kb)


@userbot_router.callback_query(Text("templates"))
async def anon(callback: CallbackQuery):
    await callback.message.edit_text("Select your template", reply_markup=kb.get_templates_inl())


@userbot_router.callback_query(Text(startswith="get_temp"))
async def anon(callback: CallbackQuery):
    _, temp_id = callback.data.split("|")
    temp = Template.get_by_id(temp_id)
    await callback.message.edit_text("choose action", reply_markup=kb.change_template_inl(temp_id))


@userbot_router.callback_query(Text(startswith="change_temp"))
async def anon(callback: CallbackQuery):
    _, temp_id, action = callback.data.split("|")
    if action == "show":
        template = Template.get_by_id(temp_id)
        msg = get_template_full_msg(template)
        await callback.message.edit_text(msg)

    elif action == "delete":
        template = Template.get_by_id(temp_id)
        msg = get_template_full_msg(template, no_markdown=True)
        Template.delete().where(Template.id == template.id).execute()
        await callback.message.edit_text(f"♻️ Template deleted\n`{msg}`")

    else:
        await callback.message.edit_text("Choose type",
                                     reply_markup=kb.template_action_inl(temp_id, action))


class UpdateFieldFSM(StatesGroup):
    new_value = State()


@userbot_router.callback_query(Text(startswith="temp_action"))
async def anon(callback: CallbackQuery, state: FSMContext):
    _, temp_id, action, type_ = callback.data.split("|")
    await state.update_data(type=type_)
    await state.set_state(UpdateFieldFSM.new_value)
    template = Template.get_by_id(temp_id)
    await state.update_data(template=template)
    if type_ == "triggers":
        msg_1 = "Send all triggers, each of which is on the new line!\n" \
              "Don't forget *copy previous* triggers!"
        msg_2 = "\n".join([i.phrase for i in template.triggers])
        if not msg_2:
            msg_2 = "Trigger 1\ntrigger 2"
    else:
        msg_1 = "Send me updated data in the same format"
        msg_2 = f"{template.name}\n{template.text}"

    # await callback.message.delete()
    await callback.message.edit_text(msg_1)
    await callback.message.answer(f'`{msg_2}`', reply_markup=cancel_kb)


@userbot_router.message(UpdateFieldFSM.new_value)
async def anon(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    type_ = data['type']
    template: Template = data['template']
    if type_ == "triggers":
        # triggers = message.text.split("\n")
        with db.atomic():
            Trigger.delete().where(Trigger.template == template).execute()
            print([{"phrase": tr, "template": template} for tr in message.text.split("\n")])
            # Trigger.bulk_create(
            Trigger.insert_many(
                [
                    {"phrase": tr, "template": template}
                    for tr in message.text.split("\n")
                ]
            ).execute()
    elif type_ == "template":
        try:
            name, text = message.text.split("\n")
        except ValueError:
            await message.reply("❌ Wrong format! Must be only 2 rows!",
                                reply_markup=kb.ai_kb)
            await state.clear()
            return
        template.name = name
        template.text = text
        template.save()

    msg = get_template_full_msg(template)
    await message.answer(f"✅ {type_.capitalize()} updated!\n{msg}",
                         reply_markup=kb.ai_kb)