import asyncio
from loguru import logger

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.filters import Text, Command
from aiogram import F, Router

from setup import bot, chat_id
from src.database.tables import Task
from src.telegram.handlers.todo import inform_about_new_task

user_router = Router()


async def reminding():
    logger.info("reminding started!")
    while True:
        await asyncio.sleep(1200)
        tasks = Task.select().where(Task.executed == False)
        count = tasks.count()
        if count > 0:
            msg = f"You have {count} unfinished tasks❗️\n" \
                  f"Send /tasks to see them"
            await bot.send_message(chat_id, msg)
        else:
            logger.info("All tasks is done!")


async def send_all_active_tasks():
    tasks = Task.select().where(Task.executed == False)
    for task in tasks:
        await inform_about_new_task(task)


# @user_router.message(F.text == "/start")
# async def anon(message: Message):


@user_router.message(F.text.in_({"/tasks", "📖 Tasks"}))
async def anon(message: Message):
    await send_all_active_tasks()
    # await message.answer("Main", reply_markup=kb)
