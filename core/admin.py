from settings import Config

async def get_users_channel(client):
    user_data = []
    async for member in client.get_chat_members(Config.CHANNEL_ID):
        #user_info = await bot_parse.get_users(member.user.id)
        #chat_member = await bot_parse.get_chat_member(chat_id, user_info.id)
        photo_file_id = None
        if member.user.photo:
            photo_file_id = member.user.photo.big_file_id

        user_data.append({
            "ID": member.user.id,
            "Username": member.user.username,
            "First Name": member.user.first_name,
            "Last Name": member.user.last_name,
            "Is Bot": member.user.is_bot,
            "Joined Date": member.joined_date.strftime(
             "%Y-%m-%d %H:%M:%S") if member.joined_date else None,
            "Profile Photo File ID": photo_file_id,
            "Phone number": member.user.phone_number,
            "Language code": member.user.language_code
        })

    return user_data


async def get_users_channels(client):
    member_count = await client.get_chat_members_count(Config.CHANNEL_ID)
    return member_count
