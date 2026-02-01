import pytest
from src.masks import get_mask_card_number, get_mask_account

# ТЕСТЫ КАРТЫ

def test_get_mask_card_number_base(sample_card_number):
    """Проверка базового случая через фикстуру"""
    assert get_mask_card_number(sample_card_number) == "7000 79** **** 6361"

@pytest.mark.parametrize("card_num, expected", [
    ("1234567812345678", "1234 56** **** 5678"),
    ("1111222233334444", "1111 22** **** 4444"),
])
def test_get_mask_card_number_variants(card_num, expected):
    """Проверка различных вариаций номеров"""
    assert get_mask_card_number(card_num) == expected

@pytest.mark.parametrize("invalid_card, error_msg", [
    ("123", "Номер карты должен содержать 16 цифр"),
    ("700079228960636a", "Номер карты должен содержать только цифры"),
    ("7000-7922-8960-6361", "Номер карты должен содержать только цифры"),
])
def test_get_mask_card_number_errors(invalid_card, error_msg):
    """Проверка негативных сценариев карты"""
    with pytest.raises(ValueError, match=error_msg):
        get_mask_card_number(invalid_card)

# ТЕСТЫ СЧЕТА

def test_get_mask_account_base(sample_account_number):
    """Проверка базового случая через фикстуру"""
    assert get_mask_account(sample_account_number) == "**4305"

@pytest.mark.parametrize("acc_num, expected", [
    ("12345678901234567890", "**7890"),
    ("12345", "**2345"),
])
def test_get_mask_account_variants(acc_num, expected):
    """Проверка различных вариаций счетов"""
    assert get_mask_account(acc_num) == expected

@pytest.mark.parametrize("invalid_acc, error_msg", [
    ("123", "Номер счета слишком короткий"),
    ("7365410843013587430s", "Номер счета должен содержать только цифры"),
])
def test_get_mask_account_errors(invalid_acc, error_msg):
    """Проверка всех негативных сценариев счета"""
    with pytest.raises(ValueError, match=error_msg):
        get_mask_account(invalid_acc)
