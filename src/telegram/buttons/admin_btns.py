from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb0 = [
    [KeyboardButton(text="Email"), KeyboardButton(text="Number")]
]

main_kb = ReplyKeyboardMarkup(
    keyboard=kb0,
    resize_keyboard=True
)


kb1 = [
    [KeyboardButton(text="Show all emails"), KeyboardButton(text="Receive message")],
    [KeyboardButton(text="Create new email"), KeyboardButton(text="Delete email")],
    [KeyboardButton(text="Go back")]
]

email_kb = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)

kb1 = [
    [KeyboardButton(text="Show all numbers"), KeyboardButton(text="Receive msg")],
    [KeyboardButton(text="Create new number"), KeyboardButton(text="Delete number")],
    [KeyboardButton(text="Show balance"), KeyboardButton(text="Go back")]
]

phone_kb = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Cancel")]],
    resize_keyboard=True
)

cancel_and_delete_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Cancel"), KeyboardButton(text='Delete all')]],
    resize_keyboard=True
)


cancel_kb_number = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Cancel number")]],
    resize_keyboard=True
)


skip_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Skip"), KeyboardButton(text="Cancel")]],
    resize_keyboard=True
)


how_many_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="1"), KeyboardButton(text="Cancel")]],
    resize_keyboard=True
)


service_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Google (gmail)"), KeyboardButton(text="Uber")]],
    resize_keyboard=True
)