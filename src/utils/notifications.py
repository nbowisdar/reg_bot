from setup import bot, support_id


async def end_message_to_support(text: str):
    await bot.send_message(support_id, text)
