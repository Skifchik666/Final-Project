import pytest
from pages.registr_page import RegistrPage
from pages.locators import AuthLocators
from settings import *

def test_page_left_registration(selenium):
    """TKPT-11  В левой части формы «Регистрация» находится продуктовый слоган "Персональный помощник в цифровом мире Ростелекома"."""
    try:
        page_reg = RegistrPage(selenium)
        assert page_reg.page_left_registration.text != ''
    except AssertionError:
        print('Элемент отсутствует в левой части формы')

def test_elements_of_registr(selenium):
    """TKPT-12 Проверка страницы "Регистрация" на наличее основных элементов."""
    try:
        page_reg = RegistrPage(selenium)
        card_of_reg = [page_reg.first_name, page_reg.last_name, page_reg.address_registration,
                       page_reg.email_registration, page_reg.passw_registration,
                       page_reg.passw_registration_confirm, page_reg.registration_btn]
        for i in range(len(card_of_reg)):
            assert page_reg.first_name in card_of_reg
            assert page_reg.last_name in card_of_reg
            assert page_reg.email_registration in card_of_reg
            assert page_reg.address_registration in card_of_reg
            assert page_reg.passw_registration in card_of_reg
            assert page_reg.passw_registration_confirm in card_of_reg
            assert page_reg.registration_btn in card_of_reg
    except AssertionError:
        print('Элемент отсутствует в форме «Регистрация»')

def test_registr_by_invalid_data(selenium):
    """TKPT-13 Регистрация пользователя по email, который уже был использован для регистрации."""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.f_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.l_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email)
    page_reg.email_registration.clear()
    page_reg.passw_registration.send_keys(Settings.valid_password)
    page_reg.passw_registration.clear()
    page_reg.passw_registration_confirm.send_keys(Settings.valid_password)
    page_reg.passw_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert "Учётная запись уже существует" in page_reg.find_other_element(*AuthLocators.error_account_exists).text

def test_registr_by_valid_data(selenium):
    """TKPT-14 Регистрация пользователя с валидными данными"""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.f_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.l_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email_for_reg)
    page_reg.email_registration.clear()
    page_reg.passw_registration.send_keys(Settings.valid_password)
    page_reg.passw_registration.clear()
    page_reg.passw_registration_confirm.send_keys(Settings.valid_password)
    page_reg.passw_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert page_reg.find_other_element(*AuthLocators.email_confirm).text == 'Подтверждение email'

def test_names_elements_of_registr(selenium):
    """TKPT-15 Названия элементов страницы «Регистрация» соответствуют Требованию."""
    try:
        page_reg = RegistrPage(selenium)
        assert 'Имя' in page_reg.card_of_registration.text
        assert 'Фамилия' in page_reg.card_of_registration.text
        assert 'Регион' in page_reg.card_of_registration.text
        assert 'E-mail или мобильный телефон' in page_reg.card_of_registration.text
        assert 'Пароль' in page_reg.card_of_registration.text
        assert 'Подтверждение пароля' in page_reg.card_of_registration.text
        assert 'Продолжить' in page_reg.card_of_registration.text
    except AssertionError:
        print('Название элемента в форме «Регистрация» не соответствует Требованию')

@pytest.mark.parametrize("invalid_first_name",
                         [
                             (Settings.russian_simvol) * 1
                             , (Settings.russian_simvol) * 31
                             , (Settings.russian_simvol) * 260
                             , (Settings.empty), (Settings.numbers)
                             , (Settings.latin_generate_string)
                             , (Settings.chinese_chars), (Settings.special_chars)
                         ],
                         ids=
                         [
                             'russ_symbols=1', 'russ_symbols=31', 'russ_symbols=260',
                             'empty', 'numbers', 'latin_symbols', 'chinese_symbols', 'special_symbols'
                         ])
def test_first_name_by_invalid_data(selenium, invalid_first_name):
    """TKPT-16 Проверка поля ввода "Имя" страницы «Регистрация» невалидными данными"""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(invalid_first_name)
    page_reg.first_name.clear()
    page_reg.registration_btn.click()

    assert 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.' in \
           page_reg.find_other_element(*AuthLocators.error_first_name).text

@pytest.mark.parametrize("valid_first_name",
                         [
                             (Settings.russian_simvol) * 2
                             , (Settings.russian_simvol) * 3
                             , (Settings.russian_simvol) * 15
                             , (Settings.russian_simvol) * 29
                             , (Settings.russian_simvol) * 30
                         ],
                         ids=
                         [
                             'russ_symbols=2', 'russ_symbols=3', 'russ_symbols=15',
                             'russ_symbols=29', 'russ_symbols=30'
                         ])
def test_first_name_by_valid_data(selenium, valid_first_name):
    """TKPT-18 Проверка поля ввода "пароль" страницы «Регистрация» валидными данными."""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(valid_first_name)
    page_reg.first_name.clear()
    page_reg.registration_btn.click()

    assert 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.' not in page_reg.container_f_name.text

def test_passw_registration_confirm_valid_data(selenium):
    """TKPT-19 Проверка поля ввода "Пароль" и "Подтвердить пароль" страницы «Регистрация» валидными данными: пароли совпадают.."""
    page_reg = RegistrPage(selenium)
    page_reg.passw_registration.send_keys(Settings.passw1)
    page_reg.passw_registration.clear()
    page_reg.passw_registration_confirm.send_keys(Settings.passw1)
    page_reg.passw_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert 'Пароли не совпадают' not in page_reg.container_passw_confirm.text

def test_passw_registration_confirm_invalid_data(selenium):
    """TKPT-20 Проверка поля ввода "Пароль" и "Подтвердить пароль" формы «Регистрация» невалидными данными: пароли не совпадают.."""
    page_reg = RegistrPage(selenium)
    page_reg.passw_registration.send_keys(Settings.passw1)
    page_reg.passw_registration.clear()
    page_reg.passw_registration_confirm.send_keys(Settings.passw2)
    page_reg.passw_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert 'Пароли не совпадают' in page_reg.find_other_element(*AuthLocators.error_passw_confirm).text