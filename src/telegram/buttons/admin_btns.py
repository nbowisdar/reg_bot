from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

cancel_skip_admin_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Skip")],
    [KeyboardButton(text="❌ Cancel")]
], resize_keyboard=True)


ready_type_inl = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Uber", callback_data=f"choose_ready_type|Uber"),
     InlineKeyboardButton(text="Lyft", callback_data=f"choose_ready_type|Lyft"),
     InlineKeyboardButton(text="Doorsdash", callback_data=f"choose_ready_type|Doorsdash")]
    ]
)


def ready_action_inl(sr_type) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Add", callback_data=f"ready|add|{sr_type}"),
         InlineKeyboardButton(text="✂️ Take away", callback_data=f"ready|take|{sr_type}")]
    ]
    )

hide_inl_btn = InlineKeyboardButton(text="↙️ Hide", callback_data=f"hide")

##############
kb0 = [
    [KeyboardButton(text="Email"), KeyboardButton(text="Number")],
    [KeyboardButton(text="📖 Tasks")]
]

main_kb = ReplyKeyboardMarkup(
    keyboard=kb0,
    resize_keyboard=True
)


task_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="New task"), KeyboardButton(text="Show active")],
    [KeyboardButton(text="⬅️ Back")]], resize_keyboard=True
)


def build_ready_emails_kb(emails: list[str]):
    builder = InlineKeyboardBuilder()
    for email in emails:
        builder.row(InlineKeyboardButton(
            text=email, callback_data=f'read_email|{email}'
        ))
    builder.row(hide_inl_btn)
    return builder.as_markup()


kb1 = [
    [KeyboardButton(text="All emails"), KeyboardButton(text="Ready"), KeyboardButton(text="In work")],
    [KeyboardButton(text="Receive message"), KeyboardButton(text="Create new email")],
    [KeyboardButton(text="Delete email"), KeyboardButton(text="Go back")]
]

email_kb = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)


def build_web_app_kb() -> InlineKeyboardMarkup:
    app = WebAppInfo(url="https://134.209.127.175:8000/message_in_tg")
    # app = WebAppInfo(url="/message_in_tg")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Watch full message", web_app=app)]
        ]
    )


kb2 = [
    [KeyboardButton(text="Show all numbers"), KeyboardButton(text="Receive msg")],
    [KeyboardButton(text="Create new number"), KeyboardButton(text="Delete number")],
    [KeyboardButton(text="Show balance"), KeyboardButton(text="Go back")]
]

phone_kb = ReplyKeyboardMarkup(
    keyboard=kb2,
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

cancel_and_delete_email_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Cancel"), KeyboardButton(text='🗑 Delete list of emails')]],
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
    keyboard=[[KeyboardButton(text="Google (gmail)"), KeyboardButton(text="Uber")],
              [KeyboardButton(text="Lyft"), KeyboardButton(text="Cancel")]],
    resize_keyboard=True
)
