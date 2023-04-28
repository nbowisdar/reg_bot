import asyncio
from loguru import logger
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram import F, Router

from setup import bot, support_id
from src.database.tables import Task
from src.telegram.handlers.todo import inform_about_new_task

user_router = Router()





#
# @user_router.message(F.text.in_({"/tasks", "📖 Tasks"}))
# async def anon(message: Message):
#     await send_all_active_tasks()
    # await message.answer("Main", reply_markup=kb)
