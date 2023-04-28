# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

hide_inl_btn = types.InlineKeyboardButton(text="↙️ Hide", callback_data=f"hide")


def update_status_order_choice(task_id) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [hide_inl_btn,
         types.InlineKeyboardButton(text="✅ Confirm", callback_data=f"task|{task_id}|confirm")]
    ])


user_main_kb = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text="📖 Tasks")],
], resize_keyboard=True)