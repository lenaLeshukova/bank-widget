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


def transaction_descriptions(transactions):
    """
    Генератор, который возвращает описание каждой транзакции.
    """
    for transaction in transactions:
        # Извлекаем описание, если ключа нет — вернется None или пустая строка
        yield transaction.get("description", "Описание отсутствует")


#  Пример использования

# Список транзакций
transactions = [
    {"description": "Перевод организации"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод с карты на карту"},
    {"description": "Перевод организации"}
]

descriptions = transaction_descriptions(transactions)

for _ in range(5):
    try:
        print(next(descriptions))
    except StopIteration:
        break  # Останавливаем цикл, если транзакции закончились


def card_number_generator(start, end):
    for number in range(start, end + 1):
        # 1. Превращаем число в строку
        num_str = str(number)

        # 2. Считаем, сколько нулей нужно добавить в начало
        zeros_needed = 16 - len(num_str)

        # 3. Создаем строку из нулей и соединяем с числом
        full_card_number = ("0" * zeros_needed) + num_str

        # 4. Расставляем пробелы вручную через срезы
        formatted_card = (
                full_card_number[0:4] + " " +
                full_card_number[4:8] + " " +
                full_card_number[8:12] + " " +
                full_card_number[12:16]
        )

        yield formatted_card


# Проверка
for card in card_number_generator(1, 3):
    print(card)
