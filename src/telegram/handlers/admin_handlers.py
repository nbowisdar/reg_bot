from aiogram.types import Message
from aiogram.filters import Text, Command
from aiogram import F
from setup import admin_router


async def main(message: Message):
    await message.answer("Main page")