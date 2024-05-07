import os
from pyrogram import Client, filters
from settings import Config
from pyrogram.types import Message
from permissions.permissions import check_authorization, create_admin
from core.admin import get_users_channel, get_users_channels

bot_parse = Client(
    "my_account", api_id=Config.API_ID,
    api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN
)


@bot_parse.on_message(filters.command('start'))
async def command_start(
    client: Client,
    message: Message
):
    """Обработчик команды на запуск бота по сбору данных."""

    if not await check_authorization(message.from_user.id):
        await client.send_message(
            message.chat.id,
            'Управлять ботом могут только Администраторы.'
        )
    else:
        await client.send_message(
            message.chat.id,
            'Вы прошли авторизацию!',
        )

        @bot_parse.on_message(filters.command('new_admin'))
        async def new_admin(
            client: Client,
            message: Message
        ):
            await client.send_message(
                message.chat.id,
                'Введите user_id и username администратора через запятую'
            )

            @bot_parse.on_message(filters.text)
            async def get_user(
                client: Client,
                message: Message
            ):
                user = message.text.split(', ')
                data = {
                    'user_id': int(user[0]),
                    'username': user[1],
                    'is_admin': True
                }
                if not await create_admin(data):
                    await client.send_message(
                        message.chat.id,
                        'Ошибка'
                    )
                else:
                    await client.send_message(
                        message.chat.id,
                        'Новый админ создан'
                    )

@bot_parse.on_message(filters.command('parsing_info'))
async def parsing_info(client: Client, message: Message):
    chat_id = message.chat.id
    user_data = await get_users_channel(client)
    total_users = len(user_data)
    file_name = "user_data.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"Total Users: {total_users}\n\n")
        for user in user_data:
            file.write(f"ID: {user['ID']}\n")
            file.write(f"Username: {user['Username']}\n")
            file.write(f"First Name: {user['First Name']}\n")
            file.write(f"Last Name: {user['Last Name']}\n")
            file.write(f"Is Bot: {user['Is Bot']}\n")
            file.write(f"Joined Date: {user['Joined Date']}\n")
            file.write(f"Profile Photo File ID: {user['Profile Photo File ID']}\n\n")

    await client.send_document(chat_id, file_name)
    os.remove(file_name)

@bot_parse.on_message(filters.command('parsing_count'))
async def parsing_count(client: Client, message: Message):
    chat_id = message.chat.id
    user_count = await get_users_channels(client)
    await client.send_message(chat_id, f"Собрано информации о {user_count} пользователях.")
