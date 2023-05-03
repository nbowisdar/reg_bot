from pyrogram import Client, filters

from setup import API_ID, API_HASH

app = Client("sessions/ai_bot", API_ID, API_HASH)


@app.on_message(filters.text & filters.private)
async def echo(client, message):
    await message.reply(message.text)


app.run()  # Automatically start() and idle()