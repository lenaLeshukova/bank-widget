import json
import logging
import os

from src.external_api import convert_to_rub

# Логирование
# Определяем корень проекта (на уровень выше текущей папки src)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
log_directory = os.path.join(project_root, "logs")

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, "utils.log")

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Режим 'w' обеспечит перезапись лога при каждом запуске
file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_financial_transactions(path):
    """
    Принимает путь до JSON-файла и возвращает список словарей.
    Возвращает пустой список, если файл не найден, пуст или формат данных неверен.
    """
    logger.info(f"Попытка чтения транзакций из файла: {path}")

    # Проверяем, существует ли файл по указанному пути
    if not os.path.exists(path):
        logger.error(f"Файл не найден по пути: {path}")
        return []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Проверяем, что данные являются списком
            if isinstance(data, list):
                logger.info(f"Успешно загружено транзакций: {len(data)}")
                return data
            else:
                logger.warning(f"Данные в файле {path} не являются списком")
                return []


    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {path}: {e}")
        return []


def get_transaction_amount(transaction: dict) -> float:
    """
    Принимает транзакцию и возвращает сумму в рублях (float).
    Если валюта не RUB, обращается к external_api для конвертации.
    """
    logger.info("Начало обработки суммы транзакции")

    # Извлекаем сумму и код валюты
    amount_data = transaction.get("operationAmount", {})
    amount = amount_data.get("amount")
    currency_code = amount_data.get("currency", {}).get("code")

    if amount is None or currency_code is None:
        logger.warning("Транзакция не содержит суммы или кода валюты")
        return 0.0
    try:

        amount = float(amount)

        if currency_code == "RUB":
            logger.info(f"Сумма в рублях: {amount}")
            return amount

        elif currency_code in ["USD", "EUR"]:
            logger.info(f"Требуется конвертация для валюты: {currency_code}")
            return convert_to_rub(amount, currency_code)
        else:
            # Для других валют
            logger.warning(f"Неподдерживаемая валюта: {currency_code}")
            return 0.0

    except ValueError:
        logger.error(f"Некорректный формат суммы: {amount}")
        return 0.0


if __name__ == "__main__":
    # Тест. Валюта, требующая конвертации (INFO)
    test_transaction_usd = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"code": "USD"}
        }
    }
    get_transaction_amount(test_transaction_usd)

    # Тест. Файл не найден (ERROR)
    get_financial_transactions("non_existent_file.json")

    # Тест. Ошибка формата суммы (ERROR)
    test_transaction_bad_amount = {
        "operationAmount": {
            "amount": "сто рублей",
            "currency": {"code": "RUB"}
        }
    }
    get_transaction_amount(test_transaction_bad_amount)
