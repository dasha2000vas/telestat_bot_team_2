# telestat_bot_team_2
<h4>Telestat - это Telegram-Бот для маркетинговых исследований телеграм каналов. Один бот(bot_parse) парсит информацию о подписчиках выбранного канала, сохраняет ее в google таблицу, второй(bot_report) - выводит отчет в чате.</h4>

Доступ к ботам имеют только админы, сохраненные в базе данных. Добавить админа может только суперпользователь, который создается при инициализации базы данных.

В проекте доступны следующие функции: bot_parse - добавление, удаление и получение админов, настройка интервала автоматического сбора данных и запуск сбора данных в google-таблицу, bot_report - формирование отчета на основе google-таблицы и отправка его в чат. Для обоих ботов настроено логирование.

---

## Как скачать и запустить проект:

1. **Клонировать репозиторий и перейти в папку с ним:**

```bash
git clone git@github.com:dasha2000vas/telestat_bot_team_2.git
cd telestat_bot_team_2
```

2. **Создать и заполнить файл .env:**

```python
DB_URL = sqlite+aiosqlite:///./admins.db
MY_ID = id_владельца_бота
MY_USERNAME = username_владельца_бота
MY_PHONE = телефонный_номер_владельца_бота
EMAIL = электронный_адрес_которому_будет_предоставлен_доступ_к_google-таблице
```

Создать ботов и получить их токены с помощью BotFather:

```python
BOT_TOKEN = токен_бота-парсера
BOT_TOKEN_REPORT = токен_бота_для_получения_отчета
```

Войти на сайте https://my.telegram.org/. Перейти в раздел API development tools, создать новое приложение(new application). Под заголовком App Configuration будут необходимые api_id и api_hash.

```python
API_ID = 
API_HASH = 
```

Получить JSON-файл с ключом доступа к сервисному аккаунту на Google Cloud Platform. Перенести информацию из этого файла в .env:

```python
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
```

3. **Создать и активировать виртуальное окружение:**

```bash
python -m venv venv
source venv/Scripts/activate
```

4. **Установить зависимости из файла requirements.txt:**

```bash
pip install -r requirements.txt
```

5. **Применить миграции для таблиц:**

```bash
alembic upgrade head
```

6. **Запустить бот:**

```bash
python main.py 
```

---

## Технический стек:

* aiogoogle5.7.0
* aiosqlite0.20.0
* alembic1.13.1
* Pyrogram2.0.106
* SQLAlchemy2.0.29

---

## Авторы

| Имя  | GitHub |
| ------------- | :-----: |
| Олег Карапоткин (тимлид) | [✔️](https://github.com/VanDerMusculus) |
| Павел Кошкаров | [✔️](https://github.com/pavel-koshkarov3) |
| Дарья Василевская | [✔️](https://github.com/dasha2000vas) |
| Алексей Комков | [✔️](https://github.com/KomkovAleksey) |
| Максим | [✔️](https://github.com/Maxis1981) |
