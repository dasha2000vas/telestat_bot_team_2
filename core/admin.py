from settings import Config
from constants import COUNTRY_CODES, LANGUAGE_CODES


async def get_users_channel(client):
    user_data = []
    async for member in client.get_chat_members(Config.CHANNEL_ID):
        photo_file_id = None
        if member.user.photo:
            photo_file_id = member.user.photo.big_file_id
        phone_number = member.user.phone_number
        language_code = member.user.language_code
        country = await get_country({"phone_number": phone_number, "language_code": language_code})

        user_data.append({
            "ID": member.user.id,
            "Username": member.user.username,
            "First Name": member.user.first_name,
            "Last Name": member.user.last_name,
            "Is Bot": member.user.is_bot,
            "Joined Date": member.joined_date.strftime(
             "%Y-%m-%d %H:%M:%S") if member.joined_date else None,
            "Profile Photo File ID": photo_file_id,
            "Phone number": phone_number,
            "Language code": language_code,
            "Country": country
        })

    return user_data


async def get_users_channels(client):
    member_count = await client.get_chat_members_count(Config.CHANNEL_ID)
    return member_count


async def get_country(user_data):
    if user_data.get("phone_number"):
        phone_country = await get_country_phone_number(user_data["phone_number"])
        return phone_country
    elif user_data.get("language_code"):
        language_country = await get_country_language_code(user_data["language_code"])
        return language_country
    else:
        return "Неизвестно"


async def get_country_phone_number(phone_number):
    for code, country in COUNTRY_CODES.items():
        if phone_number.startswith(code):
            return country
    return "Неизвестно"


async def get_country_language_code(language_code):
    return LANGUAGE_CODES.get(language_code, "Неизвестно")
