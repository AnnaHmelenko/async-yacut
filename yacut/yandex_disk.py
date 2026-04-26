import urllib.parse

import aiohttp
from flask import current_app


API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


def get_auth_headers():
    return {
        'Authorization': f'OAuth {current_app.config["DISK_TOKEN"]}'
    }


async def get_upload_url(session, disk_path):
    params = {
        'path': disk_path,
        'overwrite': 'True'
    }

    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=get_auth_headers(),
        params=params
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return data['href']


async def upload_file_to_disk(session, file_storage, upload_url):
    file_storage.stream.seek(0)
    file_data = file_storage.read()

    async with session.put(upload_url, data=file_data) as response:
        response.raise_for_status()

        location = response.headers['Location']
        location = urllib.parse.unquote(location)
        return location.replace('/disk', '')


async def get_download_link(session, disk_path):
    async with session.get(
        DOWNLOAD_LINK_URL,
        headers=get_auth_headers(),
        params={'path': disk_path}
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return data['href']


async def upload_file_and_get_download_link(file_storage):
    disk_path = f'app:/{file_storage.filename}'

    async with aiohttp.ClientSession() as session:
        upload_url = await get_upload_url(session, disk_path)
        uploaded_path = await upload_file_to_disk(
            session,
            file_storage,
            upload_url
        )
        download_link = await get_download_link(session, uploaded_path)

    return download_link
