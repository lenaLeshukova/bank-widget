import pytest

from src.processing import filter_by_state, sort_by_date, filter_by_query, count_operations_by_category


# Тесты для filter_by_state
def test_filter_by_state_executed(sample_data):
    result = filter_by_state(sample_data)  # По умолчанию 'EXECUTED'
    assert len(result) == 3
    assert all(item['state'] == 'EXECUTED' for item in result)


def test_filter_by_state_canceled(sample_data):
    result = filter_by_state(sample_data, 'CANCELED')
    assert len(result) == 1
    assert result[0]['id'] == 2


def test_filter_by_state_empty_list():
    assert filter_by_state([], 'EXECUTED') == []


# Тесты для sort_by_date
def test_sort_by_date_descending(sample_data):
    result = sort_by_date(sample_data)  # По умолчанию True (убывание)
    assert result[0]['date'] == '2023-05-01'
    assert result[-1]['date'] == '2022-12-31'


def test_sort_by_date_ascending(sample_data):
    result = sort_by_date(sample_data, descending=False)
    assert result[0]['date'] == '2022-12-31'
    assert result[-1]['date'] == '2023-05-01'


# Тесты для filter_by_query
@pytest.mark.parametrize("query, expected_count", [
    ("перевод", 3),
    ("ОПЛАТА", 1),
    ("несуществующий", 0),
])
def test_filter_by_query(sample_data, query, expected_count):
    result = filter_by_query(sample_data, query)
    assert len(result) == expected_count


# Тестируем filter_by_query на некорректные типы данных
def test_filter_by_query_invalid_type():
    # Если вместо строки поиска передать None или число
    with pytest.raises(TypeError):
        filter_by_query([{'description': 'test'}], None)  # re.escape упадет на None


# Тестируем работу с пустыми значениями в описании
def test_filter_by_query_none_description():
    data = [{'id': 1, 'description': None}]
    # Функция проверяет if item.get('description'), так что ошибки не будет
    assert filter_by_query(data, "перевод") == []


# Тесты для count_operations_by_category
def test_count_operations_by_category(sample_data):
    categories = ['Перевод организации', 'Оплата услуг', 'Внешний перевод', 'Пустая категория']
    expected = {
        'Перевод организации': 1,
        'Оплата услуг': 1,
        'Внешний перевод': 1,
        'Пустая категория': 0
    }
    assert count_operations_by_category(sample_data, categories) == expected


#  Тестируем на абсолютно пустой вход
@pytest.mark.parametrize("func", [filter_by_state, sort_by_date, filter_by_query])
def test_functions_with_empty_list(func):
    if func == filter_by_query:
        assert func([], "query") == []
    else:
        assert func([]) == []
