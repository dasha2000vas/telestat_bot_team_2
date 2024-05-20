from datetime import datetime
from aiogoogle import Aiogoogle

from settings import Configs, configure_logging

logger = configure_logging()


async def set_user_permissions(wrapper_services, spreadsheetId):
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': Configs.EMAIL
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetId,
            json=permissions_body,
            fields='id'
        ))


async def check_spreadsheet_exist(wrapper_services, title):
    """
    Функция для проверки существования таблицы.
    """
    service = await wrapper_services.discover('drive', 'v3')
    response = await wrapper_services.as_service_account(
        service.files.list(
            q='mimeType="application/vnd.google-apps.spreadsheet"'
        )
    )
    for file in response['files']:
        if file['name'] == title:
            logger.info(f'Обнаружено файл с именем {title}')
            return file['id']


async def create_sheet(wrapper_services, spreadsheet_id):
    """
    Функция для создания листа.
    """
    sheet_name = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    service = await wrapper_services.discover('sheets', 'v4')
    requests = [{
        'addSheet': {
            'properties': {
                'sheetType': 'GRID',
                'title': sheet_name
            }
        }
    }]
    body = {
        'requests': requests
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.batchUpdate(
            spreadsheetId=spreadsheet_id,
            json=body
        )
    )
    logger.info(f'Лист с именем {sheet_name} создан')
    return sheet_name


async def create_spreadsheet(wrapper_services, title):
    """
    Функция для создания таблицы.
    """
    sheet_name = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': title,
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': sheet_name
            }
        }]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetId = response['spreadsheetId']
    await set_user_permissions(wrapper_services, spreadsheetId)
    logger.info(f'Файл с именем {sheet_name} создан')
    return spreadsheetId, sheet_name


async def spreadsheet_update_values(
    wrapper_services, spreadsheetId, data, sheet_name
):
    """
    Функция для выгрузки данных на лист в таблице.
    """
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [[], [
        'ID',
        'username',
        'First Name',
        'Last Name',
        'Is Bot',
        'Joined Date',
        'Profile Photo File ID',
        'Phone number',
        'Language code',
        'Country'
    ]]
    for user in data:
        table_values.append([
            user['ID'],
            user['Username'],
            user['First Name'],
            user['Last Name'],
            user['Is Bot'],
            user['Joined Date'],
            user['Profile Photo File ID'],
            user['Phone number'],
            user['Language code'],
            user['Country']
        ])
    request_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetId,
            range=f'{sheet_name}!A1:M{2 + len(data)}',
            valueInputOption='USER_ENTERED',
            json=request_body
        )
    )


async def get_all_files():
    """
    Функция для получения названий и ссылок на все файлы на гугл диске.
    """
    async with Aiogoogle(
        service_account_creds=Configs.CREDENTIALS
    ) as wrapper_services:
        service = await wrapper_services.discover('drive', 'v3')
        json_res = await wrapper_services.as_service_account(
            service.files.list(
                q='mimeType="application/vnd.google-apps.spreadsheet"'
            ),
        )
        res = {}
        for file in json_res['files']:
            res[file['name']] = file['id']
        logger.info(f'Найдены файлы: {res}')
        return res


async def get_sheet_lists(value):
    """
    Функция для получения списка листов в таблице.
    """
    async with Aiogoogle(
        service_account_creds=Configs.CREDENTIALS
    ) as wrapper_services:
        service = await wrapper_services.discover('sheets', 'v4')
        json_res = await wrapper_services.as_service_account(
            service.spreadsheets.get(
                spreadsheetId=value,
            ),
        )
        list_title = []
        for i in json_res['sheets']:
            list_title.append(i['properties']['title'])
        logger.info(f'Найдены листы: {list_title}')
        return list_title


async def get_data_from_lists(id, value):
    """
    Функция для получения данных из двух последних листов таблицы.
    """
    async with Aiogoogle(
        service_account_creds=Configs.CREDENTIALS
    ) as wrapper_services:
        res = {}
        service = await wrapper_services.discover('sheets', 'v4')
        if len(value) > 2:
            value = value[-2:]
        for item in value:
            json_res = await wrapper_services.as_service_account(
                service.spreadsheets.values.get(
                    spreadsheetId=id,
                    range=f"{item}!A3:J250"
                ),
            )
            res[item] = len(json_res['values'])
        logger.info('Собраны данные из последних двух листов таблицы')
        return res


async def delete_all_files_by_name(name):
    """
    Функция для удаления файлов по названию.
    """
    res = await get_all_files()
    print(res)
    async with Aiogoogle(
        service_account_creds=Configs.CREDENTIALS
    ) as wrapper_services:
        service = await wrapper_services.discover('drive', 'v3')
        await wrapper_services.as_service_account(
            service.files.delete(fileId=res[name])
        )
        print(f"All files with name {name} delete.")

