from setup import bot_notify, support_id


async def end_message_to_support(text: str):
    await bot_notify.send_message(support_id, text)
