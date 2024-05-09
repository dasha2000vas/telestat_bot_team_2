from pyrogram import Client
from constants import COUNTRY_CODES, LANGUAGE_CODES


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
            # phone_number = member.user.phone_number
            # language_code = member.user.language_code
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
        # member_count = await self.bot.get_chat_members_count(self.value)
        return await self.bot.get_chat_members_count(self.value)


async def get_country(member_data):
    if member_data.get("phone_number"):
        # phone_country = await get_country_phone_number(
        #     member_data["phone_number"]
        #     )
        return await get_country_phone_number(
            member_data["phone_number"]
            )
    elif member_data.get("language_code"):
        # language_country = await get_country_language_code(
        #     member_data["language_code"]
        #     )
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
