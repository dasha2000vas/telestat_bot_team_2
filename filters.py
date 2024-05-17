from pyrogram import filters


async def set_time_filter(_, __, query):
    return query.data in ["1", "300", "600", "900", "1440", "custom", "no_interval"]

time_filter = filters.create(set_time_filter)
