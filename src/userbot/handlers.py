from pyrogram import Client

app = Client("my_account")


@app.on_message()
async def my_handler(client, message):
    await message.forward("me")


app.run()