from dotenv import load_dotenv
from yandex_functions import *
import pytest
import os


load_dotenv()
url_ = 'https://cloud-api.yandex.net/v1/disk/resources'


@pytest.fixture(scope='function')
def folder_yandex() -> str:
    return 'test_folder_1'


@pytest.fixture(scope='package')
def url() -> str:
    return url_


@pytest.fixture(scope='function')
def ya_token() -> str:
    yield os.getenv('ya_token')
    print('\nКонец теста')


@pytest.mark.skipif('v1/disk/resources' not in url_, reason='Неправильная ссылка')
def test_status_code_url(ya_token):
    status_code = get_info_yandex_disk(ya_token).status_code
    assert status_code == 200, f'При подключении к Яндекс Диску произошла ошибка {status_code}'


@pytest.mark.xfail(reason='Специально провальный тест')
def test_status_code_url_error(ya_token):
    status_code = get_info_yandex_disk(ya_token + '101010').status_code
    assert status_code == 200, f'При подключении к Яндекс Диску произошла ошибка {status_code}'


@pytest.mark.parametrize('folder', [
    '11111__334#@*DJ',
    '``-120391',
    'folder_folder_folder'
])
def test_check_created_name_folder(url, ya_token, folder):
    create_folder_yandex(url, ya_token, folder)
    name_folder = get_name_folder(url, ya_token, folder)
    delete_folder_yandex(url, ya_token, folder)
    assert name_folder == folder, f'Название созданной папки не соответствует имени {folder}'


@pytest.mark.parametrize('folder', [
    'test_folder_1',
    'test_folder_2',
    'test_folder_3'
])
def test_create_one_folder(url, ya_token, folder):
    status_code = create_folder_yandex(url, ya_token, folder)
    delete_folder_yandex(url, ya_token, folder)
    assert status_code == 201, f'Код статус-ответа при создании {folder=} должен быть 201, текущий {status_code=}'


def test_create_two_folder(url, ya_token, folder_yandex):
    create_folder_yandex(url, ya_token, folder_yandex)
    status_code = create_folder_yandex(url, ya_token, folder_yandex)
    delete_folder_yandex(url, ya_token, folder_yandex)
    assert status_code == 409, f'Папка {folder_yandex} не должна создаваться повторно'