import asyncio
from bot_parse import bot_parse
from core.init_db import create_super_user



def main():
    bot_parse.run()


loop = asyncio.get_event_loop()
tasks = [
    loop.create_task(create_super_user()),
    loop.create_task(main())
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()