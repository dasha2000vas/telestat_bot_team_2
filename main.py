import asyncio
from bot_parse import bot_parse
from core.init_db import create_super_user


def main():
    bot_parse.run()


loop = asyncio.get_event_loop()
loop.run_until_complete(create_super_user())
loop.run_forever(main())
loop.close()
