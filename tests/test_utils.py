import json
from unittest.mock import patch, mock_open

from src.utils import get_financial_transactions, get_transaction_amount


@patch("os.path.exists")
def test_get_transactions_success(mock_exists, sample_transactions):
    """
    Тест успешного получения данных.
    Используем фикстуру sample_transactions.
    """
    mock_exists.return_value = True

    # Превращаем данные из фикстуры в строку JSON
    json_data = json.dumps(sample_transactions)

    with patch("builtins.open", mock_open(read_data=json_data)):
        result = get_financial_transactions("data/operations.json")
        assert result == sample_transactions
        assert len(result) == 2


@patch("os.path.exists")
def test_get_transactions_empty(mock_exists, empty_file_content):
    """Тест: файл пуст (JSONDecodeError)."""
    mock_exists.return_value = True
    with patch("builtins.open", mock_open(read_data=empty_file_content)):
        assert get_financial_transactions("data/empty.json") == []


@patch("os.path.exists")
def test_get_transactions_not_list(mock_exists, not_list_content):
    """Тест: в файле словарь вместо списка."""
    mock_exists.return_value = True
    with patch("builtins.open", mock_open(read_data=not_list_content)):
        assert get_financial_transactions("data/wrong.json") == []


def test_get_transaction_amount_rub():
    """Тест: транзакция в рублях возвращается как float без конвертации."""
    transaction = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"code": "RUB"}
        }
    }

    # Используем patch как контекстный менеджер, чтобы убедиться, что конвертер НЕ вызывался
    with patch("src.utils.convert_to_rub") as mock_convert:
        result = get_transaction_amount(transaction)

        assert result == 100.50
        assert isinstance(result, float)
        mock_convert.assert_not_called()


@patch("src.utils.convert_to_rub")
def test_get_transaction_amount_usd(mock_convert, mock_api_response):
    """Тест: транзакция в USD вызывает функцию конвертации."""
    transaction = {
        "operationAmount": {
            "amount": "100.0",
            "currency": {"code": "USD"}
        }
    }

    # Настраиваем мок, используя значение фикстуры
    mock_convert.return_value = mock_api_response["result"]

    result = get_transaction_amount(transaction)

    assert result == 7550.0
    # Проверяем, что конвертер был вызван с правильными аргументами
    mock_convert.assert_called_once_with(100.0, "USD")


def test_get_transaction_amount_invalid_data():
    """Тест: корректная обработка пустой транзакции или отсутствующих полей."""
    assert get_transaction_amount({}) == 0.0
    assert get_transaction_amount({"operationAmount": {}}) == 0.0
