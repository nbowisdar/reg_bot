from multiprocessing import Process

from loguru import logger
from pyrogram import Client, filters
from pyrogram import types
from setup import API_ID, API_HASH, prod
from src.database.tables import Trigger
from src.utils.grammar import correct_text
from src.utils.notifications import end_message_to_support


userbot_app = Client("sessions/ai_bot", API_ID, API_HASH)


@userbot_app.on_message(filters.text & filters.private)
async def echo(client, message: types.Message):

    if prod:
        corrected_text = await correct_text(message.text)
    else:
        corrected_text = message.text

    count = 0
    temp = None
    cur_temp = None
    for trig in Trigger.select():
        if trig.phrase in corrected_text.casefold() and trig.template != cur_temp:
            temp = trig.template.text
            count += 1
            cur_temp = trig.template
            # await message.reply(trig.template.text)
    if count == 1 and temp:
        await message.reply(temp)
        return
    if count > 1:
        type_error = "🛑Contains more then one trigger"
    else:
        type_error = "🛑Doesn't contain any trigger"

    msg = f"❗️ New messages from user @{message.from_user.username} ❗️\n" \
          f'Message: \n"{corrected_text}"\n\n{type_error}'
    await end_message_to_support(msg)


# run option

def start_userbot():
    userbot_app.run()


def run_userbot():
    proc = Process(target=start_userbot)
    proc.start()
    logger.info("Userbot started!")


if __name__ == '__main__':
    start_userbot()