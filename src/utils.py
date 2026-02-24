import json
import os
from src.external_api import convert_to_rub

def get_financial_transactions(path):
    """
    Принимает путь до JSON-файла и возвращает список словарей.
    Возвращает пустой список, если файл не найден, пуст или формат данных неверен.
    """
    # Проверяем, существует ли файл по указанному пути
    if not os.path.exists(path):
        return []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Проверяем, что данные являются списком
            if isinstance(data, list):
                return data
            else:
                return []

    except (json.JSONDecodeError, FileNotFoundError):
        # Если файл пустой или содержит некорректный JSON
        return []

def get_transaction_amount(transaction: dict) -> float:
    """
    Принимает транзакцию и возвращает сумму в рублях (float).
    Если валюта не RUB, обращается к external_api для конвертации.
    """
    # Извлекаем сумму и код валюты
    amount = transaction.get("operationAmount", {}).get("amount")
    currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    if amount is None or currency_code is None:
        return 0.0

    amount = float(amount)

    if currency_code == "RUB":
        return amount
    elif currency_code in ["USD", "EUR"]:
        return convert_to_rub(amount, currency_code)
    else:
        # Для других валют
        return 0.0
    