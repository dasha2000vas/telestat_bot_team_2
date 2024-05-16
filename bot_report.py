from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Message
from settings import Configs, manager, configure_logging
from constants import Commands
from services.google_api_services import (
    get_all_files, get_sheet_lists, get_data_from_lists,
    delete_all_files_by_name
)
from services.get_data_tlg import get_activity
from buttons.buttons import report_menu_keyboard

from permissions.permissions import check_admin

logger = configure_logging()

bot_report = Client(
    'report_acc',
    api_id=Configs.API_ID,
    api_hash=Configs.API_HASH,
    bot_token=Configs.BOT_TOKEN_REPORT
)


@bot_report.on_message(filters.command('start'))
async def command_start(
    client: Client,
    message: Message
):
    """Обработчик команды на запуск бота по сбору данных."""
    if not await check_admin(message.from_user.id):
        await client.send_message(
            message.chat.id,
            'Управлять ботом могут только Администраторы.'
        )
        logger.warning(f'Пользователь {message.from_user.username} не прошел авторизацию')
    else:
        await client.send_message(
            message.chat.id,
            'Вы прошли авторизацию!',
            reply_markup=report_menu_keyboard
        )
        logger.info(f'Пользователь {message.from_user.username} прошел авторизацию')


@bot_report.on_message(filters.command('delete_sheet'))
async def delete_sheet(
    client: Client,
    message: Message
):
    """Метод использовался при разработке"""
    await delete_all_files_by_name()


@bot_report.on_message(filters.regex(Commands.request_report.value))
async def report(
    client: Client,
    message: Message
):
    """Формирование отчета. Только админы!"""
    if not await check_admin(message.from_user.id):
        await client.send_message(
            message.chat.id, 'Сформировать отчет может только админ!')
        logger.warning(f'Пользователь {message.from_user.username} пытался сформировать отчет')
    else:
        await client.send_message(
            message.chat.id,
            'Введите название канала',
        )
        manager.set_report_flag[message.from_user.id] = True


@bot_report.on_message(filters.text)
async def all_incoming_messages(
    client: Client,
    message: Message,
    manager=manager
):
    """Ловим все сообщения в зависимости от наличия флага"""
    if manager.set_report_flag[message.from_user.id]:
        manager.report[message.from_user.id] = message.text
        await client.send_message(message.chat.id, 'Идет формирование отчета')
        logger.info(f'Идет формирование отчета канала {manager.report[message.from_user.id]}')
        files = await get_all_files()
        res = await get_sheet_lists(files[manager.report[message.from_user.id]])
        data = await get_data_from_lists(files[manager.report[message.from_user.id]], res)
        activity = await get_activity(manager.report[message.from_user.id])
        msg = ''
        for k in data:
            msg = (f'Отчет по каналу {manager.report[message.from_user.id]}\n'
                   f'Кол-во подписчиков: {data[max(data)]}\n'
                   f'Приток/отток подписчиков: {data[max(data)] - data[min(data)]}\n'
                   f'Среднее количество просмотров: {activity["avg_views"]}\n'
                   f'Среднее количество реакций: {activity["avg_reactions"]}\n'
                   f'Среднее количество репостов: {activity["avg_forwards"]}\n'
                   )
        await client.send_message(message.chat.id, msg)
        logger.info(f'Формирование отчета по каналу {manager.report[message.from_user.id]} завершено')
        del manager.set_report_flag[message.from_user.id]
        del manager.report[message.from_user.id]
