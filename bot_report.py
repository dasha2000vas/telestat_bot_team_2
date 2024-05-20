from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
from settings import Configs, manager
from constants import Commands
from services.google_api_services import (
    get_all_files, get_sheet_lists, get_data_from_lists,
    delete_all_files_by_name
)
from services.get_data_tlg import get_activity
from buttons.buttons import report_menu_keyboard, make_inline_keyboard_report

from permissions.permissions import check_admin


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
    else:
        await client.send_message(
            message.chat.id,
            'Вы прошли авторизацию!',
            reply_markup=report_menu_keyboard
        )


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
    else:
        manager.files[message.from_user.id] = await get_all_files()
        await client.send_message(
            message.chat.id,
            'Введите название канала',
            reply_markup=await make_inline_keyboard_report(manager.files[message.from_user.id])
        )
        manager.set_report_flag[message.from_user.id] = True


# @bot_report.on_message(filters.text)
@bot_report.on_callback_query()
async def all_incoming_messages(
    client: Client,
    callback: CallbackQuery,
    manager=manager
):
    """Ловим все сообщения в зависимости от наличия флага"""
    if manager.set_report_flag[callback.from_user.id]:
        manager.report[callback.from_user.id] = callback.data
        username = ''
        for name in manager.files[callback.from_user.id]:
            if manager.files[callback.from_user.id][name] == callback.data:
                username = name
        await callback.edit_message_text('Идет формирование отчета', reply_markup=None)
        res = await get_sheet_lists(manager.report[callback.from_user.id])
        data = await get_data_from_lists(manager.report[callback.from_user.id], res)
        activity = await get_activity(username)
        msg = ''
        for k in data:
            msg = (f'Отчет по каналу {username}\n'
                   f'Кол-во подписчиков: {data[max(data)]}\n'
                   f'Приток/отток подписчиков: {data[max(data)] - data[min(data)]}\n'
                   f'Среднее количество просмотров: {activity["avg_views"]}\n'
                   f'Среднее количество реакций: {activity["avg_reactions"]}\n'
                   f'Среднее количество репостов: {activity["avg_forwards"]}\n'
                   )
        await client.send_message(callback.message.chat.id, msg)
        del manager.set_report_flag[callback.from_user.id]
        del manager.report[callback.from_user.id]
        del manager.files[callback.from_user.id]
