import pytest

from src.widget import mask_account_card, get_date


# ТЕСТЫ ДЛЯ mask_account_card

@pytest.mark.parametrize("input_data, expected", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
    ("Счет 73654108430135874305", "Счет **4305"),
])
def test_mask_account_card_variants(input_data, expected):
    """Проверка различных типов карт и счетов"""
    assert mask_account_card(input_data) == expected


def test_mask_account_card_with_fixtures(sample_card_number, sample_account_number):
    """Проверка работы функции с использованием фикстур"""
    card_input = f"Visa {sample_card_number}"
    acc_input = f"Счет {sample_account_number}"

    assert mask_account_card(card_input) == "Visa 7000 79** **** 6361"
    assert mask_account_card(acc_input) == "Счет **4305"


# ТЕСТЫ ДЛЯ get_date

@pytest.mark.parametrize("date_raw, expected_date", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-31T23:59:59.999999", "31.12.2023"),
    ("2025-01-01T00:00:00.000000", "01.01.2025"),
])
def test_get_date(date_raw, expected_date):
    """Проверка корректного форматирования даты"""
    assert get_date(date_raw) == expected_date


def test_get_date_invalid_format():
    """Пример теста на некорректную длину строки даты"""
    with pytest.raises(ValueError):
        get_date("2024-03")  # Слишком короткая строка вызовет ошибку индекса


@pytest.mark.parametrize("invalid_date, error_msg", [
    ("2024-13-11T02:26:18", "Месяц должен быть в диапазоне от 01 до 12"),
    ("2024-00-11T02:26:18", "Месяц должен быть в диапазоне от 01 до 12"),
    ("2024-99-11T02:26:18", "Месяц должен быть в диапазоне от 01 до 12"),
])
def test_get_date_month_validation(invalid_date, error_msg):
    """Проверка выброса исключения при некорректном месяце"""
    with pytest.raises(ValueError, match=error_msg):
        get_date(invalid_date)


@pytest.mark.parametrize("valid_date, expected", [
    ("2024-01-11T02:26:18", "11.01.2024"),  # Январь
    ("2024-12-31T02:26:18", "31.12.2024"),  # Декабрь
])
def test_get_date_month_boundaries(valid_date, expected):
    """Проверка работы на границах допустимых месяцев"""
    assert get_date(valid_date) == expected
