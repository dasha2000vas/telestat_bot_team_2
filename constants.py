from enum import Enum
"""Два словаря для определения страны пользователя по номеру телефона или
языку. Если скрыто, то страна - Неизвестно"""
COUNTRY_CODES = {
    "1": "USA",
    "44": "UK",
    "33": "France",
    "7": "Russia",
    "964": "Iraq",
    "49": "Germany",
    "86": "China",
    "81": "Japan",
    "82": "Korea",
    "39": "Italy",
    "34": "Spain",
    "351": "Portugal",
    "375": "Belarus",
}

LANGUAGE_CODES = {
    "en": "Europe/USA",
    "fr": "France",
    "ru": "Russia",
    "es": "Spain",
    "de": "Germany",
    "it": "Italy",
    "zh": "China",
    "ja": "Japan",
    "ko": "Korea",
    "pt": "Portugal",
}


class Commands(Enum):
    """Команды для хэндлеров"""
    admin_management = 'Управление админами'
    add_admin = 'Добавить админа'
    del_admin = 'Удалить админа'
    all_admins = 'Все админы'
    collect_data = 'Сбор данных'
    time_management = 'Настройка интервала и сбор данных'
    remove_job = 'Отменить сбор данных'
    back = 'Назад'
    request_report = 'Сформировать отчет'


class BotParseManager:
    """Флаги для перехвата всех сообщений"""
    add_admin_flag = False
    del_admin_flag = False
    set_interval_flag = {1: False}
    interval = {}
    set_report_flag = {1: False}
    report = {}
    files = {}
    set_channel_flag = {1: False}
