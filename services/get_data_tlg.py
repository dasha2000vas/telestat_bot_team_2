from pyrogram import Client
from constants import COUNTRY_CODES, LANGUAGE_CODES
import os
from settings import Config
from aiogoogle import Aiogoogle
from pyrogram.raw import functions
from settings import bot_user, user_bot
from services.google_api_services import (
    check_spreadsheet_exist,
    create_sheet,
    create_spreadsheet,
    spreadsheet_update_values
)


class GetParticipantInfo():
    """Класс для получения информации о пользователях группы/канала"""

    def __init__(
        self,
        bot: Client,
        value: str,
    ):
        self.bot = bot
        self.value = value

    async def get_members_channel(self):
        member_data = []
        async for member in self.bot.get_chat_members(self.value):
            photo_file_id = None
            if member.user.photo:
                photo_file_id = member.user.photo.big_file_id
            country = await get_country(
                {"phone_number": member.user.phone_number,
                 "language_code": member.user.language_code}
                )

            member_data.append({
                "ID": member.user.id,
                "Username": member.user.username,
                "First Name": member.user.first_name,
                "Last Name": member.user.last_name,
                "Is Bot": member.user.is_bot,
                "Joined Date": member.joined_date.strftime(
                    "%Y-%m-%d %H:%M:%S") if member.joined_date else None,
                "Profile Photo File ID": photo_file_id,
                "Phone number": member.user.phone_number,
                "Language code": member.user.language_code,
                "Country": country
            })

        return member_data

    async def get_members_count(self):
        return await self.bot.get_chat_members_count(self.value)


async def get_country(member_data):
    if member_data.get("phone_number"):
        return await get_country_phone_number(
            member_data["phone_number"]
            )
    elif member_data.get("language_code"):
        return await get_country_language_code(
            member_data["language_code"]
            )
    else:
        return "Неизвестно"


async def get_country_phone_number(phone_number):
    for code, country in COUNTRY_CODES.items():
        if phone_number.startswith(code):
            return country
    return "Неизвестно"


async def get_country_language_code(language_code):
    return LANGUAGE_CODES.get(language_code, "Неизвестно")


async def get_data(channel, client, message):
    member_list = await channel.get_members_channel()
    total_members = await channel.get_members_count()
    file_name = "user_data.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"Total Users: {total_members}\n\n")
        for user in member_list:
            file.write(f"ID: {user['ID']}\n")
            file.write(f"Username: {user['Username']}\n")
            file.write(f"First Name: {user['First Name']}\n")
            file.write(f"Last Name: {user['Last Name']}\n")
            file.write(f"Is Bot: {user['Is Bot']}\n")
            file.write(f"Joined Date: {user['Joined Date']}\n")
            file.write(f"Profile Photo File ID: {user['Profile Photo File ID']}\n")
            file.write(f"Phone number: {user['Phone number']}\n")
            file.write(f"Language code: {user['Language code']}\n")
            file.write(f"Country: {user['Country']}\n\n")

    await client.send_document(message.chat.id, file_name)
    await client.send_message(
        message.chat.id, f"Собрано информации о {total_members} пользователях.")
    os.remove(file_name)
    async with Aiogoogle(
        service_account_creds=Config.CREDENTIALS
    ) as wrapper_services:
        spreadsheet_id = await check_spreadsheet_exist(
            wrapper_services, channel.value
        )
        if not spreadsheet_id:
            spreadsheet_id, sheet_name = await create_spreadsheet(
                wrapper_services, channel.value
            )
        else:
            sheet_name = await create_sheet(
                wrapper_services, spreadsheet_id
            )
        await spreadsheet_update_values(
            wrapper_services, spreadsheet_id,
            member_list, sheet_name
        )
        await client.send_message(
            message.chat.id,
            f"Собрано информации о {total_members} пользователях. Ссылка на файл:"
            f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
        )


async def get_msg(msg, interval):
    lst = msg.text.split(', ')
    if len(lst) == 2:
        return lst
    else:
        return [msg.text, interval]


@bot_user
async def get_channels(bot: Client = user_bot):
    """Получение телеграмм каналов."""
    return (await bot.invoke(
        (functions.channels.get_admined_public_channels.GetAdminedPublicChannels())))


@bot_user
async def get_chat_link_joiners(chat_id: str, invite_link: str, bot: Client = user_bot):
    joiners = bot.get_chat_invite_link_joiners(chat_id, invite_link)
    users = []
    async for user in joiners:
        users.append(user)
    return users


@bot_user
async def get_chat_invite_links(chat_id: str, admin_id: str, bot: Client = user_bot):
    links = bot.get_chat_admin_invite_links(chat_id, admin_id)
    items = []
    async for item in links:
        items.append(item)
    return items
