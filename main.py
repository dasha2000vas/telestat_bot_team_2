import os
from dotenv import load_dotenv
from pyrogram import Client, filters

load_dotenv()

tg_id = os.getenv('TELEGRAM_ID')
tg_hash = os.getenv('TELEGRAM_HASH')
bot_tk = os.getenv('BOT_TOKEN')


app = Client("my_account", api_id=tg_id, api_hash=tg_hash, bot_token=bot_tk)


@app.on_message(filters.text & filters.private)
async def echo(client, message):
    await message.reply(message.text)

app.run()
