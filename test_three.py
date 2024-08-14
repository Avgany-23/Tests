from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome, ChromeOptions
from time import sleep
from dotenv import load_dotenv
import os
import pytest


load_dotenv()


@pytest.fixture(scope='module')
def driver_():
    """Фикстура для теста test_incorrect_login"""
    path = ChromeDriverManager().install()
    browser_service = Service(executable_path=path)
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = Chrome(service=browser_service, options=options)
    driver.get('https://passport.yandex.ru/auth/list')
    yield driver
    driver.close()


@pytest.fixture(scope='function')
def driver():
    """Фикстура для всех тестов кроме test_incorrect_login"""
    path = ChromeDriverManager().install()
    browser_service = Service(executable_path=path)
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = Chrome(service=browser_service, options=options)
    driver.get('https://passport.yandex.ru/auth/list')
    yield driver
    driver.close()


def test_check_html_main_element(driver):
    field_auth_content = driver.find_element(By.XPATH, '//div[@class="passp-auth-content"]')
    assert field_auth_content.is_displayed(), 'Окно должно быть дисплеем'
    assert field_auth_content.is_enabled(), 'Окно должно быть доступным'
    assert not field_auth_content.is_selected(), 'Окно нельзя "выбрать"'


def test_check_buttons(driver):
    button_email = driver.find_element(By.XPATH,
                            '//button[@class="Button2 Button2_checked Button2_size_l Button2_view_default"]')
    button_phone = driver.find_element(By.XPATH, '//button[@class="Button2 Button2_size_l Button2_view_clear"]')
    button_enter = driver.find_element(By.XPATH, '//button[@id="passp:sign-in"]')
    assert button_email.text == 'Почта', (f'Кнопка выбора авторизации по почте называется {button_email.text}, '
                                         f'вместо "Почта"')
    assert button_phone.text == 'Телефон', (f'Кнопка выбора авторизации по телефону называется {button_phone.text}, '
                                           f'вместо "Телефон"')
    assert button_enter.text == 'Войти', f'Кнопка "Войти" называется неверно - {button_enter.text}'


def test_correct_login(driver):
    # Поле для ввода логина
    field_put_login = driver.find_element(By.XPATH, '//input[@class="Textinput-Control"]')
    field_put_login.send_keys(os.getenv('login_yandex'))

    # Кнопка "войти"
    button_put = driver.find_element(By.XPATH, '//button[@id="passp:sign-in"]')
    button_put.click()
    sleep(0.5)

    # Поле для ввода пароля Textinput-Control
    field_put_password = driver.find_element(By.XPATH, '//input[@class="Textinput-Control"]')
    field_put_password.send_keys(os.getenv('password_yandex'))

    # Кнопка "продолжить"
    button_continue = driver.find_element(By.XPATH, '//button[@id="passp:sign-in"]')
    button_continue.click()
    sleep(2.5)

    # Варианты вылезающих окон после успешного входа: главное меню или потверждение номера телефона
    paths = [('//div[@class="app-shell_root__mG_ht"]', 'Главная'),
             ('//div[@class="layout_head"]', 'Безопасный вход')]
    test_, field_profile = None, None
    for path in paths:
        try:
            field_profile = driver.find_element(By.XPATH, path[0])
            test_ = path[1]
            break
        except:
            continue

    assert test_ in field_profile.text, 'Не удалось авторизоваться с верными данными для входа'


@pytest.mark.parametrize('login', [
    os.getenv('login_yandex').replace('@', ''),
    os.getenv('login_yandex')[:-1],
    '32rfdj3rf93iroj',
    '2123123@yandex.ru',
    '21sdf23123@dsfsdfsd.ru',])
def test_incorrect_login(driver_, login):
    responses = [
        'Логин введен некорректно или удален',
        'Такой логин не подойдет',
        'Такого аккаунта нет'
    ]
    # Поле для ввода логина
    sleep(0.5)
    field_put_login = driver_.find_element(By.XPATH, '//input[@class="Textinput-Control"]')
    field_put_login.send_keys(login)

    # Кнопка "войти"
    button_put = driver_.find_element(By.XPATH, '//button[@id="passp:sign-in"]')
    button_put.click()
    sleep(0.5)

    # Тест подсказки с неправильным вводом логина
    field_incorrect_data = driver_.find_element(By.XPATH, '//div[@id="field:input-login:hint"]')

    assert field_incorrect_data.text.strip() in responses, f'Логин {login} не выдаёт одну из ошибок в списке {responses}'


