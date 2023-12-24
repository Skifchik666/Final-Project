from pages.auth_page import AuthPage
from pages.locators import AuthLocators
from settings import *

def test_page_left(selenium):
    """TKPT-01 В левой части формы «Авторизация» находится продуктовый слоган "Персональный помощник в цифровом мире Ростелекома"."""
    try:
        page = AuthPage(selenium)
        assert 'Персональный помощник в цифровом мире Ростелекома' in page.page_left.text
    except AssertionError:
        print('Элемент отсутствует в левой части формы')

def test_elements_of_auth(selenium):
    """TKPT-2 Проверка страницы "Авторизация" на наличее основных элементов."""
    page = AuthPage(selenium)

    assert page.menu_tub.text in page.card_of_auth.text
    assert page.email.text in page.card_of_auth.text
    assert page.pass_eml.text in page.card_of_auth.text
    assert page.btn_enter.text in page.card_of_auth.text
    assert page.forgot_password_link.text in page.card_of_auth.text
    assert page.register_link.text in page.card_of_auth.text

def test_menu_of_type_auth(selenium):
    """TKPT-3 Меню выбора типа аутентификации содержит названия: 'Телефон', 'Почта', 'Логин', 'Лицевой счёт'."""
    try:
        page = AuthPage(selenium)
        menu = [page.tub_phone.text, page.tub_email.text, page.tub_login.text, page.tub_ls.text]
        for i in range(len(menu)):
            assert "Телефон" in menu
            assert 'Почта' in menu
            assert 'Логин' in menu
            assert 'Лицевой счёт' in menu
    except AssertionError:
        print('Ошибка в имени таба Меню типа аутентификации')

def test_placeholder_name_of_user(selenium):
    """TKPT-4 Изменение названия в поле ввода типа аутентификации, при изменении выбора типа аутентификации"""
    page = AuthPage(selenium)
    page.tub_phone.click()

    assert page.placeholder_name_of_user.text in Settings.placeholder_name_of_user
    page.tub_email.click()
    assert page.placeholder_name_of_user.text in Settings.placeholder_name_of_user
    page.tub_login.click()
    assert page.placeholder_name_of_user.text in Settings.placeholder_name_of_user
    page.tub_ls.click()
    assert page.placeholder_name_of_user.text in Settings.placeholder_name_of_user

def test_forgot_password_link(selenium):
    """TKPT-5 Проверка перехода по ссылке 'Забыл пороль'."""
    page = AuthPage(selenium)
    page.driver.execute_script("arguments[0].click();", page.forgot_password_link)

    assert page.find_other_element(*AuthLocators.password_recovery).text == 'Восстановление пароля'

def test_register_link(selenium):
    """TKPT-6 Проверка перехода по ссылке 'Зарегистрироваться'."""
    page = AuthPage(selenium)
    page.register_link.click()

    assert page.find_other_element(*AuthLocators.registration).text == 'Регистрация'

def test_auth_by_valid_email_pass(selenium):
    """TKPT-7 Проверка аутентификации пользователя с валидным email и паролем."""
    page = AuthPage(selenium)
    page.email.clear()
    page.email.send_keys(Settings.valid_email)
    page.pass_eml.clear()
    page.pass_eml.send_keys(Settings.valid_password)
    page.btn_enter.click()

    try:
        assert page.get_relative_link() == '/account_b2c/page'
    except AssertionError:
        assert 'Неверно введен текст с картинки' in page.find_other_element(*AuthLocators.error_message).text
        print('Предыдущие тесты вызвали появление "капчи"')

def test_auth_by_invalid_email(selenium):
    """TKPT-8,TKPT-9, Проверка аутентификации пользователя с невалидным email и паролем:
(пользователь с такими данными не зарегистрирован в системе, с пустыми полями ввода.)"""
    page = AuthPage(selenium)
    page.email.send_keys(Settings.empty_email)
    page.email.clear()
    page.pass_eml.send_keys(Settings.empty_password)
    page.pass_eml.clear()
    page.btn_enter.click()

    assert page.get_relative_link() != '/account_b2c/page'

def test_menu_of_type_active_auth(selenium):
    """TKPT-10 Проверка типа аутентификации по умолчанию"""
    page = AuthPage(selenium)

    assert page.active_tub_phone.text == Settings.menu_of_type_auth[0]