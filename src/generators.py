def filter_by_currency(transactions, currency_code):
    """
    Возвращает итератор, который выдает транзакции с заданной валютой.
    """
    for transaction in transactions:
        # Проверяем наличие вложенных ключей, чтобы избежать ошибок
        try:
            current_currency = transaction["operationAmount"]["currency"]["code"]
            if current_currency == currency_code:
                yield transaction
        except (KeyError, TypeError):
            # Пропускаем транзакцию, если структура данных неверна
            continue

# Пример использования

transactions = [
    {
        "id": 939719570,
        "operationAmount": {"currency": {"code": "USD"}}
    },
    {
        "id": 123456789,
        "operationAmount": {"currency": {"code": "RUB"}}
    },
    {
        "id": 142264268,
        "operationAmount": {"currency": {"code": "USD"}}
    }
]

usd_transactions = filter_by_currency(transactions, "USD")

# Выводим первые две найденные транзакции
for _ in range(2):
    print(next(usd_transactions))
