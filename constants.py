from settings import Config
from enum import Enum

COUNTRY_CODES = {
    "1": "USA",
    "44": "UK",
    "33": "France",
    "7": "Russia",
    "9": "Russia",
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
    "en": "English",
    "fr": "French",
    "ru": "Russia",
    "es": "Spain",
    "de": "Germany",
    "it": "Italy",
    "zh": "China",
    "ja": "Japan",
    "ko": "Korea",
    "pt": "Portugal",
}

SUPERUSER = {
    'user_id': Config.MY_ID,
    'username': Config.MY_USERNAME,
    'is_superuser': True,
    'is_admin': True
}


class Commands(Enum):
    admin_management = 'Управление админами'
    add_admin = 'Добавить админа'
    del_admin = 'Удалить админа'
    all_admins = 'Все админы'
    collect_data = 'Cбор данных'
    run_data_collection = 'Начать сбор данных'
    time_management = 'Задать интервал сбора данных'
    back = 'Назад'
