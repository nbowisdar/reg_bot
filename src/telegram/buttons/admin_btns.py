from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from src.database.tables import Template

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


sex_inl = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🙎‍♂️", callback_data=f"choose_sex|🙎‍♂️"),
     InlineKeyboardButton(text="🙎‍♀️", callback_data=f"choose_sex|🙎‍♀️"),
    ]
])


sex_inl_out = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🙎‍♂️", callback_data=f"out_sex|🙎‍♂️"),
     InlineKeyboardButton(text="🙎‍♀️", callback_data=f"out_sex|🙎‍♀️"),
     InlineKeyboardButton(text="❓", callback_data=f"out_sex|❓"),
    ]
])


def ready_action_inl(sr_type) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Add", callback_data=f"ready|add|{sr_type}"),
         InlineKeyboardButton(text="✂️ Take away", callback_data=f"ready|take|{sr_type}")]
    ]
    )

hide_inl_btn = InlineKeyboardButton(text="↙️ Hide", callback_data=f"hide")

##############

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Email"), KeyboardButton(text="Number")],
        [KeyboardButton(text="📖 Tasks"), KeyboardButton(text="🤖 AI")]
    ],
    resize_keyboard=True
)

ai_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📒 Templates"), KeyboardButton(text="💽 json")],
    [KeyboardButton(text="⬅️ Back")]], resize_keyboard=True
)


json_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="⬇️ Get"), KeyboardButton(text="⬆️ Upload")],
    [KeyboardButton(text="↩️ Back")]], resize_keyboard=True
)


temp_first_inl = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🆕 Create", callback_data="new_template"),
     InlineKeyboardButton(text="📃 Show & Modify", callback_data="templates")]
    ]
)


def get_templates_inl() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for temp in Template.select():
        builder.row(InlineKeyboardButton(
            text=f'{temp.id}) {temp.name}', callback_data=f'get_temp|{temp.id}'
        ))
    builder.row(hide_inl_btn)
    return builder.as_markup()


def change_template_inl(temp_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    temp = Template.get_by_id(temp_id)
    builder.row(
        InlineKeyboardButton(
            text=f'👀 Show', callback_data=f'change_temp|{temp.id}|show'
        ),
        InlineKeyboardButton(
            text=f'🛠️ Update', callback_data=f'change_temp|{temp.id}|update'
        ),
        InlineKeyboardButton(
            text=f'♻️ Delete', callback_data=f'change_temp|{temp.id}|delete'
        ),
    )
    builder.row(hide_inl_btn)
    return builder.as_markup()


def template_action_inl(temp_id, action) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    temp = Template.get_by_id(temp_id)
    builder.row(
        InlineKeyboardButton(
            text=f'📒 Template', callback_data=f'temp_action|{temp.id}|{action}|template'
        ),
        InlineKeyboardButton(
            text=f'📚 Replies', callback_data=f'temp_action|{temp.id}|{action}|triggers'
        )
    )
    builder.row(hide_inl_btn)
    return builder.as_markup()



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

# KeyboardButton(text="In work")
kb1 = [
    [KeyboardButton(text="All emails"), KeyboardButton(text="Ready emails")],
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
