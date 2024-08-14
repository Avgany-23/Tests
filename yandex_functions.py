import requests


def get_info_yandex_disk(token: str) -> requests.Response:
    """Ответ на запрос к получению метаинформации о диске пользователя"""
    url = 'https://cloud-api.yandex.net/v1/disk'
    headers = {'Authorization': token}
    return requests.get(url, headers=headers)


def create_folder_yandex(url_disk: str, token: str, folder: str) -> int:
    "Функция для создания папки на яндекс диске"
    headers = {'Authorization': token}
    params = {'path': folder}
    response = requests.put(url_disk, headers=headers, params=params)
    return response.status_code


def delete_folder_yandex(url_disk: str, token: str, folder: str) -> int:
    """Функция для удаления папки"""
    headers = {'Authorization': token}
    params = {'path': folder}
    response = requests.delete(url_disk, headers=headers, params=params)
    return response.status_code


def get_name_folder(url_disk: str, token: str, folder: str) -> str:
    """Функция для получение имени папки"""
    headers = {'Authorization': token}
    params = {'path': folder}
    response = requests.get(url_disk, headers=headers, params=params)
    return response.json()['name']
