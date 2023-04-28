from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Text, Command
from aiogram import F, Router
import src.telegram.buttons.admin_btns as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram import types

from setup import bot, chat_id
from src.database.tables import Task

todo_router = Router()


async def inform_about_new_task(task: Task):
    msg = "New Task❗️❗️\n" \
          f"{task.title}\n"
    if task.desc:
        msg += f"\n{task.desc}"
    await bot.send_message(chat_id, msg)


@todo_router.message(F.text == "❌ Cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state:
        await state.clear()
    await message.answer(
        "❌ Canceled", reply_markup=kb.task_menu,
    )


@todo_router.message(Text('⬅️ Back'))
async def anon(message: Message):
    await message.answer("Main", reply_markup=kb.main_kb)



@todo_router.message(Command(commands='admin'))
async def anon(message: Message):
    await message.answer("You are admin!")


class TaskFSM(StatesGroup):
    title = State()
    desc = State()


@todo_router.message(Text("Tasks"))
async def anon(message: Message):
    tasks = Task.select().where(Task.executed == False)
    await message.answer(f"Total unfinished tasks - {tasks.count()}", reply_markup=kb.task_menu)


@todo_router.message(Text("Show active"))
async def anon(message: Message):
    await message.answer("Tasks:")


@todo_router.message(Text("New task"))
async def anon(message: Message, state: FSMContext):
    await message.answer("Write task title", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(TaskFSM.title)


@todo_router.message(TaskFSM.title)
async def anon(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Write description if needed", reply_markup=kb.cancel_skip_admin_kb)
    await state.set_state(TaskFSM.desc)


@todo_router.message(TaskFSM.desc)
async def anon(message: Message, state: FSMContext):
    desc = False
    if message.text == "Skip":
        desc = message.text
    data = await state.get_data()
    await state.clear()
    task = Task.create(title=data['title'], desc=desc)
    await message.answer("✅ New task created!", reply_markup=kb.task_menu)
    await inform_about_new_task(task)


