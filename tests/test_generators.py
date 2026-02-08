import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


# Тесты для filter_by_currency

def test_filter_by_currency_valid(transactions_data):
    """Проверка корректной фильтрации по USD"""
    usd_transactions = list(filter_by_currency(transactions_data, "USD"))
    assert len(usd_transactions) == 2
    assert usd_transactions[0]["id"] == 1
    assert usd_transactions[1]["id"] == 3

def test_filter_by_currency_empty_result(transactions_data):
    """Проверка случая, когда валюта отсутствует"""
    eur_transactions = list(filter_by_currency(transactions_data, "EUR"))
    assert len(eur_transactions) == 0

def test_filter_by_currency_empty_list():
    """Проверка работы с пустым списком"""
    result = list(filter_by_currency([], "USD"))
    assert result == []

# Тесты для transaction_descriptions

def test_transaction_descriptions_content(transactions_data):
    """Проверка корректности описаний"""
    descriptions = transaction_descriptions(transactions_data)
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Оплата услуг"

@pytest.mark.parametrize("count", [0, 1, 3])
def test_transaction_descriptions_count(transactions_data, count):
    """Тестирование разного количества входных данных"""
    input_data = transactions_data[:count]
    result = list(transaction_descriptions(input_data))
    assert len(result) == count

# Тесты для card_number_generator

@pytest.mark.parametrize("start, end, expected", [
    (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
    (9999999999999998, 9999999999999999, ["9999 9999 9999 9998", "9999 9999 9999 9999"])
])
def test_card_number_generator_ranges(start, end, expected):
    """Проверка диапазонов, крайних значений и форматирования"""
    gen = card_number_generator(start, end)
    result = list(gen)
    assert result == expected

def test_card_number_generator_format():
    """Проверка формата (длина и пробелы)"""
    card = next(card_number_generator(10, 10))
    assert len(card) == 19  # 16 цифр + 3 пробела
    assert card[4] == " "
    assert card[9] == " "
    assert card[14] == " "

def test_card_number_generator_stop():
    """Проверка корректного завершения генератора"""
    gen = card_number_generator(1, 1)
    next(gen)
    with pytest.raises(StopIteration):
        next(gen)
