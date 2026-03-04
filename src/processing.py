import re
from collections import Counter


def filter_by_state(data: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    data: Список словарей с данными о транзакциях.
    state: Строка для фильтрации (по умолчанию 'EXECUTED').
    return: Новый список словарей, у которых ключ state
    соответствует указанному значению
    """
    return [item for item in data if item.get('state') == state]


def sort_by_date(data: list[dict], descending: bool = True) -> list[dict]:
    """
    Сортирует список словарей по дате (ключ 'date')
    data: Список словарей с данными о транзакциях
    descending: Порядок сортировки (True для убывания, False для возрастания).
    return: Новый список словарей, отсортированный по дате.
    """
    # Сортируем, используя ключ сортировки
    return sorted(
        data,
        key=lambda item: item['date'],
        reverse=descending
    )


def filter_by_query(data: list[dict], search_query: str) -> list[dict]:
    """
    Фильтрует список словарей по наличию строки поиска в описании (description).
    Использует регулярные выражения для гибкого поиска.
    """
    # Экранируем спецсимволы в запросе и включаем игнорирование регистра. Используем re.escape, чтобы если в поиске придет что-то вроде "+", программа не выдала ошибку.
    pattern = re.compile(re.escape(search_query), re.IGNORECASE)

    return [
        item for item in data
        if item.get('description') and pattern.search(item['description'])
    ]


def count_operations_by_category(data: list[dict], categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество операций в каждой из указанных категорий.
    Категория ищется в поле 'description'.
    """
    # Извлекаем все описания из данных, которые есть в списке категорий
    descriptions_in_data = [
        item.get("description")
        for item in data
        if item.get("description") in categories
    ]

    # Считаем вхождения с помощью Counter
    counts = Counter(descriptions_in_data)

    # Формируем итоговый словарь, чтобы в нем были все запрашиваемые категории (даже с 0)
    return {category: counts.get(category, 0) for category in categories}


# Пример использования:
if __name__ == "__main__":
    data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03', 'description': 'Перевод организации'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30', 'description': 'Перевод с карты на карту'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12', 'description': 'Оплата услуг'},
    ]

    categories = ['Перевод организации', 'Оплата услуг', 'Внешний перевод']

    result = count_operations_by_category(data, categories)
    print(result)
    # Вывод: {'Перевод организации': 2, 'Оплата услуг': 1, 'Внешний перевод': 0}

    # Пример поиска "перевод" (найдет и "Перевод", и "перевод")
    print(filter_by_query(data, "перевод"))
