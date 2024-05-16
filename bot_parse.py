from pyrogram import Client, filters
from settings import Configs, manager, configure_logging
from pyrogram.types import Message, CallbackQuery

from constants import Commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from buttons.buttons import (
    admin_keyboard,
    data_collection_keyboard,
    main_menu_keyboard,
    time_keyboard
)
from permissions.permissions import (
    check_admin, check_superuser
)
from core.admin import create_admin, delete_admin, get_all_admins
from core.validation import validate_data_on_create, validate_data_on_delete
from services.get_data_tlg import (
    GetParticipantInfo, get_data, get_msg,
    get_channels, get_chat_invite_links, get_chat_link_joiners
)

logger = configure_logging()

bot_parse = Client(
    "my_account", api_id=Configs.API_ID,
    api_hash=Configs.API_HASH, bot_token=Configs.BOT_TOKEN
)

scheduler = AsyncIOScheduler()
scheduler.start()


@bot_parse.on_message(filters.command('start'))
async def command_start(
    client: Client,
    message: Message
):
    """Обработчик команды на запуск бота по сбору данных."""
    logger.info('Авторизация')
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
            reply_markup=main_menu_keyboard
        )
        logger.info(f'Пользователь {message.from_user.username} прошел авторизацию')


@bot_parse.on_message(filters.command('get_channels'))
async def get_channels_admin(client: Client, message: Message):
    """Недоработано. Метод возвращает все каналы владельца,
    на котором открыта сессия"""
    channels = await get_channels()
    msg = ''
    for channel in channels.chats:
        msg += (f'id канала: {channel.id}, '
                f'username: {channel.username}\n')
    await client.send_message(
        message.chat.id,
        msg
    )


@bot_parse.on_message(filters.command('get_joiners'))
async def get_joiners(client: Client, message: Message):
    """Недоработано. В телеграмме собрать все возможные пригласительные
    ссылки с канала может только владелец канал. Админ может собрать только
    свои ссылки. Тогда отчеты должен формировать только владелец канал, чтобы
    можно было собрать полный отчет по желанию заказчика"""
    links_lst = []
    joiners = {}
    objs = await get_chat_invite_links(chat_id='test_telestat2', admin_id='me')
    for obj in objs:
        links_lst.append(obj.invite_link)
    for link in links_lst:
        user = await get_chat_link_joiners(chat_id='test_telestat2', invite_link=link)
        joiners[link] = user
    msg = ''
    for k in joiners:
        for i in joiners[k]:
            msg += f'Ссылка: {k}, пользователь {i.user.username}\n'
    await client.send_message(message.chat.id, msg)


@bot_parse.on_message(filters.regex(Commands.back.value))
async def main_menu(
    client: Client,
    message: Message
):
    """Меню с основными разделами бота."""

    await client.send_message(
        message.chat.id,
        'Выберите раздел',
        reply_markup=main_menu_keyboard
    )


@bot_parse.on_message(filters.regex(Commands.admin_management.value))
async def admin_buttons(
    client: Client,
    message: Message
):
    """Действия, связанные с админами."""

    await client.send_message(
        message.chat.id,
        text='Выберите действие',
        reply_markup=admin_keyboard
    )


@bot_parse.on_message(filters.regex(Commands.add_admin.value))
async def new_admin(
    client: Client,
    message: Message
):
    """Добавление админа. Только суперпользователь!"""
    if not await check_superuser(message.from_user.id):
        await client.send_message(
            message.chat.id, 'Добавить админа может только суперпользователь!')
        logger.warning(f'Пользователь {message.from_user.username} пытался добавить админа')
    else:
        await client.send_message(
            message.chat.id,
            'Введите user_id и username администратора через запятую и пробел'
        )
        manager.add_admin_flag = True


@bot_parse.on_message(filters.regex(Commands.del_admin.value))
async def del_admin(
    client: Client,
    message: Message
):
    """Удаление админа. Только суперпользователь!"""
    if not await check_superuser(message.from_user.id):
        await client.send_message(
            message.chat.id, 'Удалить админа может только суперпользователь!')
        logger.warning(f'Пользователь {message.from_user.username} пытался удалить админа')
    else:
        await client.send_message(
            message.chat.id,
            'Введите user_id администратора'
        )
        manager.del_admin_flag = True


@bot_parse.on_message(filters.regex(Commands.all_admins.value))
async def all_admins(
    client: Client,
    message: Message
):
    """Список админов. Все админы могут пользоваться!"""
    if not await check_superuser(message.from_user.id):
        await client.send_message(
            message.chat.id, 'Получить список админов может только суперпользователь!')
        logger.warning(f'Пользователь {message.from_user.username} пытался получить список всех админов')
    else:
        admins_list = await get_all_admins()
        reply_message = ''
        for adm in admins_list:
            reply_message += (f'User_id админа: {adm.user_id}, '
                              f'username: {adm.username}\n')
        await client.send_message(
            message.chat.id,
            reply_message
        )
        logger.info('Получены все пользователи')


@bot_parse.on_message(filters.regex(Commands.collect_data.value))
async def data_collection_buttons(
    client: Client,
    message: Message
):
    """Действия, связанные со сбором данных."""

    await client.send_message(
        message.chat.id,
        text='Выберите действие',
        reply_markup=data_collection_keyboard
    )


@bot_parse.on_message(filters.regex(Commands.remove_job.value))
async def remove_job_button(
    client: Client,
    message: Message
):
    """Недоработано. Не получилось создать в БД таблицу с запланированными работами"""
    print(scheduler.get_job('test_telestat2'))
    await client.send_message(
        message.chat.id,
        text='Укажите id запланированной работы по сбору данных'
    )


@bot_parse.on_message(filters.regex(Commands.time_management.value))
async def time_management(client: Client, message: Message):
    """Настройка интервала и сбор данных. Только админы!"""
    if not await check_admin(message.from_user.id):
        await client.send_message(
            message.chat.id, 'Настраивать время и собирать данные может только админ!')
        logger.warning(f'Пользователь {message.from_user.username} пытался собрать данные')
    else:
        await client.send_message(
                message.chat.id,
                'Установите интервал сбора данных',
                reply_markup=time_keyboard
            )

    @bot_parse.on_callback_query()
    async def set_time(client: Client, callback: CallbackQuery):
        """Ловим колбэк с клавиатуры. Варианты: установленный интервал, свой
        интервал и без интервала"""
        manager.interval[callback.from_user.id] = callback.data
        msg = ''
        if manager.interval[callback.from_user.id] == 'custom':
            msg += 'Введите chat_id канала или группы. Через запятую с пробелом добавьте интервал в минутах'
        else:
            msg += 'Введите chat_id канала или группы'
        await client.delete_messages(message.chat.id, callback.message.id)
        await client.send_message(
            callback.message.chat.id,
            msg
        )
        manager.set_interval_flag[callback.from_user.id] = True


@bot_parse.on_message(filters.text)
async def all_incoming_messages(
    client: Client,
    message: Message,
    manager=manager
):
    """Ловим все сообщения в зависимости от наличия флага"""
    if manager.add_admin_flag:
        obj = await validate_data_on_create(message.text)
        if not obj:
            await client.send_message(
                message.chat.id,
                'Ошибка при валидации данных'
            )
            logger.warning('Ошибка при валидации данных')
        else:
            if not await create_admin(obj):
                await client.send_message(
                    message.chat.id,
                    'Админ с таким user_id уже существует'
                )
                logger.warning('Попытка создать админа с существующим user_id')
            else:
                await client.send_message(
                    message.chat.id,
                    'Новый админ создан'
                )
                logger.info('Добавлен новый админ')
            manager.add_admin_flag = False

    if manager.del_admin_flag:
        obj = await validate_data_on_delete(message.text)
        if not obj:
            await client.send_message(
                message.chat.id,
                'Ошибка при валидации данных'
            )
            logger.warning('Ошибка при валидации данных')
        else:
            if not await delete_admin(obj):
                await client.send_message(
                    message.chat.id,
                    'Админ с таким user_id не существует'
                )
                logger.warning('Попытка удалить несуществующего админа')
            else:
                await client.send_message(
                    message.chat.id,
                    f'Админ с user_id {obj} удален'
                )
                logger.info('Удален админ')
                manager.del_admin_flag = False

    if manager.set_interval_flag[message.from_user.id]:
        value = await get_msg(message, manager.interval[message.from_user.id])
        channel = GetParticipantInfo(
                client, value[0]
            )
        if value[1] == 'no_interval':
            await client.send_message(
                message.chat.id,
                'Собираю данные. Интервал не настроен. По окончании придет ссылка на файл',
                reply_markup=main_menu_keyboard
            )
            logger.info('Идет сбора данных')
            await get_data(channel, client, message)
        else:
            await client.send_message(
                message.chat.id,
                f'Собираю данные. Задача будет выполняться с заданным интервалом - {value[1]} мин. По окончании будет приходить ссылка на файл',
                reply_markup=main_menu_keyboard
            )
            logger.info('Идет сбор данных')
            await get_data(channel, client, message)
            scheduler.add_job(get_data, 'interval', minutes=int(value[1]), kwargs={'channel': channel, 'client': client, 'message': message}, id=value[0] + f'_{message.from_user.id}', replace_existing=True)
            logger.info(f'Запланирован сбор данных с интервалом {value[1]} минут')
            logger.info(scheduler.print_jobs())
        del manager.interval[message.from_user.id]
        del manager.set_interval_flag[message.from_user.id]
