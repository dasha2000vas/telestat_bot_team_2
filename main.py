import asyncio
from bot_parse import bot_parse
from bot_report import bot_report
from core.init_db import create_super_user
from pyrogram.methods.utilities.compose import compose
from settings import configure_logging

logger = configure_logging()


async def main():
    logger.info('Бот запущен!')
    apps = [
        bot_parse,
        bot_report,
    ]

    await compose(apps)

loop = asyncio.get_event_loop()
loop.run_until_complete(create_super_user())
loop.run_until_complete(main())
loop.close()
logger.info('Бот завершил работу.')
