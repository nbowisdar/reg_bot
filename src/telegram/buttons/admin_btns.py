from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb1 = [
    [KeyboardButton(text="Show all emails"), KeyboardButton(text="Receive message")],
    [KeyboardButton(text="Create new email")]
]

email_kb = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)

kb1 = [
    [KeyboardButton(text="Show all numbers"), KeyboardButton(text="Receive message")],
    [KeyboardButton(text="Create new number")]
]

phone_kb = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)


kb2 = [
    [KeyboardButton(text="Cancel")]
]

cancel_kb = ReplyKeyboardMarkup(
    keyboard=kb2,
    resize_keyboard=True
)