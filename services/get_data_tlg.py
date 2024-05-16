from pyrogram import Client
from constants import COUNTRY_CODES, LANGUAGE_CODES
from settings import Configs, configure_logging
from aiogoogle import Aiogoogle
from pyrogram.raw import functions
from settings import bot_user, user_bot
from services.google_api_services import (
    check_spreadsheet_exist,
    create_sheet,
    create_spreadsheet,
    spreadsheet_update_values,
)
from string import ascii_lowercase

logger = configure_logging()


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
        collected_data = []
        member_list = []
        photo_file_id = None
        characters = [''] + [str(i) for i in range(10)] + [i for i in ascii_lowercase]
        for q in characters:
            async for member in self.bot.get_chat_members(
                self.value, query=q
            ):
                if member not in collected_data:
                    collected_data.append(member)

        for user in collected_data:
            try:
                photo_file_id = user.user.photo.big_file_id
            except AttributeError:
                photo_file_id = 'Фото отсутствует'
            country = await get_country(
                {"phone_number": user.user.phone_number,
                    "language_code": user.user.language_code}
                )

            member_list.append({
                "ID": user.user.id,
                "Username": user.user.username,
                "First Name": user.user.first_name,
                "Last Name": user.user.last_name,
                "Is Bot": user.user.is_bot,
                "Joined Date": user.joined_date.strftime(
                    "%Y-%m-%d %H:%M:%S") if user.joined_date else 'Отсутствует',
                "Profile Photo File ID": photo_file_id,
                "Phone number": user.user.phone_number,
                "Language code": user.user.language_code,
                "Country": country
            })

        return member_list

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
    async with Aiogoogle(
        service_account_creds=Configs.CREDENTIALS
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
            f"Собрана информация о {len(member_list)} пользователях. Ссылка на файл:\n"
            f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
        )
        logger.info(f'Собрана информация о {len(member_list)} пользователях')


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


@bot_user
async def get_chat_messages(chat_id):
    """Возвращает последние сообщения"""
    last_messages = []
    async for message in user_bot.get_chat_history(chat_id):
        last_messages.append(message)
    logger.info('Собраны последние сообщения')
    return last_messages


async def get_activity(chat_id):
    """Возвращает количество просмотров/реакций/репостов"""
    reactions = []
    views = []
    forwards = []
    for activity in await get_chat_messages(chat_id):
        if activity.reactions:
            for reaction in activity.reactions.reactions:
                try:
                    if reaction.count:
                        reactions.append(reaction.count)
                except AttributeError:
                    pass
        try:
            if activity.forwards:
                forwards.append(activity.forwards)
        except AttributeError:
            pass
        try:
            if activity.views:
                views.append(activity.views)
        except AttributeError:
            pass

    data = {
        'avg_views': 0 if len(views) == 0 else round(sum(views)/len(views), 2),
        'avg_reactions': 0 if len(reactions) == 0 else round(sum(reactions)/len(reactions), 2),
        'avg_forwards': 0 if len(forwards) == 0 else round(sum(forwards)/len(forwards), 2)
        }
    logger.info('Собраны данные о последних активностях')
    return data
